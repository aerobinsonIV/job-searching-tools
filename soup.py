import requests
from bs4 import BeautifulSoup

# Take in a URL and return a beautifulSoup object of the page
def soup_url(url, headers=""):
    
    try:
        response = requests.get(url, headers)

        html = (response.text).strip()

        return BeautifulSoup(str(html), 'html.parser')
    except:
        print(f"Failed to get {url}")
        return BeautifulSoup("", 'html.parser')

# Read in an HTML file and return a beautifulSoup object of the page
def soup_file(filename):
    
    with open(filename, "r") as f:
        html = f.read()
        html = html.strip()

    return BeautifulSoup(str(html), 'html.parser')