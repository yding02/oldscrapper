import sqlite3

def create_search_table(cursor):
    return
    sql_command = """CREATE TABLE search_results(
    id INT,
    timestamp BIGINT,
    keywords CHAR,
    num_results INT,
    top_avg_price INT,
    PRIMARY KEY (id)
    ) ;"""
    return cursor.execute(sql_command)

def create_item_table(cursor):
    return
    sql_command = """CREATE TABLE item_listings(
    id INT,
    timestamp BIGINT,
    asin CHAR UNIQUE NOT NULL,
    parent_asin CHAR,
    upc CHAR,
    price INT,
    price_low INT,
    item_name CHAR,
    item_manu CHAR,
    seller_type CHAR,
    PRIMARY KEY (id)
    );"""
    return cursor.execute(sql_command)

def dict_to_insert(paired_dict):
    """Turns a PAIRED_DICT into an insert string"""
    insert_headers = []
    insert_values = []
    for key in paired_dict.keys():
        insert_headers.append(key)
        insert_values.append(paired_dict[key])

    header_string = ""
    value_string = ""
    for i in range(len(insert_headers)):
        header_string += insert_headers[i] + ','
        value_string += '"' + str(insert_values[i]).replace('"', '""') + '",'

    return '(' + header_string[:-1] + ") VALUES (" + value_string[:-1] + ')'

def make_insert_command(table, args):
    """Makes an insert command from the values of ARGS into TABLE"""
    command_body = dict_to_insert(args)
    return "INSERT INTO " + table + " " + command_body + ";"

def insert_query(cursor, table, args):
    """Inserts data from ARGS in the form of a dictionary into TABLE"""
    sql_command = make_insert_command(table, args)
    return cursor.execute(sql_command)
