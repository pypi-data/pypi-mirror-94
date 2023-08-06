# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psion',
 'psion.jose',
 'psion.jose.jwa',
 'psion.oauth2',
 'psion.oauth2.authentication',
 'psion.oauth2.authentication.methods',
 'psion.oauth2.endpoints',
 'psion.oauth2.grants',
 'psion.oauth2.models',
 'psion.oauth2.providers',
 'psion.oidc',
 'psion.oidc.flows']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'psion',
    'version': '0.1.1',
    'description': 'Asynchronous WebAuth library for python.',
    'long_description': '# Project Psion\n\nThis library provides an implementation for asynchronous authentication and authorization of web applications.\nIt provides support for OAuth 2.1 and OpenID Connect, as well as JOSE.\n\nFor more details, please visit the documentation.\n\nAny doubts and suggestions can be sent to my [email](mailto:eduardorbr7@gmail.com).\nJust prepend the title with #Psion#, and I will try my best to answer.\n\n## JSON Object Signature and Encryption (JOSE)\n\nIt implements the following RFCs.\n\n1. [x] RFC 7515 - Json Web Signature (JWS)\n2. [ ] RFC 7516 - Json Web Encryption (JWE)\n3. [x] RFC 7517 - Json Web Key and Keyset (JWK)\n4. [x] RFC 7518 - Json Web Algorithms (JWA)\n5. [x] RFC 7519 - Json Web Token (JWT)\n\nFor more details on each feature, please visit the respective documentation.\n\n## OAuth 2.1\n\nIt implements the following RFCs and Specs.\n\n1. [x] Draft - The OAuth 2.1 Authorization Framework\n2. [x] RFC 7009 - OAuth 2.0 Token Revocation\n\n# License\n\nThis project is licensed under the MIT License.\n',
    'author': 'Eduardo Ribeiro Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/revensky/psion',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
