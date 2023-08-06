# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flightplan', 'flightplan.quickstart', 'flightplan.render']

package_data = \
{'': ['*']}

install_requires = \
['pydantic', 'pyyaml', 'typer']

entry_points = \
{'console_scripts': ['fp = flightplan.cli:main']}

setup_kwargs = {
    'name': 'flightplan',
    'version': '0.1.2',
    'description': 'Code based description for Concourse pipelines',
    'long_description': '\n\n# Flight plan - Plan your Concourse Pipeline with ease\n\nAWS CDK like tool to code Concourse pipelines (with autocompletion.)\n\n## Why not stick with YAML\n\nWriting YAML files feels not as heavy as XML, \nbut still lacks the comfort of autocompletion and some kind of structuring \n(Beside anchors or tools like [YTT](https://get-ytt.io/)).\n\nThe vision of Flightplan does not stop with replacing YAML, the real benefit\nstarts with component libraries, which ease the setup of pipelines.\n\nFurthermore these components can be updated, which make all improvements \nautomatically available to all pipelines.  \n\n## Features\n\n* Convert:\n  * YAML -> Python\n  * Python -> YAML\n* Fly integration\n  * Set pipeline\n  * Get pipeline\n* Shiped examples\n  * Hello world\n  * more to come\n\n## Disclaimer - Alpha\n\n> The package is still in alpha. Upcoming versions may include breaking changes. \n\n## Upcoming\n\n* Provide high level components that handle common use cases\n\n## Setup \n\nFlightplan requires Python 3.8 and higher.\n\n### Install FlightPlan\n\nFlightplan requires `fly` to be installed on path.\n\n```bash\npip3 install flightplan\n```\n\n## Usage\n\nIf you start with Flightplan it is recommended to have a look on the quickstart examples, \nwhich are shipped within the cli.\n\nIf you want to migrate an existing pipeline you can use \n * `fp import` - to convert YAML to Python\n * `fp get ...` - to get and convert a running pipeline \n\n### Quickstart\nGenerate a basic pipeline example.\n\n```bash\nfp quickstart\n```\n\n### Import existing pipeline file\nConvert a pipeline yaml and render a flightplan `.py` file.\n\n```bash\nfp import <src.yaml> <target.py>\n```\n\n### Import existing pipeline from fly\nConvert a pipeline from fly and render a flightplan `.py` file.\n\n```bash\nfp get <fly_target> <pipeline_name> <target.py>\n```\n\n> Static and dynamic vars will be imported as `Var(str)`, if the type of the field is limited to an int or Enum type.\n\n### Synthesize yaml from flightplan `.py` file\n\n```bash\nfp synth <src.py> <target.yaml>\n```\n\n### Direct Fly Set Pipeline\n\n```bash\nfp set <fly-target> <pipeline_name> <src.py>\n```\n\n\n\n## Examples\n\nQuickstart hello world example:\n\n```python\nfrom flightplan.render import *\n\npipe = Pipeline(\n    resource_types=[],\n    resources=[],\n    jobs=[\n        Job(\n            name="job-hello-world",\n            public=True,\n            plan=[\n                Task(\n                    task="hello-world",\n                    config=TaskConfig(\n                        platform="linux",\n                        image_resource=ImageResource(\n                            type="docker-image",\n                            source=dict(repository="busybox", tag="latest"),\n                        ),\n                        run=Command(path="echo", args=["hello world"]),\n                        inputs=[],\n                        outputs=[],\n                    ),\n                )\n            ],\n        )\n    ],\n)\n\nif __name__ == "__main__":\n    print(pipe.synth())\n``` \n',
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/flightplan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
