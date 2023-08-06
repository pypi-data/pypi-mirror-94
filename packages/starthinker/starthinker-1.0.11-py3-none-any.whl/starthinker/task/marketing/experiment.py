from operator import itemgetter
from urllib.parse import urlencode

from starthinker.util.project import project
from starthinker.util.csv import rows_to_csv
from starthinker.util.sheets import sheets_read
from starthinker.util.bigquery import query_to_rows
from starthinker.util.email import send_email
from starthinker.util.email.template import EmailTemplate

# OWNER SCHEMA
#Account Owner - STRING
#Account Owner Email - STRING
#DCM Network ID - INTEGER
#DCM Advertiser ID - INTEGER
#DBM Partner ID - INTEGER
#DBM Advertiser ID - INTEGER
#DS Agency ID - INTEGER
#DS Advertiser ID - INTEGER

# SOLUTION SCHEMA
# [Network|Partner|Agency] ID - INTEGER
# Advertiser ID - INTEGER  ( can be same as account id if not used )
# Advertiser Name - STRING ( title added to list to allow subaccounts, for example advertisers in DBM )
# Score - FLOAT ( Percent: 100 = Client Already Executing Well ( low need ), 1 = Client Currentnot Executing Well ( high need ) )

# IMPACT SCHEMA
# [Network|Partner|Agency] ID - INTEGER
# Advertiser ID - INTEGER ( must match column name above )
# Impact - PERCENT

IMPACT_SCHEMA = [
    {
        'name': 'Impact',
        'type': 'STRING'
    },
    {
        'name': 'Level',
        'type': 'INTEGER'
    },
]

OFFER_SCHEMA = [
    {
        'name': 'Client',
        'type': 'STRING'
    },
    {
        'name': 'Coverage',
        'type': 'INTEGER'
    },
    {
        'name': 'Request',
        'type': 'STRING'
    },
]


def get_owners():
  if project.verbose:
    print('GETTING OWNERS')

  owners = []

  if 'sheet' in project.task['owners']:
    owners = sheets_read(project.task['auth'],
                         project.task['owners']['sheet']['url'],
                         project.task['owners']['sheet']['tab'],
                         project.task['owners']['sheet']['range'])
  elif 'bigquery' in project.task['owners']:
    owners = query_to_rows(project.task['auth'], project.id,
                           project.task['owners']['bigquery']['dataset'],
                           project.task['owners']['bigquery']['query'])

  # group account owners by email, create easy lookup sets for ids
  owners_grouped = {}
  for owner in owners:
    try:

      print(owner[1])
      owners_grouped.setdefault(
          owner[1], {
              'Account Owner': owner[0],
              'Account Email': owner[1],
              'DCM': [],
              'DBM': [],
              'DS': [],
          })

      if len(owner) > 3 and owner[3]:
        owners_grouped[owner[1]]['DCM'].append((int(owner[2]), int(owner[3])))
      if len(owner) > 5 and owner[5]:
        owners_grouped[owner[1]]['DBM'].append((int(owner[4]), int(owner[5])))
      if len(owner) > 7 and owner[7]:
        owners_grouped[owner[1]]['DS'].append((int(owner[6]), int(owner[7])))

    except IndexError:
      print('ERROR:', owner)
      pass

  if project.verbose:
    print('GOT OWNERS:', len(owners_grouped))

  return owners_grouped.values()


def get_impacts():
  if project.verbose:
    print('GETTING IMPACTS')

  impacts = []

  if 'sheet' in project.task['impacts']:
    impacts = sheets_read(project.task['auth'],
                          project.task['impacts']['sheet']['url'],
                          project.task['impacts']['sheet']['tab'],
                          project.task['impacts']['sheet']['range'])
  elif 'bigquery' in project.task['impacts']:
    impacts = query_to_rows(project.task['auth'], project.id,
                            project.task['impacts']['bigquery']['dataset'],
                            project.task['impacts']['bigquery']['query'])

  # for easy lookup use dictionary
  impacts = dict([((int(i[0], int(i[1]))), float(i[2])) for i in impacts])

  if project.verbose:
    print('GOT IMPACTS:', len(impacts))

  return impacts


def get_solutions():
  if project.verbose:
    print('GETTING SCORES')

  for solution in project.task['solutions']:
    scores = []

    if 'sheet' in solution:
      scores = sheets_read(project.task['auth'], project.task['sheet']['url'],
                           solution['sheet']['tab'], solution['sheet']['range'])
    elif 'bigquery' in solution:
      scores = query_to_rows(project.task['auth'], project.id,
                             solution['bigquery']['dataset'],
                             solution['bigquery']['query'])

    # for easy lookup use dictionary
    solution['scores'] = {}
    for score in scores:
      solution['scores'].setdefault(str(score[0]), [])
      solution['scores'][str(score[0])].append({
          'variant_id': str(score[1]),
          'variant': score[2],
          'score': float(score[3])
      })

    if project.verbose:
      print('GOT SCORES:', len(solution['scores']))

  return project.task['solutions']


