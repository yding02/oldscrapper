import sqlhelpers
import sqlite3

def main99():
    conn = sqlite3.connect('amazon.db')
    cursor = conn.cursor()
    sql = """ALTER TABLE item_listings
               ADD item_name VARCHAR;
                    """
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return True

def main():
    generate_report()

def generate_report():
    conn = sqlite3.connect('amazon.db')
    cursor = conn.cursor()
    sql = """SELECT keywords, num_results, top_avg_price, min_price, max_price FROM search_results
             WHERE timestamp > 1474435252
             ORDER BY num_results ASC;"""
    cursor.execute(sql)
    result = cursor.fetchall()
    write_string = "Keyword;Number of Results;avg price;min price; max price;\n"
    for r in result:
        for item in r:
            write_string += str(item) + ';'
        write_string += '\n'
    f = open("20160920.txt", "w")
    f.write(write_string)
    f.close()
    conn.close()
    return True
main()
