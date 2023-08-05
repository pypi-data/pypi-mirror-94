"""check egrep.py for information on stdin/stdout"""

#"r" reads in
file_for_reading = open("GettingDataFiles/reading_file.txt", "r")
file_for_reading2 = open("GettingDataFiles/reading_file.txt")

#"w" writes -> destroys any current file with given name
file_for_writing = open("GettingDataFiles/writing_file.txt", "w")

#'a' is append -> adds to the end of the file
file_for_appending = open("GettingDataFiles/appending_file.txt", 'a')

#close files once done
file_for_writing.close()

#always use with a with statement, to make sure you don't forget to close it :
"""
with open(filename) as f : 
    data = function(f)
"""

#another example below
import re
starts_with_hash = 0
with open("GettingDataFiles/hashes_file.txt") as f :
    for line in f : #iterate through each line
        if re.match("^#", line) : #contains a hash ?
            starts_with_hash += 1

print("Starts_with_hash : ", starts_with_hash)

#getting the domain of an email adress
def get_domain(email_adress : str) -> str :
    '''split on @ and return last piece'''
    return email_adress.lower().split("@")[-1]

#test it out
assert get_domain("anish.lakkapragada@gmail.com") == "gmail.com"
assert get_domain("anish.lakkapragada@stanford.edu") == "stanford.edu"

from collections import Counter

with open("GettingDataFiles/email_addresses.txt") as f :
    domain_counts = Counter(get_domain(line.strip()) for line in f if "@" in line)


print(domain_counts)

"""
A word on CSV files : 
import csv
with open("delimited_symbol_stock_prices.txt") as f : 
    tab_reader = csv.reader(f, delimiter = "\t")
    for row in tab_reader : 
        data = row[0]
        symbol = row[1]
        closing_price = float(row[2])
        process(date, symbol, closing_price)

To process this kind of dataset : 
date:ticker:closing_price
6/20/2014:AAPL:90.91
6/20/2014:MSFT:41.68
6/20/2014:FB:64.5

with open('colon_delimited_stock_prices.txt') as f : 
    colon_reader = csv.DictReader(f, delimiter = ":")
    for dict_row in colon_reader : 
        date = dict_row["row"]
        ticker = dict_row["ticker"]
        cp = dict_row["closing_price"]
        #data function 
        
WRITING CSV FILES 

todays_prices = {'AAPL' : 90.91, 'MSFT' : 41.68, 'FB' : 64.5}
with open("comma_delimited_stock_prices", 'w') as f : 
    csv_writer = csv.writer(f, delimiter = ",")
    for stock, price in todays_prices.items() : 
        csv_writer.writerow([stock, price])
"""

#scraping the web!!!

from bs4 import BeautifulSoup
import requests

url = "https://raw.githubusercontent.com/joelgrus/data/master/getting-data.html"

html = requests.get(url).text
soup = BeautifulSoup(html, "html5lib")

#finding the first paragraph with <p> tag
first_paragraph = soup.find("p")

first_paragraph_text = soup.p.text
first_paragraph_words = soup.p.text.split()

#extract a tag's attributes
first_paragraph_id = soup.p["id"]
first_paragraph_id2 = soup.p.get("id") #returns None if no id

all_paragraphs = soup.find_all("p")
paragraphs_with_ids = [p for p in soup("p") if p.get('id')]

important_paragraphs = soup("p", {"class" : "important"})
important_paragraphs2 = soup('p', 'important')
important_paragraphs3 = [p for p in soup('p')
                         if 'important' in p.get('class', [])]

spans_inside_divs = [span
                     for div in soup('div')
                     for span in div('span')] #for each <div> on the page


url = "https://www.house.gov/representatives"
text = requests.get(url).text
soup = BeautifulSoup(text, "html5lib")

all_urls = [a["href"]
            for a in soup('a')
            if a.has_attr('href')]

print("Length URLS : ", len(all_urls))

import re
regex = r"^https?://.*\.house\.gov/?$" #must start with "http://" or "https://" and end in "house.gov" or ".house.gov/"

assert re.match(regex, "http://joel.house.gov")
assert re.match(regex, "https://anish.house.gov")
assert re.match(regex, "http://joel.house.gov/")
assert re.match(regex, "https://anish.house.gov/")
assert not re.match(regex, "https://ankit.house.com/")
assert not re.match(regex, "ankit.house.gov/")
assert not re.match(regex, "https://ankit.house.gov/cornell/")

good_urls = [url for url in all_urls if re.match(regex, url)]

print("Length URLS : ", len(good_urls))

good_urls = list(set(good_urls))

print("Length URLS : ", len(good_urls))

html = requests.get("https://jayapal.house.gov").text
soup = BeautifulSoup(html, "html5lib")

links = {a["href"] for a in soup('a') if 'press releases' in a.text.lower()} #use a set to avoid duplicates

print(links)

from typing import Dict, Set
press_releases : Dict[str, Set[str]] = {}

