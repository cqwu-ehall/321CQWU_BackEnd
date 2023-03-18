import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TASK_TEMPLATE_ID = os.getenv('TASK_TEMPLATE_ID')
TASK_TEMPLATE_FAIL_ID = os.getenv('TASK_TEMPLATE_FAIL_ID')
