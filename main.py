import cv2
import numpy as np
import os
import unidecode
import sqlite3
from datetime import datetime, timedelta
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Tạo thư mục lưu ảnh nếu chưa tồn tại
face_images_folder = 'D:/Python/Python_DA5/face_images_folder'
# Thêm thông tin người dùng vào cơ sở dữ liệu
conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db")  
cursor = conn.cursor()
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Person(
        ID INTEGER,
        Name TEXT
    );
''')
if not os.path.exists(face_images_folder):
    os.makedirs(face_images_folder)
def KhoiTaoCap():
    cap = cv2.VideoCapture(0)  # Sử dụng 0 thay vì 1 để chọn webcam mặc định (hoặc 1 nếu bạn muốn chọn webcam thứ hai).
    cap.set(3, 640)
    cap.set(4, 480)   
    return cap
def remove_accent(input_str):
    # Hàm loại bỏ dấu từ chuỗi
    return unidecode.unidecode(input_str)
# Kiểm tra xem ID có tồn tại hay chưa
# Tạo cơ sở dữ liệu lưu tên và id cho NHIỀU nhân viên
def KiemTraId(id):
    conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db")  
    # Kiểm tra xem id đã tồn tại trong CSDL chưa
    cursor = conn.execute("SELECT * FROM Person WHERE ID=?", (id,))
    isRecordExist = cursor.fetchone() 
    return isRecordExist
def QuetKhuonMat(user_name, user_id):
    cap = KhoiTaoCap()
    sample_number = 0
    while sample_number < 20:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sample_number += 1
            # Lưu ảnh với định dạng: User.[id].[sample_number].jpg
            img_path = os.path.join(face_images_folder, f'{user_name}.{user_id}.{sample_number}.jpg')
            print("Lưu thành công")
            cv2.imwrite(img_path, img[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Vẽ khung cho mặt hình ảnh
        cv2.imshow('img', img)
        cv2.waitKey(300)  # Delay 300 milliseconds between frames
    print("Quá trình lưu ảnh kết thúc.")

def taoSQLCho1Nguoi():

    db_name = f"test01"
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect(db_name + '.db')

    # Tạo một đối tượng cursor từ kết nối
    cursor = conn.cursor()
    # Tạo bảng trong cơ sở dữ liệu
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name}(
            user_id INTEGER,
            username TEXT,
            thoigian TEXT,
            ngaythangnam INTEGER
        );
    ''')
    print(f"Cơ sở dữ liệu '{db_name}.db' đã được tạo và người dùng đã được thêm vào.")

def ThemThongTinNhanVien(id):
    if not KiemTraId(id):
        print(f"Không có {id}")
        user_name = input("Nhập Name: ")
        name = remove_accent(user_name.capitalize())
        QuetKhuonMat(name, id)
        taoSQLCho1Nguoi()
        query = "INSERT INTO Person(ID, Name) VALUES (?, ?)"
        conn.execute(query, (id, name))
        conn.commit()  # Thêm dòng này để xác nhận thay đổi
        conn.close()  # Đóng kết nối           
        print("Thêm thông tin người dùng thành công.")    
    else:
        print("Có " + id)
def XoaThongTin(id):
    if KiemTraId(id): # Có có id
        # Xóa thông tin người dùng khỏi CSDL SQL
        ids = searchIDataChamCong(id)
        idss = ids[0][0]
        if idss: 
            cursor = conn.cursor() 
            cursor.execute("DELETE FROM Person WHERE ID=?", (id,))            
            name = ids[0][1]
            # Xóa các tệp tin ảnh liên quan
            for file in os.listdir(face_images_folder):
                if file.startswith(f'{name}.{id}.'):
                    file_path = os.path.join(face_images_folder, file)
                    os.remove(file_path)
            conn.commit()
            conn.close()        
            print(f"Đã xóa thông tin người dùng với ID {id} và tất cả ảnh liên quan.")
        else:
            print(f"Không tìm thấy người dùng với ID {id}.")
    else:
        print(f"Không tìm thấy người dùng với ID {id}.")
