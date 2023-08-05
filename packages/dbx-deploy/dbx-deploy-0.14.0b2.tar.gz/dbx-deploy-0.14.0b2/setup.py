# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbxdeploy',
 'dbxdeploy.cluster',
 'dbxdeploy.dbc',
 'dbxdeploy.dbfs',
 'dbxdeploy.deploy',
 'dbxdeploy.git',
 'dbxdeploy.job',
 'dbxdeploy.notebook',
 'dbxdeploy.notebook.converter',
 'dbxdeploy.package',
 'dbxdeploy.s3',
 'dbxdeploy.string',
 'dbxdeploy.workspace']

package_data = \
{'': ['*'],
 'dbxdeploy': ['_config/.gitignore',
               '_config/.gitignore',
               '_config/.gitignore',
               '_config/config.yaml',
               '_config/config.yaml',
               '_config/config.yaml',
               '_config/config_test.yaml',
               '_config/config_test.yaml',
               '_config/config_test.yaml']}

install_requires = \
['boto3>=1.16.0,<2.0.0',
 'console-bundle>=0.3.1,<0.4.0',
 'databricks-api>=0.3.0,<1.0.0',
 'dbx-notebook-exporter>=0.4.0,<0.5.0',
 'nbconvert>=5.6,<6.0',
 'pyfony-bundles>=0.3.2,<0.4.0',
 'pyfony-core>=0.7.1,<0.8.0',
 'pygit2>=1.3,<2.0',
 'python-box>=3.4,<4.0',
 'tomlkit>=0.5.8,<1.0.0']

entry_points = \
{'pyfony.bundle': ['create = dbxdeploy.DbxDeployBundle:DbxDeployBundle']}

setup_kwargs = {
    'name': 'dbx-deploy',
    'version': '0.14.0b2',
    'description': 'Databricks Deployment Tool',
    'long_description': 'Databricks project deployment package\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/dbx-deploy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
