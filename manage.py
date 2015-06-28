# -*- coding: utf-8 -*-

import os
import sys
import urllib

from flask.ext.script import Command, Option
from flask.ext.script import Manager
from voyage import app


manager = Manager(app)

class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def __init__(self, host='127.0.0.1', port=8000, workers=6):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-t', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def run(self, *args, **kwargs):
        run_args = sys.argv[2:]
        run_args.append('voyage:voyage_app')
        os.execvp('gunicorn', [''] + run_args)

manager.add_command("gunicorn",GunicornServer)

@manager.command
def list_routes():
    "Lists all routes currently defined in application"
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def list_dirs():
    "Lists all important dirs in the project"
    print "{0:20s} {1}".format("Template Dir: ", app.template_folder)
    print "{0:20s} {1}".format("Uploads Dir: ", app.config['UPLOAD_FOLDER'])

if __name__ == "__main__":
    manager.run()