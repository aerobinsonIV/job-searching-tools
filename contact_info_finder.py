import os
import re

directory = "dumps/allegro"

def read_file(path):
    with open(path, "r", encoding = 'utf8') as f:
        return f.read()

def find_phone_numbers(input_text):
    phone_num_regexes = []

    # List of potential phone number patterns
    phone_num_regexes.append(re.compile(r'\d\d\d-\d\d\d-\d\d\d\d'))
    # phone_num_regexes.append(re.compile(r'\d\d\d\d\d\d\d\d\d\d'))
    phone_num_regexes.append(re.compile(r'\(\d\d\d\)-\d\d\d-\d\d\d\d'))

    phone_numbers = []

    for regex in phone_num_regexes:
        numbers = re.findall(regex, input_text)
        phone_numbers += numbers
    
    return phone_numbers

# Take in a folder and a function that returns a list of contact info items in a string
# Run search function on all files in folder and display new unique results for each file
def find_in_all_files(directory, search_function):
    
    all = []

    all_files = os.listdir(directory)
    for filename in all_files:
        
        # Read downloaded page
        path = os.path.join(directory, filename)
        text = read_file(path)
        
        this_page_items = search_function(text)

        # Are there any matches on this page?
        if len(this_page_items) > 0:

            unique = []
            for item in this_page_items:
                
                # Have we already found this item on this or another page?
                if item not in all and item not in unique:
                    unique.append(item)
        
            # Skip printing this page's link if there are no unique items to show on it
            if len(unique) > 0:
                # Convert filename back to link and print
                link_equivalent = str(filename).replace("~", "/").replace("//", "://")
                print(f"\n{link_equivalent}:")

                for item in unique:
                    print(item)

find_in_all_files(directory, find_phone_numbers)