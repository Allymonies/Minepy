import json

with open("auths.json") as f:
	auths = json.loads(f.read())

c = 0
for auth in auths:
	print(str(c) + ": " + auth[3]["name"] + " (" + auth[3]["id"][0:8] + ")")
	c += 1
print(str(c) + ": Sign in on new account")
