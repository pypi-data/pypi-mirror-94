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

import pysftp
import gzip
import datetime
import uuid
import os
import csv

from starthinker.util.project import project
from starthinker.util.bigquery import io_to_table, make_schema


def clean_csv(input_file,
              output_file_name,
              num_fields,
              header=True,
              append_to_lines=''):
  if os.path.isfile(output_file_name):
    os.remove(output_file_name)

  output_file = open(output_file_name, 'w')

  for line in input_file:
    if header:
      header = False
    elif len(line) > 1:
      line = line.strip()
      while line.count(',') < (num_fields - 1):
        line += ','
      output_file.write(line + append_to_lines + '\n')
    else:
      break

  output_file.close()


# loop all parameters and replace with values, for lists turn them into strings
def query_parameters(query, parameters):
  while '[PARAMETER]' in query:
    parameter = parameters.pop(0)
    if isinstance(parameter, list) or isinstance(parameter, tuple):
      parameter = ', '.join([str(p) for p in parameter])
    query = query.replace('[PARAMETER]', parameter, 1)
  if project.verbose:
    print('QUERY:', query)
  return query


@project.from_parameters
def sftp():

  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None
  sftp_configs = project.task['from']['sftp']['connection']
  sftp_configs['cnopts'] = cnopts
  sftp = pysftp.Connection(**sftp_configs)

  file_name = (
      datetime.datetime.now() +
      datetime.timedelta(project.task['from']['sftp'].get('day', 0))).strftime(
          project.task['from']['sftp']['file'])
  input_file_name = '/tmp/%s.csv' % str(uuid.uuid1())
  sftp.get(file_name, localpath=input_file_name)

  compression = project.task['from']['sftp'].get('compression', None)

  if 'table' in project.task['to']:
    input_file = None
    if compression == 'gzip':
      input_file = gzip.open(input_file_name, 'rb')
      uncompressed_file = '/tmp/%s.csv' % str(uuid.uuid1())

      out = open(uncompressed_file, 'wb')
      for line in input_file:
        if len(line) > 1:
          out.write(line)
      out.close()
      input_file.close()

      os.remove(input_file_name)
      input_file_name = uncompressed_file

    input_file = open(input_file_name, 'rb')

    reader = csv.reader(input_file)
    header = next(reader)
    input_file.seek(0)
    schema = make_schema(header)
    output_file_name = '/tmp/%s.csv' % str(uuid.uuid1())
    clean_csv(input_file, output_file_name, len(header), header=True)
    input_file.close()

    output_file = open(output_file_name, 'rb')
    io_to_table(
        project.task['auth'],
        project.id,
        project.task['to'].get('dataset'),
        project.task['to'].get('table'),
        output_file,
        'CSV',
        schema,
        skip_rows=0,
        disposition=project.task['to'].get('write_disposition',
                                           'WRITE_TRUNCATE'))
    output_file.close()

    os.remove(input_file_name)

  os.remove(output_file_name)


if __name__ == '__main__':
  sftp()
