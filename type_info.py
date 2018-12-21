#!/usr/bin/env python3

#This python script gets you attributes for any object

import json
import gzip

import esi_calling

#Uncomment the one you want to use.
#TQ
datasource ='tranquility'
#SISI
#datasource ='singularity'

esi_calling.set_user_agent('Hirmuolio/ESI-type-ID-attributes')


	

def print_normal_attributes(esi_response):
	type_info = esi_response.json()
	for key in type_info:
		if key not in ['dogma_attributes', 'dogma_effects', 'type_id', 'name', 'description']:
			print( '{:<20s} {:<}'.format(key, type_info[key]))
			#print(key, ': ', type_info[key])

			
def print_dogma_attributes(esi_response):
	
	type_info = esi_response.json()
	if 'dogma_attributes' not in type_info:
		print(type_info['name'], ' has no dogma attributes')
	else:
		print('\ndogma attributes:\n')
		length = len(type_info['dogma_attributes'])
		
		new_attributes = []
		
		for n in range(0, length):
			dogma_id = type_info['dogma_attributes'][n]['attribute_id']
			if not str(dogma_id) in dogma_attributes:
				#Find what this ID is for
				new_attributes.append(dogma_id)
		
		if len(new_attributes) != 0:
			#print('Getting info on', len(new_attributes), 'dogma attributes')
			esi_response_arrays = esi_calling.call_esi(scope = '/v1/dogma/attributes/{par}', url_parameters = new_attributes, datasource = datasource, job = 'get info on dogma attribute')
				
			for array in esi_response_arrays:
				response_json = array[0].json()
				dogma_attributes[str(response_json['attribute_id'])] = response_json #[ response_json['name'], response_json['display_name'], response_json['description'] ]
			#Save the ID list
			with gzip.GzipFile('dogma_attributes.gz', 'w') as outfile:
				outfile.write(json.dumps(dogma_attributes, indent=2).encode('utf-8'))
				
				
		for n in range(0, length):
			dogma_id = type_info['dogma_attributes'][n]['attribute_id']
			value = type_info['dogma_attributes'][n]['value']
			name = dogma_attributes[str(dogma_id)]['name']
			display_name = dogma_attributes[str(dogma_id)]['display_name']
			description = dogma_attributes[str(dogma_id)]['description']
			print( '{:<30s} {:<10s} {:<}{:<}'.format(name, str(value), '( '+display_name, ', '+description+' )'))
			
			
			
def print_dogma_effects(esi_response):
	type_info = esi_response.json()
	if 'dogma_effects' not in type_info:
		print(type_info['name'], ' has no dogma effects')
	else:
		print('\ndogma effects:\n')
		length = len(type_info['dogma_effects'])
		new_effects = []
		
		for n in range(0, length):
			dogma_id = type_info['dogma_effects'][n]['effect_id']
			if not str(dogma_id) in dogma_effects:
				#Find what this ID is for
				new_effects.append(dogma_id)
		
		if len(new_effects) != 0:
			#print('Getting info on', len(new_effects), 'dogma effects')
			esi_response_arrays = esi_calling.call_esi(scope = '/v2/dogma/effects/{par}', url_parameters = new_effects, datasource = datasource, job = 'get info on dogma attribute')
				
			for array in esi_response_arrays:
				response_json = array[0].json()
				dogma_effects[str(response_json['effect_id'])] = response_json
			#Save the ID list
			with gzip.GzipFile('dogma_effects.gz', 'w') as outfile:
				outfile.write(json.dumps(dogma_effects, indent=2).encode('utf-8'))
				
		for n in range(0, length):
			dogma_id = type_info['dogma_effects'][n]['effect_id']
			
			name = dogma_effects[str(dogma_id)]['name']
			
			print(name)
			for key in dogma_effects[str(dogma_id)]:
				if key != 'name':
					if dogma_effects[str(dogma_id)][key] == '':
						print( '  ', key, ': ""' )
					else:
						print( '  ', key, ': ', dogma_effects[str(dogma_id)][key] )
			
			#display_name = dogma_effects[str(dogma_id)]['display_name']
			#description = dogma_effects[str(dogma_id)]['description']
			#print( '{:<30s} {:<}{:<}'.format(name, '( '+display_name, ', '+description+' )'))

def parse_stats(esi_response):
	type_info = esi_response.json()
	#Print the output
		
	print('\n----')
	print('Type ID:', type_info['type_id'])
	print('Name:', type_info['name'])
	print('Description:', type_info['description'])
	
	print('\nAttributes:\n')
	print_normal_attributes(esi_response)
	
	print_dogma_attributes(esi_response)
	
	print_dogma_effects(esi_response)
	
	print('----\n')

try:
	#Load cached dogma attribute ID info
	with gzip.GzipFile('dogma_attributes.gz', 'r') as fin:
		dogma_attributes = json.loads(fin.read().decode('utf-8'))
except FileNotFoundError:
	#No file found. Start from scratch
    dogma_attributes = {}

try:
	#Load cached dogma effect ID info
	with gzip.GzipFile('dogma_effects.gz', 'r') as fin:
		dogma_effects = json.loads(fin.read().decode('utf-8'))
except FileNotFoundError:
	#No file found. Start from scratch
    dogma_effects = {}

while True:
	#Call ESI
	type_id = input("Give type ID: ")
	
	esi_response = esi_calling.call_esi(scope = '/v3/universe/types/{par}', url_parameters = [type_id], datasource = datasource, job = 'get type ID attributes')[0][0]
	if esi_response.status_code == 404:
		print('404 - Type ID: ' + type_id + ' not found')
	else:
		parse_stats(esi_response)
	
