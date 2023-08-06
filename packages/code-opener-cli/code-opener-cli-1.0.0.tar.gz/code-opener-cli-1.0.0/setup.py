# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_opener_cli', 'code_opener_cli.tests', 'code_opener_cli.utils']

package_data = \
{'': ['*'], 'code_opener_cli': ['resources/*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['copen = code_opener_cli.main:app']}

setup_kwargs = {
    'name': 'code-opener-cli',
    'version': '1.0.0',
    'description': 'The CLI to handle your projects and Editors smartly',
    'long_description': "# Code Opener CLI ⌨️\n\nThe command line interface to add any project as favorite and open it from anywhere using just one command. Use `copen add` to add and `copen open <project_name>` to open and . See commands to get idea on more things supported by Code Opener CLI \n\n# Commands\n\n## See Lists of Projects Added \n\n```\ncopen see\n``` \n\n## Add a Project\n\n- <b> Method 1 : </b> \n    1. Adding Project just requires you to go to project using `cd` for the first time and type command <br>\n    `copen add` \n\n    ```\n    cd path/to/your/project\n    copen add\n    ```\n    2. This will ask for project name, give any nick name to project which is handy to you and press Enter.\n    <br>\n    Done :smile:, now you can open this project from anywhere . \n\n- <b> Method 2 : </b> \n        You can also directly add using one of the following single command :\n    1. Using short name `-pn` :\n        ```\n        copen add -pn <project_name>\n        ```\n    2. Using defualt Option name :\n        ```\n        copen add --project-name <project_name>\n        ```\n\n\n## Open a Project\n\nAfter a project is added , you can easily open it from anywhere using this command . Remember that project_name is the name/nick name that you gave to your project .\n\n```\n copen open <project_name>\n```\n\n\n## Remove a Project\n\n- <b> Method 1 :</b>\n    1. Removing Project is very easy using \n    ```\n    copen remove\n    ```\n    2. This will ask you for the project name and confirmation.\n\n- <b> Method 2 :</b>\n    You can also directly remove using one of the following single command :\n    1. Using short name `-pn` :\n        ```\n        copen remove -pn <project_name>\n        ```\n    2. Using defualt Option name :\n        ```\n        copen remove --project-name <project_name>\n        ```\n\n## Other handy commands \n\n- `copen` : Will display welcome message\n- `copen --help` : Provides list of commands\n- `copen <add/remove/see/open> --help` : Provides you help for particular command\n- `copen --version` : Provides you the version of code-opener-cli\n\n## Contributing to Project\n\nLet's take this project to next level together 🎉 You can find the guidelines to contribute to this project [here](https://github.com/shan7030/code-opener-cli/blob/master/CONTRIBUTING.md).\n\n## Changelogs\n\nAll notable changes to this projects can be found in [CHANGELOG.md](https://github.com/shan7030/code-opener-cli/blob/master/CHANGELOG.md) .\nCurrently, this CLI supports on VSCode, but support for other code editors/IDE's will be added soon :smile: .",
    'author': 'Shantanu Joshi',
    'author_email': 'shantanujoshi7030@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
