import azparse
import sqlhelpers
import sqlite3
import time
import os
import os.path

def find_files(path):
    """Finds files in PATH and returns them"""
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    paths = []
    for file in files:
        paths.append(os.path.join(path, file))
    return paths

def extract_data(file):
    """Extracts xml data from FILE and returns data in a dictionary"""
    try:
        parse_obj = azparse.parse_file(file)

        paired_dict = {}
        if azparse.handler(parse_obj, 'ItemPage') != '1':
            return False
        paired_dict["timestamp"] = int(time.time())
        paired_dict["keywords"] = azparse.keywords(parse_obj)
        paired_dict["num_results"] = azparse.num_results(parse_obj)
        try:
            paired_dict["min_price"], paired_dict["top_avg_price"], paired_dict["max_price"] = azparse.price_data(parse_obj) 
        except Exception as e:
            print(e)
            print("No price data")
        
        return paired_dict
    except Exception as e:
        print(e)
        print("Error extracting", file)
        return False

def main(path):
    conn = sqlite3.connect("amazon.db")
    cursor = conn.cursor()
    files = find_files(path)
    for file in files:
        data = extract_data(file)
        if data:
            try:
                sqlhelpers.insert_query(cursor, "search_results", data)
            except Exception as e:
                print(e)
                print("Failure to insert", file)
    print("committing")    
    conn.commit()
    conn.close()
    print("success")
    return True
