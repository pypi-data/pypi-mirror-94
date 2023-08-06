# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_tester']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0',
 'djangorestframework',
 'inflection>=0.4.0,<0.5.0',
 'openapi-spec-validator>=0.2.9,<0.3.0',
 'prance>=0.16.0,<0.17.0',
 'pyYAML']

setup_kwargs = {
    'name': 'drf-openapi-tester',
    'version': '1.1.0',
    'description': 'Django test utility for validating OpenAPI response documentation',
    'long_description': '\n<p align="center"><h1 align=\'center\'>DRF OpenAPI Tester</h1></p>\n<p align="center">\n    <em>A test utility for validating response documentation</em>\n</p>\n<p align="center">\n    <a href="https://pypi.org/project/drf-openapi-tester/">\n        <img src="https://img.shields.io/pypi/v/drf-openapi-tester.svg" alt="Package version">\n    </a>\n    <a href="https://codecov.io/gh/snok/drf-openapi-tester">\n        <img src="https://codecov.io/gh/snok/drf-openapi-tester/branch/master/graph/badge.svg" alt="Code coverage">\n    </a>\n    <a href="https://pypi.org/project/drf-openapi-tester/">\n        <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="Supported Python versions">\n    </a>\n    <a href="https://pypi.python.org/pypi/drf-openapi-tester">\n        <img src="https://img.shields.io/badge/django%20versions-2.2%2B-blue" alt="Supported Django versions">\n    </a>\n    <a href="http://mypy-lang.org/">\n        <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n    </a>\n</p>\n\nDRF OpenAPI Tester is a simple test utility. Its aim is to make it easy for\ndevelopers to catch and correct documentation errors in their OpenAPI schemas.\n\n## Installation\n\n\n```shell script\npip install drf-openapi-tester\n```\n\n## How does it work?\n\nTesting your schema is as simple as calling `validate_response` at the end\nof a regular test.\n\n```python\nfrom openapi_tester.case_testers import is_camel_case\nfrom openapi_tester.schema_tester import SchemaTester\n\nschema_tester = SchemaTester(case_tester=is_camel_case)\n\n\ndef test_response_documentation(client):\n    response = client.get(\'api/v1/test/1\')\n\n    assert response.status_code == 200\n    assert response.json() == expected_response\n\n    schema_tester.validate_response(response=response)\n```\n\n## Supported OpenAPI Implementations\n\nWhether we\'re able to test your schema or not will depend on how it\'s implemented.\nWe currently support the following:\n\n- Testing dynamically rendered OpenAPI schemas with [drf-yasg](https://github.com/axnsan12/drf-yasg)\n- Testing dynamically rendered OpenAPI schemas with [drf-spectacular](https://github.com/tfranzel/drf-spectacular)\n- Testing any implementation which generates a static yaml or json file (e.g., like [DRF](https://www.django-rest-framework.org/topics/documenting-your-api/#generating-documentation-from-openapi-schemas))\n\nIf you\'re using another method to generate your schema and\nwould like to use this package, feel free to add an issue or\ncreate a PR.\n\nAdding a new implementation is as easy as adding the\nrequired logic needed to load the OpenAPI schema.\n\n## Features\n\nThe primary feature of the schema tester is to validate your API responses\nwith respect to your documented responses.\nIf your schema correctly describes a response, nothing happens;\nif it doesn\'t, we throw an error.\n\nThe second, optional feature, is checking the [case](https://en.wikipedia.org/wiki/Naming_convention_(programming)) of your\nresponse keys. Checking that your responses are camel cased is\nprobably the most common standard, but the package supplies case testers\nfor the following formats:\n\n- `camelCase`\n- `snake_case`\n- `PascalCase`\n- `kebab-case`\n\n## The schema tester\n\nThe schema tester is a class, and can be instantiated once or multiple times, depending on your needs.\n\n```python\nfrom openapi_tester.schema_tester import SchemaTester\nfrom openapi_tester.case_testers import is_camel_case\n\ntester = SchemaTester(\n    case_tester=is_camel_case,\n    ignore_case=[\'IP\'],\n    schema_file_path=file_path\n)\n```\n\n### Case tester\n\nThe case tester argument takes a callable to validate the case\nof both your response schemas and responses. If nothing is passed,\ncase validation is skipped.\n\n### Ignore case\n\nList of keys to ignore. In some cases you might want to declare a global\nlist of exempt keys; keys that you know are not properly cased, but you do not intend to correct.\n\nSee the response tester description for info about ignoring keys for individal responses.\n\n### Schema file path\n\nThis is the path to your OpenAPI schema. **This is only required if you use the\nStaticSchemaLoader loader class, i.e., you\'re not using `drf-yasg` or `drf-spectacular`.**\n\n## The validate response method\n\nTo test a response, you call the `validate_response` method.\n\n```python\nfrom .conftest import tester\n\ndef test_response_documentation(client):\n    response = client.get(\'api/v1/test/1\')\n    tester.validate_response(response=response)\n```\n\nIf you want to override the instantiated `ignore_case` list,\nor `case_tester` for a single test, you can pass these directly\nto the function.\n\n```python\nfrom .conftest import tester\nfrom openapi_tester.case_testers import is_snake_case\n\ndef test_response_documentation(client):\n    ...\n    tester.validate_response(\n        response=response,\n        case_tester=is_snake_case,\n        ignore_case=[\'DHCP\']\n    )\n```\n\n### Supporting the project\n\nPlease leave a ✭ if this project helped you 👏 and contributions are always welcome!\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': "Na'aman Hirschfeld",
    'maintainer_email': 'nhirschfeld@gmail.com',
    'url': 'https://github.com/snok/drf-openapi-tester',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
