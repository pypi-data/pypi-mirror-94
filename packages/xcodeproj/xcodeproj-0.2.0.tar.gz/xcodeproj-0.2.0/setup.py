# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcodeproj']

package_data = \
{'': ['*']}

install_requires = \
['deserialize>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'xcodeproj',
    'version': '0.2.0',
    'description': "A utility for interacting with Xcode's xcodeproj bundle format.",
    'long_description': "# xcodeproj\n\n`xcodeproj` is a utility for interacting with Xcode's xcodeproj bundle format.\n\n## Contributing\n\nThis project welcomes contributions and suggestions.  Most contributions require you to agree to a\nContributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us\nthe rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.\n\nWhen you submit a pull request, a CLA bot will automatically determine whether you need to provide\na CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions\nprovided by the bot. You will only need to do this once across all repos using our CLA.\n\nThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).\nFor more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or\ncontact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.\n\n## Trademarks\n\nThis project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft \ntrademarks or logos is subject to and must follow \n[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).\nUse of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.\nAny use of third-party trademarks or logos are subject to those third-party's policies.\n",
    'author': 'Dale Myers',
    'author_email': 'dalemy@microsoft.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Microsoft/xcodeproj',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
