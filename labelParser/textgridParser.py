#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import textgrid as tgp
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../batchProcessing/'))
import batchProcessing as BP
 

def TextGrid2Dict(textgrid_file, tier_name):
	
	tg_dict={}
	par_obj = tgp.TextGrid.load(textgrid_file)	#loading the object	
	tiers= tgp.TextGrid._find_tiers(par_obj)	#finding existing tiers
	
	for tier in tiers:
		
		if tier.tier_name() == tier_name:	#iterating over tiers and selecting the one specified
			
			tier_details = tier.make_simple_transcript();		#this function parse the file nicely and return cool tuples
			
			for line in tier_details:
				
				annotation = line[2]								#annotation string
				
				if annotation.find('[') != -1 and annotation.find(']') !=-1:
					phrase_type = annotation[annotation.find('[')+1:annotation.find(']')]		#type of the phrase
				else:
					phrase_type = "A0"							# in case the phrase subtype is not annotated take it A0
				
				phrase_class = annotation[0:annotation.find('[')]				#class of the phrase
				
				if len(annotation) >0 and re.match('\s+', annotation) is None:			# constructing a dictionary
					#check if this phrase is adde to the dictionary
					if tg_dict.has_key(phrase_class):
						#checking if the phrase type already exist in the dictinary
						if tg_dict[phrase_class].has_key(phrase_type):
							
							tg_dict[phrase_class][phrase_type].append(tuple(map(float,line[0:2])))
						else:
							tg_dict[phrase_class][phrase_type] = []
							tg_dict[phrase_class][phrase_type].append(tuple(map(float,line[0:2])))
					else:
						
						tg_dict[phrase_class] =  {};
						tg_dict[phrase_class][phrase_type] = []
						tg_dict[phrase_class][phrase_type].append(tuple(map(float,line[0:2])))
						
	
	return tg_dict	

def TextGrid2Dict_NEWFORMAT(textgrid_file):
	
	tg_dict={}
	par_obj = tgp.TextGrid.load(textgrid_file)	#loading the object	
	tiers= tgp.TextGrid._find_tiers(par_obj)	#finding existing tiers
	
	for tier in tiers:
			tier_details = tier.make_simple_transcript();		#this function parse the file nicely and return cool tuples
			
			for line in tier_details:
				if line[2] == '':
					continue
				if tg_dict.has_key(line[2]):
					tg_dict[line[2]].append((line[0], line[1]))
				else:
					tg_dict[line[2]]=[]
					tg_dict[line[2]].append((line[0], line[1]))
	
	return tg_dict	
	
	

def AppendPhraseStats(phrase_dict, Phrase_Stats):
  #this function appends the stats of  the dictionary phrase_dict which contains phrase info about a file obtained using 
  # function TextGrid2Dict. Phrase_Stats is the base dictionary to append the information. This would be handy to handle large number
  # of files to get the stats quickly.
	
	if len(Phrase_Stats.keys()) == 0:
		Phrase_Stats['Phrases'] = {};
		
	
	for phrase in phrase_dict.keys():
		n_phrases =0;
		for ptype in phrase_dict[phrase].keys():
			n_phrases = n_phrases+ len(phrase_dict[phrase][ptype])
			
		#Phrase_Stats['Phrases'][phrase]=n_phrases
		
		if Phrase_Stats['Phrases'].has_key(phrase):
			Phrase_Stats['Phrases'][phrase]=Phrase_Stats['Phrases'][phrase] + n_phrases
		else:
			Phrase_Stats['Phrases'][phrase] = n_phrases	
	
	Phrase_Stats['#DiffPhraseTypes'] = len(phrase_dict.keys());
	return Phrase_Stats
	
	
def ComputeDatabaseStats(root_dir):
  # this function computes the stats of all the phrase find in a root directory
	
	#get all the file list in a given directory of a specific type
	file_names  = BP.GetFileNamesInDir(root_dir, filter=".textgrid")
	Phrase_Stats = {}
	#print "files detected ="+str(len(file_names))
	
	for file_name in file_names:
		
		phrase_dict = TextGrid2Dict(file_name,"Kaustuv_Anotations_Simple")
		Phrase_Stats = AppendPhraseStats(phrase_dict, Phrase_Stats)
		
	
	return Phrase_Stats
	
