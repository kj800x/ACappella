import os

def basedir(): #Base dir for your site, with a trailing slash.
    return "/".join(os.path.abspath( __file__ ).split('/')[:-2]) + "/"

def getdatabases():
    return {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'acappella',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'acappella',
        'PASSWORD': 'password',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
def getsecret():
    return '30 character random string. Make It So'

def gettemplatedirs():
    return (
      basedir() + "templates",
    )

def getstaticdirs():
    return (
      basedir() + "static",
    )
