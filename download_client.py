import requests
from bson.objectid import ObjectId
from flask import json

from mongodb_client import get_db
import base64


username = 'arjun'
password = '123456'
response = requests.post("http://localhost:8081/login", verify=False, auth=(username, password),
                         headers={'Content-Type': 'application/json'})
assert response.status_code == 200
access_token = json.loads(response.text)['access_token']
access_token_auth = "access_token {0}".format(access_token)

uploadId='5f02ac4da163cabf41630f4d'
byte_test=bytearray()

resp = requests.get("http://0.0.0.0:8082/download/"+uploadId,
                     headers=dict(
                         Authorization=access_token_auth))

decoded_resp = resp.content.decode('utf-8')
response_json = json.loads(decoded_resp)

print(response_json['chunk'])
print("\n")

chunk_size=int(response_json['total_chunks']) #16
chunk_number=1

chunk = response_json['chunk']

c = chunk.encode('utf-8')
bc = base64.b64decode(c)
byte_test.extend(bc)

chunk_size=chunk_size-1

while chunk_size>=1:
    print(chunk_size)
    resp = requests.get("http://0.0.0.0:8082/download/" + uploadId,
                        headers=dict(
                            Authorization=access_token_auth),data=dict(chunk_number=str(chunk_number)))
                            # Authorization=access_token_auth),data=dict(chunk_number=str(15)))

    decoded_resp = resp.content.decode('utf-8')
    response_json = json.loads(decoded_resp)
    print(response_json['chunk'])
    print("\n")

    chunk=response_json['chunk']
    c = chunk.encode('utf-8')
    bc=base64.b64decode(c)

    byte_test.extend(bc)

    chunk_number= chunk_number + 1
    chunk_size=chunk_size-1
    print(chunk_number)

print(byte_test)
f = open("demofile2.png", "wb")
f.write(byte_test)
f.close()

#
# rs=get_db()['uploads'].find_one({'_id': ObjectId('5f02ac4da163cabf41630f4d')},{})
#
# byte_test=bytearray()
#
# for chunk in rs['chunks']:
#     c=chunk.encode('utf-8')
#     bc=base64.b64decode(c)
#     byte_test.extend(bc)
#
# print(byte_test)
#
#
# f = open("demofile2.png", "wb")
# f.write(byte_test)
# f.close()
