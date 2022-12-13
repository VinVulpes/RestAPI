
from app import app, client

#----------------------------------
# Проверка get
res = client.get('/tasks')
print(res.get_json())