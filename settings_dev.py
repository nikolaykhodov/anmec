# Django settings for s project.
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(os.path.dirname(__file__), 'liketools_debug.sqlite'),  # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'anmec',  # Or path to database file if using sqlite3.
        'USER': 'anmec',                      # Not used with sqlite3.
        'PASSWORD': '1',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}
