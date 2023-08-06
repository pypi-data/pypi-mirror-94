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

from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.patch import patch_log
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def insertion_order_clear():
  table_create(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "DV_InsertionOrders",
    Discovery_To_BigQuery(
      "displayvideo",
      "v1").method_schema("advertisers.insertionOrders.list"
    )
  )

  sheets_clear(
    project.task["auth_sheets"],
    project.task["sheet"],
    "Insertion Orders",
    "A2:Z"
  )


def insertion_order_load():

  # load multiple partners from user defined sheet
  def insertion_order_load_multiple():
    rows = get_rows(
      project.task["auth_sheets"],
      { "sheets": {
        "sheet": project.task["sheet"],
        "tab": "Advertisers",
        "range": "A2:A"
      }}
    )

    for row in rows:
      yield from API_DV360(
        project.task["auth_dv"],
        iterate=True
      ).advertisers().insertionOrders().list(
        advertiserId=lookup_id(row[0])
      ).execute()

  # write insertion orders to database and sheet
  put_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table": "DV_InsertionOrders",
      "schema": Discovery_To_BigQuery(
        "displayvideo",
        "v1"
      ).method_schema("advertisers.insertionOrders.list"),
      "format": "JSON"
    }},
    insertion_order_load_multiple()
  )

  # write insertion orders to sheet
  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "query": """SELECT
        CONCAT(P.displayName, ' - ', P.partnerId),
        CONCAT(A.displayName, ' - ', A.advertiserId),
        CONCAT(C.displayName, ' - ', C.campaignId),
        CONCAT(I.displayName, ' - ', I.insertionOrderId),
        'PATCH',
        I.entityStatus,
        I.entityStatus,
        I.displayName,
        I.displayName,
        I.budget.budgetUnit,
        I.budget.budgetUnit,
        I.budget.automationType,
        I.budget.automationType,
        I.performanceGoal.performanceGoalType,
        I.performanceGoal.performanceGoalType,
        I.performanceGoal.performanceGoalAmountMicros / 1000000,
        I.performanceGoal.performanceGoalAmountMicros / 1000000,
        I.performanceGoal.performanceGoalPercentageMicros / 1000000,
        I.performanceGoal.performanceGoalPercentageMicros / 1000000,
        I.performanceGoal.performanceGoalString,
        I.performanceGoal.performanceGoalString
        FROM `{dataset}.DV_InsertionOrders` AS I
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON I.campaignId=C.campaignId
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON I.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
      """.format(**project.task),
      "legacy": False
    }}
  )

  put_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Insertion Orders",
      "range": "A2"
    }},
    rows
  )


