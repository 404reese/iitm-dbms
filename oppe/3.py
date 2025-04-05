import os
import sys
import psycopg2

# Read the date from date.txt
with open("date.txt", "r") as file:
    date_input = file.read().strip()

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database=sys.argv[1],
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        host=os.environ.get('PGHOST'),
        port=os.environ.get('PGPORT')
    )
    
    cursor = conn.cursor()
    
    # SQL query to retrieve the main referee's name for the given date
    query = """
        SELECT r.name
        FROM matches m
        JOIN match_referees mr ON m.match_num = mr.match_num
        JOIN referees r ON mr.referee = r.referee_id
        WHERE m.match_date = %s;
    """
    cursor.execute(query, (date_input,))
    result = cursor.fetchone()
    
    if result:
        full_name = result[0].strip()
        parts = full_name.split()
        
        if len(parts) < 1:
            print("Invalid name format")
        else:
            surname = parts[-1]
            initials = [part[0].upper() + '.' for part in parts[:-1]]
            formatted_name = f"{surname} {' '.join(initials)}"
            print(formatted_name)
    else:
        print("No match found for the given date.")
    
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


# code 2
import os
import sys
import psycopg2

# --- Configuration ---
DATE_FILE = "date.txt"

# --- Helper function for name formatting ---
def format_referee_name(full_name):
    """Formats the referee name as 'Lastname F. M.'"""
    if not full_name or not isinstance(full_name, str):
        return "Invalid name data"

    parts = full_name.strip().split()

    if len(parts) == 0:
        return "Empty name"
    elif len(parts) == 1:
        # Only one name part, return it as is (or decide on specific handling)
        # Based on "Kennedy Sapam" -> "Sapam K.", the last part is the surname.
        # This case doesn't fit the examples well, but we'll return it.
        return parts[0]
    else:
        last_name = parts[-1]
        # Get initials for all parts *before* the last name
        initials = [part[0] + "." for part in parts[:-1]]
        return f"{last_name} {' '.join(initials)}"

# --- Main script ---
conn = None  # Initialize conn to None for the finally block
try:
    # 1. Read the date from the file
    try:
        with open(DATE_FILE, "r") as file:
            # Read the first line and strip leading/trailing whitespace
            # Also take only the first word in case there's more on the line
            match_date_str = file.readline().strip().split()[0]
            # Optional: Add validation to ensure it looks like a date YYYY-MM-DD
            if not (len(match_date_str) == 10 and match_date_str[4] == '-' and match_date_str[7] == '-'):
                 print(f"Error: Date '{match_date_str}' from {DATE_FILE} is not in YYYY-MM-DD format.", file=sys.stderr)
                 sys.exit(1) # Exit if date format is wrong

    except FileNotFoundError:
        print(f"Error: File '{DATE_FILE}' not found in the current directory.", file=sys.stderr)
        sys.exit(1)
    except IndexError:
        print(f"Error: File '{DATE_FILE}' is empty or contains no data on the first line.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{DATE_FILE}': {e}", file=sys.stderr)
        sys.exit(1)


    # 2. Get Database Credentials
    db_name = sys.argv[1] if len(sys.argv) > 1 else None
    db_user = os.environ.get('PGUSER')
    db_password = os.environ.get('PGPASSWORD')
    db_host = os.environ.get('PGHOST')
    db_port = os.environ.get('PGPORT')

    if not db_name:
        print("Error: Database name must be provided as a command-line argument.", file=sys.stderr)
        sys.exit(1)
    if not db_user or not db_password or not db_host or not db_port:
        print("Error: Ensure PGUSER, PGPASSWORD, PGHOST, and PGPORT environment variables are set.", file=sys.stderr)
        sys.exit(1)

    # 3. Connect to the database
    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cursor = conn.cursor()

    # 4. Construct and execute the SQL query
    # Joins matches -> match_referees -> referees based on the date
    query = """
    SELECT r.name
    FROM referees r
    JOIN match_referees mr ON r.referee_id = mr.referee
    JOIN matches m ON mr.match_num = m.match_num
    WHERE m.match_date = %s;
    """

    # Execute using parameterized query to prevent SQL injection
    cursor.execute(query, (match_date_str,))

    # 5. Fetch the result
    result = cursor.fetchone() # Fetches the first row found

    # 6. Process and print the result
    if result:
        referee_full_name = result[0]
        formatted_name = format_referee_name(referee_full_name)
        print(formatted_name)
    else:
        print(f"No main referee found for match date {match_date_str}")

    # Clean up
    cursor.close()

except psycopg2.Error as e:
    print(f"Database error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    # Ensure the connection is closed even if errors occur
    if conn:
        conn.close()