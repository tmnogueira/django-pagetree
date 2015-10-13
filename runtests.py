""" run tests for pagetree

$ virtualenv ve
$ ./ve/bin/pip install Django==1.8
$ ./ve/bin/pip install -r test_reqs.txt
$ ./ve/bin/python runtests.py
"""


import django
from django.conf import settings
from django.core.management import call_command


def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),

        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'pagetree',
            'django_markwhat',
            'django_jenkins',
        ),
        TEST_RUNNER = 'django.test.runner.DiscoverRunner',

        COVERAGE_EXCLUDES_FOLDERS = ['migrations'],
        ROOT_URLCONF = 'pagetree.tests.urls',
        PAGEBLOCKS = ['pagetree.TestBlock', ],

        PROJECT_APPS = [
            'pagetree',
        ],
        # Django replaces this, but it still wants it. *shrugs*
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'HOST': '',
                'PORT': '',
                'USER': '',
                'PASSWORD': '',
            }
        },
    )

    try:
        # required by Django 1.7 and later
        django.setup()
    except AttributeError:
        pass

    # Fire off the tests
    call_command('test')
    call_command('jenkins', '--enable-coverage')

if __name__ == '__main__':
    main()
