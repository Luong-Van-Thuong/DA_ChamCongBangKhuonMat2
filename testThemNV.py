import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db")  
cursor = conn.cursor()

# Tạo bảng (nếu chưa tồn tại)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Person(
        ID INTEGER,
        Name TEXT
    );
''')

# Nhập dữ liệu từ người dùng
user_id = int(input("Nhập ID: "))
user_name = input("Nhập tên: ")

# Thêm dữ liệu vào bảng Person
cursor.execute('INSERT INTO Person (ID, Name) VALUES (?, ?)', (user_id, user_name))

# Lưu (commit) thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng kết nối
conn.close()