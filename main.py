import crawler
import contact_info_finder


url = "https://absolute-metrology.com/"
dir = "dumps/ams"


company_name = url[url.find("://") + 3:url.find(".")]

print(company_name)

crawler.crawl_and_save(url, 99, dir)

contact_info_finder.find_in_all_files(dir, contact_info_finder.find_phone_numbers, None)
contact_info_finder.find_in_all_files(dir, contact_info_finder.find_email_addrs, company_name)

