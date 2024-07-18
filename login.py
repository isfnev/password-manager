import oracledb

conn = oracledb.connect(user='abhishek', password='negi88412', dsn='localhost:1521/XEPDB1')
cursor = conn.cursor()

def create_account(email:str, password:str)->None:
    if (check_element_presence(email)):
        print('There is an account already linked with it')
    else:
        try:
            cursor.execute(f"insert into logindb(email, password) values ('{email}', '{password}')")
            conn.commit()
        except oracledb.DatabaseError as e:
            print(f'Database error:{e}')

def show_logindb()->None:
    try:
        cursor.execute('select * from logindb')
    except oracledb.DatabaseError as e:
        print(f'Database error:{e}')
    for i in cursor:
        print(i)

def check_element_presence(value:str)->bool:
    cursor = conn.cursor()
    try:
        query = f"SELECT 1 FROM logindb WHERE email = :value"
        cursor.execute(query, value=value)

        result = cursor.fetchone()

        return result is not None
    except oracledb.DatabaseError as e:
        print(f"Database error: {e}")
        return False

def main():
    create_account('ksdfkj@gmsdkfjksjil','skdjkfjsew')
    show_logindb()
    cursor.close()
    conn.close()

if __name__=='__main__':
    main()
