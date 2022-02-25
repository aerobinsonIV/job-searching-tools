from soup import *

base = "http://www.absolute-metrology.com/"

class Node:
    def __init__(self, url, soup, parent, depth: int):
        self.url = url
        self.soup = soup
        self.parent = parent
        self.depth = depth
    
    def __eq__(self, other):
        if self.url == other.url:
            print(f"{self} == {other}")
            return True
        else:
            print(f"{self} != {other}")
            return False

    def __repr__(self) -> str:
        return f"{self.url} @ depth {self.depth}"

def is_rel_link(link):
    if link[:4] == "http":
        return False
    else:
        return True

def clean_link(link, base):
    if is_rel_link(link):
        return base + link
    else:
        return link

def is_valid_link(link):
    
    valid_extensions = ["html", "asp", "aspx", "php", "htm", "xhtml"]
    
    for ext in valid_extensions:
        if link[-len(ext):] == ext:
            return True

    return False

def get_links(soup):
    links = []

    anchors = soup.find_all('a', href = True)

    for anchor in anchors:
        href = anchor['href']
        if href not in links:
            if is_valid_link(href):
                links.append(clean_link(href, base))

    return links


base_url = "http://www.absolute-metrology.com/"
crawl_depth = 99

base_node = Node(base_url, None, None, 0)

queue = []
queue.append(base_node)

searched = []

while len(queue) > 0:

    # Pop a non-expanded node off the queue
    current_node = queue.pop(0)

    if current_node.depth >= crawl_depth:
        searched.append(current_node)
        print(f"Not expanding {current_node}")
        continue

    print(f"Expanding {current_node}")
    
    # Download page at URL
    current_node.soup = soup_url(current_node.url)

    # Get links on page
    links = get_links(current_node.soup)

    # Make nodes for newly found links and append 
    for link in links:
        new_node = Node(link, None, current_node, current_node.depth + 1)
        if new_node not in queue and new_node not in searched:
            print(f"Enqueuing {new_node}")
            queue.append(new_node)

    searched.append(current_node)

print("\nDone.\nSearched nodes:\n")

for node in searched:
    print(node)


# ams_soup = soup_file("index.html")
# links = get_links(ams_soup)
# print("\n\n\n")
# for link in links:
#     print(link)