import sys
import time
import azclass
import os
from os.path import join

def write_file(text, directory):
    """Accepts inputs of strings and writes to file"""
    try:
        f = open(directory, 'wb')
        f.write(text)
        f.close()
        return True
    except Exception as e:
        print(e)
        print("error encountered in writing")
        return False

def read_list(file_path):
    """Reads a list of items stored on FILE_PATH and returns a list
    the items"""
    try:
        f = open(file_path, 'r')
        items = f.read()
        f.close()
        item_list = items.split('\n')
        k = 0
        max_k = len(item_list)
        while k < max_k:
            item_list[k] = item_list[k].strip(' ')
            k += 1
        while '' in item_list:
            item_list.remove('')
        return item_list
    except Exception as e:
        print(e)
        print("Error encountered in reading")
        return False
    
def main(read_file, write_directory, start = 0, index = 'All', max_page = 5):
    items = read_list(read_file)
    if not items:
        print("No items, closing")
        return False
    count = int(start)
    request = azclass.Azurl('AWSECommerceService', 'webservices.amazon.com', '/onca/xml', os.environ["AWS_PUBLIC_KEY"], os.environ["AWS_PRIVATE_KEY"], os.environ["AWS_USER_NAME"])
    request.add_params({"Operation":"ItemSearch",
                        "SearchIndex":index,
                        "ResponseGroup":"ItemAttributes,OfferFull,SalesRank"})
    max_count = len(items)
    while count < max_count:
        print(count)
        for page in range(1, max_page+1):
            time.sleep(2)
            request.add_params({"Keywords":items[count],
                                "ItemPage":str(page)})
            request.make_url()
            try:
                response = request.fetch_url()
            except Exception as e:
                print(e)
            if not response:
                print("item", count, page, "failed")
            else:
                text = response.read()
                text = text.decode().splitlines()
                #to avoid malformed xml
                final_text = "".join(text)            
                write_file(final_text.encode(encoding='UTF-8'), join(write_directory, str(round(time.time()))+'.xml'))
        count += 1
    return True

parameters = sys.argv
if len(parameters) < 2+1 or len(parameters) > 5+1:
    print("invalid parameters")
else:
    main(*parameters[1:])
