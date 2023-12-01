import cv2
import numpy as np
import os
import unidecode
import sqlite3
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Tạo thư mục lưu ảnh nếu chưa tồn tại
face_images_folder = 'D:/Python/Python_DA5/face_images_folder'
# Thêm thông tin người dùng vào cơ sở dữ liệu
conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db")  

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
def KiemTraId(id):
    # conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db")  
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

def ThemThongTin(id):
    if not KiemTraId(id):
        print(f"Không có {id}")
        user_name = input("Nhập Name: ")
        name = remove_accent(user_name.capitalize())
        QuetKhuonMat(name, id)
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
        ids = searchID(id)
        if ids: 
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


# Hàm tìm kiến thông tin của người dùng
def searchID(id):
    cursor = conn.cursor()
    # id = input("Nhap ID: ")
    cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
    result = cursor.fetchall()
    # if result:
    #     print("Kết quả tìm kiếm:")
    #     for row in result:
    #         print(f"ID: {row[0]}, Name: {row[1]}")
    # else:
    #     print("Không tìm thấy kết quả.")
    # conn.close()
    return result

def searchName(name):
    cursor = conn.cursor()
    # name = input("Nhap Name: ")
    cursor.execute("SELECT * FROM Person WHERE Name=?", (name,))
    result = cursor.fetchall()
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

while True:
    try:
        user_input = input("Nhập id: ")
        id = int(user_input)
        break
    except ValueError:
        print("Vui lòng chỉ nhập id là số")

# ids = searchID(id)
# for row in ids:
#     print(f"ID: {row[0]}, Name: {row[1]}")
# name = ids[0][1]
# print("Name: " + name)
# id = input("Nhập name: ")
# ids = searchName(id)
# for row in ids:
#     print(f"ID: {row[0]}, Name: {row[1]}")
# ThemThongTin(id)
# XoaThongTin(id)
CapNhat(id)
# thoi_Gian()


