import re

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
Ha HaHa
MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )
coreyms.com
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234

cat
mat
bat
hat ght huh
hhj

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''

sentence = 'Start a sentence and then bring it to an end'

pattern = re.compile(r'a')

matches = pattern.finditer(text_to_search)

#for match in matches:
 #   print(match)
    
# Let's find all phone numbers

pattern=re.compile(r'\d{3}[-*]\d{3}[-*]\d{4}')

matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)
    
  
# Let's find all names including their prefixes Mr or Mrs

pattern3=re.compile(r'Mr?s?\.?\s[A-Z][a-z]*')

# solution with grop

pattern3=re.compile(r'M(r|s|rs)\.?\s[A-Z][a-z]*')


matches = pattern3.finditer(text_to_search)

for match in matches:
    print(match)    
   
# Let's find all 3 letter words, except the ones starting in b

pattern2=re.compile(r'\b[^b\s][a-zA-Z]{2}\b')

matches = pattern2.finditer(text_to_search)

#for match in matches:
 #   print(match)     
    
    
# now let's find all phone numbers in a txt file

with open ('re_ex.txt','r') as f:
    myfile=f.read()
    
numbers= pattern.finditer(myfile)  

for match in numbers:
    print(match)

# let's find all email adresses
emails_test = '''
CoreyMSchafer@gmail.com
corey.schafer@university.edu
corey-321-schafer@my-work.net
'''

pattern4= re.compile(r'[a-zA-Z0-9-]+@[a-zA-Z.-]+(com|edu|net)')


emails= pattern4.finditer(emails_test)  

for match in emails:
    print(match)


# let's try to read someone elses re

pattern5 = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
#--> finds
    # words and numbers with underscores, dots, +, and - (at least 1)
    # followed by @
    # followed by words and numvbers (at least one)
    # followed by a .
    # followed by words and numvers, -, . (at leasr one)
    

emails= pattern5.finditer(emails_test)  

for match in emails:
    print(match)

###########
# capturing infos from groups


urls = '''
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
'''


# let's capture all urls

pattern6= re.compile(r'(https|http)://(www.)?(\w+)(.com|.gov)')

url_test= pattern6.finditer(urls)

for match in url_test:
    print(match)
# match object has group object

print(match.group(1))
#https

print(match.group(2))
#www.

print(match.group(3))
#google

print(match.group(4))
#.com

new_urls= pattern6.sub(r'\3\4',urls)

print(new_urls)




################
# different methods:
    
#findall - list of strings - when groups are defined, it returns a tuple
# of the groups    


# match
# returns the first match - only at beginning of string

# Let's now use the groups to substitute
# - we substitute the string which is found with the third or 4th group


# search
# - searches the entire string, prints out the first match

############
# flags in re

# add to e.g. find lower or upper case IGNORECASE


# Let's get a list of the names in the txt file, and put it in lower case
# write new file with lower, case names

with open ('re_ex.txt','r') as f:
    myfile=f.read()

pattern_names=re.compile(r'([A-Z][a-z]+)[ ]([A-Z][a-z]+)\n')

all_names=re.finditer(pattern_names,myfile)

new_names=[]
for i in all_names:
    new_name= i.group(1).lower() + " "+ i.group(2).lower()
    new_names.append(new_name)
   
print(new_names)

# Let's try to do this in a list comprehension
all_names=re.finditer(pattern_names,myfile)

new_names_2=[i.group(1).lower() + " "+ i.group(2).lower() for i in all_names]



print(new_names_2)



# okay cool!

# try to do it with re.sub --> cannot perform string operations
with open ('re_ex.txt','r') as f:
    myfile=f.read()

new_names_3=re.sub(pattern_names,r'\1 ',myfile)

#print(new_names_3)