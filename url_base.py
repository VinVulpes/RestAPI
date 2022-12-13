'''
Provides base url to other apps
'''
PORT = 5000
BASE_URL = 'http://localhost:'+str(PORT)
URL_TASKS = BASE_URL + '/tasks'
URL_TASK_ORDER = BASE_URL + '/orders/'+'1'
URL_POST_ORDER = BASE_URL + '/orders'
URL_POST_TASKS = BASE_URL + '/tasks'
URL_ORDERS = BASE_URL + '/orders'
URL_DURATION = BASE_URL + '/duration/'+'1'
