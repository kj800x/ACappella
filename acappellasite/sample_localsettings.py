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
    return 'huje#^(t2=8=-t@#e@jg9ec&c)l8zp-l7to552^ubvx*v-rmig'

def gettemplatedirs():
   return (
    "/home/kevin/django/ACappella/templates", #DevelopmentServer
   #"/www/django/acappellasite/templates", #ProductionServer
)

def getstaticdirs():
   return (
    "/home/kevin/django/ACappella/static", #DevelopmentServer
   #"/www/django/acappellasite/templates", #ProductionServer
)
