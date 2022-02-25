from soup import *

base_url = "http://www.absolute-metrology.com/"
start_url = "http://www.absolute-metrology.com/index.html"

class Node:
    def __init__(self, url, soup, parent, depth: int):
        self.url = url
        self.soup = soup
        self.parent = parent
        self.depth = depth
    
    def __eq__(self, other):
        return self.url == other.url

    def __repr__(self) -> str:
        return f"{self.url} @ depth {self.depth}"

def is_rel_link(link):
    if link[:4] == "http":
        return False
    else:
        return True

def clean_link(link, base):
    if is_rel_link(link):
        return (base + link).strip()
    else:
        return link.strip()

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
                links.append(clean_link(href, base_url))

    return links

crawl_depth = 99

base_node = Node(start_url, None, None, 0)

queue = []
queue.append(base_node)

searched = []

# Main loop
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
        if (new_node not in queue) and (new_node not in searched) and (new_node != current_node):
            # print(f"Enqueuing {new_node}")
            queue.append(new_node)
        # else:
            # print(f"Not enqueuing {new_node}")

    searched.append(current_node)

print("\nDone.\nSearched nodes:\n")

for node in searched:
    print(node)
