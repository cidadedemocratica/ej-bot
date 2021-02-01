"""
This file is used to test bot post requests
To use it, you must have the actions server and bot running
And execute
$ python3 post.py
"""

import requests
import json

post_url = "http://localhost:5005/webhooks/rest/webhook"

headers = {"content-type": "application/json"}

params = {"message": "constante"}

r = requests.post(post_url, data=json.dumps(params), headers=headers)

print(r.text)
