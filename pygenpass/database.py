"""
Copyright (c) 2019 paint-it

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sqlite3  # library for database

from termcolor import colored
import sys

class DatabaseConnection:
    """ Class of database entries for user's information."""

    def __init__(self):
        """Used to create database and then to connect with generated databse file
        Checked for table is created? if not then created as per required values """
        try:
            self.con = sqlite3.connect("generated_password.db")
            self.cursor_obj = self.con.cursor()
            self.cursor_obj.execute(
                """CREATE TABLE IF NOT EXISTS passwords(
                id integer PRIMARY KEY,portal_name text NOT NULL UNIQUE, password varchar,
                creation_date varchar, email varchar, portal_url varchar)
                """
            )
            self.con.commit()
        except  sqlite3.Error as e:
            # Catch any SQLite error and print the error message
            print(f"Database error occurred: {e}")
            sys.exit(1)  # Exit the program if a database error occurs

        except Exception as e:
            # Catch any other exceptions and print the error message
            print(f"An error occurred: {e}")
            sys.exit(1)  # Exit the program if an unexpected error occurs


    def insert_data(self, portal_name, password, creation_date, email, portal_url):
        """Adding values into database"""
        try:
            self.cursor_obj.execute(
                """INSERT INTO passwords
                (portal_name, password, creation_date, email, portal_url)
                VALUES (?, ?, ?, ?, ?)""",
                (portal_name, password, creation_date, email, portal_url),
            )
            self.con.commit()
        except sqlite3.IntegrityError:
            print(
                colored(f"Error: A record with the portal name '{portal_name}' already exists.", "green")
            )

        except sqlite3.Error as e:
            print(f"Database error occurred while inserting data: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_data(self, portal_name):
        """Deleting values from database"""
        try:
            self.cursor_obj.execute(
                """DELETE from passwords where portal_name = ?""", (portal_name,)
            )
            self.con.commit()
            print(f"Data for portal '{portal_name}' deleted successfully.")

        except sqlite3.Error as e:
            print(f"Database error occurred while deleting data: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_data(self, portal_name, password):
        """Updating values in database"""
        try:
            self.cursor_obj.execute(
                """UPDATE passwords SET password =? WHERE portal_name =?""",
                (password, portal_name),
            )
            self.con.commit()
            print(f"Password for portal '{portal_name}' updated successfully.")

        except sqlite3.Error as e:
            print(f"Database error occurred while updating data: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def show_data(self, portal_name):
        """All inserted data will showed"""
        try:
            self.cursor_obj.execute(
                """SELECT password FROM passwords WHERE portal_name=?""", (portal_name,)
            )
            row = self.cursor_obj.fetchone()

            if row:
                return row[0]
            else:
                print(f"No data found for portal '{portal_name}'.")
                return None
        except sqlite3.Error as e:
            print(f"Database error occurred while fetching data: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def show_all_data(self):
        """Showing all data saved in database"""
        try:
            self.cursor_obj.execute("""SELECT * FROM passwords""")
            rows = self.cursor_obj.fetchall()
            return rows

        except sqlite3.Error as e:
            print(f"Database error occurred while fetching all data: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_connection(self):
        """Safely close the database connection."""
        try:
            if self.con:
                self.con.close()
                print("Database connection closed successfully.")
        
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred while closing the connection: {e}")
