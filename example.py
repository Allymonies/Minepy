import ast
import getpass
import json
import minepy
import sys
import yggdrasil

def handler(self, packet_id, data)
	pass

with open("auths.json") as f:
	auths = ast.literal_eval(f.read())

c = 0
for auth in auths:
	print(str(c) + ": " + auth[2]["name"] + " (" + auth[2]["id"][0:8] + ")")
	c += 1
print(str(c) + ": Sign in on new account")
choice = int(input())
if choice == len(auths):
	print("Username:")
	username = input()
	print("Password:")
	password = getpass.getpass()
	newAuth = yggdrasil.authenticate(username, password)
	if "error" in newAuth:
		print("Error has occurred.")
		print("Please make sure your login details are valid.")
		sys.exit()
	else:
		print("Logged in as " + newAuth[2]["name"])
		print("UUID is " + newAuth[2]["id"])
		print("Adding auth to auths.json...")
		auths.append(newAuth)
		with open("auths.json","w") as f:
			f.write(str(auths))
		print("Auth saved.")
		auth = newAuth
elif choice >= 0 and choice < len(auths):
	auth = auths[choice]
	print("Using " + auths[choice][2]["name"])
elif choice > len(auths) or choice < 0:
	print("Choice must be between 0 and " + str(len(auths)))
	sys.exit()

print("Validating...")
valid = yggdrasil.validate(auth[0],auth[1])
if valid == True:
	print("Validation success!")
else:
	print("Validation failed, attempting to refresh token...")
	refresh = yggdrasil.refresh(auth[0],auth[1])
	if not "error" in refresh:
		auth = refresh
		print("Refreshed successfully!")
	else:
		print("Failed to refresh, exiting...")
		sys.exit()
print("Server ip?")
ip = input()
if ip.find(":") == -1:
	host = ip
	port = 25565
else:
	host = ip[0:ip.find(":")]
	port = ip[ip.find(":")+1:]
connection = minepy.Connect(host, port, handler)
status = json.loads(connection.status())
print(host + " on version " + status["version"]["name"] + " with " + str(status["players"]["online"]) + "/" + str(status["players"]["max"]) + " players online.")
