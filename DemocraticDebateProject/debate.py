# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:31:36 2020

@author: sbenhedia
"""

# In this script, I am loading a html text from the internet, i.e. the transcript 
# from the last democratic debate, then I will get the most frequently words
# used by each candidate and put in into a neat graph

########
# I will need the following packages
#
#
#
#
import re
import numpy as np
import requests
from bs4 import BeautifulSoup
#import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import random
from PIL import Image
from wordcloud import WordCloud, STOPWORDS


##########
# Step 1
# LOADING THE DATA
##########

url="https://www.nbcnews.com/politics/2020-election/full-transcript-ninth-democratic-debate-las-vegas-n1139546"

r=requests.get(url)
html_doc=r.text
soup=BeautifulSoup(html_doc)

##########
# Step 2
# Creating a dictionary in with the speakers as keys,
# and a list of words they said as values
##########

# empty dictionary

debate_dict_all={}


for i in soup.find_all('p'):
    lit=[i.text]
    lit1=list(lit[0].split(" "))
    
    try:
        if re.match(r'^[^a-z().\d]*$',lit1[0]) and re.match(r'^[A-Z]+',lit1[0]) and lit1[0]!= "I":
            key=lit1[0].strip(":")
            value=lit1[1:]
            if key in debate_dict_all.keys():
                debate_dict_all[key]= debate_dict_all[key]+value
            else:
                debate_dict_all.update( {key: value} )
        else:
            value=lit1
            debate_dict_all[key]= debate_dict_all[key]+value
            
            
    except:
        pass

print(debate_dict_all.keys())
#dict_keys(['HOLT', 'SANDERS', 'WARREN', 'BLOOMBERG', 'BUTTIGIEG', 
#'KLOBUCHAR', 'BIDEN', 'JACKSON', 'TODD', 'HAUC', 'RALSTON', 'PROTESTORS'])

# Let us delete the ones which are not candidates from the dictionary
del debate_dict_all['HOLT']
del debate_dict_all['JACKSON']
del debate_dict_all['TODD']
del debate_dict_all['HAUC']
del debate_dict_all['RALSTON']
del debate_dict_all['PROTESTORS']

# cool, now we have a dictionary with every speaker and each word they said

# Let's also write a function, which gives out a dictionary with each
# speaker as the key, and all the content words he says as values

stopwords = set(STOPWORDS)
stopwords.add("well")
stopwords.add("going")
stopwords.add("one")
stopwords.add("said")
stopwords.add("applause")
stopwords.add("say")
stopwords.add("it")
stopwords.add("able")
stopwords.add("is")


def content_words_dict(speaker_word_dict):
    ''' content_words_dictcreate_freq_dictionary(dict)=dict
    This function returns a dictionary content_words from a dictionary
    in which they keys are the speakers and a list of words including content
    words are the value. It basically deletes all function words from the list.
    It also checks for certain compounds, i.e. health care, health insurance, health record, donald trump
    >>> content_words_dict(original")
    content_words'''
    content_dict={}
    for key in speaker_word_dict:
        value_list=[]
        i=0
        for value in speaker_word_dict[key]:
            
            
            value= value.strip(',.;?!-_()" "').lower()
            if value not in stopwords:

                if value == 'health':
                    if speaker_word_dict[key][i+1].strip(',.;?!-_()').lower()=='care':
                        value = (value + speaker_word_dict[key][i+1].strip(',.;?!-_()').lower())
                    elif speaker_word_dict[key][i+1].strip(',.;?!-_()').lower()=='insurance':
                        value = (value + speaker_word_dict[key][i+1].strip(',.;?!-_()').lower())
                    elif speaker_word_dict[key][i+1].strip(',.;?!-_()').lower()=='record':
                        value = (value + speaker_word_dict[key][i+1].strip(',.;?!-_()').lower())
                    
                    value_list.append(value)
                    
                if value == 'care' or value == 'insurance' or value == 'record' :
                        if speaker_word_dict[key][i-1].strip(',.;?!-_()').lower()=='health':
                            pass
                        else:
                            value_list.append(value)
                            
                if value == 'donald':
                    if speaker_word_dict[key][i+1].strip(',.;?!-_()').lower()=='trump':
                        value = (value +" "+ speaker_word_dict[key][i+1].strip(',.;?!-_()').lower())
                    value_list.append(value)
                    
                if value == 'trump':
                        if speaker_word_dict[key][i-1].strip(',.;?!-_()').lower()=='donald':
                            pass
                        else:
                            value_list.append(value)                            
                else:
                    
                    value_list.append(value)
            i=i+1
        content_dict[key]=value_list
    return content_dict
                

debate_dict_content =content_words_dict(debate_dict_all)     

##########
# Steo 3
#Analyzing who said the most
##########
speak_freq_all=[]
speak_freq_content=[]

for key in debate_dict_all:
    print(key," said ",len(debate_dict_all[key])," words", len(debate_dict_content[key]), " of which were content words.!")
    speak_freq_all.append(len(debate_dict_all[key]))
    speak_freq_content.append(len(debate_dict_content[key]))


# Let's plot this
w = 10
h = 5
d = 70
plt.figure(figsize=(w, h), dpi=d)

N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1=plt.barh(ind, speak_freq_all, width, color=['royalblue','red','darkorange','lightseagreen','limegreen','indigo'])
p2=plt.barh(ind, speak_freq_content, width,
             left=speak_freq_all,color=['dodgerblue','tomato','orange',  'turquoise','lightgreen', 'mediumpurple'])

plt.yticks(ind,debate_dict_all.keys())
#plt.legend((p1[0], p2[0]), ('Content', 'Overall'),loc="lower left")
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
legend_x = 1
legend_x_2 = 2

legend_y = 0.5
legend_elements = [Patch(facecolor='royalblue', label='content words'),
                   Patch(facecolor='red', label='content words'),
                   Patch(facecolor='darkorange', label='content words'),
                   Patch(facecolor='lightseagreen', label='content words'),
                   Patch(facecolor='limegreen'),
                   Patch(facecolor='indigo'),
                   Patch(facecolor='dodgerblue', label='content words'),
                   Patch(facecolor='tomato', label='content words'),
                   Patch(facecolor='orange', label='content words'),
                   Patch(facecolor='turquoise', label='all words'),
                   Patch(facecolor='lightgreen', label='all words'),
                   Patch(facecolor='mediumpurple', label='all words')]

#plt.legend(handles=legend_elements,loc='center left', bbox_to_anchor=(legend_x, legend_y))

ax.set_title("Words spoken", fontdict={'fontsize': 14,'fontweight':"bold"}, y=1.1)
plt.savefig("plot.png")

plt.show()



#############
# Pie legends


fig, (ax1, ax2) = plt.subplots(2, 1, subplot_kw={'aspect':'equal'})

ax1.set_title("Legend", fontdict={'fontsize': 14,'fontweight':"bold"})
sizes = [1, 1, 1, 1,1,1]
colors=['dodgerblue','tomato','orange',  'turquoise','lightgreen', 'mediumpurple']
colors2= ['royalblue','red','darkorange','lightseagreen','limegreen','indigo']

legend_elements_c=[Patch(facecolor='black',linestyle=":",label='all words')]
legend_x_2=1

ax1.pie(sizes,colors=colors, shadow=True, startangle=140)
ax1.text(1.5,0,"content words")

ax2.pie(sizes,colors=colors2, shadow=True, startangle=140)
ax2.text(1.5,0,"all words")

plt.savefig("labels.png")

plt.show()


#############
# Proportion graph: Who spoke the most?


fig, ax = plt.subplots(figsize=(6, 3.5), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)


data = speak_freq_all
speakers = list(debate_dict_all.keys())
pattern= ['royalblue','red','darkorange','lightseagreen','limegreen','indigo']

wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color='w'),colors=pattern)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
       bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(speakers[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Who said the most?", fontdict={'fontsize': 14,'fontweight':"bold"}, y=1.2)


plt.savefig("propotions_pie.png")

plt.show()

#that is a good start but now let's go on



##########
# Step 4
#Analyzing what was said the most by whom
##########

# we need to build dictionaries



# writing a function to create a dictionary of types and frequencies

def create_freq_dictionary(list_of_words):
    ''' create_freq_dictionary(list)=dict
    This function returns a dictionary from a list of words. In this dictionary
    each word is a key, and its frequency is the value.
    
    >>> create_freq_dictionary("original")
    lex'''

    
    #creating empty dictionary and list, as well as counters
    lex = dict()
    words = []
    i = 0
    j = 0
    
    #iterating through the list of lines (usually generated by
    # the .readlines() function)
    
    for word in list_of_words:
            
        #clean up lines by stripping line breaks and punctuation
            word = word.strip("\n")
            word = word.strip("\".?!,;()/#'")
            
        # deleting numbers and digits from the lines
            word=re.sub(r'\d+',"",word)
            
        #converting everything in lower case (if not the case already)
            word = word.lower()
            
        
            #adding new tokens to exsiting list of words
            words.append(word)

    # creating the dictionary with words as keys and frequencies as values by

    # using a counter to iterate through each of the elements in the word list    
    while (i < len(words)):
        
            #accesing the element in the word list using the counter
            wort = words[i]
            # setting another counter to 0 for each element in the word list
            j = 0
            
            # iterating through the word list
            for elem in words:
                # comparing if it is the same same element/type as the one
                # accessed in line 132
                if elem == wort:
                    # if so, adding 1 to the counter j
                    j = j + 1
                else:
                    continue
            # creating a dictionary entry with the element, i.e. the word
            #type as a key and the frequency as the value
            lex[wort] = j
            # adding one to the counter i to access the next entity in the word
            #list
            i = i + 1
            
    # return the dictionary        
    return(lex)

Sanders=create_freq_dictionary(debate_dict_content['SANDERS'])
Klobuchar=create_freq_dictionary(debate_dict_content['KLOBUCHAR'])
Warren=create_freq_dictionary(debate_dict_content['WARREN'])
Bloomberg=create_freq_dictionary(debate_dict_content['BLOOMBERG'])
Buttigieg=create_freq_dictionary(debate_dict_content['BUTTIGIEG'])
Biden=create_freq_dictionary(debate_dict_content['BIDEN'])


list_all_tokens=[]

for key in debate_dict_content.keys():
    for element in debate_dict_content[key]:
        list_all_tokens.append(element)

# create dict for everything
All_freqs=create_freq_dictionary(list_all_tokens)




# get a dictionary which has the frequencies as its keys
lex2={}
for elem in All_freqs:
            key = All_freqs[elem]
            value = elem
    
            if key in lex2:
                lex2[key] = lex2[key] + elem
            else:
                lex2[key] = value
                


def freq_words(m,dictio):
    '''freq_words(int,int,str)=str
    m= number of most frequent words you want to get
    dictio= dictionary you want to get the frequencies from

    This program counts the frequency of words in a text t is return the m words with the most
    frequency

    >>> fre(1,"my_d")
    Most frequent: 
    Least frequent:

    ''' 

    list_keys =[]
    for element in dictio.keys():
        list_keys.append(element)
    i=0

    #most frequent
    list_keys.sort()
    list_keys = list_keys[::-1]
    while(i<m):
        print(dictio[list_keys[i]],"is the ", str(i+1), "most frequent word.",list_keys[i])
        i=i+1

freq_words(11,lex2)

### Let's put this into a nice plot

file1 = open("myfile.txt","w")#write mode 

file1.write("People is mentioned 107 times.\n")
file1.write("think is mentioned 65 times.\n")
file1.write("Donald Trump is mentioned 58 times.\n")
file1.write("President is mentioned 52 times\n")
file1.write("Health Care and way is mentioned 48 times.\n")
file1.write("want is mentioned 45 times.\n")
file1.write("right is mentioned 44 times.\n")
file1.write("country is mentioned 42 times.\n")
file1.write("need is mentioned 41 times.\n")
file1.write("care and will is mentioned 40 times.\n")

file1.close() 


# Let's plot the type-token ratio for each person

types=[]
tokens= speak_freq_content
tt_ratio=[]
full=[1,1,1,1,1,1]

# to get the types we just need to get the number of keys of the dictionarys
all_dict= Sanders,Warren,Bloomberg,Buttigieg,Klobuchar,Warren
for entry in all_dict:
    types.append(len(entry.keys()))



# getting the type token frequency:
i=0
for token in tokens:
    tt_ratio.append(types[i]/token)
    i=i+1
    


w = 10
h = 5
d = 70
plt.figure(figsize=(w, h), dpi=d)

N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.8       # the width of the bars: can also be len(x) sequence



p1=plt.bar(ind, tt_ratio, width, color=['royalblue','red','darkorange','lightseagreen','limegreen','indigo'], tick_label="type")
#p2=plt.bar(ind, full, width,bottom=tt_ratio, color=['dodgerblue','tomato','orange','turquoise','lightgreen','mediumpurple'])




plt.xticks(ind,debate_dict_all.keys(), rotation=20)
#plt.legend((p1[0], p2[0]), ('Content', 'Overall'),loc="lower left")
ax = plt.subplot(111)
ax.set_ylim(0,1)
ax.text(0.4,0.7, "Repetitions?", size=55, color='grey',alpha=0.4)
#ax.text(1.5,0.7, "tokens", size=55, color='grey',alpha=0.4)

ax.set_title("Type-token ratio aka repetition measure", fontdict={'fontsize': 14,'fontweight':"bold"}, y=1.1)
plt.savefig("TT-ratio.png")
plt.show()


# Word clouds

# Let us write a function which returns a word map for a certain
# dictionary, with a certain picture, in a certain color


def blue_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(236, 90%%, %d%%)" % random.randint(50, 100)


def red_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(7, 82%%, %d%%)" % random.randint(35, 58)

def purple_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(266, 84%%, %d%%)" % random.randint(39, 70)

def green_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(147, 45%%, %d%%)" % random.randint(46, 68)

def orange_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(40, 85%%, %d%%)" % random.randint(52, 71)

def teal_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(186, 58%%, %d%%)" % random.randint(31, 63)




def save_create_map(dictionary,image, color,name ):


    # read the mask image which is in the directory
    mask_pic = np.array(Image.open(image))

    wc = WordCloud(background_color="white", max_words=2000, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='darkblue')

    # generate word cloud
    wc.generate_from_frequencies(dictionary)


    plt.title(name, fontsize=25, loc='center')
    
    if color is 'blue':
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='darkblue')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        plt.imshow(wc.recolor(color_func=blue_color_func, random_state=3),
           interpolation="bilinear")
        
    if color is 'teal':
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='teal')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        
        plt.imshow(wc.recolor(color_func=teal_color_func, random_state=3),
           interpolation="bilinear")


    if color is 'red':
        
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='darkred')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        plt.imshow(wc.recolor(color_func=red_color_func, random_state=3),
           interpolation="bilinear")
        
    if color is 'orange':
        
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='orange')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        plt.imshow(wc.recolor(color_func=orange_color_func, random_state=3),
           interpolation="bilinear")        



    if color is 'green':
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='darkgreen')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        plt.imshow(wc.recolor(color_func=green_color_func, random_state=3),
           interpolation="bilinear")

    if color is 'purple':
        wc = WordCloud(background_color="white", max_words=120, mask=mask_pic,
               stopwords=stopwords, contour_width=3, contour_color='purple')
        
        wc.generate_from_frequencies(dictionary)
        plt.title(name, fontsize=25, loc='center')

        plt.imshow(wc.recolor(color_func=purple_color_func, random_state=3),
           interpolation="bilinear")




    # store to file
    wc.to_file("figures\\"+ name+ ".png")

    # show
    #plt.axis("off")
    #plt.figure()
    #plt.imshow(mask_pic, cmap=plt.cm.gray, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()


save_create_map(Sanders,'donkey.jpg','blue','Bernie Sanders')
save_create_map(Biden,'donkey2.jpg','purple','Joe Biden')
save_create_map(Buttigieg,'donkey2.jpg','teal','Pete Buttigieg')
save_create_map(Bloomberg,'donkey.jpg','orange','Mike Bloomberg')
save_create_map(Warren,'donkey.jpg','red','Elizabeth Warren')
save_create_map(Klobuchar,'donkey2.jpg','green','Amy Klobuchar')
