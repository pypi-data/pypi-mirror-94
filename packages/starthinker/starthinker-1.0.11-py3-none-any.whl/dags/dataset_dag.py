###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

BigQuery Dataset

Create and permission a dataset in BigQuery.

  - Specify the name of the dataset.
  - If dataset exists, it is inchanged.
  - Add emails and / or groups to add read permission.
  - CAUTION: Removing permissions in StarThinker has no effect.
  - CAUTION: To remove permissions you have to edit the dataset.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'dataset_dataset': '',  # Name of Google BigQuery dataset to create.
  'dataset_emails': [],  # Comma separated emails.
  'dataset_groups': [],  # Comma separated groups.
}

RECIPE = {
  'tasks': [
    {
      'dataset': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Credentials used for writing data.'
          }
        },
        'dataset': {
          'field': {
            'name': 'dataset_dataset',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Name of Google BigQuery dataset to create.'
          }
        },
        'emails': {
          'field': {
            'name': 'dataset_emails',
            'kind': 'string_list',
            'order': 2,
            'default': [
            ],
            'description': 'Comma separated emails.'
          }
        },
        'groups': {
          'field': {
            'name': 'dataset_groups',
            'kind': 'string_list',
            'order': 3,
            'default': [
            ],
            'description': 'Comma separated groups.'
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dataset', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
