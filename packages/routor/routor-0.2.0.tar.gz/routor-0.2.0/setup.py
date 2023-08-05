# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routor', 'routor.api', 'routor.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'more-itertools>=8.6.0,<9.0.0',
 'networkx-astar-path>=1.0.1,<2.0.0',
 'networkx>=2.5,<3.0',
 'osmnx>=0.16.2,<0.17.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'uvicorn>=0.13.2,<0.14.0']

entry_points = \
{'console_scripts': ['routor = routor.cli:main']}

setup_kwargs = {
    'name': 'routor',
    'version': '0.2.0',
    'description': 'Simple osm routing engine.',
    'long_description': '# routor\n\n![PyPI](https://img.shields.io/pypi/v/routor?style=flat-square)\n![GitHub Workflow Status (main)](https://img.shields.io/github/workflow/status/escaped/routor/Test%20&%20Lint/main?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/routor/main?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/routor?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/routor?style=flat-square)\n\nSimple osm routing engine.\n\n## Requirements\n\n* Python 3.6.1 or newer\n\n## Installation\n\n```sh\npip install routor\n```\n\n## Usage\n\n### CLI\n\nThe CLI offers multiple commands, use `routor --help` to find out more.\n\n#### Download map\n\nDownloads a compatible map from OSM, eg.\n\n```sh\nroutor download "Bristol, England" ./bristol.graphml\n```\n\n#### Calculate route\n\nDetermine the optimal route between two points using the given weight function and print the route as `JSON` to `stdout`.\n\n```sh\nroutor route -- ./bristol.graphml  "51.47967237816338,-2.6174926757812496" "51.45422084861252,-2.564105987548828" "routor.weights.length"\n```\n\n### Web API\n\n#### Configuration\n\nThe configuration is either read from a `.env` file or the environment.\nBefore you are able to run the server, you have to set the variables mentioned in [routor/api/config.py](routor/api/config.py).\n\n#### Run the API\n\nThe api is served using [uvicorn](https://www.uvicorn.org/).\nTo start the server run\n\n```sh\nuvicorn routor.api:app\n```\n\nThe API will be available at http://127.0.0.1:8000 and the docs at http://127.0.0.1:8000/docs.\n\n#### Register a new weight function\n\nExisting weight functions are defined in [routor/weights.py](routor/weights.py).\nTo add a new weight functon, you have to create a new project and add `routor` as dependency.\nCreate a new file, eg. `main.py` and add the following content, which will become the entrypoint for `uvicorn`.\n\n```python\n# main.py\nfrom typing import Optional\n\nfrom routor.api.main import app  # noqa\nfrom routor.weights import register\nfrom routor import models\n\n\ndef my_weight_func(prev_edge: Optional[models.Edge], edge: models.Edge) -> float:\n    ...\n    return ...\n\n\nregister(my_weight_func, "weight_func")\n```\n\nStart the server with `uvicorn main:app` and the weight function will be available as `weight_func` when calling the api.\n\n### As library\n\nYou can also use the engine as a library.\nTo calculate a route from A to B you can do\n\n```python\nfrom routor.engine import Engine\nfrom routor import models, weights\n\n...\nmap_path = Path(...)\nengine = Engine(map_path)\n\norigin = models.Location(latitude=51.47967237816338, longitude=-2.6174926757812496)\ndestination = models.Location(latitude=51.45422084861252, longitude=-2.564105987548828)\n\nroute = engine.route(origin, destination, weights.length)  # shortest distance\n```\n\n## Available weight-functions\n\n### `"length"` / `routor.weights.length`\n\nCalculates the shortest path from A to B, only the length of an edge is taken into account.\n\n### `"travel_time"` / `routor.weight.travel_time`\n\nCalculates the fastest route based on [travel time](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.speed.add_edge_travel_times).\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nAdditionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) are installed to provide a better debugging experience.\nTo enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n',
    'author': 'Alexander Frenzel',
    'author_email': 'alex@relatedworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/escaped/routor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
