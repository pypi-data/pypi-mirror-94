# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lido',
 'lido.constants',
 'lido.contracts',
 'lido.eth2deposit',
 'lido.eth2deposit.utils',
 'lido.multicall',
 'lido.utils']

package_data = \
{'': ['*'], 'lido.contracts': ['abi/goerli/*', 'abi/mainnet/*']}

install_requires = \
['py-ecc>=5.1.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'ssz>=0.2.4,<0.3.0',
 'web3>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'lido',
    'version': '0.2.2',
    'description': 'Network helpers for Lido',
    'long_description': '# Lido\n\nThis library consolidates various functions to efficiently load network data for Lido, validate node operator keys and find key duplicates.\n\n## Installation\n\nThis library is available on PyPi:\n\n`pip install lido`\n\n## Main Features\n\n### Multicall Function Calls\n\nInstead of making network requests one-by-one, this library combines many requests into one RPC call. It uses [banteg/multicall.py](https://github.com/banteg/multicall.py), a Python wrapper for [makerdao/multicall](https://github.com/makerdao/multicall).\n\n### Multiprocess Signature Validations\n\nWhen using `validate_keys_multi()`, this library spreads processing of key signature validations to all system cores.\n\n### Automatic Testnet / Mainnet Switching\n\nDepending on the supplied WEB3_PROVIDER_URI, a correct network will be used. Even an appropriate ABI will be loaded for the chain automatically.\n\n## Helpers Provided\n\n- get_operators_data() -> operator_data - load node operator data\n\n- get_operators_keys(operator_data) -> operator_data - fetches and adds keys to operator_data\n- validate_keys_mono(operator_data) -> operator_data - validates keys in single process and adds validation results to operator_data\n- validate_keys_multi(operator_data) -> operator_data - validates keys in multiple processes and adds validation results to operator_data, requires a main function (see example)\n- validate_key([[key,depositSignature]]) -> Boolean - low-level validation function\n- find_duplicates(operator_data) -> operator_data - finds duplicate keys and adds results to operator_data\n\n- fetch_and_validate() -> operator_data - combines fetching operator data and running all validations on it - useful when you would be running all validations on data anyway\n\n- get_stats() -> stats - fetches various constants from Lido contract, but you can even pass a list of functions to fetch eg get_stats([isStopped])\n\nYou can mix and match these functions, but make sure to use get_operators_data() first.\n\n## Notes\n\n1. Signature validation will be skipped if its results are already present in operator_data. This way you can safely load validation results from cache and add `["valid_signature"] = Boolean` to already checked keys.\n\n## How to Use\n\nUse a RPC provider url as an environment variable and run your script:\n\n`WEB3_PROVIDER_URI=https://eth-mainnet.provider.xx example.py`\n\nSee `example.py` for a complete example, make sure to use a main function and a script entry point check when using validate_keys_multi() or fetch_and_validate().\n\n## Options\n\nIf you are testing a new deployment of Lido, these environment variables can override addresses and ABIs:\n\n- LIDO_ADDRESS\n- REGISTRY_ADDRESS\n- LIDO_ABI (the file-path to the contract\'s ABI)\n- REGISTRY_ABI (the file-path to the contract\'s ABI)\n\n`WEB3_PROVIDER_URI=https://eth-mainnet.provider.xx LIDO_ADDRESS=XXX REGISTRY_ADDRESS=XXX LIDO_ABI=xxx.json REGISTRY_ABI=xxx.json example.py`\n',
    'author': 'Lido',
    'author_email': 'info@lido.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lido.fi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7.1,<4',
}


setup(**setup_kwargs)
