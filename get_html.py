import requests

# Take in a URL and return a beautifulSoup object of the page
def html_from_url(url, headers=""):
    
    try:
        response = requests.get(url, headers)

        html = (response.text).strip()

        return html
    except:
        print(f"Failed to get {url}")
        return ""

# Read in an HTML file and return a beautifulSoup object of the page
def html_from_file(filename):
    
    with open(filename, "r", encoding = 'utf8') as f:
        html = f.read()
        html = html.strip()

    return html