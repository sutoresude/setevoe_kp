import mysql.connector
from mysql.connector import Error
from config import db_config

def create_connection_mysql_db(db_host, user_name, user_password, db_name = None):
    connection_db = None
    try:
        connection_db = mysql.connector.connect(
            host = db_host,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("Подключение к MySQL успешно выполнено")
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)
    return connection_db


conn = create_connection_mysql_db(db_config["mysql"]["host"],
                                  db_config["mysql"]["user"],
                                  db_config["mysql"]["pass"])
cursor = conn.cursor()
create_db_sql_query = 'CREATE DATABASE {}'.format('Poliklinika')
cursor.execute(create_db_sql_query)
cursor.close()
conn.close()

conn = create_connection_mysql_db(db_config["mysql"]["host"],
                                  db_config["mysql"]["user"],
                                  db_config["mysql"]["pass"],
                                  "Poliklinika")
try:
    # создание таблицы с пациентами
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT, 
    fullname TEXT NOT NULL, 
    address TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    date_of_disease TEXT NOT NULL,
    doctor TEXT NOT NULL, 
    PRIMARY KEY (id)
    ) ENGINE = InnoDB'''
    cursor.execute(create_table_query)
    conn.commit()

    # создание таблицы с докторами
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT, 
        fullname TEXT NOT NULL, 
        room_number INT,
        zone_number INT,
        date_and_time_of_work TEXT, 
        PRIMARY KEY (id)
        ) ENGINE = InnoDB'''
    cursor.execute(create_table_query)
    conn.commit()

    # создание таблицы с болезнями
    cursor = conn.cursor()
    create_table_query = '''
            CREATE TABLE IF NOT EXISTS diseases (
            id INT AUTO_INCREMENT, 
            name TEXT NOT NULL,
            symptoms TEXT NOT NULL, 
            medicine TEXT NOT NULL, 
            PRIMARY KEY (id)
            ) ENGINE = InnoDB'''
    cursor.execute(create_table_query)
    conn.commit()

    # вставка данных в таблицу с пациентами изначальной инфы
    insert_patients_table_query = '''
    INSERT INTO
    `patients` (`fullname`, `address`, `diagnosis`, `date_of_disease`, `doctor`) 
    VALUES
    ('Pavlova Antonina Mikhailovna', 'nevsky prospect 24', 'herpes', '24.05.2024', 'Petrov Anton Ivanovich'),
    ('Germanenko Pytr Vasilyevich', 'ligovsky prospect 33', 'diarrhea', '26.05.2024', 'Rymsky Vasily Petrovich'),
    ('Timiryazev Antonin Pavlovich', 'petrovsky prospect 4', 'acne', '20.05.2024', 'Petrov Anton Ivanovich'),
    ('Klimashin Igor Pethovich', 'oktyabrskaya embankment 15', 'diarrhea', '24.05.2024', 'Rymsky Vasily Petrovich');'''
    cursor.execute(insert_patients_table_query)
    conn.commit()

    # вставка данных в таблицу с докторами изначальной инфы
    insert_doctors_table_query = '''
       INSERT INTO
       `doctors` (`fullname`, `room_number`, `zone_number`, `date_and_time_of_work` )
       VALUES
       ('Petrov Anton Ivanovich', 11, '1', '10-18 monday-friday'),
       ('Rymsky Vasily Petrovich', 15, '2', '09-17 friday-wedsday');'''
    cursor.execute(insert_doctors_table_query)
    conn.commit()

    # вставка данных в таблицу с болезнями изначальной инфы
    insert_diseases_table_query = '''
       INSERT INTO
       `diseases` (`name`,`symptoms`,`medicine`)
       VALUES
       ('herpes', 'small red dots', 'allomedin'),
       ('diarrhea', 'irritable bowel', 'smekta'),
       ('acne','big red dots', 'basiron');'''
    cursor.execute(insert_diseases_table_query)
    conn.commit()

except Error as error:
    print(error)
finally:
    cursor.close()
    conn.close()