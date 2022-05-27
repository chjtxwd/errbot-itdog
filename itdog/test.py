import requests
import pandas as pd
import json

api = 'http://itdog.chatops.1671409927271754.cn-shanghai.fc.devsapp.net/itdog?url='
url = api+'https://www.google.com'
r = requests.get(url)
r = json.loads(r.text)
result = list()
for each in r:
    each = json.loads(each)
    result.append(each)
for each in result:
    for key in each.keys():
      tmp = list()
      tmp.append(each[key])
      each[key] = tmp
df = pd.DataFrame(result)
http_status = df.http_code.value_counts()
http_status = http_status.div(http_status.sum())
http_status = http_status.apply(lambda x: format(x, '.2%')) 
markdown = http_status.to_markdown() 
print(markdown)

