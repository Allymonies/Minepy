import requests

base = "https://authserver.mojang.com"

def authenticate(username, password, clientToken = None, requestUser = True, debug = False):
	endpoint = "/authenticate"
	data = {
		"agent": {
			"name": "Minecraft",
			"version": 1
			},
		"username": username,
		"password": password,
		"requestUser": requestUser
		}
	if clientToken != None:
		data["clientToken"] = clientToken
	response = requests.post(base + endpoint, json = data)
	resp = response.json()
	if debug:
		return resp
	elif not "error" in resp:
		if not "user" in resp:
			return [resp["accessToken"], resp["clientToken"], resp["selectedProfile"]]
		else:
			return [resp["accessToken"], resp["clientToken"], resp["selectedProfile"], resp["user"]]
	else:
		return resp

def refresh(accessToken, clientToken, requestUser = True, debug = False):
	endpoint = "/refresh"
	data = {
		"accessToken": accessToken,
		"clientToken": clientToken,
		"requestUser": requestUser
		}
	response = requests.post(base + endpoint, json = data)
	resp = response.json()
	if debug:
		return resp
	elif not "error" in resp:
		if not "user" in resp:
			return [resp["accessToken"], resp["clientToken"], resp["selectedProfile"]]
		else:
			return [resp["accessToken"], resp["clientToken"], resp["selectedProfile"], resp["user"]]	
	else:
		return resp

def validate(accessToken, clientToken = None):
	endpoint = "/validate"
	data = {
		"accessToken": accessToken,
		}
	if clientToken:
		data["clientToken"] = clientToken
	response = requests.post(base + endpoint, json = data)
	if response.status_code == 204:
		return True
	else:
		return response.json()

def signout(username, password):
	endpoint = "/signout"
	data = {
		"username": username,
		"password": password
		}
	response = requests.post(base + endpoint, json = data)
	if response.text == "":
		return True
	else:
		return response.json()

def invalidate(accessToken, clientToken):
	endpoint = "/invalidate"
	data = {
		"accessToken": accessToken,
		"clientToken": clientToken
		}
	response = requests.post(base + endpoint, json = data)
	if response.text == "":
		return True
	else:
		return response.json()