def insertion_order_audit():

  # Move Insertion Order To BigQuery
  rows = get_rows(
    project.task["auth_sheets"], {
      "sheets": {
        "sheet": project.task["sheet"],
        "tab": "Insertion Orders",
        "range": "A2:Z"
      }
    }
  )

  put_rows(
    project.task["auth_bigquery"], {
      "bigquery": {
        "dataset": project.task["dataset"],
        "table": "SHEET_InsertionOrders",
        "schema": [
          { "name": "Partner", "type": "STRING" },
          { "name": "Advertiser", "type": "STRING" },
          { "name": "Campaign", "type": "STRING" },
          { "name": "Insertion_Order", "type": "STRING" },
          { "name": "Action", "type": "STRING" },
          { "name": "Status", "type": "STRING" },
          { "name": "Status_Edit", "type": "STRING" },
          { "name": "Name", "type": "STRING" },
          { "name": "Name_Edit", "type": "STRING" },
          { "name": "Budget_Unit", "type": "STRING" },
          { "name": "Budget_Unit_Edit", "type": "STRING" },
          { "name": "Budget_Automation", "type": "STRING" },
          { "name": "Budget_Automation_Edit", "type": "STRING" },
          { "name": "Performance_Goal_Type", "type": "STRING" },
          { "name": "Performance_Goal_Type_Edit", "type": "STRING" },
          { "name": "Performance_Goal_Amount", "type": "FLOAT" },
          { "name": "Performance_Goal_Amount_Edit", "type": "FLOAT" },
          { "name": "Performance_Goal_Percent", "type": "FLOAT" },
          { "name": "Performance_Goal_Percent_Edit", "type": "FLOAT" },
          { "name": "Performance_Goal_String", "type": "STRING" },
          { "name": "Performance_Goal_String_Edit", "type": "STRING" },
        ],
        "format": "CSV"
      }
    },
    rows
  )

  # Create Insert View
  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "INSERT_InsertionOrders",
    """SELECT
      REGEXP_EXTRACT(S_IO.Advertiser, r' - (\d+)$') AS advertiserId,
      REGEXP_EXTRACT(S_IO.Campaign, r' - (\d+)$') AS campaignId,
      S_IO.Insertion_Order AS displayName,
      'ENTITY_STATUS_DRAFT' AS entityStatus,
      STRUCT(
        S_PC.Cost_Type_Edit As costType,
        S_PC.Fee_Type_Edit As feeType,
        S_PC.Invoice_Type_Edit AS invoiceType,
        S_PC.Fee_Amount_Edit AS feeAmount,
        S_PC.Fee_Percent_Edit * 1000 AS feePercentageMillis
      ) AS partnerCosts,
      STRUCT(
        S_P.Period_Edit As pacingPeriod,
        S_P.Type_Edit As pacingType,
        S_P.Daily_Budget_Edit AS dailyMaxMicros,
        S_P.Daily_Impressions_Edit AS dailyMaxImpressions
      ) AS pacing,
      STRUCT(
        S_FC.Unlimited_Edit AS unlimited,
        S_FC.Time_Unit_Edit AS timeUnit,
        S_FC.Time_Count_Edit AS timeUnitCount,
        S_FC.Max_impressions_Edit AS maxImpressions
      ) AS frequencyCap,
      STRUCT(
        S_ID.Integration_Code_Edit As integrationCode,
        S_ID.Details_Edit As details
      ) AS integrationDetails,
      STRUCT(
        S_IO.Performance_Goal_Type_Edit AS performanceGoalType,
        S_IO.Performance_Goal_Amount_Edit * 100000 AS performanceGoalAmountMicros,
        S_IO.Performance_Goal_Percent_Edit * 100000 AS performanceGoalPercentageMicros,
        S_IO.Performance_Goal_String_Edit AS performanceGoalString
      ) AS performanceGoal,
      STRUCT(
        S_IO.Budget_Unit_Edit AS budgetUnit,
        S_IO.Budget_Automation_Edit AS automationType,
        (SELECT ARRAY(
          SELECT
            STRUCT(
             S_S.Budget_Edit * 100000 AS budgetAmountMicros,
             S_S.Description_Edit AS description,
             STRUCT (
               STRUCT (
                 EXTRACT(YEAR FROM CAST(S_S.Start_Date_Edit AS Date)) AS year,
                 EXTRACT(MONTH FROM CAST(S_S.Start_Date_Edit AS DATE)) AS month,
                 EXTRACT(DAY FROM CAST(S_S.Start_Date_Edit AS DATE)) AS day
               ) AS startDate,
               STRUCT (
                 EXTRACT(YEAR FROM CAST(S_S.End_Date_Edit AS Date)) AS year,
                 EXTRACT(MONTH FROM CAST(S_S.End_Date_Edit AS DATE)) AS month,
                 EXTRACT(DAY FROM CAST(S_S.End_Date_Edit AS DATE)) AS day
             ) AS endDate
           ) AS dateRange
          ) AS budgetSegments
          FROM `{dataset}.SHEET_Segments` AS  S_S
          WHERE S_IO.Insertion_Order=S_S.Insertion_Order
        )) AS budgetSegments
      ) AS budget,
      STRUCT(
        IF(S_BS.Fixed_Bid_Edit IS NOT NULL,
          STRUCT(
            S_BS.Fixed_Bid_Edit * 100000 AS bidAmountMicros
          ),
          NULL
        ) AS fixedBid,
        IF(S_BS.Auto_Bid_Goal_Edit IS NOT NULL,
          STRUCT(
            S_BS.Auto_Bid_Goal_Edit AS performanceGoalType,
            S_BS.Auto_Bid_Amount_Edit * 100000 AS maxAverageCpmBidAmountMicros,
            S_BS.Auto_Bid_Algorithm_Edit AS customBiddingAlgorithmId
          ),
          NULL
        ) AS maximizeSpendAutoBid,
        IF(S_BS.Performance_Goal_Type_Edit IS NOT NULL,
          STRUCT(
            S_BS.Performance_Goal_Type_Edit AS performanceGoalType,
            S_BS.Performance_Goal_Amount_Edit * 100000 AS performanceGoalAmountMicros,
            S_BS.Performance_Goal_Average_CPM_Bid_Edit * 100000 AS maxAverageCpmBidAmountMicros,
            S_BS.Performance_Goal_Algorithm_Edit AS customBiddingAlgorithmId
          ),
          NULL
        ) AS performanceGoalAutoBid
      )
      AS bidStrategy
      FROM `{dataset}.SHEET_InsertionOrders` As S_IO
      LEFT JOIN `{dataset}.SHEET_Segments` As S_S ON S_IO.Insertion_Order=S_S.Insertion_Order
      LEFT JOIN `{dataset}.SHEET_PartnerCosts` As S_PC ON S_IO.Insertion_Order=S_PC.Insertion_Order
      LEFT JOIN `{dataset}.SHEET_Pacing` As S_P ON S_IO.Insertion_Order=S_P.Insertion_Order
      LEFT JOIN `{dataset}.SHEET_FrequencyCaps` As S_FC ON S_IO.Insertion_Order=S_FC.Insertion_Order
      LEFT JOIN `{dataset}.SHEET_IntegrationDetails` As S_ID ON S_IO.Insertion_Order=S_ID.Insertion_Order
      LEFT JOIN `{dataset}.SHEET_BidStrategy` As S_BS ON S_IO.Insertion_Order=S_BS.Insertion_Order
      LEFT JOIN `{dataset}.DV_InsertionOrders` As DV_IO ON S_IO.Insertion_Order=DV_IO.displayName
      WHERE S_IO.Action="INSERT"
      AND DV_IO IS NULL
    """.format(**project.task),
    legacy=False
  )

  # Create Audit View And Write To Sheets
  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "AUDIT_InsertionOrders",
    """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Insertion Order' AS Operation,
            CASE
              WHEN Name_Edit IS NULL THEN 'Missing Name.'
              WHEN Budget_Unit_Edit IS NULL THEN 'Missing Budget Unit.'
              WHEN Budget_Automation_Edit IS NULL THEN 'Missing Budget Automation.'
              WHEN Performance_Goal_Type_Edit IS NULL THEN 'Missing Goal Type.'
              WHEN Performance_Goal_Amount_Edit IS NULL
              AND Performance_Goal_Percent_Edit IS NULL
              AND Performance_Goal_String_Edit IS NULL THEN 'Missing Goal Amount / Percent / String.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_InsertionOrders`
        )
        WHERE
          Error IS NOT NULL
      ),
      /* Check duplicate inserts */
      DUPLICATE_ERRORS AS (
        SELECT
          'Insertion_Order' AS Operation,
          'Duplicate Insertion Order name, insert will be ignored.' AS Error,
          'WARNING' AS Severity,
          COALESCE(S_IO.Insertion_Order, 'BLANK') AS Id
        FROM `{dataset}.SHEET_InsertionOrders` As S_IO
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS DV_IO ON S_IO.Insertion_Order=DV_IO.displayName
        WHERE S_IO.Action="INSERT"
        AND DV_IO IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      UNION ALL
      SELECT * FROM DUPLICATE_ERRORS
      ;
    """.format(**project.task),
    legacy=False
  )

  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "PATCH_InsertionOrders",
    """SELECT *
      FROM `{dataset}.SHEET_InsertionOrders`
      WHERE Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_InsertionOrders` WHERE Severity='ERROR')
    """.format(**project.task),
    legacy=False
  )


