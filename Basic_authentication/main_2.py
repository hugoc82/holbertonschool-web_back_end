#!/usr/bin/env python3
""" Main 2 - Test authentication requirement
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/stats", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status", ["/api/v1/status/", "/api/v1/stats/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats/"]))
print(a.authorization_header())
print(a.current_user())
