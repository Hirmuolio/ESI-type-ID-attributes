#!/usr/bin/env python3

#This python script gets you attributes for any object

import json

import esi_calling

#Uncomment the one you want to use.
#TQ
datasource ='tranquility'
#SISI
#datasource ='singularity'

def parse_stats(esi_response):
	npc_stats = esi_response.json()

	#Check if it has attributes.
	#If it does do the things
	try:
		length = len(npc_stats['dogma_attributes'])
	except KeyError:
		print('Type ID',npc_stats['type_id'],'-',npc_stats['name'],'-','has no attributes')
		return

	for n in range(0, length):
		dogma_id = npc_stats['dogma_attributes'][n]['attribute_id']
		if not str(dogma_id) in attributes:
			#Find what this ID is for
			print('Getting info on dogma attribute ID', dogma_id)
			
			esi_response = esi_calling.call_esi(scope = '/v1/dogma/attributes/{par}', url_parameter = dogma_id, parameters={}, datasource = datasource, job = 'get info on dogma attribute')

			response_json = esi_response.json()
			attributes[str(dogma_id)] = [ response_json['name'], response_json['display_name'], response_json['description'] ]
			
			
	#Save the ID list
	with open('attributes.txt', 'w') as outfile:
		json.dump(attributes, outfile, indent=4)

	#Print the output
		
	print('\n----')
	print('Type ID:', npc_stats['type_id'])
	print('Name:', npc_stats['name'])
	print('Description:', npc_stats['description'])
	print('----')
	print('Attributes:')

	for n in range(0, length):
		dogma_id = npc_stats['dogma_attributes'][n]['attribute_id']
		value = npc_stats['dogma_attributes'][n]['value']
		name = attributes[str(dogma_id)][0]
		display_name = attributes[str(dogma_id)][1]
		description = attributes[str(dogma_id)][2]
		print( '{:<30s} {:<10s} {:<}{:<}'.format(name, str(value), '( '+display_name, ', '+description+' )'))
	print('----\n')
	return

try:
	#Load cached dogma attribute ID info
    attributes = json.load(open('attributes.txt'))
except FileNotFoundError:
	#No file found. Start from scratch
    attributes = {}

while True:
	#Call ESI
	type_id = input("Give type ID: ")
	
	esi_response = esi_calling.call_esi(scope = '/v3/universe/types/{par}', url_parameter = type_id, parameters={}, datasource = datasource, job = 'get type ID attributes')
	
	if esi_response.status_code == 404:
		print('404 - Type ID: ' + type_id + ' not found')
	else:
		parse_stats(esi_response)
	
