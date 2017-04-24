# Written by Matt Shilling with code from Adele Gilpin 
# For CS162 Students
#
# Requirements: Python 3, BeautifulSoup 4
#

from bs4 import BeautifulSoup
import urllib

# delim = character(s) seperating book entries
# change to whatever you want 
delim = " | "

# list options
print("1.) List of books banned by governments")
print("2.) List of books about food and drink")
print("3.) List of books written by CEOs")
l = int(input("Pick a list: "))

# choose datafile
fname = str(input("Enter datafile: "))

# show user the format the file will be in
print("Format: TITLE YEAR GENRE AUTHOR")

# list is selected
if l == 1:
    sub = "List_of_books_banned_by_governments"
elif l == 2:
    sub = "List_of_books_about_food_and_drink"
elif l == 3:
    sub = "List_of_books_written_by_CEOs"
else:
    print("Choose a valid option, please. Run program again.")
    quit()
    
# Thanks Adele Gilpin!
wiki = "https://en.wikipedia.org/wiki/"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib.request.Request(wiki+sub,headers=header)
page = urllib.request.urlopen(req)
soup = BeautifulSoup(page, "html5lib")

# find the tables in the html
tables = soup.find_all("table", { "class" : "wikitable sortable" })

# if you decide to implement your own list, this might help if
# there is more than one table in the wiki page
if tables == []:
    tables = soup.find_all("table", { "class" : "wikitable" })

# List_of_books_banned_by_governments
def create_list_banned(cells,f):
    if len(cells) == 5:
        
        title = cells[0].find(text=True)
        auth_list = cells[1].findAll(text=True)
        pub_year = cells[2].find(text=True)
        genre = cells[3].find(text=True)

        # there is sometimes a list of mult. authors
        author = ""
        for x in auth_list:
            author += x

        #author = author.replace(" and ",delim)
        #author = author.replace(" & ",delim)
        author = author.replace('"',"")
            
        line = '{1}{0}{2}{0}{3}{0}{4}\n'.format(delim, title, pub_year, genre, author)
        f.write(line)

#List_of_books_about_food_and_drink
def create_list_food(cells,f):
    if len(cells) == 3:
        title = cells[0].find(text=True)
        auth_list = cells[1].findAll(text=True)
        pub_year = cells[2].find(text=True)
        genre = "Food"

        # there is sometimes a list of mult. authors
        author = ""
        for x in auth_list:
            author += x
        
        #author = author.replace(" and ",delim)
        #author = author.replace(" & ",delim)
        author = author.replace('"',"")
        
        line = '{1}{0}{2}{0}{3}{0}{4}\n'.format(delim, title, pub_year, genre, author)
        f.write(line)

#List_of_books_written_by_CEOs
def create_list_business(cells,f):
    if len(cells) == 4:
        title = cells[0].find(text=True)
        auth_list = cells[1].findAll(text=True)
        pub_year = cells[3].find(text=True)
        genre = "Business"

        # there is sometimes a list of mult. authors
        author = ""
        for x in auth_list:
            author += x
            
        #author = author.replace(" and ",delim)
        #author = author.replace(" & ",delim)
        author = author.replace('"',"")
            
        line = '{1}{0}{2}{0}{3}{0}{4}\n'.format(delim, title, pub_year, genre, author)
        f.write(line)


# open file with append mode, utf-8 encoding
f = open(fname, 'a', encoding="utf8")


# loop through the tables to find all data elements
for table in tables:
    
    #For each "tr", assign each "td" to a variable.
    for row in table.findAll("tr"):
        
        cells = row.findAll("td")

        # make datafile per user selection
        if l == 1:
            create_list_banned(cells,f)
        if l == 2:
            create_list_food(cells,f)
        if l == 3:
            create_list_business(cells,f)
    
#close file
f.close()

print("List written to {0}".format(fname))
