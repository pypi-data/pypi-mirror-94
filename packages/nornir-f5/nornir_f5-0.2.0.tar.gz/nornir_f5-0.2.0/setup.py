# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_f5',
 'nornir_f5.plugins',
 'nornir_f5.plugins.connections',
 'nornir_f5.plugins.tasks',
 'nornir_f5.plugins.tasks.bigip',
 'nornir_f5.plugins.tasks.bigip.cm',
 'nornir_f5.plugins.tasks.bigip.shared',
 'nornir_f5.plugins.tasks.bigip.shared.file_transfer',
 'nornir_f5.plugins.tasks.bigip.shared.iapp',
 'nornir_f5.plugins.tasks.bigip.sys',
 'nornir_f5.plugins.tasks.bigip.util']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.0.0,<4.0.0',
 'packaging>=20.8,<21.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.3,<2.0.0']

entry_points = \
{'nornir.plugins.connections': ['f5 = '
                                'nornir_f5.plugins.connections:F5iControlREST']}

setup_kwargs = {
    'name': 'nornir-f5',
    'version': '0.2.0',
    'description': 'F5 plugins for Nornir',
    'long_description': '# nornir_f5\n\n![Build Status](https://github.com/erjac77/nornir_f5/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/erjac77/nornir_f5/branch/master/graph/badge.svg?token=XXIASNEDFR)](https://codecov.io/gh/erjac77/nornir_f5)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub license](https://img.shields.io/github/license/erjac77/nornir_f5.svg)](https://github.com/erjac77/nornir_f5/blob/master/LICENSE)\n\nConnection plugin and various tasks to interact with F5 systems via the iControlREST API.\n\n## Installation\n\n### Pip\n\n```bash\npip install nornir_f5\n```\n\n### Poetry\n\n```bash\npoetry add nornir_f5\n```\n\n## Usage\n\n```python\nfrom nornir import InitNornir\nfrom nornir.core.task import Result, Task\nfrom nornir_utils.plugins.functions import print_result\n\nfrom nornir_f5.plugins.tasks import (\n    f5_atc,\n    f5_bigip_cm_config_sync,\n    f5_bigip_cm_failover_status,\n)\n\ndef as3_post(task: Task, as3_tenant: str) -> Result:\n    # Get the failover status of the device.\n    failover_status = task.run(\n        name="Get failover status", task=f5_bigip_cm_failover_status\n    ).result\n\n    # If it\'s the ACTIVE device, send the declaration and perform a sync.\n    if failover_status == "ACTIVE":\n        task.run(\n            name="AS3 POST",\n            task=f5_atc,\n            atc_method="POST",\n            atc_service="AS3",\n            as3_tenant=as3_tenant,\n            atc_declaration_file=task.host["appsvcs"][as3_tenant][\n                "atc_declaration_file"\n            ],\n        )\n\n        task.run(\n            name="Synchronize the devices",\n            task=f5_bigip_cm_config_sync,\n            device_group=task.host["device_group"],\n        )\n\n        return Result(\n            host=task.host,\n            result="ACTIVE device, AS3 declaration successfully deployed.",\n        )\n    # Else, do nothing...\n    else:\n        return Result(host=task.host, result="STANDBY device, skipped.")\n\nnr = InitNornir(config_file="config.yml")\nnr = nr.filter(platform="f5_bigip")\n\nresult = nr.run(\n    name="POST AS3 Declaration from file",\n    task=as3_post,\n    as3_tenant="Simple_01",\n)\n\nprint_result(result)\n```\n\n## Plugins\n\n### Connections\n\n* __f5__: Connect to F5 BIG-IP systems using iControl REST.\n\n### Tasks\n\n* __f5_atc__: Deploy an F5 Automation Tool Chain (ATC) declaration (AS3, DO and TS*) on a BIG-IP system.\n* __f5_bigip_cm_config_sync__: Synchronize the configuration between BIG-IP systems.\n* __f5_bigip_cm_failover_status__: Get the failover status of the BIG-IP system.\n* __f5_bigip_cm_sync_status__: Get the configuration synchronization status of the BIG-IP system.\n* __f5_bigip_shared_file_transfer_uploads__: Upload a file to a BIG-IP system.\n* __f5_bigip_shared_iapp_lx_package__: Manage Javascript LX packages on a BIG-IP system.\n* __f5_bigip_sys_version__: Get software version information for the BIG-IP system.\n* __f5_bigip_util_unix_ls__: List information about the FILEs or directory content on a BIG-IP system.\n* __f5_bigip_util_unix_rm__: Delete a file on a BIG-IP system.\n\n## Roadmap\n\n* ATC:\n  * *Support Telemetry (TS)\n  * Support BIG-IQ\n* Support dry-run mode\n\n## Authors\n\n* Eric Jacob (@erjac77)\n',
    'author': 'Eric Jacob',
    'author_email': 'erjac77@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erjac77/nornir_f5',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
