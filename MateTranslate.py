#!/usr/bin/env python3

import urllib.parse
import requests

# Generate a random device ID
input_str = "?u?d?d?u?d?u?d?u-?u?d?u?d-?d?d?d?u-?u?d?u?u-?d?u?d?u?d?d?u?d?d?d?d?d"
device_id = ''.join([str(int(c) if c.isdigit() else ord(c) - 87) for c in input_str]).lstrip("0")

# Get user input
email = input("Enter your email address: ")
password = input("Enter your password: ")

# Make the API call to register the user
name = "Mate Trans"
register_url = f"https://sync.matetranslate.com/register_user?bought_pro_before=0&d_av=13.4.1&d_id={device_id}&d_platform=ios&d_sv=14.3.0&email={urllib.parse.quote(email)}&gdpr_consent=1&has_pro=1&lang=en&name={urllib.parse.quote(name)}&pwd={urllib.parse.quote(password)}"
headers = {
	"Accept": "application/json",
	"Accept-Language": "en-AU;q=1.0, en-AU;q=0.9",
	"Connection": "keep-alive",
	"Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
	"User-Agent": "Mate/13.4.1 (andriiliakh.InstTranslate-ios-free; build:462; iOS 14.3.0) Alamofire/13.4.1"
}
response = requests.get(register_url, headers=headers)

# Check if the register was successful
if "token\":\"" in response.text and email in response.text:  # fix string formatting
	print("Registration successful!")
	# Get the authentication token
	token_start = response.text.index("token\":\"") + len("token\":\"")
	token_end = response.text.index("\"", token_start)
	token = response.text[token_start:token_end]
	
	# Revoke the authentication token
	if token:
		revoke_url = f"https://sync.matetranslate.com/revoke_token?lang=en&token={urllib.parse.quote(token)}"
		response = requests.get(revoke_url, headers=headers)
		if "{\"success\":true}" in response.text:
			print("Token revocation successful!")
			# Login with the registered email and password
			login_url = f"https://sync.matetranslate.com/login?bought_pro_before=0&d_av=13.4.1&d_id={device_id}&d_platform=ios&d_sv=14.3.0&email={urllib.parse.quote(email)}&gdpr_consent=1&has_pro=1&lang=en&method=e&pwd={urllib.parse.quote(password)}"
			response = requests.get(login_url, headers=headers)
			# Check if the login was successful
			if "has_pro\":true" in response.text and "isLifetime\":true" in response.text:
				print("Upgrade to lifetime successful!")
			else:
				print("Upgrade failed.")
		else:
			print("Token revocation failed. Please start again")
	else:
		print("No token found. Please start again")
else:
	# If the email is already taken, try to log in instead
	print("Email is already taken. Trying to log in.")
	login_url = f"https://sync.matetranslate.com/login?bought_pro_before=0&d_av=13.4.1&d_id={device_id}&d_platform=ios&d_sv=14.3.0&email={urllib.parse.quote(email)}&gdpr_consent=1&has_pro=1&lang=en&method=e&pwd={urllib.parse.quote(password)}"
	response = requests.get(login_url, headers=headers)
	# Check if the login was successful
	if "has_pro\":true" in response.text and "isLifetime\":true" in response.text:
		print("Upgrade to lifetime successful!")
		
	if "The password you've entered is wrong" in response.text:
		print("The password you've entered is wrong, please try again")
		
	else:
		print("Upgrade failed.")
		
while True:
	option = input("Press R to restart script, Press E to Exit: ")
	if option.upper() == "R":
		exec(open(__file__).read())
	elif option.upper() == "E":
		break