for house_url in good_urls :
    html = requests.get(house_url).text
    soup = BeautifulSoup(html, "html5lib")
    pr_links = {a["href"] for a in soup('a') if 'press releases' in a.text.lower()}  # use a set to avoid duplicates

    print(f"{house_url} : {pr_links}")
    press_releases[house_url] = pr_links


def paragraph_mentions(text : str, keyword : str) -> bool :
    """
    Returns True if a <p> inside the text mentions {keyword}
    """

    soup = BeautifulSoup(text, "html5lib")
    paragraphs = [p.get_text() for p in soup("p")] #get all paragraphs

    return any(keyword.lower() in paragraph.lower()
               for paragraph in paragraphs) #do any of the words in the paragraph have the keyword?

text = """<body><h1>Facebook</h1><p>Twitter</p>"""
assert paragraph_mentions(text, "twitter") #is inside a paragraph (<p>)
assert not paragraph_mentions(text, "facebook") #not inside a <p>
assert not paragraph_mentions(text, "Facebook")

data_mentions = 0
for house_url, pr_links in press_releases.items() :
    for pr_link in pr_links :
        url = f"{house_url}/{pr_link}" #PR link
        text = requests.get(url).text

        if paragraph_mentions(text, "data") :
            print(f"{house_url}")
            data_mentions += 1
            break

print("Data mentions : ", data_mentions)

#using JSON (Javascript Object Notation)
import json
serialized = """{"title" : "Data Science Book", 
              "author" : "Joel Grus", 
              "publicationYear" : 2019, 
              "topics" : ["data", "science", "data science"]}"""

#parse the JSON to create a Python dict
deserialized = json.loads(serialized)
print(deserialized)
assert deserialized["publicationYear"] == 2019
assert "data science" in deserialized["topics"]

import requests, json
github_user = "joelgrus"
endpoint = f"https://api.github.com/users/{github_user}/repos"
repos = json.loads(requests.get(endpoint).text)

from dateutil.parser import parse
dates = [parse(repo["created_at"]) for repo in repos]
month_counts = Counter(date.month for date in dates)
weekday_counts = Counter(date.weekday() for date in dates)

last_5_repos = sorted(repos,
                      key = lambda r : r["pushed_at"],
                      reverse = True)[:5]

last_5_langs = [repo["language"]
                for repo in last_5_repos]

CONSUMER_KEY = "rC6SdpUepwfLNmrd2k1kgTAan"
CONSUMER_SECRET = "cjHW1eKIZJDx5WrirgLGdcPX4yykQwUFmBLRf0fZodmLSM6ipi"

import os, webbrowser
from twython import Twython

#get a temporary client to retrieve an authentication URL
temp_client = Twython(CONSUMER_KEY, CONSUMER_SECRET)
temp_creds = temp_client.get_authentication_tokens()
url = temp_creds['auth_url']

#visit the frickin url to authorize the application to get a pin
print(f"go visit {url} and get the PIN code and paste it below")
webbrowser.open(url)
PIN_CODE = input("please enter the PIN code : ")

#now use the PIN_CODE to get the actual tokens
auth_client = Twython(CONSUMER_KEY,
                      CONSUMER_SECRET,
                      temp_creds["oauth_token"],
                      temp_creds["oauth_token_secret"])
final_step = auth_client.get_authorized_tokens(PIN_CODE)
ACCESS_TOKEN = final_step['oauth_token']
ACCESS_TOKEN_SECRET = final_step["oauth_token_secret"]

#get a new twython instance using them now
twitter = Twython(CONSUMER_KEY,
                  CONSUMER_SECRET,
                  ACCESS_TOKEN,
                  ACCESS_TOKEN_SECRET)

#done with twitter authentication
#search for all tweets containing the phrase "data science"
for status in twitter.search(q = "data science")['statuses'] :
    user = status['user']['screen_name']
    text = status['text']
    print(f"{user}:{text}\n")

"""
Notes on the Streaming API : 

-> the twitter search api only shows a few texts, and we want A LOT
-> use the TwythonStreamer class to get many tweets
"""

from twython import TwythonStreamer

tweets = [] #never append data to global vars in practice
max_tweets = 300
class MyStreamer(TwythonStreamer) :
    def on_success(self, data):
        """
        What do we do when Twitter sends us data?
        Here data will be a python dict to represent a single tweet.
        """

        #collect only english tweets
        if data.get('lang') == "en" :
            tweets.append(data)
            print(f"received tweet # {len(tweets)}")

        #stop when we have collected enough
        if len(tweets) >= max_tweets :
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) #create a new instance

#start consuming public statuses that have the keyword "data"
stream.statuses.filter(track = "data")

#or get a sample of all tweets
stream.statuses.sample()

from collections import Counter
top_hashtags = Counter(hashtag["text"].lower()
                       for tweet in tweets
                       for hashtag in tweet['entities']['hashtags'])

print(top_hashtags.most_common(500))




