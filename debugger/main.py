# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
import logging

from flask import Flask, request

# Enable cloud debugger
try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

# Adjust logging level to INFO
logging.basicConfig(level=logging.INFO)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


# There is a bug in the code.
class StringProcessor():
    def __init__(self, string):
        self._string = string

    def Reverse(self):
        if self._string == '':
            return ''

        chars = [c for c in self._string]
        left = 0
        right = len(chars) - 1
        while True:
            tmp = chars[left]
            chars[left] = chars[right]
            chars[right] = tmp
            if left >= right:
                break
            left += 1
            right -= 1

        return ''.join(chars)


@app.route('/reverse_string', methods=['GET'])
def ReverseString():
    try:
        s = str(request.args.get('string'))
    except Exception as e:
        print(e)
        return 'Not a valid string!'

    current = StringProcessor(s).Reverse()
    expected = s[::-1]
    return '''
        <body style="background-color: black;">
        <div style="margin: 40px auto; width:1000px;">
        <h1 style="color: orange; text-align: center;">Cloud Guru Reversi!</h1>
        <table style="width:400px; margin: 0 auto; font-size: 24px; color: white; line-height: 48px;">
            <tr><th>Program Function Output:</th><th>{}</th></tr>
            <tr><th>Python Function Output:</th><th>{}</th><tr>
        </table>
        </div>
        </body>
    '''.format(current, expected)


@app.route('/')
def Hello():
    """Return a friendly HTTP greeting."""
    return '''
        <html>
        <head>
        <style>
        input#submit {
            background-color: orange; 
            color: black; 
            font-size:24px; 
            padding: 16px;
        }
        input#submit:hover {
            background-color: black;
            color: orange;
        }
        </style>
        </head>
        <body style="background-color: black;">
        <div style="margin: 20px auto; width:1000px;">
        <h1 style="color:orange; font-size: 48px; text-align:center;">Greetings, Cloud Gurus! </br>Let's play Reversi! </br>Enter a string to reverse it.</h1>
        <p style="text-align:center;">
        <form method="get" action="reverse_string">
            <p style="text-align:center; color:white;"><input style="color:black;font-size:24px" type=text name=string value="">
            <p style="text-align:center;"><input id="submit" type=submit value="Reversi!">
        </form>
        </p>
        </div>
        </body>
        </html>
    '''


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
