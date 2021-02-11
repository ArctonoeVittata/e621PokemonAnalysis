#https://e621.net/help/api

#imports
import requests
import time
from datetime import datetime
import csv
from os import system
from APIAccessInfo import username, key, useragent
from PokemonLists import baselist, alolist,galist

#login info
headers={"User-Agent":useragent}
params={"login":username,"api_key":key}

#main function
def main(pokemonList,alolaList,galarList,params,headers):
	dataList=createPokemonList(pokemonList,alolaList,galarList)
	time=recordTime("PST")
	countedDataList=getPostCount(dataList,params,headers)
	saveData(countedDataList,time)

#create dictionary for pokemon data from lists
def createPokemonList(base,alola,galar):
	for pokemon in alola:
		base.append("Alolan_"+pokemon)
	for pokemon in galar:
		base.append("Galarian_"+pokemon)
	dataList=[]
	for pokemon in base:
		dataList=dataList+[{"name":pokemon,"tag count":0}]
	return dataList

#Record time and time zone
def recordTime(timeZone):
	date=datetime.now().timetuple() #datetime recorded at beginning of process.
	dateStr=""
	for element in date:
		tempString=str(element)
		if len(tempString)==1:
			tempString="0"+tempString
		dateStr+=tempString
	dateTimeZone=dateStr[0:14]+timeZone #datetime saved as yyyymmddhhmmssTimeZone for title of CSV
	return dateTimeZone

#count number of posts for each pokemon based on library imput
def getPostCount(datalist,params,headers):
	totnum=len(datalist)
	i=0
	percent=0
	print("0%")
	#all uses of sleep(1) are to prevent more than 1 request per second.
	for pokemon in datalist:
		#code to display percent complete. Estimation based on number of pokemon
		i+=1
		prevpercent=percent
		percent=str(int(100*i/totnum))
		if percent==100 and 100*i/totnum<100:
			percent=99
		if percent!=prevpercent:
			system('cls')
			print(str(percent)+"%")
		
		#find code
		time.sleep(1)
		#find if tag is valid
		response=requests.get("https://e621.net/tags.json?commit=Search&search%5Bhide_empty%5D=yes&search%5Bname_matches%5D="+pokemon["name"]+"&search%5Border%5D=date",params=params,headers=headers)
		if str(response)!="<Response [200]>": #error test
			print(response)
		if response.json()!={'tags': []}: #if tag is valid (if dictionary for tag is not empty)
			page=0 #set page of tag to 0
			total=0 #set number of entries for tag to 0
			nextpage=True #set loop to happen
			while nextpage:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon.
				response=requests.get("https://e621.net/posts.json?limit=320&tags=-rating%3Asafe+"+pokemon["name"]+"&page="+str(page),params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)
				tagcount=len(response.json()["posts"])
				total+=tagcount #add number of posts on this page to overall total
				if tagcount!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					nextpage=False #exit loop
					pokemon["tag count"]=total #set the number of posts of the pokemon to the number of posts found via this part of the code
		else: #if tage is not valid
			page=0 #set page of tag to 0
			total=0 #set number of entries for tag to 0
			nextpage=True #set loop to happen
			while nextpage:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon, but with "_(pokémon)" added to the end to prevent ambiguity. i.e. gloom
				response=requests.get("https://e621.net/posts.json?limit=320&tags=-rating%3Asafe+"+pokemon["name"]+"_(pokémon)&page="+str(page),params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)
				tagcount=len(response.json()["posts"])
				total+=tagcount #add number of posts on this page to overall total
				if tagcount!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					nextpage=False #exit loop
					pokemon["tag count"]=total #set the number of posts of the pokemon to the number of posts found via this part of the code
		
	#sort list by most tagged and return
	datalist=sorted(datalist, key=lambda pokemon: pokemon["tag count"],reverse=True)
	return datalist
	
#save dictionary as csv
def saveData(dataList,dateString):
	i=0
	with open('pokemonPostCount'+dateString+'.csv', 'w', newline='') as csvfile:
		sheet=csv.writer(csvfile)
		for pokemon in dataList:
			i+=1
			#writes each line of csv as "rank,pokemon name,number of posts".
			#♀ and ♂ cannot be written to a CSV, so special cases are made for the nidorans.
			if "♀" in pokemon["name"]:
				sheet.writerow([str(i),"Nidoran female",str(pokemon["tag count"])])
			elif "♂" in pokemon["name"]:
				sheet.writerow([str(i),"Nidoran male",str(pokemon["tag count"])])
			else:
				sheet.writerow([str(i),pokemon["name"],str(pokemon["tag count"])])
	print("Done!")

#Run main	
main(baselist,alolist,galist,params,headers)

