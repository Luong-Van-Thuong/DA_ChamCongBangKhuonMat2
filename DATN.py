import numpy as np
import os
import sqlite3
import cv2
from datetime import datetime
from PIL import Image
import numpy as np
import pandas as pd
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Tạo thư mục lưu ảnh nếu chưa tồn tại
current_directory = os.getcwd()
# Tao folder anh
folder_name = "face_images_folder"
face_images_folder = os.path.join(current_directory, folder_name)
os.makedirs(face_images_folder, exist_ok=True)
# Tao file data          
file_sql = "DuLieuNguoiDung.db"
datafile = os.path.join(current_directory, file_sql)
ketNoiData = sqlite3.connect(datafile)
cursor = ketNoiData.cursor()
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Person(
        ID INTEGER,
        Name TEXT
    );
''')
# Tao file data
file_sql2 = "test01.db"
datafile2 = os.path.join(current_directory, file_sql2)
ketNoiData2 = sqlite3.connect(datafile2)
cursor1 = ketNoiData2.cursor()
cursor1.execute(f'''
    CREATE TABLE IF NOT EXISTS test(
        id INTEGER,
        name TEXT, 
        thoigian TEXT,
        ngaythangnam INTEGER
    );
''')
# Tao duong dan file test01
# file_sql3 = "test01.db"
# datafile3 = os.path.join(current_directory, file_sql3)
def xoaToanBoDuLieu():
    cursor = ketNoiData.cursor()
    cursor.execute("DELETE FROM Person")  # Thay 'table_name' bằng tên bảng bạn muốn xóa dữ liệu
    ketNoiData.commit()
    print("Xóa toàn bộ dữ liệu thành công.")
def layToanBoDuLieu():
    cursor = ketNoiData.cursor()
    cursor.execute("SELECT * FROM Person")  # Thay 'table_name' bằng tên bảng bạn muốn lấy dữ liệu
    rows = cursor.fetchall()
    return rows

def KiemTraId(id):
    cursor = ketNoiData.cursor()  # Sử dụng con trỏ của kết nối đến cơ sở dữ liệu
    cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
    row = cursor.fetchone()
    return row is not None
def KhoiTaoCap():
    cap = cv2.VideoCapture(0)  # Sử dụng 0 thay vì 1 để chọn webcam mặc định (hoặc 1 nếu bạn muốn chọn webcam thứ hai).
    cap.set(3, 640)
    cap.set(4, 480)   
    return cap
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
    cap.release()
def themMoiNhanVien():
    print("Chay ham nay")
    id1 = input("Nhap id: ")
    id = int(id1)
    name = input("Nhap ten: ")
    if (KiemTraId(id) != None):
        print(f"Thêm {id}")
        QuetKhuonMat(name, id)
        cursor = ketNoiData.cursor()
        query = "INSERT INTO Person(ID, Name) VALUES (?, ?)"
        cursor.execute(query, (id, name))
        ketNoiData.commit()  # Thêm dòng này để xác nhận thay đổi
        ketNoiData.close()  # Đóng kết nối           
        print("Thêm thông tin người dùng thành công.")    
    else:
        print("Có id " + str(id) + " trong danh sách rồi")
def training():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = face_images_folder
    def getImagesWithID(path):
        imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces
    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)

    if not os.path.exists('detect person/trainer'):
        os.makedirs('detect person/trainer')

    recognizer.save("detect person/trainer/face_trainner.yml")
    cv2.destroyAllWindows()

def chamCong():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("detect person/trainer/face_trainner.yml")
    try:
    # Đọc dữ liệu từ trong file Traning 
        recognizer.read("detect person/trainer/face_trainner.yml")
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
    def getProfile(Id):
        # conn = sqlite3.connect(r"D:\DO AN 5\DOAN5_02\app\src\main\assets\DuLieuNguoiDung.db")  
        with sqlite3.connect(datafile) as conn:
            query="SELECT * FROM Person WHERE ID="+str(Id)
            cursor=conn.execute(query)
            profile=None
            for row in cursor:
                profile=row
        return profile
#     # Lấy thông in nhân viên thông qua id
    def searchIDataChamCong(id):
        # conn = sqlite3.connect(r"D:\DO AN 5\DOAN5_02\app\src\main\assets\DuLieuNguoiDung.db")  
        with sqlite3.connect(datafile) as conn:
            cursor = conn.cursor()
            # id = input("Nhap ID: ")
            cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
            result = cursor.fetchall()
        return result
    def luuThoiGianChamCong(id):
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
        # conn = sqlite3.connect(db_name + '.db')
        conn = sqlite3.connect(datafile2) 
        cursor = conn.cursor()

        # Truy vấn dữ liệu từ bảng 'test'
        query = "SELECT * FROM test"
        df = pd.read_sql_query(query, conn)
        df.to_excel('test01.xlsx', index=False) 
        # cursor.execute(f"INSERT INTO {db_name} (user_id, username, thoigian, ngaythangnam) VALUES (?, ?, ?, ?)", (user_id, username, thoigian, ngaythangnam))
        cursor.execute(f"INSERT INTO {db_name_table} (id, name, thoigian, ngaythangnam) VALUES (?, ?, ?, ?)", (user_id, username, thoigian, ngaythangnam))
        conn.commit()
        conn.close()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX
    luuHayKhongLuu = 0
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
                if profile is not None:
                    # Lấy dữ liệu từ trong SQL id được lưu trước tên
                    cv2.putText(img, ""+str(profile[1]) + str(profile[0]), (x+10, y), font, 1, (0,255,0), 1)
                    # luuThoiGianChamCong(profile[0], profile[1])
                    luuHayKhongLuu = 1
                    cv2.putText(img, "Cham cong thanh cong", (x-100, y-30), font, 1, (0,255,0), 1)
            else:
                cv2.putText(img, "Unknown", (x, y + h + 30), font, 0.4, (0, 255, 0), 1)
        cv2.imshow('img', img)
        if cv2.waitKey(1) == 27:
            break

    if(luuHayKhongLuu == 1):
        luuThoiGianChamCong(profile[0])
        print("CHẤM CÔNG THÀNH CÔNG")
    else:
        print("CHẤM CÔNG KHÔNG THÀNH CÔNG")
    cap.release()
    cv2.destroyAllWindows()


while True:
    print("Nhap chuc nang")
    print("1: Cham cong, 2: Them moi, 3: Training, 4: Xoa, 5: Hien thị")
    cn = input("Nhap cn: ")
    if(cn == "1"):
        chamCong()
    elif(cn == "2"):
        themMoiNhanVien()
    elif(cn == "3"):
        training()
    elif(cn == "4"):
        xoaToanBoDuLieu()
    elif(cn == "5"):
        layToanBoDuLieu()
    else:
        break













