def insertion_order_patch(commit=False):

  patches = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"PATCH_InsertionOrders",
    }},
    as_object=True
  )

  for row in rows:
    if row['Action'] == "DELETE":
      patches.append({
        "operation": "Insertion Orders",
        "action": "DELETE",
        "partner": row['Partner'],
        "advertiser": row['Advertiser'],
        "campaign": row['Campaign'],
        "insertion_order": row['Insertion_Order'],
        "parameters": {
          "advertiserId": lookup_id(row['Advertiser']),
          "insertionOrderId": lookup_id(row['Insertion_Order'])
        }
      })

    elif row['Action'] == "PATCH":
      insertion_order = {}

      if row['Name'] != row['Name_Edit']:
        insertion_order["displayName"] = row['Name_Edit']

      if row['Budget_Unit'] != row['Budget_Unit_Edit']:
        insertion_order.setdefault("budget", {})
        insertion_order["budget"]["budgetUnit"] = row['Budget_Unit_Edit']

      if row['Budget_Automation'] != row['Budget_Automation_Edit']:
        insertion_order.setdefault("budget", {})
        insertion_order["budget"]["automationType"] = row['Budget_Automation_Edit']

      if row['Performance_Goal_Type'] != row['Performance_Goal_Type_Edit']:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalType"] = row['Performance_Goal_Type_Edit']

      if row['Performance_Goal_Amount'] != row['Performance_Goal_Amount_Edit']:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalAmountMicros"] = int(
          float(row['Performance_Goal_Amount_Edit']) * 1000000
        )

      if row['Performance_Goal_Percent'] != row['Performance_Goal_Percent_Edit']:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalPercentageMicros"] = int(
          float(row['Performance_Goal_Percent_Edit']) * 1000000
        )

      if row['Performance_Goal_String'] != row['Performance_Goal_String_Edit']:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalString"] = row['Performance_Goal_String_Edit']

      if insertion_order:
        patches.append({
          "operation": "Insertion Orders",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "campaign": row['Campaign'],
          "insertion_order": row['Insertion_Order'],
          "parameters": {
            "advertiserId": lookup_id(row['Advertiser']),
            "insertionOrderId": lookup_id(row['Insertion_Order']),
            "body": insertion_order
          }
        })

  patch_masks(patches)
  patch_preview(patches)

  if commit:
    insertion_order_commit(patches)


def insertion_order_insert(commit=False):
  inserts = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"INSERT_InsertionOrders",
    }},
    as_object=True
  )

  for row in rows:
    inserts.append({
      "operation": "Insertion Orders",
      "action": "INSERT",
      "partner": None,
      "advertiser": row['advertiserId'],
      "campaign": row['campaignId'],
      "insertion_order": row['displayName'],
      "parameters": {
        "advertiserId": row['advertiserId'],
        "body":row
      }
    })

  if commit:
    insertion_order_commit(inserts)
  else:
    patch_preview(inserts)


def insertion_order_commit(patches):
  for patch in patches:
    if not patch.get("insertion_order"):
      continue
    print("API INSERTION ORDER:", patch["action"], patch["insertion_order"])
    try:
      if patch["action"] == "DELETE":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().insertionOrders().delete(
          **patch["parameters"]
        ).execute()
        patch["success"] = response
      elif patch["action"] == "PATCH":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().insertionOrders().patch(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["insertionOrderId"]
      elif patch["action"] == "INSERT":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().insertionOrders().create(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["insertionOrderId"]
    except Exception as e:
      patch["error"] = str(e)
    finally:
      patch_log(patch)
  patch_log()
