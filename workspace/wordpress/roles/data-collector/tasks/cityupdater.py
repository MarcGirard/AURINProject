import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import couchdb

print("Please enter the password")
password_provided = input()
password = password_provided.encode() 
salt = b'salt_' 
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
try:
	decrypted = f.decrypt(b'gAAAAABezWarvyr-225xZ7yBU9NtFfNS193l9r7zScyf8fZHKLvDKeYjfqMRGarBDHBjemul9CGgZnexlfg939DMFasQXBmXiULMxd5WKhJH9-kWPl2UYqNfkHR3ohQFUZqX2JQ9X8_S')
	couchIP = decrypted.decode()
	couch = couchdb.Server(couchIP)
	with open('Aus.json','r',encoding = 'utf-8') as f:
		citydata = json.load(f)

	states = citydata["states"]

	db2 = couch['aussteamids']
	for d_id in db2.view('_all_docs'):
		docid = d_id['id']
		aus_doc = db2[docid]
		for y in list(aus_doc):
			if y == "_id":
				continue
			elif y == "_rev":
				continue
			else:

				if(y == 'loccityid'):
					city_id = str(aus_doc[y])
					for x in states:
						cities = states[x]['cities']
						if city_id in cities:
							citydetails = cities[city_id]
							for z in citydetails:
								if z == "coordinates_accuracy_level":
									continue
								else:
									try:

										aus_doc[z] = citydetails[z]
										db2.save(aus_doc)
										print(docid," updated")
									except BaseException as e:
										print("error occured")
except BaseException as e:
        print("Invalid Password")
