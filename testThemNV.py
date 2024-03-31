import sqlite3
import os
file_sql = "DuLieuNguoiDung.db"
current_directory = os.getcwd()
datafile = os.path.join(current_directory, file_sql)
ketNoiData = sqlite3.connect(datafile)
cursor = ketNoiData.cursor()
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Person(
        ID INTEGER,
        Name TEXT
    );
''')
# Thực thi truy vấn để lấy dữ liệu từ bảng Person
cursor.execute("SELECT * FROM Person")

# Lấy tất cả các dòng dữ liệu
rows = cursor.fetchall()

# In ra dữ liệu
for row in rows:
    print(row)
    

# Đóng kết nối
ketNoiData.close()