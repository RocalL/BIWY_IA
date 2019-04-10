import psycopg2

def bdd_connect():
    try:
        connection = psycopg2.connect(user='tfrieerfftsnhh',password='fc3f34cad9dc486ee12dae073396bcdd394ec341ea4ca14269dd623563e46ee4',host='ec2-54-228-252-67.eu-west-1.compute.amazonaws.com',database='dbnnftuqdohm1v',port='5432')
    except (Exception, psycopg2.Error) as error :
        connection.rollback()
        print("Failed inserting record into python_users table {}".format(error))
    finally:
        if(connection):
            return connection

def bdd_get_p_from_cp(id_checkpoint):
    connection = bdd_connect()
    sql_select_query = """select presence_id_person from "presence" where presence_id_checkpoint = %s"""
    cursor = connection.cursor()
    cursor.execute(sql_select_query, (id_checkpoint,))
    result = []
    for i in cursor.fetchall():
        result.append(i[0])
    cursor.close()
    connection.close()
    return result

def bdd_insert_presence(update_time, id_checkpoint):
    connection = bdd_connect()
    cursor = connection.cursor()
    for i in update_time:
        date = update_time[i]
        cursor.execute("""update "presence" set presence_check_time = %s where presence_id_person = %s and presence_id_checkpoint = %s""",(update_time[i],i,str(1)))
    cursor.close()
    connection.commit()
    connection.close()
