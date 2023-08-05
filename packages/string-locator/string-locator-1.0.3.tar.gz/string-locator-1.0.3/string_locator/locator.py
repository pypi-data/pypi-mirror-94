# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:50:49 2021

@author: Srirag
"""
import os

def locate(text,path):
    total_file,file_name=[],[]
    
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            total_file.append(os.path.join(root,name))
    
    for filename in total_file:
        try:
            with open(filename) as f:
                      if text.lower() in f.read().lower():
                          file_name.append(filename)
        except: pass
    
    return file_name


