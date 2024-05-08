import mysql.connector
#su dung thu vien tabulate -- cai dat: command prompt -> pip install tabulate
from tabulate import tabulate

# dinh nghia ham ket noi
def connectdatabase(database = ''):
    if(database == ''):
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = ''
        )
        print('Database not exists')
    else:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = database
        )
        print('Database is ', database)
    return connection

# dinh nghia ham tao database
def create_database(database):
    con = connectdatabase()
    cursor = con.cursor()
    cursor.execute('create database if not exists ' + database)
    print('Tao co so du lieu thanh cong!')

# dinh nghia ham tao bang
def create_table():
    con = connectdatabase('bkap01')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Computer (ComputerId INT AUTO_INCREMENT PRIMARY KEY, \
                    ComputerName VARCHAR(255), Price DECIMAL(10, 2),ProductionDate date, Quantity INT, Brand VARCHAR(255))")
    print('Tao bang thanh cong!')

#tao database & bang
database = 'bkap01'
create_database(database)
create_table()

# dinh nghia ham them du lieu va kiem tra trung ma
def insert_computer(database):
    con = connectdatabase(database)
    cursor = con.cursor()
    computer_id = input("Nhập mã máy tính: ")
    cursor.execute("SELECT * FROM Computer WHERE ComputerId = %s", (computer_id,))
    if cursor.fetchone() is not None:
        print("Mã máy tính đã tồn tại!")
        return

    computer_name = input("Nhập tên máy tính: ")
    price = float(input("Nhập giá máy tính: "))
    production_date = input('Nhap ngay thang nam san xuat (yyyy-MM-dd): ')
    quantity = int(input("Nhập số lượng máy tính: "))
    brand = input("Nhập hãng sản xuất: ")

    sql = "INSERT INTO Computer (ComputerId, ComputerName, Price, ProductionDate, Quantity, Brand) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (computer_id, computer_name, price, production_date, quantity, brand)
    cursor.execute(sql, values)
    con.commit()
    con.close()
    cursor.close()
    print("Đã thêm dữ liệu thành công!")

# dinh nghia ham show du lieu
def show_computer(database):
    con = connectdatabase(database) 
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Computer")
    rows = cursor.fetchall()
    table =[]
    for row in rows:
        table.append([row[0],row[1],row[2], row[3], row[4], row[5]])
    cursor.close()
    con.close()
    return table if table else False

# dinh nghia ham tim kiem du lieu theo id
def findById(database, id):
    con = connectdatabase(database)
    cursor = con.cursor()
    sql = 'SELECT * FROM Computer where ComputerId = %s'
    values = (id,)
    cursor.execute(sql,values)
    rows = cursor.fetchall()
    data =[]
    for row in rows:
        data.append([row[0],row[1],row[2], row[3], row[4], row[5]])
    cursor.close()
    con.close()
    return data[0] if data else False

# dinh nghia ham sua du lieu
def update_computer(database, id):
    if(findById(database, id)):
        con = connectdatabase(database) 
        cursor = con.cursor()
        sql = 'update Computer set ComputerName= %s, Price = %s, ProductionDate = %s, Quantity= %s, Brand= %s where ComputerId = %s'
        computer_name = input("Nhập tên máy tính: ")
        price = float(input("Nhập giá máy tính: "))
        production_date = input('Nhap ngay thang nam san xuat (yyyy-MM-dd): ')
        quantity = int(input("Nhập số lượng máy tính: "))
        brand = input("Nhập hãng sản xuất: ")
        values = (computer_name, price, production_date, quantity, brand, id)
        cursor.execute(sql, values)
        con.commit()
        con.close()
        cursor.close()
        print('Cap nhat thanh cong!')
    else:
        print('May tinh co ma', id, 'khong ton tai!')

