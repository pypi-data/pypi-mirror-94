# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pixivapi']

package_data = \
{'': ['*']}

install_requires = \
['cloudscraper>=1.2.48,<2.0.0', 'requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pixiv-api',
    'version': '1.0.0',
    'description': 'A library for the Pixiv API.',
    'long_description': '=========\npixiv-api\n=========\n\n|CI| |Codecov| |Docs| |PyPI|\n\n.. |CI| image:: https://img.shields.io/github/workflow/status/azuline/pixiv-api/CI\n   :target: https://github.com/azuline/pixiv-api/actions\n.. |Codecov| image:: https://img.shields.io/codecov/c/github/azuline/pixiv-api?token=TJSEWBI2ZC\n   :target: https://codecov.io/gh/azuline/pixiv-api\n.. |Docs| image:: https://readthedocs.org/projects/pixiv-api/badge/?version=latest\n   :target: https://pixiv-api.readthedocs.io/en/latest/?badge=latest\n.. |PyPI| image:: https://img.shields.io/pypi/v/pixiv-api.svg\n   :target: https://pypi.python.org/pypi/pixiv-api\n\nA documented, idiomatic, and tested wrapper library around Pixiv\'s App API.\n\nSupports Python versions 3.6+.\n\nInstall with:\n\n.. code-block:: bash\n\n   $ pip install pixiv-api\n\nQuickstart\n==========\n\nTo start making requests to the Pixiv API, instantiate a client object.\n\n.. code-block:: python\n\n   from pixivapi import Client\n\n   client = Client()\n\nThe client can be authenticated to Pixiv\'s API in multiple ways. One is by\nlogging in with a username and password:\n\n.. code-block:: python\n\n   client.login("username", "password")\n\nAnd another is with a refresh token.\n\n.. code-block:: python\n\n   client.authenticate("refresh_token")\n\nOnce authenticated, a refresh token can be saved for future authorizations.\n\n.. code-block:: python\n\n   refresh_token = client.refresh_token\n\nAfter authenticating, the client can begin making requests to all of the\nPixiv endpoints. For example, the following code block downloads an\nimage from Pixiv.\n\n.. code-block:: python\n\n   from pathlib import Path\n   from pixivapi import Size\n\n   illustration = client.fetch_illustration(75523989)\n\n   illustration.download(\n       directory=Path.home() / "my_pixiv_images",\n       size=Size.ORIGINAL,\n   )\n\nAnd the next code block downloads all illustrations of an artist.\n\n.. code-block:: python\n\n   from pathlib import Path\n   from pixivapi import Size\n\n   artist_id = 2188232\n   directory = Path.home() / "wlop"\n\n   response = client.fetch_user_illustrations(artist_id)\n\n   while True:\n       for illust in response["illustrations"]:\n           illust.download(directory=directory, size=Size.ORIGINAL)\n\n       if not response["next"]:\n           break\n\n       response = client.fetch_user_illustrations(\n           artist_id,\n           offset=response["next"],\n       )\n\nRead the full documentation at https://pixiv-api.readthedocs.io.\n',
    'author': 'blissful',
    'author_email': 'blissful@sunsetglow.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azuline/pixiv-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
