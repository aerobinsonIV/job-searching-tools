import requests
from bs4 import BeautifulSoup

# Take in a URL and return a beautifulSoup object of the page
def soup_url(url, headers=""):
    response = requests.get(url, headers)

    html = response.text

    return BeautifulSoup(str(html), 'html.parser')

# Read in an HTML file and return a beautifulSoup object of the page
def soup_file(filename):
    
    with open(filename, "r") as f:
        html = f.read()

    return BeautifulSoup(str(html), 'html.parser')