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

import json
import argparse
import textwrap

from starthinker.util.project import project
from starthinker.util.email import send_email
from starthinker.util.email.template import EmailTemplate


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Command line to send email template via gMail.

      Email templates are JSON that assembles into both HTMl and TXT parts of an email.
      For email sample see: https://github.com/google/starthinker/blob/master/starthinker/task/newsletter/sample.json

      Example:
        - Generate an HTML page from a template, then view via browser.
          python helper.py --template sample.json > ~/Downloads/email.html

        - Send an email template via gMail.
          python helper.py --template sample.json --email_to kenjora@google.com --email_from kenjora@google.com -u $STARTHINKER_USER
  """))

  # get parameters
  parser.add_argument(
      '--template',
      help='template to use for email',
      default=None,
      required=True)
  parser.add_argument('--email_to', help='email to', default=None)
  parser.add_argument('--email_from', help='email from', default=None)

  # initialize project
  project.from_commandline(parser=parser, arguments=('-u', '-c', '-v'))

  # load template
  with open(project.args.template, 'r') as json_file:
    email = EmailTemplate(json.load(json_file))

  # send or print
  if project.args.email_to and project.args.email_from:
    print('EMAILING: ', project.args.email_to)
    send_email('user', project.args.email_to, project.args.email_from, None,
               email.get_subject(), email.get_text(), email.get_html())
  else:
    # write to STDOUT
    print(email.get_html())
    print('<pre style="width:600px;margin:0px auto;">%s</pre>' %
          email.get_text())


if __name__ == '__main__':
  main()
