import requests
from APIAccessInfo import username, key, useragent
import time

#login info
headers={"User-Agent":useragent}
params={"login":username,"api_key":key}

response=requests.get("https://e621.net/",params=params,headers=headers)

if str(response)=="<Response [200]>":
	print("Connection successful!")
else:
	print("Error.")
	print(str(response))
	print("Go to https://e621.net/help/api for more information")
print("")
input("Press enter to close")
