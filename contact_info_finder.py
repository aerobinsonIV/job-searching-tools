import os
import re

directory = "dumps/ams_dump"

def read_file(path):
    with open(path, "r", encoding = 'utf8') as f:
        return f.read()

def find_phone_numbers(input_text):
    phone_num_regexes = []

    # List of potential phone number patterns
    phone_num_regexes.append(re.compile(r'\d\d\d-\d\d\d-\d\d\d\d'))
    phone_num_regexes.append(re.compile(r'\d\d\d\d\d\d\d\d\d\d'))
    phone_num_regexes.append(re.compile(r'\(\d\d\d\)-\d\d\d-\d\d\d\d'))

    phone_numbers = []

    for regex in phone_num_regexes:
        numbers = re.findall(regex, input_text)
        phone_numbers += numbers
    
    return phone_numbers


def process_all_files(directory):
    
    all_files = os.listdir(directory)
    for filename in all_files:
        
        # Convert filename back to link and print
        link_equivalent = str(filename).replace("~", "/").replace("//", "://")
        print(f"\n{link_equivalent}:")
        
        # Read downloaded page
        path = os.path.join(directory, filename)
        text = read_file(path)
        
        phone_numbers = find_phone_numbers(text)

        for phone_number in phone_numbers:
            print(phone_number)

process_all_files(directory)