# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 09:33:49 2020

@author: sbenhedia
"""

# Some exercise for my coding interview

#1. Reading  & writing in dihfferent types of data

######################
# a) txt- files
######################

### Reading
myfile= open('Blurb and bio.txt','r', encoding='cp1252')

# whole text is one string, Zeilenumbruch =\n
myfile.read()

# one line
myfile.readline()

# all lines, text is list of lines
myfile.readlines()

# access to each line
for line in myfile:
    print (line)

myfile.close()

# OR

with open ('Blurb and bio.txt','r') as f:
    myfile= f.read()
    
## Writing

myfile=open('new_text.txt',"w", encoding='utf8')

myfile.write('hello')
myfile.writelines(['0\n','1\n','2\n'])

for index in range(7):
   myfile.writelines([str(index),'\n'])
   myfile.write(str(index))        
   myfile.write("%s what a pretty format" %index)

myfile.close()

#####################
# b) csv- files
####################

#reading

import pandas as pd
import csv as csv
mycsv=pd.read_csv("Intel.csv", sep=";", index_col=False, na_values="Na")

print(mycsv.head())  

#writing

# let's create a df

a=[0,1,2,2,2,5]
b=['a','b','c','d','f','a']
c=['a','b','c','d','f','a']

d= list(zip(a,b,c))
header= ['Eins','Zwei','Drei']
df=pd.DataFrame(d, columns=header)


print(df.head())

# get column  
print('1:\n',df['Eins'])
print('2:\n',df.loc[:,'Eins'])
print('3:\n',df.iloc[:,0])
# this is a df [[]]
print('4:\n',df[['Eins']], type(df[['Eins']]))



# get rows
# first row  
print(df[0:1])
# firt 2 rows
print(df[0:2])
# first 5 rows
print(df[0:5])
# rows 3-5
print(df[2:5])

# get row and colums
#df.loc[[index],[column labels]]
#df.iloc[[row number],[column number]]

#first row first two colums
print(df.loc[[0],['Eins','Zwei']])
print(df.iloc[[0],[0,1]])

# let's save our df

df.to_csv('new_csv.csv',sep=',')
    
# writing a csv line by line

with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

#####################################
# c) excel- files
#####################################

# use the pandas package

file='Daten Íntelligibility.xlsx'
excel_data= pd.ExcelFile(file)

# acess different sheets
print(excel_data.sheet_names)
#['Tabelle1', 'Tabelle2']    

Tabelle_1=excel_data.parse('Tabelle1')

Short_Tabelle1=Tabelle_1.head(n=10)

# write new excel with 1 sheet
Short_Tabelle1.to_excel("new_excel.xlsx")

# write new excel with several sheet
with pd.ExcelWriter('new_big_excel.xlsx') as writer:  
    Short_Tabelle1.to_excel(writer, sheet_name='Sheet_name_1')
    Short_Tabelle1.to_excel(writer, sheet_name='Sheet_name_2')


###############################    
# d) pickled data
#######################################

# pickled files have a more complex, i.e. non-flat structure
# they are python specific

# we define a class which and an object in the class (just for the sake
# of having something to save)
class Fruits: pass

banana = Fruits()

banana.color = 'yellow'
banana.value = 30

# this is the package needed
import pickle

# writing a pickled file
filehandler = open("Fruits.pkl","wb")
pickle.dump(banana,filehandler)
filehandler.close()

# opening a pickled file
file = open("Fruits.pkl",'rb')
object_file = pickle.load(file)
file.close()

print(object_file.color, object_file.value, sep=', ')
    
#or

with open ('Fruits.pkl', 'rb') as file:
    pic_data=pickle.load(file)
print(pic_data)
print(pic_data.color)   

# okay, cool! Works

######################## 
# e) SQL- database
#################################
    
# use pandas as pd and sqlalchemy
from sqlalchemy import create_engine

engine= create_engine('sqlite:///database.sqlite')
print(engine.table_names())

sql_df= pd.read_sql_query("SELECT*FROM 'Player'", engine)
print(sql_df.head())

# let's just save that as a csv

sql_df.to_csv("new_soccer.csv", sep=",")


#######################################
# f) HTML
#########################################

# we use the request package

import requests
# we need beautiful soup to make html more accesible
from bs4 import BeautifulSoup

#+specify url

url='https://en.wikipedia.org/wiki/Giant_panda'

# submit request
r =requests.get(url)

html_text=r.text

# Some basics for html:
    # 3 main type of elements: void (stand alone, raw text, )
    # raw text elements have start tags <> and end tags <\>
    # some element have attribues with values (inside tags) which
        # define element further
    # document structure: html (beginning/ende),head (meta data), body (main part)
    # some elemenet have children (hierarchical structucre)
    # BeautifulSoup makes use of the element structure and tags
    # to find certain elements in the text
    
soup = BeautifulSoup(html_text, 'html.parser')

#print(soup.prettify())

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())


    
# break multi-headlines into a line each --> not quite sure what this means
#chunks = (phrase.strip() for line in lines for phrase in line.split("  "))


# drop blank lines

text = '\n'.join(element for element in lines if element)

print(text, type(text))


# store data as text
pandas=open("pandas.txt","w", encoding='utf8')

pandas.write(text)

pandas.close()

##################################
# g) API & JSON
############################################
# API = code for communicating between programs

# We need to connect to an API and pull the data as JSON
# import request --> we have already done so

import json

url="http://www.omdbapi.com/?t=Harry+Potter&apikey=9e122bbb"

r= requests.get(url)

json_data2=r.json()


for key, value in json_data2.items():
    print(key,": ", value)

print(json_data2.keys())
print(json_data2['Website'])
print(json_data2['Rated'])


with open('example_2.json') as json_file:
    json_data=json.load(json_file)

for key,value in json_data.items():
    print(key,":",value)
    
# nested dictionary--> we can access different levels    
print(json_data["quiz"]['maths']['q2']['options'][2])  

###
# writing a JSON

#let's create a dict

small_dict={'animals':{'birds':["eagle","swan"],'fish':['clownfish','cod','salmon']},
                       'plants':['fern','mint','tulip']}
 
print(small_dict.keys())

print(small_dict['animals']['birds'])

# let's save it as a json

with open("sample.json", "w") as outfile: 
    json.dump(small_dict, outfile) 

# nice it worked!

# Now we read and wrote the HOPEFULLY most common file types in python

