# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envolved']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envolved',
    'version': '0.4.1',
    'description': '',
    'long_description': '# Envolved\nEnvolved is a library to make environment variable parsing powerful and effortless.\n\n```python\nfrom envolved import EnvVar\n\n# create an env var with an int value\nfoo: EnvVar[int] = EnvVar(\'FOO\', type=int, default=0)\nvalue_of_foo = foo.get()  # this method will check for the environment variable FOO, and parse it as an int\n\n# we can also have some more complex parsers\nfrom typing import List, Optional\nfrom envolved.parsers import JsonParser\n\nfoo = EnvVar(\'FOO\', type=JsonParser(List[float]))\nfoo.get()  # now we will parse the value of FOO as a JSON list, and ensure that all its inner values are numbers\n\n# we can also use schemas to combine multiple environment variables\nfrom envolved import Schema\nfrom dataclasses import dataclass\n\n\n@dataclass\n# say we want the environment to describe a ConnectionSetting\nclass ConnectionSetting:\n    host: str\n    port: int\n    user: Optional[str]\n    password: Optional[str]\n    \n# note that schemas work with any factory or class that annotates its constructor, dataclass is used for simplicity\n\nclass ConnectionSettingSchema(Schema, type=ConnectionSetting):\n    host = EnvVar(\'hostname\') \n    # we now define an env var inside the schema. Its suffix will be "hostname", and its type will be inferred from the\n    # type\'s annotation\n    port = EnvVar()  # if we like the parameter name as the env var suffix, we can leave the env var empty\n    user: str = EnvVar(\'username\')  # we can annotate the schema members to override the type inference\n    password = EnvVar(type=str, default=None)  # we can set a default to show that the type var may be missing\n\nconnection_settings: EnvVar[ConnectionSetting] = EnvVar(\'service_\', type=ConnectionSettingSchema)\nservice_connection_settings: ConnectionSetting = connection_settings.get() \n# this will look in 4 environment variables:\n# host will be extracted from service_hostname\n# port will be extracted from service_port, then converted to an int\n# user will be extracted from service_username\n# password will be extracted from service_password, and will default to None\n# finally, ConnectionSetting will be called with the parameters\n```\n',
    'author': 'ben avrahami',
    'author_email': 'avrahami.ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bentheiii/envolved',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
