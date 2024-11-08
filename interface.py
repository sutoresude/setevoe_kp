import mysql.connector
from mysql.connector import Error

db_host="localhost"
print("Здравствуйте, вас приветствует база данных поликлиники, введите,пожалуйста ваше имя пользователя")
user_name=input()
print("Введите,пожалуйста ваш пароль")
user_password=input()

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
conn = create_connection_mysql_db(db_host,
                                  user_name,
                                  user_password,
                                  "Poliklinika")
cursor = conn.cursor()

print("Кто вы? если работник регистратуры введите 1, если администратор введите 2")
post=int(input())
if post==1:
    print("Что вы хотите сделать?"
          "Если узнать информацию о пациенте введите 1")
    what1 = int(input())
    if what1 == 1:
        print("Введите ФИО(на английском языке) пациента")
        what2 = str(input())
        print("Что вы хотите сделать?"
              "Если узнать  адрес, дата заболевания, диагноз данного больного введите 1, "
              "Если ФИО лечащего врача данного больного введите 2")
        what3 = int(input())
        if what3 == 1:
            select_patient_query ="SELECT address, date_of_disease, diagnosis FROM patients WHERE fullname = %s"
            cursor.execute(select_patient_query, ((what2,)))
            query_result = cursor.fetchall()
            for x in query_result:
                z=x
                print(x)
        print("Что вы хотите сделать?"
              "Cимптомы данного заболевания и рекомендуемое лекарство введите 1")
        what34 = int(input())
        if what3 == 1:
            select_patient_query ="SELECT symptoms, medicine FROM diseases WHERE name = %s"
            cursor.execute(select_patient_query, ((z[2],)))
            query_result = cursor.fetchall()
            for x in query_result:
                print(x)

        elif what3 == 2:
            select_patient_query = "SELECT doctor FROM patients WHERE fullname = %s"
            cursor.execute(select_patient_query, ((what2,)))
            query_result = cursor.fetchall()
            for x in query_result:
                y=x
                print(x)
            print("Что вы хотите сделать дальше?"
                  "Если узнать номер кабинета, дни и часы приема данного врача, введите 1, "
                  "Если узнать больных, находящихся на лечении у данного врача, введите 2")
            what4 = int(input())
            if what4 == 1:
                select_patient_query = "SELECT room_number, date_and_time_of_work FROM doctors WHERE fullname = %s"
                cursor.execute(select_patient_query, ((y[0],)))
                query_result = cursor.fetchall()
                for x in query_result:
                    print(x)

            else:
                select_patient_query = "SELECT fullname FROM patients WHERE doctor = %s"
                cursor.execute(select_patient_query, ((y[0],)))
                query_result = cursor.fetchall()
                for x in query_result:
                    print(x)



elif post==2:

    print("Что вы хотите сделать?"
              "Если добавить нового больного, введите 1, "
              "Если уволить врача, введите 2"
              "Если изменить диагноз, введите 3"
              "Если получить отчет о работе поликлиники, введите 4")
    what5 = int(input())
    if what5 == 1:
        print('Введите полное имя на английском языке')
        fullname = str(input())
        print('Введите адрес на английском языке')
        address = str(input())
        print('Введите название болезни на английском языке')
        diagnosis = str(input())
        print('Введите дату заболевания в формате число.месяц.год')
        date_of_disease = str(input())
        print('Введите полное имя доктора на английском языке')
        doctor = str(input())
        val = (fullname, address, diagnosis, date_of_disease, doctor)
        insert_patients_table_query = '''
            INSERT INTO
            `patients` (`fullname`, `address`, `diagnosis`, `date_of_disease`, `doctor`) 
            VALUES
            (%s, %s, %s, %s, %s);'''
        cursor.execute(insert_patients_table_query, val)
        conn.commit()
    elif what5 == 2:
        print('Введите полное имя на английском языке доктора, которого хотите уволить')
        fulname = str(input())
        delete_doctor_doctors_query = '''
            DELETE FROM doctors WHERE fullname = %s;
            '''
        cursor.execute(delete_doctor_doctors_query, ((fulname, )))
        conn.commit()
    elif what5 == 3:
        print('Введите имя больного диагноз, которое хотите изменить')
        patient = str(input())
        print('Введите диагноз, на который хотите изменить')
        diag = str(input())
        val2=(diag, patient)
        update_patient_query = '''
            UPDATE patients SET diagnosis = %s WHERE fullname = %s;
            '''
        cursor.execute(update_patient_query, val2)
        conn.commit()
    elif what5 == 4:
        print('В поликлинике на данный момент количество больных равно:')
        cursor.execute("SELECT COUNT(*) FROM patients")
        result = cursor.fetchone()[0]
        print(result)
        print('В поликлинике на данный момент работают следующие врачи:')
        cursor.execute("SELECT fullname FROM doctors")
        for row in cursor.fetchall():
            print(row[0])
        print('В поликлинике на данный момент чисто заболеваний по каждому виду болезней')
        query = "SELECT diagnosis, COUNT(*) AS count FROM patients GROUP BY diagnosis"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row[0], "-", row[1])
        print('Расписание работы докторов сейчас следущее:')
        query = ("SELECT fullname, date_and_time_of_work FROM doctors")
        cursor.execute(query)
        for (fullname, date_and_time_of_work) in cursor:
            print(f"Доктор {fullname}: {date_and_time_of_work}")