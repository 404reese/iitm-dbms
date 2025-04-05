import sys
import os
import psycopg2

# Read and convert number from file
with open("number.txt", "r") as file:
    x = int(file.read().strip())  # Convert x to an integer

ot = 2000 + 5 * x + 5  # Perform arithmetic operation correctly

try:
    # Establish database connection
    connection = psycopg2.connect(
        database=sys.argv[1],
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        host=os.environ.get('PGHOST'),
        port=os.environ.get('PGPORT')
    )
    
    cursor = connection.cursor()

    # Use parameterized queries to prevent SQL injection
    query = "SELECT ISBN_no FROM book_catalogue WHERE year = %s"
    cursor.execute(query, (ot,))
    
    # Fetch and print results
    result = cursor.fetchall()
    for res in result:
        print(res[0])

    cursor.close()
    connection.close()

except (Exception, psycopg2.DatabaseError) as error:
    print("Database error:", error)


# code 2
import sys
import os
import psycopg2

file = open("number.txt","r")
x = int(file.read().strip())
ot = 2000 + 5 * x + 5

try :
    conn = psycopg2.connect(
        database = sys.argv[1],
        user = os.environ.get('PGUSER'),
        password = os.environ.get('PGPASSWORD'),
        host = os.environ.get('PGHOST'),
        port = os.environ.get('PGPORT'))
        
    cursor = conn.cursor()
    query = "SELECT ISBN_no FROM book_catalogue WHERE year = '{}'".format(ot)
    cursor.execute(query)
    
    result = cursor.fetchall()
    for i in result :
        print(i[0])
        
    cursor.close()
    conn.close()
    
except (Exception, psycopg2.DatabaseError) as error:
    print("Database error:", error)