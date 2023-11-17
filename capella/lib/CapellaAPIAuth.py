# -*- coding: utf-8 -*-
# Generic/Built-in
import base64
import hmac
import hashlib
from requests.auth import AuthBase

# Other Libs

# Owned
import time


class CapellaAPIAuth(AuthBase):
    # Extends requests AuthBase for
    # Couchbase Cloud API Authentication Handler.

    def __init__(self, secret, access, token):
        # Create an authentication handler for Couchbase Cloud APIs
        # :param str access_key: access key for Couchbase Cloud
        # :param str secret_key: secret key for Couchbase Cloud

        self.ACCESS_KEY = access
        self.SECRET_KEY = secret
        self.bearer_token = token

    def __call__(self, request):
        if "v4" in request.url:
            # Values for the header
            cbc_api_request_headers = {
                'Authorization': 'Bearer ' + self.bearer_token,
                'Content-Type': 'application/json'
            }
        else:
            # This is the endpoint being called
            # Split out from the entire URL
            endpoint = request.url.split(".com", 1)[-1]

            # The method being used
            method = request.method

            # Epoch time in milliseconds
            cbc_api_now = int(time.time() * 1000)

            # Form the message string for the Hmac hash
            cbc_api_message = method + '\n' + endpoint + '\n' + str(cbc_api_now)

            # Calculate the hmac hash value with secret key and message
            cbc_api_signature = base64.b64encode(
                hmac.new(self.SECRET_KEY.encode(),
                         cbc_api_message.encode(),
                         digestmod=hashlib.sha256).digest())

            # Values for the header
            cbc_api_request_headers = {
               'Authorization': 'Bearer ' + self.ACCESS_KEY + ':' + cbc_api_signature.decode(),
               'Couchbase-Timestamp': str(cbc_api_now),
               'Content-Type': 'application/json'
            }
        # Add our key:values to the request header
        request.headers.update(cbc_api_request_headers)

        # Return the request back
        return request

