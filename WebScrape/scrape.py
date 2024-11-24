import requests
from bs4 import BeautifulSoup
import pprint

# think of as a web browser without a window
res = requests.get('https://news.ycombinator.com/news')
# Create a soup object; parse the string returned above via .text
soup = BeautifulSoup(res.text, 'html.parser')
# print the soup object... . body gives just body for example
#  print(soup.body.contents)
# Find all the 'divs', 'a', etc.
# soup.a find first 'a' tag. Other options exist
# soup.find('a') does the same. Other options exist.
# print(soup.find_all('div'))
# Select using a css selector. 'a' selects all 'a' tags
# print(soup.select('a'))
# .score = score class   #score = score id
# grabs all the scores on the page returns list
# print(soup.select('.score'))
# grabs all titlelines, [0] returns the first.
# print(soup.select('.titleline')[0])
links = soup.select('.titleline')
subtext = soup.select('.subtext')

# scraping page 2
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links2 = soup2.select('.titleline')
subtext2 = soup2.select('.subtext')

megalink = links + links2
megasub = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for ind, item in enumerate(links):
        title = links[ind].getText()
        href = links[ind].get('href', None)
        vote = subtext[ind].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(megalink, megasub))


# Recommendations
# Beautifulsoup familiarity
# Scraping may not be necessary, check API
# Check framework like Scrapy, heavy-lifting
# Learn to scrape and place in a database.



