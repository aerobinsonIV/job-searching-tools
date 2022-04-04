import shutil
import os
import re
from get_html import *

class Node:
    def __init__(self, url, html, parent, depth: int):
        self.url = url
        self.html = html
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
        absolute_link = (base + link).strip()
    else:
        absolute_link = link.strip()
    
    # Convert accidental double / to single, remove query params
    single_slash_link = absolute_link[:9] + absolute_link[9:].replace("//", "/")

    if "?" in single_slash_link:
        return single_slash_link[:single_slash_link.find('?')]
    else:
        return single_slash_link


def is_valid_link(link, base_url):
    
    invalid_extensions = ["jpg", "png", "css", "json", "js", "xml", "ico", "webmanifest", "svg"]
    
    for ext in invalid_extensions:
        if link[-len(ext):] == ext:
            return False

    if "#" in link:
        return False

    if "javascript:" in link:
        return False

    if "//" in link[10:]:
        return False

    if "mailto:" in link:
        return False

    if " " in link:
        return False

    if "http" in link[14:]:
        return False
    
    # Check domain, we don't care about links that lead to external sites
    if link[0:len(base_url)] != base_url:
        return False

    return True

def get_links(html, base_url):
    links = []

    # Find all strings that match form href="/some/link"
    
    # https://regex101.com/ is useful for testing, more visual
    # ? is means "lazy", i.e. match as few chars as possible. This matches the first closing angle bracket rather than the last.
    href_regex = re.compile(r'href=.*?>')
    hrefs = re.findall(href_regex, html)

    # Extract actual links, clean, return only unique links
    for href in hrefs:
        # href may or may not have double quotes around the link. Remove them if present
        link = href.replace('"', "")[5:-1].strip()
        cleaned_link = clean_link(link, base_url)
        if cleaned_link not in links:
            if is_valid_link(cleaned_link, base_url):
                links.append(cleaned_link)

    return links

def dump_nodes_to_files(node_list, output_dir):
    
    try:
        shutil.rmtree(output_dir)
    except:
        pass
    
    os.mkdir(output_dir)

    for node in node_list:
        filename = node.url.replace("/", "~").replace(":", "").replace("?", "")
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding = 'utf8') as f:
            f.write(str(node.html))

def crawl_and_save(base_url, crawl_depth, output_dir):

    base_node = Node(base_url, None, None, 0)

    queue = []
    queue.append(base_node)

    searched = []

    # Main loop
    while len(queue) > 0:

        # Pop a non-expanded node off the queue
        current_node = queue.pop(0)

        if current_node.depth >= crawl_depth:
            searched.append(current_node)
            continue

        print(f"Getting {current_node}")
        
        # Download page at URL
        current_node.html = html_from_url(current_node.url)

        # Get links on page
        links = get_links(current_node.html, base_url)

        # Make nodes for newly found links and append 
        for link in links:
            new_node = Node(link, None, current_node, current_node.depth + 1)
            if (new_node not in queue) and (new_node not in searched) and (new_node != current_node):
                queue.append(new_node)

        searched.append(current_node)

    dump_nodes_to_files(searched, output_dir)
