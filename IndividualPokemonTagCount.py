#https://e621.net/help/api

#imports
import requests
import time
from datetime import datetime
import csv
from os import system
from APIAccessInfo import username, key, user_agent
from PokemonLists import base_list, alola_list,galar_list

#login info
headers={"User-Agent":user_agent}
params={"login":username,"api_key":key}

#main function
def main(pokemon_list,alola_list,galar_list,params,headers):
	data_list=create_pokemon_list(pokemon_list,alola_list,galar_list)
	time=record_time("PST") #change if in different time zone
	counted_data_list=get_post_count(data_list,params,headers)
	save_data(counted_data_list,time)

#create dictionary for pokemon data from lists
def create_pokemon_list(base,alola,galar):
	for pokemon in alola:
		base.append("Alolan_"+pokemon)
	for pokemon in galar:
		base.append("Galarian_"+pokemon)
	data_list=[]
	for pokemon in base:
		data_list=data_list+[{"name":pokemon,"tag count":0}]
	return data_list

#Record time and time zone
def record_time(time_zone):
	date=datetime.now().timetuple() #datetime recorded at beginning of process.
	date_str=""
	for element in date:
		temp_string=str(element)
		if len(temp_string)==1:
			temp_string="0"+temp_string
		date_str+=temp_string
	date_time_zone=date_str[0:14]+time_zone #datetime saved as yyyymmddhhmmssTimeZone for title of CSV
	return date_time_zone

#count number of posts for each pokemon based on library imput
def get_post_count(data_list,params,headers):
	tot_num=len(data_list)
	i=0
	percent=0
	print("0%")
	#all uses of sleep(1) are to prevent more than 1 request per second.
	for pokemon in data_list:
		#code to display percent complete. Estimation based on number of pokemon
		i+=1
		prev_percent=percent
		percent=str(int(100*i/tot_num))
		if percent==100 and 100*i/tot_num<100:
			percent=99
		if percent!=prev_percent:
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
			next_page=True #set loop to happen
			while next_page:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon.
				response=requests.get("https://e621.net/posts.json?limit=320&tags=-rating%3Asafe+"+pokemon["name"]+"&page="+str(page),params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)
				tag_count=len(response.json()["posts"])
				total+=tag_count #add number of posts on this page to overall total
				if tag_count!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					next_page=False #exit loop
					pokemon["tag count"]=total #set the number of posts of the pokemon to the number of posts found via this part of the code
		else: #if tage is not valid
			page=0 #set page of tag to 0
			total=0 #set number of entries for tag to 0
			next_page=True #set loop to happen
			while next_page:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon, but with "_(pokémon)" added to the end to prevent ambiguity. i.e. gloom
				response=requests.get("https://e621.net/posts.json?limit=320&tags=-rating%3Asafe+"+pokemon["name"]+"_(pokémon)&page="+str(page),params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)
				tag_count=len(response.json()["posts"])
				total+=tag_count #add number of posts on this page to overall total
				if tag_count!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					next_page=False #exit loop
					pokemon["tag count"]=total #set the number of posts of the pokemon to the number of posts found via this part of the code
		
	#sort list by most tagged and return
	data_list=sorted(data_list, key=lambda pokemon: pokemon["tag count"],reverse=True)
	return data_list
	
#save dictionary as csv
def save_data(data_list,date_string):
	i=0
	with open('pokemonPostCount'+date_string+'.csv', 'w', newline='') as csvfile:
		sheet=csv.writer(csvfile)
		for pokemon in data_list:
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
main(base_list,alola_list,galar_list,params,headers)

