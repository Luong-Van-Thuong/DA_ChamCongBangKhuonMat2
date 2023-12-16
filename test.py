import sqlite3
from datetime import datetime, timedelta
conn = sqlite3.connect("D:/Python/Python_DA5/test01.db") 
def themtt():
    while True:
        user_input = input("Nhập id: ")
        id = int(user_input)
        name = input("Nhập tên: ")
        gio = input("Nhập giờ: ")
        phut = input("Nhập phút: ")
        ngay = input("Nhập ngày: ")
        thang = input("Nhập tháng: ")
        nam = input("Nhập năm: ")
        thoigian = f"{gio}:{phut}"
        ngaythangnam = f"{ngay}/{thang}/{nam}"
        query = "INSERT INTO test (id, name, thoigian, ngaythangnam) VALUES (?, ?, ?, ?)"
        conn.execute(query, (id, name, thoigian, ngaythangnam))
        conn.commit()  # Thêm dòng này để xác nhận thay đổi
          # Đóng kết nối           
        print("Thêm thông tin người dùng thành công.")   
        i = input("Bạn có muốn nhập tiếp nữa hay không(có:1/không:0): ")
        if(i == "0"):
            break
    conn.close()
def hienthi():
    # Tạo đối tượng cursor
    cursor = conn.cursor()

    # Thực hiện truy vấn SELECT để lấy toàn bộ dữ liệu từ bảng 'test'
    cursor.execute('SELECT * FROM test')

    # Lấy tất cả các dòng dữ liệu
    all_data = cursor.fetchall()

    # In dữ liệu
    for row in all_data:
        print(row)

    # Đóng kết nối
    conn.close()
# themtt()
hienthi()


















