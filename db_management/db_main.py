import sqlite3

def print_db_formated(db_name,table_name):
    output_string=""
    output_string=f"{output_string}\n{table_name}:"
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Retrieve column names from the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Retrieve data from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Print column headers
        header = " | ".join(column_names)
        output_string=f"{output_string}\n{header}"
        output_string=f"{output_string}\n{"-" * len(header)}"

        # Print rows
        for row in rows:
            formatted_row = " | ".join(map(str, row))
            output_string=f"{output_string}\n{formatted_row}"

    except sqlite3.Error as e:
        output_string=f"Error: {e}"
    finally:
        conn.close()
        return output_string
