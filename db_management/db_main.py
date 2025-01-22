# care mostly chatgpt my beloved

import sqlite3

def print_db_formated(db_name,table_name):
    output_string=""
    output_string=f"{output_string}\n{table_name}:"
    try:
    
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        
        header = " | ".join(column_names)
        output_string=f"{output_string}\n{header}"
        output_string=f"{output_string}\n{"-" * len(header)}"

        
        for row in rows:
            formatted_row = " | ".join(map(str, row))
            output_string=f"{output_string}\n{formatted_row}"

    except sqlite3.Error as e:
        output_string=f"Error: {e}"
    finally:
        conn.close()
        return output_string
    
def exec_query(query_lvl,db_name,table_name,username,password):
    if query_lvl == 1: 
        try:
            
            #check for multistatement injection this is bad it will also detect for 
            # ; if it is in string therefore executescript will be used that is not working
            # for selction of data only for multiline shit
            # i need to intigrate this into the outcomment and quoted detection for it to work
            # but times are hard presentation is tomorow

            if ";" in username or ";" in password:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                # Main Select
                cursor.executescript(f"""
                    SELECT password
                    FROM {table_name}
                    WHERE username = \"{username}\" and password = \"{password}\"
                            """)  

            else:
                # Connect to the database
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                # Main Select
                cursor.execute(f"""
                    SELECT password
                    FROM {table_name}
                    WHERE username = \"{username}\" and password = \"{password}\"
                            """)  
            
            # here late use query from Query class
            output_string=cursor.fetchall()
            if output_string ==[]:
                output_string = "False"
            elif output_string != []:
                output_string = "True"
                
        except sqlite3.Error as e:
            output_string=f"Error: {e}"
        finally:
            conn.close()
            return output_string +"\n"

    elif query_lvl == 2:
        try:
            # Connect to the database

            if ";" in username or ";" in password:  #! read line 42 this shit is some real shit

                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                # Main Select
                cursor.executescript(f"""
                    SELECT password
                    FROM {table_name}
                    WHERE username = CAST(\"{username}\" as TEXT) and password = CAST(\"{password}\" as TEXT)
                            """)  
                
            else:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                # Main Select
                cursor.execute(f"""
                    SELECT password
                    FROM {table_name}
                    WHERE username = CAST(\"{username}\" as TEXT) and password = CAST(\"{password}\" as TEXT)
                            """)  
            
            # here late use query from Query class
            output_string=cursor.fetchall()
            if output_string ==[]:
                output_string = "False"
            elif output_string != []:
                output_string = "True"
                
        except sqlite3.Error as e:
            output_string=f"Error: {e}"
        finally:
            conn.close()
            return output_string +"\n"


    elif query_lvl == 3:
        try:
            # Connect to the database
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            real_query = """
                SELECT password
                FROM users
                WHERE username = ? AND password = ?
                        """
            # Main Select
            cursor.execute(real_query,(username,password))


            # here late use query from Query class
            output_string=cursor.fetchall()
            if output_string ==[]:
                output_string = "False"
            elif output_string != []:
                output_string = "True"
                
        except sqlite3.Error as e:
            output_string=f"Error: {e}"
        finally:
            conn.close()
            return output_string +"\n"
        
# meine fresse ist dieser Code scheiße XD