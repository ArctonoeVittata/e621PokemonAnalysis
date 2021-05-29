#https://e621.net/help/api

#imports
import sys
import requests
import time
from datetime import datetime
import csv
from os import system
from APIAccessInfo import username, key, user_agent
from PokemonLists import base_list

#login info
headers={"User-Agent":user_agent}
params={"login":username,"api_key":key}

def main(pokemon_list,params,headers):
	target_tags=["male","female","intersex","ambiguous_gender"]
	data_list=create_pokemon_list(pokemon_list,target_tags)
	time=record_time("PST") #change if in different time zone
	print(time)
	counted_data_list=get_tag_counts(data_list,params,headers)
	save_data(counted_data_list,time,target_tags)

#create dictionary for pokemon data from lists
def create_pokemon_list(base,target_tags):
	data_list=[]
	for pokemon in base:
		tempdict={"name":pokemon,"count":0}
		for tag in target_tags:
			tempdict[tag]=0
		data_list.append(tempdict)
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

#counts frequency of desired tags for each Pokémon
def get_tag_counts(data_list,params,headers):
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
			#set number of entries for tag to 0
			next_page=True #set loop to happen
			while next_page:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon.
				response=requests.get("https://e621.net/posts.json?page="+str(page)+"&tags=solo+-rating%3As+~"+pokemon["name"]+"+~alolan_"+pokemon["name"]+"+~galarian_"+pokemon["name"]+"+~mega_"+pokemon["name"]+"+~gigantamax_"+pokemon["name"]+"&limit=320",params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)
							
				tag_count=len(response.json()["posts"])
				tag_list=[]
				if tag_count!=0:
					for post in response.json()["posts"]:
						pokemon["count"]=pokemon["count"]+1
						tag_list=[]
						for category in post["tags"]:
							tag_list=tag_list+post["tags"][category]
						for target_tag in pokemon:
							if target_tag in tag_list:
								pokemon[target_tag]=pokemon[target_tag]+1

				if tag_count!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					next_page=False #exit loop
		else: #if tage is not valid
			page=0 #set page of tag to 0
			total=0 #set number of entries for tag to 0
			next_page=True #set loop to happen
			while next_page:
				page+=1 #set to next page
				time.sleep(1)
				#gets 320 posts from given page with tags "-rating:safe" and the pokemon, but with "_(pokémon)" added to the end to prevent ambiguity. i.e. gloom
				response=requests.get("https://e621.net/posts.json?page="+str(page)+"&tags=solo+-rating%3As+~"+pokemon["name"]+"_(pokémon)+~alolan_"+pokemon["name"]+"+~galarian_"+pokemon["name"]+"+~mega_"+pokemon["name"]+"+~gigantamax_"+pokemon["name"]+"&limit=320",params=params,headers=headers)
				if str(response)!="<Response [200]>": #error test
					print(response)				
				
				tag_count=len(response.json()["posts"])
				tag_list=[]
				if tag_count!=0:
					for post in response.json()["posts"]:
						pokemon["count"]=pokemon["count"]+1
						tag_list=[]
						for category in post["tags"]:
							tag_list=tag_list+post["tags"][category]
						for target_tag in pokemon:
							if target_tag in tag_list:
								pokemon[target_tag]=pokemon[target_tag]+1


				if tag_count!=320: #if there are not 320 posts, then this is the last page of posts of the tag
					next_page=False #exit loop
		
	#sort list by most tagged and return
	data_list=sorted(data_list, key=lambda pokemon: pokemon["count"],reverse=True)
	return data_list
	
def save_data(data_list,date_string,target_tags):
	i=0
	with open('soloTagPerPokemonCount'+date_string+'.csv', 'w', newline='') as csvfile:
		sheet=csv.writer(csvfile)
		#first line:
		row_list=["Rank","Pokemon","Count"]
		for tag in target_tags:
				row_list.append("#"+tag)
				row_list.append("%"+tag)
		sheet.writerow(row_list)
		for pokemon in data_list:
			i+=1
			#writes each line of csv as "rank,pokemon name,total posts,count for tag,% for tag".
			#♀ and ♂ cannot be written to a CSV, so special cases are made for the nidorans.
			row_list=[str(i),pokemon["name"],str(pokemon["count"])]
			for tag in target_tags:
				row_list.append(str(pokemon[tag]))
				if pokemon["count"]==0:
					row_list.append("N/A")
				else:
					row_list.append(str(round(100*pokemon[tag]/pokemon["count"],2))+"%")
			
			if "♀" in pokemon["name"]:
				row_list[1]="Nidoran female"
			elif "♂" in pokemon["name"]:
				row_list[1]="Nidoran male"
				
			sheet.writerow(row_list)
	print("Done!")

#run main
main(base_list,params,headers)
