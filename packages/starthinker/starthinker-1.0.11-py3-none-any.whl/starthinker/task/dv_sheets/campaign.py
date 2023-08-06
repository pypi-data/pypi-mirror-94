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

from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_sheets.patch import patch_clear
from starthinker.task.dv_sheets.patch import patch_log
from starthinker.task.dv_sheets.patch import patch_masks
from starthinker.task.dv_sheets.patch import patch_preview


def campaign_clear():
  table_create(
      project.task['auth_bigquery'],
      project.id,
      project.task['dataset'],
      'DV_Campaigns',
      Discovery_To_BigQuery('displayvideo',
                            'v1').method_schema('advertisers.campaigns.list'),
  )

  sheets_clear(project.task['auth_sheets'], project.task['sheet'], 'Campaigns', 'B2:Z')


def campaign_load():

  # load multiple partners from user defined sheet
  def campaign_load_multiple():
    rows = get_rows(
        project.task['auth_sheets'], {
            'sheets': {
                'sheet': project.task['sheet'],
                'tab': 'Advertisers',
                'range': 'A2:A'
            }
        })

    for row in rows:
      yield from API_DV360(
          project.task['auth_dv'], iterate=True).advertisers().campaigns().list(
              advertiserId=lookup_id(row[0])).execute()

  # write campaigns to database and sheet
  put_rows(
      project.task['auth_bigquery'], {
          'bigquery': {
              'dataset':
                  project.task['dataset'],
              'table':
                  'DV_Campaigns',
              'schema':
                  Discovery_To_BigQuery(
                      'displayvideo',
                      'v1').method_schema('advertisers.campaigns.list'),
              'format':
                  'JSON'
          }
      }, campaign_load_multiple())

  # write campaigns to sheet
  rows = get_rows(
      project.task['auth_bigquery'], {
          'bigquery': {
              'dataset':
                  project.task['dataset'],
              'query':
                  """SELECT
         CONCAT(P.displayName, ' - ', P.partnerId),
         CONCAT(A.displayName, ' - ', A.advertiserId),
         CONCAT(C.displayName, ' - ', C.campaignId),
         C.entityStatus
         FROM `{dataset}.DV_Campaigns` AS C
         LEFT JOIN `{dataset}.DV_Advertisers` AS A
         ON C.advertiserId=A.advertiserId
         LEFT JOIN `{dataset}.DV_Partners` AS P
         ON A.partnerId=P.partnerId
       """.format(**project.task),
              'legacy':
                  False
          }
      })

  put_rows(project.task['auth_sheets'], {
      'sheets': {
          'sheet': project.task['sheet'],
          'tab': 'Campaigns',
          'range': 'B2'
      }
  }, rows)


def campaign_commit(patches):
  for patch in patches:
    if not patch.get('campaign'):
      continue
    print('API CALL', patch['action'], patch['advertiser'], patch['campaign'])
    try:
      if patch['action'] == 'DELETE':
        response = API_DV360(
            project.task['auth_dv']).advertisers().campaigns().delete(
                **patch['parameters']).execute()
        patch['success'] = response
      elif patch['action'] == 'PATCH':
        response = API_DV360(project.task['auth_dv']).advertisers().campaigns().patch(
            **patch['parameters']).execute()
        patch['success'] = response['campaignId']
    except Exception as e:
      patch['error'] = str(e)
    finally:
      patch_log(patch)
  patch_log()
