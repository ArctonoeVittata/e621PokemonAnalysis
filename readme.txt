Github link: https://github.com/ArctonoeVittata/e621PokemonAnalysis

The goal of this project is to create data on pornographic Pokémon media by accessing the website e621.net using its API.
Below are the files currently in this project, their function, necessary libraries, and output format.

All files run on python.
For more info about the e621 API, go to https://e621.net/help/api

List of Pokémon generated using list generator on https://www.dragonflycave.com, then edited to fit formatting of e621 tags.

APIAccessInfo.py
In order to run any code that accesses the e621 API, this file must be in the same directory as the code being ran, and this file must be edited.
The file contains 3 lines:
username=""
This is where you put your e621 username.
key=""
This is where you put your access key. To get this key, go to https://e621.net/users/home while signed in to e621.net, go to "Manage API Access", then generate a key.
useragent="IWantStatsOnPokemonTags (by "+username+" on e621)"
As a default, the user agent of the project will be set to "IWantStatsOnPokemonTags", followed by your e621 username.
Edit this line to change the name of the project if you wish, but make sure to keep the "(by [username] on e621)" to comply with the e621 API rules.

PokemonLists.py
In order to run any code that uses a list of Pokémon, this file must be in the same directory as the code being ran.
This list and associated code group all alternate forms of Pokémon together.
For example, Meowth, Alolan Meowth, Galarian Meowth, and Gigantamax Meowth are all consiterd the same Pokémon.
This file requires no editing, but if it is out of date, it can be edited to add more Pokémon.
This can also be edited if your project cares about specific forms of Pokémon (i.e. Lycanroc_midday vs Lycanroc_midnight.) or if the program is to be adapted for some other use.

TestConnection.py
This code requires the directory "requests" and the file "APIAccessInfo.py"
This code tests the user's connection to the e621 API. If the connection is unsuccessful, it gives the error code from e621.net.

IndividualPokemonTagCount.py
This code requires the directory "requests" and the files "APIAccessInfo.py" and "PokemonLists.py"
This code creates a csv file with each Pokémon and the number of nsfw posts it has on e621, ordered based on number of posts.
As e621 has a 1 request per second limit, and due to the number of Pokémon that exist, this code takes a long time to run.
To ensure the code is progressing, the terminal will display a percent progress estimated based on what Pokémon in the list is being recorded.
All other counters use the same estimation method.
The output format of the csv is, by line:
rank of Pokémon, name of Pokémon, number of nsfw posts of Pokémon

SoloTagPerPokemonCount.py
This code requires the directory "requests" and the files "APIAccessInfo.py" and "PokemonLists.py"
This code creates a csv file with each Pokémon, the number of nsfw posts with the "solo" tag, and for all the targetted tags, the count and ratio of posts that have that tag.
The reason solo posts are used will be explained further in the next code.
Note that the target tags can be changed. The default tags are "male", "female", "intersex", and "ambiguous_gender"
The output format of the csv is, by line:
rank of Pokémon (by solo count), name of Pokémon, number of posts of Pokémon (by solo count), number of posts of 1st target tag, percent of posts of 1st target tag, and so on for every additional tag.

TagPerPokemonSoloEstimateCount.py
This code requires the directory "requests" and the files "APIAccessInfo.py" and "PokemonLists.py"
This code creates a csv file with each Pokémon, the number of nsfw posts, number with "solo" tag, and for all the targetted tags, the ratio and estimated count of posts that have that tag.
After some minor testing, using the "solo" tag as an estimate for the proportion of tags appearing for a certain Pokémon appears more accurate than using all posts (which would include images of Pokémon alongside the target Pokémon that may be the reason for the tag).
Using these ratios and the number of posts of a given Pokémon, the number of posts of that Pokémon depicted with the tag is estimated.
More testing will be done, and ideally a better estimate will be created.
The output format of the csv is, by line:
rank of Pokémon, name of Pokémon, number of posts, number of solo posts, percent of posts that are solo, estimated number of posts of 1st tag, estimated percent of posts of 1st tag, and so on for every additional tag.

To Be Added:
Additional testing for how to best estimate tag ratios.
An actual user interface.