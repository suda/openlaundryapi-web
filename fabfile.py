from fabric.api import *

env.hosts = ['appsome@web208.webfaction.com']

def clean():
    "Removes all unnesesary files like *.pyc"
    run('cd %s; find . -name "*.pyc" -exec rm -rf {} \;' % (env.base_dir))

def git_pull():
    "Updates the repository"
    run("cd %s; git checkout %s" % (env.base_dir, env.branch))
    run("cd %s; git pull %s %s" % (env.base_dir, env.repository, env.branch))

def install_requirements():
    "Install the required packages from the requirements file using pip"
    run('cd /home/appsome/webapps/openlaundryapi/; pip-2.7 install --install-option="--install-scripts=$PWD/bin" --install-option="--install-lib=$PWD/lib/python2.7" -r openlaundryapi/requirements.txt')

def migrate():
    "performs syncdb and migrate command"
    run("cd %s; python2.7 manage.py syncdb" % env.base_dir)
    run("cd %s; python2.7 manage.py migrate" % env.base_dir)

def collect_static():
    "Collects all static"
    run("cd %s; python2.7 manage.py collectstatic --noinput" % env.base_dir)

def apache_restart():
    "Restarts Apache"
    run("/home/appsome/webapps/openlaundryapi/apache2/bin/restart")

def production():
    "Production settings"
    env.repository = 'origin'
    env.branch = 'master'
    env.base_dir = '/home/appsome/webapps/openlaundryapi/openlaundryapi/'

def staging():
    "Staging settings"
    env.repository = 'origin'
    env.branch = 'staging'
    #env.base_dir = '/home/appsome/webapps/openlaundryapi/openlaundryapi/'

def deploy():
    "Deploys (git_pull, install_requirements, migrate, collect_static, apache_restart)"
    clean()
    git_pull()
    #install_requirements()
    migrate()
    collect_static()
    apache_restart()
