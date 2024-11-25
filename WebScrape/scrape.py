# Import necessary libraries
import requests  # For making HTTP requests to retrieve data from web pages
from bs4 import BeautifulSoup  # For parsing HTML content from the web
import pprint  # For pretty printing data (i.e., making it readable)

# Think of requests as a web browser without a window
# Use requests.get() to fetch the HTML content of the first page
res = requests.get('https://news.ycombinator.com/news')
# Create a BeautifulSoup object to parse the HTML returned above via .text
# 'html.parser' is the parser used for processing the HTML
soup = BeautifulSoup(res.text, 'html.parser')

# Printing the contents of the body of the HTML, this will list all the tags inside the body of the page
# print(soup.body.contents)

# Finding all elements of a specific type (e.g., all <div> tags)
# soup.a finds the first 'a' tag. You can use soup.find('a') for the same result. 
# Both find and find_all can be used to locate tags, but find returns the first match, while find_all returns all matches
# print(soup.find_all('div'))

# Selecting using a CSS selector (this selects all 'a' tags)
# soup.select() can be used to apply CSS selectors to find matching elements
# print(soup.select('a'))

# The '.score' class in the soup is used to identify elements containing the score of the story
# In the case of scores, we can use this selector to grab all the score elements
# print(soup.select('.score'))

# Grabbing all the titles of the stories, .titleline represents the class containing the titles of the stories
# [0] returns the first item from the list of titles
# print(soup.select('.titleline')[0])

# Collecting the links (titles of the stories) and subtext (scores, user comments, etc.) from the first page
links = soup.select('.titleline')
subtext = soup.select('.subtext')

# Scraping the second page of the website to get additional data
res2 = requests.get('https://news.ycombinator.com/news?p=2')  # p=2 indicates the second page
soup2 = BeautifulSoup(res2.text, 'html.parser')
links2 = soup2.select('.titleline')  # Get the titles from the second page
subtext2 = soup2.select('.subtext')  # Get the subtext (scores) from the second page

# Combining the links and subtext from both pages
megalink = links + links2
megasub = subtext + subtext2

# Function to sort the stories by their votes in descending order
# hnlist is the list of stories containing title, link, and votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k: k['votes'], reverse=True)

# Function to create a custom list of stories (title, link, votes) from the links and subtext lists
# This function filters stories with at least 100 votes and returns them sorted by votes
def create_custom_hn(links, subtext):
    hn = []  # List to store the filtered stories
    for ind, item in enumerate(links):  # Loop through all the links (story titles)
        title = links[ind].getText()  # Extract the text (title) of the story
        href = links[ind].get('href', None)  # Extract the href (link) of the story
        vote = subtext[ind].select('.score')  # Get the score for the story from the subtext

        # If a score is found, process it
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))  # Extract and convert the score to an integer
            # Only add the story if the points are greater than 99
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    
    # Return the sorted list of stories by votes
    return sort_stories_by_votes(hn)

# Pretty print the final list of stories that have at least 100 votes, sorted by votes
pprint.pprint(create_custom_hn(megalink, megasub))

# Recommendations:
# 1. Familiarize yourself with BeautifulSoup to become comfortable with HTML parsing.
# 2. Scraping may not always be necessary—check if an API is available for easier access to data.
# 3. If scraping becomes complex, consider using a framework like Scrapy that can handle the heavy lifting.
# 4. Learn how to store scraped data into a database for easier access and analysis.
