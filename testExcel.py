import pandas as pd
import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('test01.db')  # Thay 'ten_file.db' bằng tên của cơ sở dữ liệu SQLite của bạn

# Truy vấn dữ liệu từ bảng 'test'
query = "SELECT * FROM test"
df = pd.read_sql_query(query, conn)

# Đóng kết nối đến cơ sở dữ liệu SQLite
conn.close()

# Lưu DataFrame vào tệp Excel
df.to_excel('test01.xlsx', index=False)  # Thay 'ten_file_excel.xlsx' bằng tên bạn muốn đặt cho tệp Excel

