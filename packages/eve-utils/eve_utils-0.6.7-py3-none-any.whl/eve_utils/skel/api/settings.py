"""
Settings to configure Eve's behaviours.
"""
import domain
from configuration import SETTINGS

MONGO_HOST = SETTINGS.get('ES_MONGO_HOST')
MONGO_PORT = SETTINGS.get('ES_MONGO_PORT')
MONGO_DBNAME = SETTINGS.get('ES_MONGO_DBNAME')
if 'ES_MONGO_AUTH_SOURCE' in SETTINGS.keys():
    MONGO_AUTH_SOURCE = SETTINGS.get('ES_MONGO_AUTH_SOURCE')
if 'ES_MONGO_USERNAME' in SETTINGS.keys():
    MONGO_USERNAME = SETTINGS.get('ES_MONGO_USERNAME')
if 'ES_MONGO_PASSWORD' in SETTINGS.keys():
    MONGO_PASSWORD = SETTINGS.get('ES_MONGO_PASSWORD')

# the default BLACKLIST is ['$where', '$regex'] - this line turns on regex
MONGO_QUERY_BLACKLIST = ['$where']

RENDERERS = ['eve.render.JSONRenderer']  # removed eve.render.XMLRenderer

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
PAGINATION_LIMIT = 1000
PAGINATION_DEFAULT = 500

# http://python-eve.org/features.html#operations-log
# OPLOG = True
# OPLOG_ENDPOINT = '_oplog'

SCHEMA_ENDPOINT = '_schema'
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

X_DOMAINS = '*'
X_EXPOSE_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
X_HEADERS = [
    'Accept',
    'Authorization',
    'If-Match',
    'Access-Control-Expose-Headers',
    'Access-Control-Allow-Origin',
    'Content-Type',
    'Pragma',
    'X-Requested-With',
    'Cache-Control'
]

RETURN_MEDIA_AS_BASE64_STRING = False
RETURN_MEDIA_AS_URL = True

if 'MEDIA_BASE_URL' in SETTINGS.keys():
    MEDIA_BASE_URL = SETTINGS.get('ES_MEDIA_BASE_URL')
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']

DOMAIN = domain.DOMAIN

UPLOAD_FOLDER = 'uploads/'

OPTIMIZE_PAGINATION_FOR_SPEED = True
