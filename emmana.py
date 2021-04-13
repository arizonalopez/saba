from myproject.models import Role, User, Comment
from myproject import create_app, db
from flask_migrate import upgrade
import os
import sys
import click
from flask_script import Manager

app = create_app('default')

manager = Manager(app)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Comment=Comment)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
        help='Run tests under code coverage.')
def test(coverage):
    '''Run the unit test'''
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)

@app.cli.command()
@click.option('--length', default=25,
    help='Number of functions to include in the profiler report')
@click.option('--profile-dir', default=None,
    help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    '''Start the app under the code profiler.'''
    from werkzeug.contrib.profiler import ProfilerMiddleware as PM
    app.wsgi_app = PM(app.wsgi_app, restrictions=[length],
        profile_dir=profile_dir)
    app.run(debug=False)

@manager.command
def deploy():
    '''Run deployment tasks'''
    upgrade()
    Role.insert_roles()
    User.add_self_follows()
    

if __name__ == '__main__':
    app.run(debug=True)