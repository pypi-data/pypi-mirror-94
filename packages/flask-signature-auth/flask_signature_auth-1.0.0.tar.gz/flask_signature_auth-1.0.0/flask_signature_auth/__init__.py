import cryptography.exceptions
import base64
import hashlib
import logging
import json
import re
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1, PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from flask import g, jsonify, request
from functools import wraps
from jwcrypto import jwk, jws
from urllib.parse import parse_qs, quote as quote_qs

_log = logging.getLogger(__name__)


def _bytes_to_base64str(input):
  if isinstance(input, bytes):
    return base64.b64encode(input).decode('ascii')
  raise TypeError('"input" must be an instance of "bytes"')


def _base64str_to_bytes(input):
  if isinstance(input, str) or isinstance(input, bytes):
    return base64.b64decode(input.encode('ascii'))
  raise TypeError('"input" must be an instance of "bytes" or "str"')


class ChallengeVerificationError(Exception):
  pass


class SignatureVerificationError(Exception):
  pass


class InvalidSignatureError(SignatureVerificationError):
  pass


class PublicKeyNotFoundError(SignatureVerificationError):
  pass


class ParseError(SignatureVerificationError):
  pass


class KeyCollection(dict):
  pass

class HTTPUser(object):
  def __init__(self, key_id: str):
    self.key_id = key_id

class SignatureAuthorizationHeader(object):
  def __init__(self, key_id, algorithm, headers, signature, created_timestamp):
    self.key_id = key_id
    self.algorithm = algorithm
    self.headers = headers
    self.signature = signature
    self.created_timestamp = created_timestamp


