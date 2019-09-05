import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/Capaal/TddBook'

#Extra notes: After running this via "fab deploy:host=jason@superlists.3dtwenty.com -I --port=35556"
#Switch to the server and run: cat ./deploy_tools/nginx.template.conf | sed "s/DOMAIN/superlists.3dtwenty.com/g"
#Paste results into /etc/nginx/nginx.conf
# Then cat ./deploy_tools/gunicorn-systemd.template.service | sed "s/DOMAIN/superlists.3dtwenty.com/g" | sudo tee /etc/systemd/system/gunicorn-superlists.3dtwenty.com
# followed by sudo systemctl daemon-reload sudo systemctl reload nginx sudo systemctl enable gunicorn-superlists.3dtwenty.com sudo systemctl start gunicorn-superlists.3dtwenty.com


def deploy():
	siteFolder = f'/home/{env.user}/Sites/{env.host}'
	run(f'mkdir -p {siteFolder}')
	with cd(siteFolder):
		_get_latest_source()
		_update_virtualenv()
		_create_or_update_dotenv()
		_update_static_files()
		_update_database()

def _get_latest_source():
	if exists('.git'):
		run('git fetch')
	else:
		run(f'git clone {REPO_URL} .')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'git reset --hard {current_commit}')

def _update_virtualenv():
	if not exists('virtualenv/bin/pip'):
		run(f'python -m venv virtualenv')
	run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
	append('.env', 'DJANGO_DEBUG_FALSE=y')
	append('.env', f'SITENAME={env.host}')
	currentContents = run('cat .env')
	if 'DJANGO_SECRET_KEY' not in currentContents:
		newSecret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
		append('.env', f'DJANGO_SECRET_KEY={newSecret}')

def _update_static_files():
	run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
	run('./virtualenv/bin/python manage.py migrate --noinput')
