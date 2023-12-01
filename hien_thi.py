import numpy as np
import os
import pickle, sqlite3
import cv2
from PIL import Image
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer = cv2.face_LBPHFaceRecognizer.create()
#recognizer.read("huanluyen/huanluyen.yml")
recognizer.read("detect person/trainer/face_trainner.yml")
dataChamCong = sqlite3.connect("D:/Python/Python_DA5/DataChamCong.db")  

try:
    # Đọc dữ liệu từ trong file Traning 
    recognizer.read("detect person/trainer/face_trainner.yml")
except cv2.error as e:
    print(f"OpenCV Error: {e}")

# Hàm đọc dữ liệu từ file DuLieuNguoiDung    
def getProfile(Id):
    conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db") 
    query="SELECT * FROM Person WHERE ID="+str(Id)
    cursor=conn.execute(query)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
def luuThoiGianChamCong(id, name):
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
    a = f"{gio}:{phut}"
    b = f"{ngay}/{thang}/{nam}"
    # In giá trị của a và b
    print("a:", a)
    print("b:", b)
    # Lưu dữ liệu vào trong SQL
    query = "INSERT INTO ChamCong(ID, Name, ThoiGian, NgayThangNam) VALUES (?, ?, ?, ?)"
    dataChamCong.execute(query, (id, name, a, b))
    dataChamCong.commit()  # Thêm dòng này để xác nhận thay đổi
    dataChamCong.close()  # Đóng kết nối           
    print("Thêm thông tin người dùng thành công.") 
# luuThoiGianChamCong()
# Hàm tìm kiến thông tin của người dùng
def searchID(id):
    cursor = dataChamCong.cursor()
    cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
    result = cursor.fetchall()
    return result

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
while True:
    #comment the next line and make sure the image being read is names img when using imread
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        # Du doan khuon mat
        nbr_predicted, conf = recognizer.predict(gray[y:y+h, x:x+w])
        # Neu dung thi 
        if conf < 90:   
            profile=getProfile(nbr_predicted)
            if profile != None:
                # Lấy dữ liệu từ trong SQL id được lưu trước tên
                cv2.putText(img, ""+str(profile[1]), (x+10, y), font, 1, (0,255,0), 1);
                luuThoiGianChamCong(profile[0], profile[1])
                print("Chấm công thành công")
        else:
            cv2.putText(img, "Unknown", (x, y + h + 30), font, 0.4, (0, 255, 0), 1);
    cv2.imshow('img', img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
# ids = searchID(id)
# for row in ids:
#     print(f"ID: {row[0]}, Name: {row[1]}")