Github link: https://github.com/ArctonoeVittata/e621PokemonAnalysis

The goal of this project is to create data on pornographic pokemon media by accessing the website e621.net using its API.
Below are the files currently in this project, their function, necessary libraries, and output format.

All files run on python.
For more info about the e621 API, go to https://e621.net/help/api

Lists of pokemon generated using list generator on https://www.dragonflycave.com, then edited to fit formatting of e621 tags.

APIAccessInfo.py
In order to run any code that accesses the e621 API, this file must be in the same directory as the code being ran, and this file must be edited.
The file contains 3 lines:
username=""
This is where you put your e621 username.
key=""
This is where you put your access key. To get this key, go to https://e621.net/users/home while signed in to e621.net, go to "Manage API Access", then generate a key.
useragent="IWantStatsOnPokemonTags (by "+username+" on e621)"
As a default, the user agent of the project will be set to "IWantStatsOnPokemonTags", followed by your e621 username. Edit this line to change the name of the project, but make sure to keep the "(by username on e621)" to comply with the e621 API rules.

PokemonLists.py
In order to run any code that uses a list of pokemon, this file must be in the same directory as the code being ran. This file requires no editing, but if it is out of date, it can be edited to add more pokemon.
This can also be edited if your project cares about specific forms of pokemon (i.e. Lycanroc_midday vs Lycanroc_midnight.)
This file consists of 3 lists: one of default pokemon, one of alolan regional variants, and one of galarian regional variants. This is due to e621 tagging interpreting regional variants as distinct from the default variety.


IndividualPokemonTagCount.py
This code requires the following directories:
requests
As this code accesses the e621 API, APIAccessInfo.py is required.
This code creates a csv file with each pokemon and the number of posts it has on e621, ordered based on number of posts.
As e621 has a 1 request per second limit, and due to the number of pokemon that exist, this code takes a long time to run.
To ensure the code is progressing, the terminal will display a percent progress estimated based on what pokemon in the list is being recorded.
The output format of the csv is, by line:
rank of pokemon,name of pokemon,number of nsfw posts of pokemon

To be created:
Code that allows testing of access to e621 API.
Code that shows correlation of certain pokemon with other tags.