class FlaskSignatureAuth(object):
  known_algorithms = [
      'rsa-sha256'
  ]

  def __init__(self, ttl=10, headers=['(request-target)', '(created)', 'Digest'], algorithm='rsa-sha256', key_bytes=None, key_locator=None, header_name='Authorization'):
    assert algorithm in self.__class__.known_algorithms
    assert not (
        key_bytes is None and key_locator is None), "Either `key_bytes` or `key_locator` must be set."
    assert not (
        key_bytes is not None and key_locator is not None), "Either `key_bytes` or `key_locator` must be set, not both."

    self._algorithm = algorithm
    self._headers = headers
    self._header_name = header_name
    self._ttl = ttl
    self._hashfn = hashlib.sha256
    self._hasher_name = SHA256()
    self._keypair = rsa.generate_private_key(
        public_exponent=65537, key_size=2048)
    self._key_bytes = key_bytes
    self._key_locator = key_locator

  def get_challenge(self, public_key: jwk.JWK):
    key_id = public_key.thumbprint(self._hasher_name)

    if not key_id in self._keys:
      self._keys[key_id] = public_key.export_public(as_dict=True)

    challenge = self._get_sts(key_id, expires_on=time.time() + self._ttl)
    challenge_hash = self._hashfn(challenge).digest()
    # if algorithm == 'rsa-sha256-pss':
    #   signature = self._keypair.sign(
    #       challenge_hash,
    #       padding=PSS(mgf=MGF1(self._hasher_name),
    #                   salt_length=self._hasher_name.digest_size),
    #       algorithm=self._hasher_name
    #   )
    if algorithm == 'rsa-sha256':
      signature = self._keypair.sign(
          challenge_hash,
          padding=PKCS1v15(),
          algorithm=self._hasher_name
      )
    else:
      raise NotImplementedError('Cannot sign data: invalid algorithm')

    return ':'.join([_bytes_to_base64str(obj) for obj in [challenge_hash, signature, challenge]])

  def verify_challenge(self, challenge, signature):
    if not isinstance(challenge, str):
      raise TypeError('"challenge" must be an instance of "str"')
    if not isinstance(signature, str):
      raise TypeError('"signature" must be an instance of "str"')

    expected_hash, sig, sts_bytes = [
        _base64str_to_bytes(c) for c in challenge.split(':')]
    sts_hash = self._hashfn(sts_bytes).digest()

    if expected_hash != sts_hash:
      raise ChallengeVerificationError('Digest mismatch')

    if not self._verify_signature(sig, sts_hash, self._keypair.public_key()):
      raise ChallengeVerificationError('Invalid server signature')

    key_id, expires_on = self._parse_sts(sts_bytes)

    expected_sts = self._get_sts(key_id=key_id, expires_on=expires_on)

    if expected_sts != sts_bytes:
      raise ChallengeVerificationError('STS mismatch')

    if time.time() > expires_on:
      raise ChallengeVerificationError('Challenge expired')

    challenge_hash = self._hashfn(challenge.encode('utf-8')).digest()
    client_public_key = self._get_client_key(key_id)
    if not self._verify_signature(base64.b64decode(signature), challenge_hash, client_public_key):
      raise ChallengeVerificationError('Invalid client signature')

    return key_id, client_public_key

  def challenge(self, f=None):
    def challenge_internal(f):
      @wraps(f)
      def decorated(*args, **kwargs):
        if not request.is_json:
          return 'invalid_request', 400

        try:
          self.verify_challenge(**request.json)
        except ChallengeVerificationError as err:
          _log.info("Challenge verification error:\n%s", err)
          return 'invalid_challenge', 400

        return f(*args, **kwargs)
      return decorated
    return challenge_internal

  def auth_required(self, f=None):
    def auth_required_internal(f):
      @wraps(f)
      def decorated(*args, **kwargs):
        try:
          auth_data_raw = self._get_authorization_header()
          accepted_headers = self._headers.copy()
          if 'Digest' in accepted_headers and request.data is None or len(request.data) == 0:
            accepted_headers.remove('Digest')
          auth_data_struct = self._parse_authorization_header(
              auth_data_raw, accepted_headers)
          client_public_key = self._load_key(auth_data_struct.key_id)
          sts = self._get_string_to_sign(
              auth_data_struct.created_timestamp, accepted_headers)
          self._verify_signature(sig=auth_data_struct.signature,
                                 data=sts, key=client_public_key)

          g.flask_signature_auth_http_user = HTTPUser(auth_data_struct.key_id)
        except SignatureVerificationError as err:
          _log.info("Signature verification error:\n%s", err)
          return '', 401

        return f(*args, **kwargs)
      return decorated
    return auth_required_internal

  def current_user(self):
    if hasattr(g, 'flask_signature_auth_http_user'):
      return g.flask_signature_auth_http_user

  def _get_string_to_sign(self, created_timestamp, headers):
    sts = []
    for header in headers:
      if header == "(request-target)":
        sts.append("{}: {} {}".format(
            header, request.method.lower(), request.path))
      elif header == "(created)":
        sts.append("{}: {}".format(header, created_timestamp))
      else:
        if header.lower() == "host":
          url = urlparse(request.url)
          value = request.headers.get("host", url.hostname)
          if url.scheme == "http" and url.port not in [None, 80] or url.scheme == "https" \
                  and url.port not in [443, None]:
            value = "{}:{}".format(value, url.port)
        elif header.lower() == "digest":
          if request.data is not None:
            if header not in request.headers:
              digest = self._hashfn(request.data).digest()
              value = "SHA-256=" + base64.b64encode(digest).decode()
            else:
              value = request.headers[header]
        else:
          value = request.headers[header]
        sts.append("{k}: {v}".format(k=header.lower(), v=value))

    return "\n".join(sts).encode()

  def _get_client_key(self, key_id):
    if not key_id in self._keys:
      raise ChallengeVerificationError('Key ID mismatch')

    client_public_key = jwk.JWK(**self._keys[key_id])
    return load_pem_public_key(client_public_key.export_to_pem())

  def _get_sts(self, key_id, expires_on):
    challenge_str = 'key_id=%s&expires_on=%f' % (key_id, expires_on)
    return challenge_str.encode('utf-8')

  def _parse_sts(self, input: bytes):
    sts = input.decode('utf-8')
    data = parse_qs(sts)
    key_id = data['key_id'][0]
    expires_on = float(data['expires_on'][0])

    return key_id, expires_on

  def _verify_signature(self, sig, data, key, salt_length=None):
    try:
      # if self._algorithm == 'rsa-sha256':
      #   key.verify(
      #       sig,
      #       data,
      #       padding=PSS(mgf=MGF1(
      #           self._hasher_name), salt_length=self._hasher_name.digest_size if salt_length is None else salt_length),
      #       algorithm=self._hasher_name
      #   )
      if self._algorithm == 'rsa-sha256':
        key.verify(
            sig,
            data,
            padding=PKCS1v15(),
            algorithm=self._hasher_name
        )
      else:
        raise NotImplementedError('Cannot sign data: invalid algorithm')
    except cryptography.exceptions.InvalidSignature:
      raise InvalidSignatureError()

  def _get_authorization_header(self):
    if self._header_name in request.headers:
      if self._header_name == 'Authorization':
        if 'Authorization' in request.headers:
          auth_type, auth_data = request.headers['Authorization'].split(' ', 1)
          if auth_type == 'Signature':
            return auth_data
      else:
        return request.headers[self._header_name]

  def _parse_authorization_header(self, txt, accepted_headers):
    if txt is None:
      raise ParseError('Header is empty')
    reg = re.compile('(\w+)[=] ?"?([^"]+)"?')
    signature_struct = {k: v for k, v in reg.findall(txt)}
    key_id = self._parse_key_id(signature_struct['keyId'])
    algorithm = self._parse_algorithm(signature_struct['algorithm'])
    headers = self._parse_headers(
        signature_struct['headers'], accepted_headers)
    signature = self._parse_signature(signature_struct['signature'])
    created_timestamp = int(
        signature_struct['created']) if 'created' in signature_struct else None
    return SignatureAuthorizationHeader(key_id, algorithm, headers, signature, created_timestamp)

  def _parse_key_id(self, text: str):
    if text is None or len(text) == 0:
      raise ParseError('Invalid key id')

    return text

  def _parse_algorithm(self, text: str):
    if text is None or text != self._algorithm:
      raise ParseError('Invalid algorithm')

    return text

  def _parse_headers(self, text: str, accepted_values: list):
    available_headers = [v.lower() for v in accepted_values]
    available_headers_map = {v.lower(): v for v in accepted_values}
    headers = [h.lower() for h in text.split(' ')]
    headers_map = {v.lower(): v for v in headers}

    missing_headers = []
    for h in available_headers:
      if not h in headers:
        missing_headers.append(available_headers_map[h])

    if missing_headers:
      raise ParseError('Missing required headers: "%s"' %
                       '", "'.join(missing_headers))

    extra_headers = []
    for h in headers:
      if not h in available_headers:
        extra_headers.append(headers_map[h])

    if extra_headers:
      raise ParseError('Extra headers passed: "%s"' %
                       '", "'.join(extra_headers))

    return headers

  def _parse_signature(self, text: str):
    if text is None or len(text) == 0:
      raise ParseError('Invalid signature')

    return base64.b64decode(text)

  def _load_key(self, key_id: str):
    key_bytes = None
    if not self._key_bytes is None:
      key_bytes = self._key_bytes
    elif not self._key_locator is None:
      key_bytes = self._key_locator(key_id)

    if key_bytes is None:
      raise PublicKeyNotFoundError()
    elif not isinstance(key_bytes, bytes):
      raise Exception(
          'Return value of "key_locator" must be an instance of `bytes`')

    return load_pem_public_key(key_bytes, backend=default_backend())
