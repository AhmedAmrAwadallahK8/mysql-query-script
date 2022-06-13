"""
  Query Script for DS 7330
"""
from __future__ import print_function
from re import T        # make print a function
import mysql.connector  # mysql functionality
import sys              # for misc errors
import getpass          # hidden password prompt

"""
You will have to enter all server information before getting access to your database.
Below are the required entries

SERVER   = Name of the server you are trying to access
USERNAME = Your username
DATABASE = Whatever database you want to access
PASSWORD = Your Password associated with the previously input username
"""

WIPE_PASSWORD = 0

MSQL_CONNECTION_FAILURE = 1
USER_QUIT = 2

USER_SAID_NO = 0
USER_SAID_YES = 1


def get_mysqldb_connection():
   try:
      mysql_connection = try_to_connect()
   except mysql.connector.Error as e:        
      print("SQL Error: {0}".format(e.msg))
      sys.exit(MSQL_CONNECTION_FAILURE)
   except:                                   
      print("Unexpected error: {0}".format(sys.exc_info()[0]))
      sys.exit(MSQL_CONNECTION_FAILURE)
   return mysql_connection

def query_while_user_wants_to(mysql_connection):
   mysql_cursor = get_cursor(mysql_connection)
   user_wants_to_query = True
   while(user_wants_to_query):
      execute_and_print_query(mysql_cursor, mysql_connection)
      user_wants_to_query = does_user_want_to_query()
   mysql_cursor.close()
   return

def execute_and_print_query(mysql_cursor, mysql_connection):
   get_and_execute_query_or_quit(mysql_cursor, mysql_connection)
   print_query(mysql_cursor)
   return

def get_and_execute_query_or_quit(mysql_cursor, mysql_connection):
   query_success = False
   user_wants_to_quit = False
   while not query_success:
      query = get_query_or_quit()
      user_wants_to_quit = check_if_user_quit(query)
      if user_wants_to_quit:
         quit_program(mysql_cursor, mysql_connection)
      query_success = execute_query_and_get_sucess(mysql_cursor, query)
   return

def execute_query_and_get_sucess(mysql_cursor, query):
   try:
      try_to_execute_query(mysql_cursor, query)
   except mysql.connector.Error as e:        
      print("SQL Error: {0}".format(e.msg))
      return False
   except:                                   
      print("Unexpected error: {0}".format(sys.exc_info()[0]))
      return False
   return True

def does_user_want_to_query():
   user_response = get_user_yes_or_no("Query Again? ")
   if(user_response == USER_SAID_NO):
      return False
   else:
      return True

def check_if_user_quit(user_input):
   quit_response = 'q'
   if(user_input.lower() == quit_response):
      return True
   else:
      return False

def get_cursor(mysql_connection):
   mysql_cursor = mysql_connection.cursor()
   return mysql_cursor

def get_user_yes_or_no(message):
   valid_response = False
   while(not valid_response):
      user_response = input(message + "Input \"y\" for yes or \"n\" for no: ").lower()
      valid_responses = ['y', 'n', 'yes', 'no', 'y.', 'n.', 'yes.', 'no.']
      if(user_response in valid_responses):
         valid_response = True
      else:
         print("Not a valid response, please input either \"y\" for yes or \"n\" for no.")
   user_said_no = ['n', 'no', 'n.', 'no.']
   if(user_response in user_said_no):
      return USER_SAID_NO
   else:
      return USER_SAID_YES

def print_query(mysql_cursor):
   print_table_attributes(mysql_cursor.column_names)
   print_table_rows(mysql_cursor)
   return

def quit_program(mysql_cursor, mysql_connection):
   mysql_cursor.close()
   close_mysql_connection(mysql_connection)
   sys.exit(USER_QUIT)

def print_table_attributes(column_names):
   print(" ".join(["{:<12}".format(col) for col in column_names]))
   print("--------------------------------------------")
   return

def print_table_rows(mysql_cursor):
   for row in mysql_cursor:
      print("".join(["{:<12}".format(col) for col in row]))
   return

def get_query_or_quit():
   quit_character = 'q'
   end_of_query_character = ';'
   empty_return = ''

   user_input = ''
   query = ''
   first_entry = True
   print("Query is read until \"" + end_of_query_character +  "\" character is seen")
   while(end_of_query_character not in user_input):
      if first_entry:
         user_input = input("Enter Query or press \"" + quit_character + "\" to exit>")
         first_entry = False
      else:
         user_input = input("                               ->")

      if user_input == quit_character:
         return quit_character

      if user_input != empty_return:
         query += user_input + '\n'

   return query

def close_mysql_connection(mysql_connection):
   mysql_connection.close()
   print("\nConnection terminated.", end='')
   return

def try_to_connect():
   server_name = input("Enter Server Name: ")
   username = input("Enter Username: ")
   database_name = input("Enter Database Name: ")
   password = getpass.getpass("Enter password: ")
   mysql_connection = mysql.connector.connect(host=server_name,user=username,password=password,
                                 database=database_name)
   password = WIPE_PASSWORD                              
   print("Connection established.")
   return mysql_connection

def try_to_execute_query(mysql_cursor, query):
   mysql_cursor.execute(query)
   print("Query executed: \n{0}".format(query))
   return

if __name__ == "__main__":
   mysql_connection = get_mysqldb_connection()
   query_while_user_wants_to(mysql_connection)
   close_mysql_connection(mysql_connection)