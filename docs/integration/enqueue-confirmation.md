Here is quick python snippet to enqueue a confirmation...

```python
import requests
import json

url = "http://localhost:5000/api/confirmations/enqueue"

payload = {
    "username": "user",
    "jsonPayload": json.dumps({'Phone Number' : '+1 123 456 7890', 'name' : 'john franklin'})
}

response = requests.post(url, json=payload)
```