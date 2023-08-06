# flask-signature-auth
[![Build Status](https://travis-ci.com/kunyo/flask-signature-auth.svg?branch=master)](https://travis-ci.com/kunyo/flask-signature-auth)

A Python module for Flask providing capabilities to validate signed HTTP requests.

## Install
```shell
pip install flask-signature-auth
```
## Basic usage
### Server
```python
from flask import Flask, request, jsonify
from flask_signature_auth import FlaskSignatureAuth

public_key_id = "3ed0451935d27b4f0e225486a634fe40aa3e2cfbc202efc96b174af83211189c"
public_key = b'''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5wuCpbcNOE2iily97JF+
yoaaYDQPu78UQI7IWJH37cAsct9sHkDh9ISB1D8pW6vEAcAnq6EsjUQy43p3g601
hMGflb0nj/TMfDgcnZBp3QwLrQQHoTRbzDDBGZnUKJ3+tzaGsHJ/zniCDMUT1PWR
/wd5sAxPW31CJZKkkbtls2RVygsI7BcV2G85WszzQJ9dCys94IE21TOV4ktoNysR
05lrP30PZBcNs3Myr5w+2lFH3dC0w7L16Z4db5+hWFPAqj5ZxNor+0+PiGQdl2p6
bZRawylW/Ei5hwR28PrOeHGNBbLzwfumlCCMITpkrBWefdnTimuRTjT9pWFHaS1m
YwIDAQAB
-----END PUBLIC KEY-----
'''
auth = FlaskSignatureAuth(key_bytes=public_key)
app = Flask(__name__)


@app.route('/userinfo', methods=['GET'])
@auth.auth_required()
def get_userinfo():
  return jsonify({'key_id': auth.current_user().key_id}), 200


@app.route('/userinfo', methods=['POST'])
@auth.auth_required()
def change_userinfo():

  if not request.is_json:
    return '', 400

  return jsonify({
      'key_id': auth.current_user().key_id,
      'first_name': request.json['first_name'],
      'last_name': request.json['last_name']
  }), 200
```

## Options
|Option name|Type|Optional|Default Value|Description|
|---|---|---|---|---|
|ttl|`int`|YES|`10`|The lifetime of a signed http request signature, expressed in seconds. This gets calculated using the `(created)` timestamp of a request|
|algorithm|`str`|YES|`rsa-sha256`|The algorithm used to verify signatures. See supported algorithms below|
|key_bytes|`bytes`|YES|`None`|A bytes representation of a valid PEM key|
|key_locator|`callable`|YES|`None`|A function used to retrieve the key associated with a specific key ID|
|headers|`list`|YES|`['(request-target)', '(created)', 'Digest']`|A list of headers to be included in the string to sign|
|header_name|`str`|YES|`Authorization`|Force usage of a different HTTP header to store the signature (e.g: `Signature`)|
## Supported algorithms
|Name|Notes|
|---|---|
|`rsa-sha256`|Supported padding: `PKCS1v15`|

## Examples
|||
|---|---|
|[Basic Server](./examples/basic-server.py)|A server implementation that validates an HTTP request signature using a pre-shared public-key|
|[Basic Client](./examples/basic-client.py)|A client implementation that uses Python `requests` module to send a signed HTTP request|