# Hàm tìm kiến thông tin của người dùng trong cơ sở dữ liệu DULIEUNGUOIDUNG.DB
def searchIDataChamCong(id):
    conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db") 
    cursor = conn.cursor()
    # id = input("Nhap ID: ")
    cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result
def searchName(name):
    cursor = conn.cursor()
    # name = input("Nhap Name: ")
    cursor.execute("SELECT * FROM Person WHERE Name=?", (name,))
    result = cursor.fetchall()
    return result

# //////////////////////////////////////////////////////////////////////////////////////////////
# // Truy xuất CSDL cho MỘT nhân viên
# Tạo SQL cho MỘT người dung

# Them du lieu nguoi dung cham cong
def chamcong(id):
    # Thoi gian hien tai
    thoi_gian_hien_tai = datetime.now()
    # Lay thoi gian thong tin ve gio, phut, ngay, thang, nam
    gio = thoi_gian_hien_tai.hour
    phut = thoi_gian_hien_tai.minute
    ngay = thoi_gian_hien_tai.day
    thang = thoi_gian_hien_tai.month
    nam = thoi_gian_hien_tai.year
    # Tạo biến a và b
    if 0 < gio < 10:
        gio = f"0{gio}"
    if 0 < phut < 10:
        phut = f"0{phut}"
    thoigian = f"{gio}:{phut}"
    ngaythangnam = f"{ngay}/{thang}/{nam}"
    ids = searchIDataChamCong(id)
    user_id = ids[0][0]
    username = ids[0][1]
    db_name = f"test01"
    db_name_table = f"test"
    # db_name = f"{username}_{user_id}"
    conn = sqlite3.connect(db_name + '.db')
    cursor = conn.cursor()
    # Thêm người dùng mới vào bảng
    cursor.execute(f"INSERT INTO {db_name_table} (id, name, thoigian, ngaythangnam) VALUES (?, ?, ?, ?)", (user_id, username, thoigian, ngaythangnam))
    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    print(f"Chấm công hoàn thành.")    
