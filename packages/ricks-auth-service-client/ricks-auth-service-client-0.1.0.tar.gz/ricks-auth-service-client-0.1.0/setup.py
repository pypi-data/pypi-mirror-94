# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ricks_auth_service_client']
install_requires = \
['aiohttp>=3.7.3,<4.0.0', 'python-jwt>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'ricks-auth-service-client',
    'version': '0.1.0',
    'description': 'Client library for my custom auth service',
    'long_description': '# ricks_auth_service_client\n\nAn async python client for my custom auth microservice.\n\n## Routes Covered\n\n### initialization\n\n```python\nfrom ricks_auth_service_client import AuthClient\n\nauth_client = AuthClient(\n    host="https://auth.example.com",\n    app_id="37f9a26d-03c8-4b7c-86ad-132bb82e8e38"\n)\n```\n\n### /otp/request/\n\nStart otp authentication flow with server.\n\n```python\nresult = await auth_client.authenticate(\n    "test@example.com", flow="otp"\n)\n```\n\n### /otp/confirm/\n\nComplete authentication with email and generated code.\n\n```python\nresult = await auth_client.submit_code("test@example.com", "12345678")\n```\n\n### /token/verify/\n\nSend idToken to server for verification.\n\n```python\nresult = await auth_client.verify_token_remote(token_submitted_by_client)\n```\n\n### /token/refresh/\n\nRequest a new ID Token from the server using a refresh token\n\n```python\nnew_token = await auth_client.refresh(refresh_token_from_client)\n```\n\n\n### /app/\n\nGet more info about this app from the server.\n\n```python\ninfo = await auth_client.app_info()\n```\n\n\n### /magic/request/\n\nStart authentication using magic link flow.\n\n```python\nresult = await auth_client.authenticate(\n    "test@example.com", flow="magic"\n)\n```\n\n\n## Local Verification\n\n\n',
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