def compose_link(link, parameters):
  return '%s%s%s' % (link, '&' if '?' in link else '?', urlencode(parameters))


def compose_email_solution_centric(owner):
  if project.verbose:
    print('COMPOSING: ', owner['Account Email'])

  # start an email template
  email = EmailTemplate()
  email.segment_next()
  email.greeting(owner['Account Owner'])
  email.paragraph(project.task['email']['introduction'])

  # loop through solutions
  rows = []
  for solution in owner['Solutions']:
    email.segment_next()
    email.header('Your %d Biggest %s Impact Opportunities This Week' %
                 (project.task['offers'], solution['Solution']['name']))

    # create offer matrix for each solution
    email.table(
        OFFER_SCHEMA,
        [
            (
                offer['Variant'],
                '%d%%' % int(offer['Score'] * 100),
                compose_link(
                    solution['Solution']['link'],
                    {
                        'solution':
                            solution['Solution']['name'],
                        'requester':
                            owner['Account Email'],
                        'name':
                            offer['Variant'],
                        'dbm':
                            '%s:%s' % (offer['Account_ID'], offer['Variant_ID'])
                            if solution['Solution']['key'] == 'DBM Partner ID'
                            else '',  # comma seperated list
                        'dcm':
                            '%s:%s' % (offer['Account_ID'], offer['Variant_ID'])
                            if solution['Solution']['key'] == 'DCM Network ID'
                            else '',  # comma seperated list
                        'ds':
                            '%s:%s' % (offer['Account_ID'], offer['Variant_ID'])
                            if solution['Solution']['key'] == 'DS Account ID'
                            else '',  # comma seperated list
                        'sa':
                            '%s:%s' %
                            (offer['Account_ID'], offer['Variant_ID']) if
                            solution['Solution']['key'] == 'Studio Account ID'
                            else '',  # comma seperated list
                    })) for offer in solution['Offers']
        ])

    email.paragraph(
        "Click the request link to schedule a solution for that client.  This does not deploy a solution to the client, it only contacts a specialist indicating you'd like to evaluate this solution for this client."
    )

    email.header('About ' + solution['Solution']['name'])
    email.image(solution['Solution']['image'], solution['Solution']['sample'])
    email.paragraph(solution['Solution']['description'])

    email.paragraph('Product Gap', bold=True)
    email.paragraph(solution['Solution']['gap'])

    # solution pitch
    email.paragraph('Benefits', bold=True)
    email.list(solution['Solution']['pitches'])

    # solution impact
    email.table(IMPACT_SCHEMA, [
        (i[0], '%d%%' % i[1]) for i in solution['Solution']['impacts'].items()
    ])

    email.button('Learn More', project.task['link'], big=True)

  #print(email.get_html())

  #send_email(
  #  'user',
  #  owner['Account Email'],
  #  project.task['email']['from'],
  #  project.task['email']['cc'],
  #  project.task['email']['subject'],
  #  email.get_text(),
  #  email.get_html()
  #)


def assemble_offers_solution_centric():

  owners, solutions, impacts = get_owners(), get_solutions(), get_impacts()

  # produce the following table
  # owner [
  #   solution - ( detials ) [
  #    [ client - variant, score, impact ] ( sorted by impact )

  if project.verbose:
    print('ASSEMBLING OFFERS')

  count = 0
  for owner in owners:
    owner.setdefault('Solutions', [])

    # for each owner and solution assemble a list of offers
    for solution in solutions:
      offers = []

      for account_id in owner[solution['key']]:

        scores = solution['scores'].get(account_id, [])

        # if account id has a solution score add it to the offers
        for score in scores:

          offers.append({
              'Account_ID':
                  account_id,
              'Variant_ID':
                  score['variant_id'],
              'Variant':
                  score['variant'],
              'Score':
                  score['score'],
              'Impact':
                  impacts.get(score['variant_id'], 1) *
                  (1 - score['score']
                  )  # Impact is how much revenue can be improved
          })
          count += 1

      # if offers for this account and solution exist, keep only the top ones ( largest impact to lowest )
      if offers:
        offers.sort(key=itemgetter('Impact'), reverse=True)
        offers = offers[:project.task['offers']]
        owner['Solutions'].append({'Solution': solution, 'Offers': offers})

  if project.verbose:
    print('ASSEMBLED OFFERS', count)

  if project.verbose:
    print('SENDING OFFERS')

  exit()

  # send emails
  count = 0
  for owner in owners:
    if owner['Solutions']:
      count += 1
      if count > 10:
        compose_email_solution_centric(owner)

  if project.verbose:
    print('SENT OFFERS', count)


@project.from_parameters
def marketing():
  assemble_offers_solution_centric()


if __name__ == '__main__':
  marketing()