# Hàm tìm kiếm thông tin trong cơ sở dữ liệu được tạo từ TÊN NGƯỜI DÙNG VÀ ID THUONG.1.DB......
def searchID(id):
    ids = searchIDataChamCong(id)
    idss = ids[0][0]
    names = ids[0][1]
    db_name = f"{names}_{idss}"
    # conn = sqlite3.connect(db_name + '.db')
    conn = sqlite3.connect("D:/Python/Python_DA5/test01.db")  
    cursor = conn.cursor()
    # id = input("Nhap ID: ")
    # Chọn tất cả cả dữ liệu có id cần tìm kiếm
    # cursor.execute(f"SELECT * FROM {db_name} WHERE user_id=?", (id,))
    cursor.execute(f"SELECT * FROM test WHERE id=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result
# Hàm lấy tất cả ngày chấm công của nhân 1 nhân viên
def getNgayChamCong(id):
    ids = searchIDataChamCong(id)
    idss = ids[0][0]
    names = ids[0][1]
    db_name = f"{names}_{idss}"
    # conn = sqlite3.connect(db_name + '.db')
    conn = sqlite3.connect("D:/Python/Python_DA5/Thuong_0.db")  
    cursor = conn.cursor()
    # id = input("Nhap ID: ")
    # Chọn tất cả cả dữ liệu có id cần tìm kiếm
    cursor.execute(f"SELECT ngaythangnam FROM Thuong_0 WHERE user_id=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result
# Hàm lấy tất cả ngày và giờ chấm công
def getGioChamCong(id):
    ids = searchIDataChamCong(id)
    idss = ids[0][0]
    names = ids[0][1]
    db_name = f"{names}_{idss}"
    conn = sqlite3.connect(db_name + '.db')
    cursor = conn.cursor()
    # id = input("Nhap ID: ")
    # Chọn tất cả cả dữ liệu có id cần tìm kiếm
    cursor.execute(f"SELECT thoigian FROM {db_name} WHERE user_id=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result   
# Hàm cập nhật
def CapNhat(id):
    if KiemTraId(id):
        # cursor = conn.cursor()
        ids = searchID(id)
        name = ids[0][1]     
        # Xóa ảnh cũ
        for file in os.listdir(face_images_folder):
            if file.startswith(f'{name}.{id}.'):
                file_path = os.path.join(face_images_folder, file)
                os.remove(file_path)
        name1 = input("Nhập Name thay thế: ")
        while True:
            try:
                user_input = input("Nhập id: ")
                intid = int(user_input)
                break
            except ValueError:
                print("Vui lòng chỉ nhập id là số")
        QuetKhuonMat(name1, intid)
        query = "UPDATE Person SET Name=? WHERE ID=?"
        conn.execute(query, (name1, id))
        print("Name: " + name1)
        conn.commit()
        conn.close()
        print("Cập nhập thông tin người dùng thành công.")
    else:
        print(f"Không tìm thấy người dùng với ID {id}.")
# Hàm lấy thời gian nhập dữ liệu
def thoi_Gian():
    # Thoi gian hien tai
    thoi_gian_hien_tai = datetime.now()
    # Lay thoi gian thong tin ve gio, phut, ngay, thang, nam
    gio = thoi_gian_hien_tai.hour
    phut = thoi_gian_hien_tai.minute
    ngay = thoi_gian_hien_tai.day
    thang = thoi_gian_hien_tai.month
    nam = thoi_gian_hien_tai.year
    print(f"Thời gian nhập thông tin: {gio}:{phut} Ngày {ngay}/{thang}/{nam}")
# Hàm kiểm tra 1 tháng nhân viên đi làm bao nhiêu ngày
# Không dùng hàm này
def soNgayDiLamTrongThang(id):
    data = getNgayChamCong(id)
    # data = [('2/12/2023',), ('2/12/2023',), ('2/12/2023',), ('2/12/2023',)]
    print(f"Danh sach cham cong: {data}")
    month = input("Nhập tháng cần kiểm tra: ")
    year = input("Nhập năm cần kiểm tra: ")   
    parsed_dates = [datetime.strptime(date[0], "%d/%m/%Y") for date in data]
    # filtered_dates = {date.strftime("%d/%m/%Y"): [] for date in parsed_dates}
    # Lọc ra những ngày khác nhau nhưng cùng thuộc tháng 12 năm 2023
    unique_dates = set(date.strftime("%d/%m/%Y") for date in parsed_dates if date.month == int(month) and date.year == int(year))

    # In số ngày khác nhau
    # print(f"Số ngày khác nhau trong tháng {month} năm 2023: {len(unique_dates)}")
    return len(unique_dates)
    # return len(unique_dates)
# Ham nhập tháng cần kiểm tra
def nhapThangKiemTra():
    while True:
        month = input("Nhập tháng cần kiểm tra (1-12): ")
        if month.isdigit() and 1 <= int(month) <= 12:
            return int(month)
        else:
            print("Vui lòng nhập một số từ 1 đến 12.")
# Hàm nhập năm kiểm tra
def nhapNamKiemTra():
    while True:
        year = input("Nhập năm cần kiểm tra (4 chữ số): ")
        if year.isdigit() and len(year) == 4:
            return int(year)
        else:
            print("Vui lòng nhập một số có 4 chữ số.")   
# Kiểm tra số lượng ngày đi làm
def soNgayDiLamTrongThang_(id):
    data = searchID(id)   
    month = nhapThangKiemTra()
    year = nhapNamKiemTra()  
    
    unique_dates = set(entry[3] for entry in data if datetime.strptime(entry[3], "%d/%m/%Y").month == int(month) and datetime.strptime(entry[3], "%d/%m/%Y").year == int(year))

    return len(unique_dates)
# Hàm Kiểm tra nhân viên đi làm có đủ 8 tiếng 1 ngày hay không
def KiemTraThoiGianLamTungNgay(id):
    # data = searchID(id)   
    month = nhapThangKiemTra()
    year = nhapNamKiemTra()
    data = [
        (1, 'Thuong', '02:41', '1/12/2023'),
        (1, 'Thuong', '02:42', '2/12/2023'),
        (1, 'Thuong', '16:27', '3/12/2023'),
        (1, 'Thuong', '16:28', '4/12/2023'),
        (1, 'Thuong', '02:41', '5/12/2023'),
        (1, 'Thuong', '02:42', '6/12/2023'),
        (1, 'Thuong', '16:27', '7/12/2023'),
        (1, 'Thuong', '16:28', '8/12/2023'),
        (1, 'Thuong', '02:41', '9/12/2023'),
        (1, 'Thuong', '02:42', '10/12/2023'),
        (1, 'Thuong', '02:41', '11/12/2023'),
        (1, 'Thuong', '02:42', '12/12/2023'),
        (1, 'Thuong', '16:27', '13/12/2023'),
        (1, 'Thuong', '16:28', '14/12/2023'),
        (1, 'Thuong', '02:41', '15/12/2023'),
        (1, 'Thuong', '02:42', '16/12/2023'),
        (1, 'Thuong', '16:27', '17/12/2023'),
        (1, 'Thuong', '16:28', '18/12/2023'),
        (1, 'Thuong', '02:41', '19/12/2023'),
        (1, 'Thuong', '02:42', '20/12/2023'),
        (1, 'Thuong', '02:41', '21/12/2023'),
        (1, 'Thuong', '02:42', '22/12/2023'),
        (1, 'Thuong', '16:27', '23/12/2023'),
        (1, 'Thuong', '16:28', '24/12/2023'),
        (1, 'Thuong', '02:41', '25/12/2023'),
        (1, 'Thuong', '02:42', '26/12/2023'),
        (1, 'Thuong', '16:27', '27/12/2023'),
        (1, 'Thuong', '16:28', '28/12/2023'),
        (1, 'Thuong', '02:41', '29/12/2023'),
        (1, 'Thuong', '02:42', '30/12/2023'),
        (1, 'Thuong', '02:41', '2/1/2024'),
        (1, 'Thuong', '02:42', '2/1/2024'),
        (1, 'Thuong', '16:27', '3/2/2024'),
        (1, 'Thuong', '16:28', '3/2/2024'),
        (1, 'Thuong', '03:41', '1/12/2023'),
        (1, 'Thuong', '03:42', '2/12/2023'),
        (1, 'Thuong', '17:27', '3/12/2023'),
        (1, 'Thuong', '17:28', '4/12/2023'),
        (1, 'Thuong', '03:41', '5/12/2023'),
        (1, 'Thuong', '03:42', '6/12/2023'),
        (1, 'Thuong', '17:27', '7/12/2023'),
        (1, 'Thuong', '17:28', '8/12/2023'),
        (1, 'Thuong', '03:41', '9/12/2023'),
        (1, 'Thuong', '03:42', '10/12/2023'),
        (1, 'Thuong', '03:41', '11/12/2023'),
        (1, 'Thuong', '03:42', '12/12/2023'),
        (1, 'Thuong', '17:27', '13/12/2023'),
        (1, 'Thuong', '17:28', '14/12/2023'),
        (1, 'Thuong', '03:41', '15/12/2023'),
        (1, 'Thuong', '03:42', '16/12/2023'),
        (1, 'Thuong', '17:27', '17/12/2023'),
        (1, 'Thuong', '17:28', '18/12/2023'),
        (1, 'Thuong', '03:41', '19/12/2023'),
        (1, 'Thuong', '03:42', '20/12/2023'),
        (1, 'Thuong', '03:41', '21/12/2023'),
        (1, 'Thuong', '03:42', '22/12/2023'),
        (1, 'Thuong', '17:27', '23/12/2023'),
        (1, 'Thuong', '17:28', '24/12/2023'),
        (1, 'Thuong', '03:41', '25/12/2023'),
        (1, 'Thuong', '03:42', '26/12/2023'),
        (1, 'Thuong', '17:27', '27/12/2023'),
        (1, 'Thuong', '17:28', '28/12/2023'),
        (1, 'Thuong', '03:41', '29/12/2023'),
        (1, 'Thuong', '03:42', '30/12/2023'),
        (1, 'Thuong', '03:41', '2/1/2024'),
        (1, 'Thuong', '03:42', '2/1/2024'),
        (1, 'Thuong', '17:27', '3/2/2024'),
        (1, 'Thuong', '17:28', '3/2/2024')
    ]    
    # Tìm tất cả các ngày duy nhất trong dữ liệu thuộc tháng 12 năm 2023
    # Lọc chỉ những ngày thuộc tháng 12 năm 2023
    filtered_data = [entry for entry in data if datetime.strptime(entry[3], "%d/%m/%Y").month == month and datetime.strptime(entry[3], "%d/%m/%Y").year == year]

    # Tạo danh sách để lưu trữ kết quả
    time_differences_by_date = {}

    # Lặp qua các ngày duy nhất và tính hiệu thời gian cho mỗi ngày
    for entry in filtered_data:
        target_date = entry[3]  # Sử dụng index 3 để truy cập ngày
        time_str = entry[2]  # Sử dụng index 2 để truy cập thời gian
        datetime_obj = datetime.strptime(time_str, "%H:%M")
        
        if target_date not in time_differences_by_date:
            time_differences_by_date[target_date] = []

        time_differences_by_date[target_date].append(datetime_obj)

    # Hiển thị kết quả
    for date, times_on_target_date in time_differences_by_date.items():
        if len(times_on_target_date) >= 2:
            max_time = max(times_on_target_date)
            min_time = min(times_on_target_date)
            time_difference = max_time - min_time
            print(f"Số giờ đi làm trong ngày {date}: {time_difference}")
        else:
            print(f"Không đủ dữ liệu để tính hiệu thời gian trong ngày {date}")

# Nhập id 
            
while True:
    try:
        user_input = input("Nhập id: ")
        id = int(user_input)
        break
    except ValueError:
         print("Lỗi nhập lại id")
# Lấy toàn bộ dữ liệu từ bảng Person
# cursor.execute('SELECT * FROM Person')
# rows = cursor.fetchall()

# # In dữ liệu ra màn hình
# for row in rows:
#     print(row)

# # Đóng kết nối
# conn.close()
# ThemThongTinNhanVien(id)  
# chamcong(id)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Bắt đầu gọi các hàm
# result = searchIDataChamCong(id)
# print(result)

# print(data[0])
ids = searchID(1)
print(ids)
# for row in ids:
#     print(f"ID: {row[0]}, Name: {row[1]}, Time: {row[2]}, Date: {row[3]}")
#     print(f"Ngày chấm công: {row[3]}")

# print("Name: " + name)
# id = input("Nhập name: ")
# ids = searchName(id)
# for row in ids:
#     print(f"ID: {row[0]}, Name: {row[1]}")

# XoaThongTin(id)
         

# CapNhat(id)
# thoi_Gian()
# taoSQLCho1Nguoi()

# sn = soNgayDiLamTrongThang(id)
# print(f"Số ngày đi làm: {sn}")
# print(soNgayDiLamTrongThang_(1))
# print(len(soNgayDiLamTrongThang1(1)))
# KiemTraThoiGianLamTungNgay(1)

















