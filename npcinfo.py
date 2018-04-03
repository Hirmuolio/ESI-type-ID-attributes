#This python script gets you attrinutes for any object

#!/usr/bin/env python3

import requests
import json

try:
	#Load cached dogma attribute ID info
    attributes = json.load(open('attributes.txt'))
except FileNotFoundError:
	#No file found. Start from scratch
    attributes = {}

while True:
	#Call ESI
	type_ID = input("Give type ID: ")

	Url = "https://esi.tech.ccp.is/v3/universe/types/"+type_ID+"/?datasource=tranquility&language=en-us"

	#Uncomment this to get SISI stats
	#Url = "https://esi.tech.ccp.is/v3/universe/types/"+type_ID+"/?datasource=singularity&language=en-us"

	esi_response = requests.get(Url)
	npc_Stats = esi_response.json()

	#Find out what each of the dogma IDs mean
	length = len(npc_Stats['dogma_attributes'])

	for n in range(0, length):
		dogma_id = npc_Stats['dogma_attributes'][n]['attribute_id']
		if not str(dogma_id) in attributes:
			#Find what this ID is for
			print('Getting info on dogma attribute ID', dogma_id)
			Url = "https://esi.tech.ccp.is/v1/dogma/attributes/"+str(dogma_id)+"/?datasource=tranquility"
			attributes[str(dogma_id)] = [ requests.get(Url).json()['name'], requests.get(Url).json()['display_name'], requests.get(Url).json()['description'] ]

	#Save the ID list
	with open('attributes.txt', 'w') as outfile:
		json.dump(attributes, outfile)

	#Print the output
		
	print('\n----')
	print('Type ID:', npc_Stats['type_id'])
	print('Name:', npc_Stats['name'])
	print('----')
	print('Attributes:')

	for n in range(0, length):
		dogma_id = npc_Stats['dogma_attributes'][n]['attribute_id']
		value = npc_Stats['dogma_attributes'][n]['value']
		name = attributes[str(dogma_id)][0]
		display_name = attributes[str(dogma_id)][1]
		description = attributes[str(dogma_id)][2]
		print( '{:<30s} {:<10s} {:<}{:<}'.format(name, str(value), '( '+display_name, ', '+description+' )'))
	print('----\n')
	
