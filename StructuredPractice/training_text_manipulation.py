# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 09:33:49 2020

@author: sbenhedia
"""

# Some exercise for my coding interview
  
#################################################    
#2. String operations

# Let's practice with a txt

myfile= open('Blurb and bio.txt','r', encoding='cp1252')

#lines=myfile.readlines()
#
#for line in lines:
#    print(line)
#    print(line.split(" ")[0])
##    
#    if 'Bio' in line:
#        print('Bio')
##        
#    print(line.strip('\n'))
##    
#    if line.startswith('Sonia'):
#        print(line)
#    
#    print(line.split(" ")[0].capitalize())
#    print(line.split(" ")[0].upper())
#    print(line.split(" ")[0].lower())
#    print(line.split(" ")[0].title())
#    print(line.split(" ")[0].replace("a","o"))
#    


################
# Sample tasks:

    
# 1. Turn time into an articulated version - approxmation

import re

# 09.53 - 10.08 --> ten o'clock
# 10.09 - 10.22 --> ten fiften
# 10.23 - 10.37 --> ten thirty
# 10.38 - 10.52 --> ten fortyfive

#  1. a dictionary for the hours 
string= "It is 9:30 and I am tired. 10:46 At 10:11 I should got to bed, but today I will go to bed at 3:00, maybe at 11:23, 6:54, 9:22, 2:03."

#   1st: each number for the hours

hours={'1:':'one', '2:': 'two','3:':'three','4:':'four', '5:':'five','6:':'six','7:':'seven',
       '8:':'eight','9:':'nine','10:':'ten','11:':'eleven','12:':'twelve'}

# create regular expressions for the hours (one), and for 

hours_pattern= re.compile(r'(\d{1,2}):')

# the four minute patterns
full_hour_pattern= re.compile(r':(5[^012]|0[^9])')
fifteen_pattern= re.compile(r':(0\d|1\d|2[12])')
half_pattern= re.compile(r':(2[^12]|3[^89])')
fortyfive_pattern= re.compile(r':(3[89]|4\d|5[12])')

# let's check
print(re.findall(full_hour_pattern,string))
print(re.findall(half_pattern,string))
print(re.findall(fifteen_pattern,string))
print(re.findall(fortyfive_pattern,string))
print(re.findall(hours_pattern,string))

# I will do this in two steps:

    # 1. I will substitute the minutes
new_string= re.sub(full_hour_pattern, ": o'clock", string)
new_string_2= re.sub(half_pattern, ": thirty", new_string)
new_string_3= re.sub(fifteen_pattern, ": fifteen", new_string_2)
new_string_4= re.sub(fortyfive_pattern, ": fortyfive", new_string_3)

# now let's substitute the hours


for word in new_string_4.split( " "):
    if word in hours:
        new_string_4= re.sub(word,hours[word], new_string_4) 
        
        
# 2. Connect to an API, get a JSON file and get all keys

import requests
#import json

url='http://www.omdbapi.com/?t=Shrek&apikey=9e122bbb'

r= requests.get(url)

json_file=r.json()

#for key,value in json_file.items():
 #   print(value)

# get all keys that have 5 characters
for key,value in json_file.items():
    if len(key)==5:
        print(key)



# 3. Find all capitalized words


test_str= "Hallo, mein Name ist Sonia und ich bin müde und möchte gerne schlafen gehen, aber ein bißchen muss ich noch üben."

# make word list

words= re.findall(r'[\w]+',test_str)
# write a RE

cap_words= re.compile(r'\b[A-Z][a-z]+')

all_cap_list= re.findall(cap_words,test_str)

# now, let's make them small

new_str= test_str
for word in test_str.split(" "):
    if re.match(cap_words, word):
        new_str= new_str.replace(word, word.lower())

# other solution
test_str_n=test_str
for word in words:
    if word.capitalize()== word:
        print(word)
        test_str_n= test_str_n.replace(word, word.lower())
        

# 4. Find all uppercase words and convert them into lower case

# let's do it in a list

word_list=["alo","DJ","jkjk","Hjj","hih"]

cap_list=[element.capitalize() for element in word_list]

print(cap_list)

# let's do it only, when the word starts with an h

cap_list_h=[element.capitalize() for element in word_list if element.lower().startswith("h")]
 
print(cap_list_h)

#5) connect to an API, open a JSON file, get all values with a date
    
import requests
import re
#1 connect and get data

url='http://www.omdbapi.com/?t=Home&Alone&apikey=9e122bbb'

r=requests.get(url)

json_data=r.json()

# 2 write re for date format

date_pattern=re.compile(r'\d{2}\s[\w]{3}\s\d{4}')
print(re.search(date_pattern, "huhuihh 12 May 1111"))

for key,value in json_data.items():
    if str(value)==value:    
        if (re.search(date_pattern,value)):
            print(value)
            
            
#6) get the text data from the following website and print out all words
    # which are capitalized
    
import requests
from bs4 import BeautifulSoup

url="https://de.wikipedia.org/wiki/Hausschuh"

r= requests.get(url)

html_text=(r.text)

soup=BeautifulSoup(html_text, 'html.parser')

#print(soup.prettify())

#print(soup("script"))
#print(soup("style"))

for element in soup(["script","style"]):
    element.extract()
    
plain_text=soup.get_text()    


lines=(line.strip() for line in plain_text.splitlines())



text= '\n '.join(line for line in lines if line)
        
# okay now we can check for capitalized words.

# first, let's make a list of words usinf re

word_list_wiki=re.findall(r'[\w]+', text)

#for word in word_list_wiki:
 #   if word.capitalize()== word:
  #      print(word)

text_new= text        
# now let's try to substitute these words in the text

for word in word_list_wiki:
    if word.capitalize()== word:
        new_word=word.lower()
        text_new=re.sub(word,new_word,text_new)

with open ('new_wiki.txt','w',encoding='utf-8') as p:
    p.write(text_new)
    
# yes, it worked!



#3. Write a Python program to get a string made of the first 2 and the last 2 chars from a given a string. 
#If the string length is less than 2, return instead of the empty string.


def two_string(string):
    '''str--> str'''
    if len(string)>=2:
        print(string[0:2]+ string[-2:])
        
        
# to get really good at the html stuff

import requests
from bs4 import BeautifulSoup

url='https://www.quora.com/What-website-was-developed-with-XML'

html_code=requests.get(url)

html_text=html_code.text

soup=BeautifulSoup(html_text, "lxml")

for element in soup(["script","style"]):
    element.extract()

new_html_text=soup.get_text()

    
lines= [line.strip(" ") for line in new_html_text.splitlines()]

best_text= "\n".join(line for line in lines if line)
    
print(best_text)     


########
# read texr

with open ("new_wiki.txt","r",encoding='utf8') as pan:
    pan_text=pan.readlines()

print (pan_text[0])

#write a txt
a_list=["m","n","n","k"]
with open('ghg.txt','w',encoding='utf') as b:
   # b.write("bjgjg")
    b.writelines(['1','1','4'])
    for element in a_list:
        b.write("%s\n jjjjjj" %element)