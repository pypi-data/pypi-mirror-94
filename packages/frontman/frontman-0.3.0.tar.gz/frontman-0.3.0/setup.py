# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['frontman']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['frontman = frontman.main:app']}

setup_kwargs = {
    'name': 'frontman',
    'version': '0.3.0',
    'description': 'Frontend Library Manager',
    'long_description': '# FrontMan - Frontend Library Manager\n\nTool to help manage frontend dependencies (javascript, css)\n\nInspired by [AspNet Library Manager](https://github.com/aspnet/LibraryManager)\n\n## Installation\n\n```sh\npip install frontman\n```\n\n## Usage\n\n1. Create the manifest file `frontman.json`\n\n```json\n{\n  "provider": "jsdelivr",\n  "destination": "assets",\n  "packages": [\n    {\n      "name": "jquery",\n      "version": "3.5.1",\n      "provider": "cdnjs",\n      "files": [\n        {\n          "name": "jquery.min.js",\n          "destination": "jquery"\n        }\n      ]\n    },\n    {\n      "name": "@popperjs/core",\n      "version": "2.6.0",\n      "path": "dist/umd",\n      "destination":"popper",\n      "files": [\n        {\n          "name": "popper.min.js",\n          "rename": "popper.js"\n        }\n      ]\n    },\n    {\n      "name": "bootstrap",\n      "version": "4.6.0",\n      "path": "dist",\n      "destination": "bootstrap",\n      "files": [\n        "js/bootstrap.min.js",\n        "css/bootstrap.min.css"\n      ]\n    }\n  ]\n}\n```\n\n2. Execute FrontMan\n\n```shell\nfrontman install\n```\n\nYou should see an output like this:\n\n```\nOK   https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js -> assets/jquery/jquery.min.js\nOK   https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js -> assets/popper/popper.js\nOK   https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js -> assets/bootstrap/js/bootstrap.min.js\nOK   https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css -> assets/bootstrap/css/bootstrap.min.css\n```\n\n## Force package download\n\nBy default, files that already have been downloaded will be skipped. To force download these files, use the `--force` (or `-f`) flag:\n\n```sh\nfrontman install --force\n```\n\n## Manifest Format\n\n**provider**: The server we will download the files from. It can be `cdnjs`, `jsdelivr` or `unpkg`.\n\n**destination**: Directory where the files will be downloaded.\n\n**packages**: List of packaged to be downloaded.\n\nEach package item have the following format:\n\n**name**: Name of the package, according to the chosen provider.\n\n**version**: Version of the package.\n\n**path** (Optional): The provider may serve the files in a sub path (eg. "dist"). Setting this option will strip the path from the downloaded file path.\n\n**destination** (Optional): Directory inside the top level `destination` where the files from this package will be downloaded.\n\n**provider** (Optional): Provider to use for this package.\n\n**files**: List of files to download for this package.\n\nThe files can be specified as string containing the path to the file. The path specified here will be present in the final destination (eg. "js/bootstrap.min.js" will be downloaded to "{destination}/js/bootstrap.min.js")\n\nFiles can also be specified as objects with the following format:\n\n**name**: Name of the file to download.\n\n**destination**: Directory to be appended to the previous `destination`.\n\n**rename**: Change the name of the downloaded file.\n',
    'author': 'Livio Ribeiro',
    'author_email': 'livioribeiro@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/livioribeiro/frontman',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
