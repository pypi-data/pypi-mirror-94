"""Константы"""

from logging import DEBUG

DEFAULT_HOSTNAME = '127.0.0.1'
DEFAULT_PORT = 7777
DEFAULT_PASSWORD = 'geekbrains'

MAX_CONNECTIONS = 4
ENCODING = 'utf-8'
SIZE_PACKET = 10240

DEFAULT_LOG_LEVEL = DEBUG

SUCCESS_CODE_RESPONSE = 200
CREATED_CODE_RESPONSE = 201
ACCEPTED_CODE_RESPONSE = 202
RESET_CONTENT_RESPONSE = 205

ERROR_CODE_RESPONSE = 400

AUTH_REQUIRED_RESPONSE = 511

ACTION = 'action'
TIME = 'time'
TYPE = 'type'
USER = 'user'
ACCOUNT_NAME = 'account_name'
STATUS = 'status'
ALERT = 'alert'
PUBLIC_KEY = 'public_key'
DATA = 'bin'

SERV_DB_NAME = 'server_database.db3'
FILE_CONF_NAME = "server.ini"

CLIENT_DB_NAME = 'client_database.db3'

TYPE_ACTION_PRESENCE = 'presence'
TYPE_ACTION_MESSAGE = 'msg'
TYPE_ACTION_LEAVE = 'leave'
TYPE_ACTION_ADD_CONTACT = 'add'
TYPE_ACTION_DELETE_CONTACT = 'delete'
TYPE_ACTION_GET_CONTACTS = 'get_contacts'
TYPE_ACTION_GET_USERS = 'get_users'
TYPE_ACTION_PUBLIC_KEY = 'get_public_key'

RESPONSE = 'response'
ERROR = 'error'

DEFAULT_ACCOUNT_NAME = 'Guest'
DEFAULT_STATUS = 'Ready to talk'

SUCCESS_COMMENT = 'ok'
ERROR_COMMENT = 'error message'
DUPLICATE_NAME_ERROR_COMMENT = 'Пользователь c таким именем уже существует!'
USER_NOT_EXISTS_COMMENT = 'Пользователь с таким именем не существует!'
WRONG_PASSWORD = 'Неверный пароль!'

FROM = 'from'
TO = 'to'
CONTACT = 'contact'
MESSAGE = 'message'
