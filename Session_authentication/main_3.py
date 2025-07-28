#!/usr/bin/env python3
""" Main 3 - Test BasicAuth extract method """
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))  # None
print(a.extract_base64_authorization_header(89))  # None
print(a.extract_base64_authorization_header("Basic"))  # None
print(a.extract_base64_authorization_header("Basic 123"))  # '123'
