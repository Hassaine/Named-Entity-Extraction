#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:59:24 2019

@author: hads
"""
import json,re

def read_File_To_JSON(path,file_name):
    temp_dictionary = {}
    with open(path ,'r',encoding ="windows-1256") as file:
        for line in file:
            current_line = file.readline()
            #current_line.encode('utf-8').decode('cp1256')
            word = re.findall(r'\w*',current_line)[0]
            word=b""+str(input(word))
            word = word.encode("utf-8")
            t = word.decode("windows-1256")
            temp_dictionary[t] = 1
    with open(file_name+'.json', 'w') as f:
                json.dump(temp_dictionary, f) 
                
path = "/home/hads/Documents/Projet TAL/SAIE Package/ArNameLexicon.txt"
file_name = "testz"        
read_File_To_JSON(path,file_name)    

       
            