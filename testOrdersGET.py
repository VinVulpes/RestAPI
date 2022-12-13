
from app import app, client

#----------------------------------
# Проверка get
res = client.get('/orders')
print(res.get_json())


