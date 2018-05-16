#!/usr/bin/env python3

#This python script gets you attributes for any object

import requests
import json

#Uncomment the one you want to use.
#TQ
datasource ='tranquility&language=en-us'
#SISI
#datasource ='singularity&language=en-us'

def check_error(esi_response, job):
	status_code = esi_response.status_code
	
	if status_code != 200:
		#Error
		print('Failed to '+job+'. Error',esi_response.status_code,'-', esi_response.json()['error'])
		error = True
	else:
		error = False
		try:
			#Try to print warning
			print('Warning',esi_response.headers['warning'])
		except KeyError:
			warning = False
	
	return error

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
			url = "https://esi.tech.ccp.is/v1/dogma/attributes/"+str(dogma_id)+"/?datasource="+datasource
			esi_response = requests.get(url)
			
			if not check_error(esi_response, 'get info on dogma attribute'):
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
	type_ID = input("Give type ID: ")

	Url = "https://esi.tech.ccp.is/v3/universe/types/"+type_ID+"/?datasource="+datasource

	esi_response = requests.get(Url)
	
	if not check_error(esi_response, 'get attributes for type ID'):
		parse_stats(esi_response)
	
