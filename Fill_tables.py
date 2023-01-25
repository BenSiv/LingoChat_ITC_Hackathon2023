import pymysql
import csv


DATABASE_NAME = 'itc_hackaton'
# USER = 'root'
# PASSWORD = 'root1!2@'
# HOST = 'localhost'
USER = 'm1ow7xhhjf2u87ondhja'
PASSWORD = 'pscale_pw_kI2oJ1yIUdgQQHMK4ovdB6UARJB4cf8UAmWwJliuuJp'
HOST = 'eu-central.connect.psdb.cloud'
DATA_PATH = '/Users/ofir/Documents/Data_Science/ITC/Data_Science_Course_Oct_2022/Hackaton/LingoChat_ITC_Hackathon2023/lingodata_unscaled.csv'
HASH = '$2b$10$IIFvrmGsTgvo.H2mVLrpN.UCvh3A0nwOTWWF8fdxvXe4jaOVQvTUa'

def create_connection():
    con = pymysql.connect(host=HOST,
                          user=USER,
                          password=PASSWORD,
                          database=DATABASE_NAME,
                          ssl={'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}})
    return con


def check_database(database):
    """ checks if the database exist, returns true if it is and false if it doesn't"""
    con = create_connection()

    with con.cursor() as cursor:
        try:
            check_database_sql = f"USE {database};"
            cursor.execute(check_database_sql)
            return True
        except pymysql.err.OperationalError:
            print(f"Database '{database}' doesn't exist, create database using"
                  f" -c argument to initialize the Shufersal scraper.")
            return False


def filling_table(con, database, table, variables, *data):
    """'filling_table' get a pymysql.connection.connection attribute,
    name of a database, name of a table, string of variables and a list of data
    and add it to the table """
    with con.cursor() as cursor:
        select_database = f"USE {database}"
        cursor.execute(select_database)
        variables = variables.replace("'", "")
        values = len(data) * '%s, '
        values = values.rstrip(", ")
        fill_table = f"REPLACE INTO {table} {variables} VALUES ({values})"
        cursor.execute(fill_table, [*data])
        con.commit()

def fill_interests_table():
    con = create_connection()

    with open(DATA_PATH, 'r') as data_file:
        reader = csv.DictReader(data_file)

        fields_list = reader.fieldnames.copy()
        fields_list.remove('')
        fields_list.remove('Age')
        fields_list.remove('Gender')

        for field in fields_list:
            filling_table(con, DATABASE_NAME, 'Interests', '(name)', field)

def sql_query(query, con):
    """
    "sql_connection" receives a string with sql query and returns it result using pymysql module.
    """
    with con.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def fill_users_info():
    con = create_connection()

    with open(DATA_PATH, 'r') as data_file:
        reader = csv.DictReader(data_file)
        fields_list = reader.fieldnames.copy()
        fields_list.remove('')
        fields_list.remove('Age')
        fields_list.remove('Gender')

        for user in reader:
            filling_table(con, DATABASE_NAME, 'Users', '(name, age, gender,email, password)', user[''], user['Age'], user['Gender'], 'hackathon@gmail.com', HASH)
            user_id_query = f'''SELECT id FROM Users WHERE name = "{user['']}";'''
            user_id = sql_query(user_id_query, con)[0]
            for field in fields_list:
                field_id_query = f'''SELECT id FROM Interests WHERE name = "{field}";'''
                field_id = sql_query(field_id_query, con)[0]
                try:
                    rating = int(float(user[field]))
                except ValueError:
                    rating = 0
                filling_table(con, DATABASE_NAME, 'Users_Interests', '(user_id, interests_id, rating)', user_id, field_id, rating)

def main():
    print(check_database(DATABASE_NAME))
    fill_interests_table()
    fill_users_info()

if __name__ == '__main__':
    main()
