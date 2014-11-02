# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 07:24:33 2014

@author: fodra
"""
web_page = "http://www.pap.fr/annonce/garage-a-vendre-paris-75-g439-200-annonces-par-page"
#web_page = "http://www.pap.fr/annonce/garage-a-vendre-ile-de-france-g471-200-annonces-par-page"
#web_page = "http://www.pap.fr/annonce/garage-a-vendre-200-annonces-par-page"
web_page = "http://www.pap.fr/annonce/locations-parking-paris-75-g439-200-annonces-par-page"
from urllib import *
import re
import pandas as pd
import gps

r = urlopen(web_page)
bytecode = r.read()
htmlstr = bytecode.decode()

annonce_list = re.compile('<li class="annonce">(.*?)</li>', re.DOTALL | re.IGNORECASE).findall(htmlstr) 

df = []
coordinates = []

def parse(string,tag_type,tag=None,tag_name=None):
    command = "<" + tag_type 
    if not tag == None:
        command += " " + tag + "=\"" + tag_name + "\""
    command += ">(.*?)</" + tag_type + ">"
    return re.compile(command, re.DOTALL | re.IGNORECASE).findall(string) 

class Parser(object):
    def __init__(self,annonce):
        self.annonce = annonce
    def get_price(self):
        ''' return the annonce price
        
        :returns the price of the item in euro
        '''
        price = parse(self.annonce,"span","class","prix")
        assert len(price)==1
        price = price[0].replace("&nbsp;&euro;","")
        try:
            price = float(price)
            return price
        except:
            return np.NaN
    def get_adress_gps_zipcode(self):
        adress = parse(annonce,"strong")
        assert len(adress)==1
        adress = adress[0] 
        #xy =  gps.get_coordinates(adress+ ", France")
        if "," in adress:
            code, zone = adress.split(",")
            zone = zone[0:code.find(" .")]
        else:
            code, zone = adress, ""
        code = code[code.find("(")+1:code.find(")")]
        try: 
            code = int(code)
        except:
            code = np.NaN
        return adress, xy, code
    def get_metro(self):
        return parse(annonce,"div","class","metro")
    def get_date(self):
        date = parse(annonce,"span","class","date")
        return date
    
df = []

for annonce in annonce_list:
    parser = Parser(annonce)
    price = parser.get_price()
    _,_,zipcode = parser.get_adress_gps_zipcode()
    metro = parser.get_metro()
    box = "box" in annonce
    if "digicode" in annonce or "Digicode" in annonce:
        secu = "digicode"
    elif ("bip" in annonce) or ("Bip" in annonce):
        secu = "bip"
    elif "guardien" in annonce:
        secu = "guardien"
    elif "command" in annonce:
        secu = "telecom"
    else:
        secu = None
    if "rez" in annonce:
        etage = "rdc"
    elif "sous-sol" in annonce:
        etage = "sous-sol"
    elif "tage" in annonce:
        etage = "etage"
    else: 
        etage = None
        
    line = [price,zipcode,box,secu,"ascenseur"in annonce,etage]
    df.append(line)
    print line

