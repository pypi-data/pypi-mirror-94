# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_manage']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2',
 'PyMySQL>=0.9.3',
 'SQLAlchemy>=1.3.20',
 'alembic>=1.4.3',
 'configobj>=5.0.6',
 'fastapi>=0.62.0',
 'typer>=0.3.2',
 'uvicorn>=0.11.8']

entry_points = \
{'console_scripts': ['fastapi-manage = fastapi_manage.main:app']}

setup_kwargs = {
    'name': 'fastapi-manage',
    'version': '0.7.1',
    'description': 'FastAPI template generation, database version management tools',
    'long_description': '# fastapi_manage\n\n#### Project description\nfastapi的模板生成，数据库版本管理项目。  \nFastAPI template generation, database version management tools.  \nJust like Django.  \n\nfastapi+sqlalchemy  \n\n#### Installation\n```shell\npip install fastapi-manage\n```\n\n#### Usage\n##### startproject\nCreates a fastapi project directory structure for the given project name in the\ncurrent directory or optionally in the given directory.\n```shell\nfastapi-manage startproject yourproject\n```\n\n##### makemigrations\nCreates new migration(s) for project.\n```shell\ncd ./yourproject\npython manage.py makemigrations\n```\n\n##### migrate\nUpdates database schema. Manages both apps with migrations and those without.\n```shell\ncd ./yourproject\npython manage.py migrate\n```\n\n##### runserver\nStart a Web server\n```shell\ncd ./yourproject\npython mange.py runserver\n```\nOptions:  \n-h, --host\u3000\u3000\u3000\u3000\u3000[default:127.0.0.1]  \n-p, --port\u3000\u3000\u3000\u3000\u3000[default:8000]  \n-w, --workers\u3000\u3000\u3000[default:1]  \n--reload\u3000\u3000\u3000\u3000\u3000\u3000auto-reloader  \n',
    'author': 'lewei_huang',
    'author_email': 'auxpd96@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/LeanDe/fastapi-manage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
