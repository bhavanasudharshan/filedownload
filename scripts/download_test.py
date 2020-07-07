import base64

from bson import ObjectId

from mongodb_client import get_db

rs=get_db()['uploads'].find_one({'_id': ObjectId('5f02ac4da163cabf41630f4d')})

byte_test=bytearray()

for chunk in rs['chunks']:
    c=chunk.encode('utf-8')
    bc=base64.b64decode(c)
    byte_test.extend(bc)

print(byte_test)


f = open("demofile2.png", "wb")
f.write(byte_test)
f.close()