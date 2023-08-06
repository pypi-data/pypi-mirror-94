# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alteia_cli']

package_data = \
{'': ['*'], 'alteia_cli': ['share/*']}

install_requires = \
['alteia>=1.0.2,<2.0.0',
 'click_spinner==0.1.8',
 'jsonschema==3.2.0',
 'pyinquirer>=1.0.3,<2.0.0',
 'pyyaml==5.3.1',
 'tabulate==0.8.7',
 'typer[all]==0.1.1']

entry_points = \
{'console_scripts': ['alteia = alteia_cli.main:app']}

setup_kwargs = {
    'name': 'alteia-cli',
    'version': '1.0.0',
    'description': 'CLI for Alteia',
    'long_description': '# CLI for alteia\n\n# `alteia`\n\n**Usage**:\n\n```console\n$ alteia [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `analytics`: Interact with Analytics\n* `configure`: Configure your credentials to connect to the...\n* `credentials`: Interact your Docker registry credentials\n* `products`: Interact with Products\n\n## `alteia configure`\n\nConfigure your credentials to connect to the platform\n\n**Usage**:\n\n```console\n$ alteia configure [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia analytics`\n\nInteract with Analytics\n\n**Usage**:\n\n```console\n$ alteia analytics [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a new analytic\n* `delete`: Delete an analytic\n* `list`: List the analytics\n* `share`: Share an analytic\n* `unshare`: Unshare an analytic\n\n### `alteia analytics create`\n\nCreate a new analytic\n\n**Usage**:\n\n```console\n$ alteia analytics create [OPTIONS]\n```\n\n**Options**:\n\n* `--description PATH`: Path of the Analytic description (YAML file)  [required]\n* `--company TEXT`: Company identifier\n* `--help`: Show this message and exit.\n\n### `alteia analytics delete`\n\nDelete an analytic\n\n**Usage**:\n\n```console\n$ alteia analytics delete [OPTIONS] ANALYTIC_NAME\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `alteia analytics list`\n\nList the analytics\n\n**Usage**:\n\n```console\n$ alteia analytics list [OPTIONS]\n```\n\n**Options**:\n\n* `--limit INTEGER`: Max number of analytics returned\n* `--help`: Show this message and exit.\n\n### `alteia analytics share`\n\nShare an analytic\n\n**Usage**:\n\n```console\n$ alteia analytics share [OPTIONS] ANALYTIC_NAME\n```\n\n**Options**:\n\n* `--company TEXT`: Company identifier\n* `--help`: Show this message and exit.\n\n### `alteia analytics unshare`\n\nUnshare an analytic\n\n**Usage**:\n\n```console\n$ alteia analytics unshare [OPTIONS] ANALYTIC_NAME\n```\n\n**Options**:\n\n* `--company TEXT`: Company identifier\n* `--help`: Show this message and exit.\n\n## `alteia credentials`\n\nInteract your Docker registry credentials\n\n**Usage**:\n\n```console\n$ alteia credentials [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a new credential entry\n* `delete`: Delete a credential entry by its name\n* `list`: List the existing credentials\n\n### `alteia credentials create`\n\nCreate a new credential entry\n\n**Usage**:\n\n```console\n$ alteia credentials create [OPTIONS]\n```\n\n**Options**:\n\n* `--filepath PATH`: Path of the Credential JSON file  [required]\n* `--help`: Show this message and exit.\n\n### `alteia credentials delete`\n\nDelete a credential entry by its name\n\n**Usage**:\n\n```console\n$ alteia credentials delete [OPTIONS] NAME\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `alteia credentials list`\n\nList the existing credentials\n\n**Usage**:\n\n```console\n$ alteia credentials list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia products`\n\nInteract with Products\n\n**Usage**:\n\n```console\n$ alteia products [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `cancel`: Cancel a running product\n* `list`: List the products\n* `logs`: Retrieve the logs of a product\n\n### `alteia products cancel`\n\nCancel a running product\n\n**Usage**:\n\n```console\n$ alteia products cancel [OPTIONS] PRODUCT_ID\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `alteia products list`\n\nList the products\n\n**Usage**:\n\n```console\n$ alteia products list [OPTIONS]\n```\n\n**Options**:\n\n* `-n, --limit INTEGER`: Max number of analytics returned  [default: 10]\n* `--analytic TEXT`: Analytic name\n* `--company TEXT`: Company identifier\n* `--status [pending|processing|available|rejected|failed]`: Product status\n* `--all`: If set, display also the products from internal analytics (otherwise only products from external analytics are displayed).\n* `--help`: Show this message and exit.\n\n### `alteia products logs`\n\nRetrieve the logs of a product\n\n**Usage**:\n\n```console\n$ alteia products logs [OPTIONS] PRODUCT_ID\n```\n\n**Options**:\n\n* `-f, --follow`: Follow logs\n* `--help`: Show this message and exit.\n\n---\n\n*Generated with `typer alteia_cli/main.py utils docs --name alteia`*\n',
    'author': 'Alteia Backend Team',
    'author_email': 'backend-team@alteia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
