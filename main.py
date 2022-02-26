import sys

import crawler
import contact_info_finder


if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} [url] [download directory] [crawl depth]")
    print(f"Example: {sys.argv[0]} https://absolute-metrology.com/ dumps/ams 4")
    exit(-1)

url = sys.argv[1]
dir = sys.argv[2]
crawl_depth = int(sys.argv[3])

if "www" in url:
    front_trimmed_url = url[url.find("://www.") + 7:]
else:
    front_trimmed_url = url[url.find("://") + 3:]

company_name = front_trimmed_url[:front_trimmed_url.find(".")]

print(f"|{company_name}|")

crawler.crawl_and_save(url, crawl_depth, dir)

contact_info_finder.find_in_all_files(dir, contact_info_finder.find_phone_numbers, None)
contact_info_finder.find_in_all_files(dir, contact_info_finder.find_email_addrs, company_name)