# dinh nghia ham xoa du lieu
def remove_computer(database, id):
    con = connectdatabase(database) 
    cursor = con.cursor()
    computer_id = input("Nhập mã máy tính muốn xóa: ")
    cursor.execute("SELECT * FROM Computer WHERE ComputerId = %s", (computer_id,))
    if cursor.fetchone() is None:
        print("Không tìm thấy máy tính có mã", computer_id)
        return
    cursor.execute("DELETE FROM Computer WHERE ComputerId = %s", (computer_id,))
    con.commit()
    print("Đã xóa máy tính có mã", computer_id)
    cursor.close()
    con.close()

# dinh nghia ham tim kiem du lieu theo gia
def findByPrice(database, min, max):
    con = connectdatabase(database) 
    cursor = con.cursor()
    sql = 'select * from Computer where Price between %s and %s'
    values= (min, max)
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    table =[]
    for row in rows:
        table.append([row[0],row[1],row[2], row[3], row[4], row[5]])
    cursor.close()
    con.close()
    return table if table else False

# dinh nghia ham tim kiem theo ten 
def findByName(database, keyword):
    con = connectdatabase(database) 
    cursor = con.cursor()
    sql = "select * from Computer where ComputerName like %s"
    values = ('%'+ keyword + '%',)
    cursor.execute(sql,values)
    rows = cursor.fetchall()
    table = []
    for row in rows:
        table.append([row[0],row[1],row[2], row[3], row[4], row[5]])
    cursor.close()
    con.close()
    return table if table else False

# dinh nghia ham hien thi computer >200
def display_expensive_computers():
    con = connectdatabase(database) 
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Computer WHERE Price > 200")
    rows = cursor.fetchall()
    table = []
    if not rows:
        print("Không có máy tính nào có giá trên 200")
    else:
        print("Các máy tính có giá trên 200 là: ")
        for row in rows:
            table.append([row[0],row[1],row[2], row[3], row[4], row[5]])
    cursor.close()
    con.close()
    return table if table else False
    

def main():
    while True:
        print("\nMENU:")
        print("1. Them may tinh")
        print("2. Hien thi du lieu")
        print("3. Cap nhat du lieu")
        print("4. Xoa du lieu")
        print("5. Tim kiem du lieu theo khoang gia")
        print("6. Tim kiem du lieu theo ComputerName")
        print("7. Hien thi may tinh co gia > 200")
        print("8. Thoat")

        choice = input("Moi ban chon: ")

        if choice == "1":
            insert_computer(database)

        elif choice == "2":
            data = show_computer(database)
            if(data):
                print(tabulate(data, headers=['ComputerId', 'ComputerName', 'Price', 'ProductionDate', 'Quantity', 'Brand'], floatfmt=".0f"))
            else:
                print('Khong co du lieu trong bang!')

        elif choice == "3":
            id = input('Nhap ma may tinh can chinh sua: ')
            update_computer(database,id)

        elif choice =="4":
            id = input("Nhap ma may tinh can xoa: ")
            remove_computer(database, id)

        elif choice == "5":
            min = input("Nhap gia toi thieu: ")
            max = input('Nhap gia toi da: ')
            data = findByPrice(database, min, max)
            if(data):
                print(tabulate(data, headers=['ComputerId', 'ComputerName', 'Price', 'ProductionDate', 'Quantity', 'Brand'], floatfmt=".0f"))
            else:
                print('Khong co du lieu duoc tim thay!')
                
        elif choice == "6":
            keyword = input('Nhap ten may tinh can tim: ')
            data = findByName(database, keyword)
            if(data):
                print(tabulate(data, headers=['ComputerId', 'ComputerName', 'Price', 'ProductionDate', 'Quantity', 'Brand'], floatfmt=".0f"))
            else:
                print('Khong co du lieu duoc tim thay!')

        elif choice == "7":
            data = display_expensive_computers()
            if(data):
                print(tabulate(data, headers=['ComputerId', 'ComputerName', 'Price', 'ProductionDate', 'Quantity', 'Brand'], floatfmt=".0f"))
            else:
                print('Khong co du lieu trong bang!')

        elif choice == "8":
            break
        else:
            print("Lua chon khong hop le!")
        

if __name__ == "__main__":
    main()
    