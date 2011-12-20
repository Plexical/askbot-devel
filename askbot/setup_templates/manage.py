#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

import sys
if 'test' in sys.argv:
    # These tasks must be performed here for now - askbot.__init__
    # will fail without some kind of database present, and then test
    # suites can't be run.
    import os
    pkg_guess = settings.PROJECT_ROOT.split(os.path.sep)[-1]
    os.environ['DJANGO_SETTINGS_MODULE'] = ('%s.settings' % pkg_guess)
    sys.path.append('.')
    settings.LIVESETTINGS_OPTIONS = {
        settings.SITE_ID: { 'SETTINGS':
                { 'EXTERNAL_KEYS': {
                    'RECAPTCHA_SECRET': 'must-exist' }
                }
            }
    }
    from django.test.utils import setup_test_environment
    setup_test_environment()
    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()
    from django.db import connection
    connection.creation.create_test_db(1, True)

if __name__ == "__main__":
    execute_manager(settings)
