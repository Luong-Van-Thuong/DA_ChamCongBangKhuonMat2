import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import pickle, sqlite3
import cv2
from PIL import Image
from datetime import datetime

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
conn1 = sqlite3.connect("D:/Python/Python_DA5/test01.db")
cursor1 = conn1.cursor()
cursor1.execute(f'''
    CREATE TABLE IF NOT EXISTS test(
        id INTEGER,
        name TEXT, 
        thoigian TEXT,
        ngaythang
    );
''')

def KiemTraId(id):
    cursor = conn.execute("SELECT * FROM Person WHERE ID=?", (id,))
    isRecordExist = cursor.fetchone() 
    return isRecordExist

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

def themMoiNhanVien():
    id = int1.get()
    name = str1.get()
    if not KiemTraId(id):
        print(f"Thêm {id}")
        QuetKhuonMat(name, id)
        query = "INSERT INTO Person(ID, Name) VALUES (?, ?)"
        conn.execute(query, (id, name))
        conn.commit()  # Thêm dòng này để xác nhận thay đổi
        conn.close()  # Đóng kết nối           
        print("Thêm thông tin người dùng thành công.")    
    else:
        print("Có " + str(id))


def trainning():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    path = r'D:\Python\Python_DA5\face_images_folder'
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
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("detect person/trainer/face_trainner.yml")
    try:
    # Đọc dữ liệu từ trong file Traning 
        recognizer.read("detect person/trainer/face_trainner.yml")
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
    def getProfile(Id):
        conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db") 
        query="SELECT * FROM Person WHERE ID="+str(Id)
        cursor=conn.execute(query)
        profile=None
        for row in cursor:
            profile=row
        conn.close()
        return profile
    # Lấy thông in nhân viên thông qua id
    def searchIDataChamCong(id):
        conn = sqlite3.connect("D:/Python/Python_DA5/DuLieuNguoiDung.db") 
        cursor = conn.cursor()
        # id = input("Nhap ID: ")
        cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
        result = cursor.fetchall()
        conn.close()
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
        conn = sqlite3.connect(db_name + '.db')
        cursor = conn.cursor()
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
                if profile != None:
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





# Thực hiện hàm chạy 
win = tk.Tk()

win.title("He thong nhan dien khuon mat")
win.geometry('500x300')
win.configure(bg='#000000')
label = ttk.Label(win,text="Hệ Thống Nhận Diện Khuôn Mặt",background="grey",foreground="white",font=20)
label.grid(column =1, row =0)
label.place(x=100)

label1 = ttk.Label(win,text="Nhập thông tin người dùng",background="#263D42",foreground="white", font=20)  
label1.grid(column =1, row =2)
label1.place(y=40)

label1 = ttk.Label(win,text="Id:",background="#263D42",foreground="white", font=20)  
label1.grid(column =0, row =2)
label1.place(y=80)

label2 = ttk.Label(win,text="Name:",background="#263D42",foreground="white", font=20)
label2.grid(column =0, row =3)
label2.place(y=120)

# Tạo biến kiểu IntVar
int1 =tk.IntVar()
edit_id=ttk.Entry(win,textvariable=int1, width=50)
edit_id.grid(column =1, row =2)
edit_id.focus()
edit_id.place(x=90,y=80)

# Tạo biến kiểu StringVar
str1 =tk.StringVar()
edit_name=ttk.Entry(win,textvariable=str1,width=50)
edit_name.grid(column =1, row =3)
edit_name.place(x=90,y=120)

# Nút nhấn lấy dữ liệu
btlaydulieu= ttk.Button(win, text ="Thêm nhân viên", command=themMoiNhanVien)
btlaydulieu.grid(column =0, row =4)

#  Nút nhấn train dữ liệu
bttrain= ttk.Button(win, text ="Training", command=trainning)
bttrain.grid(column =1, row =4)

# # Nút nhấn nhận diện dữ liệu
btnhandien= ttk.Button(win, text ="Chấm công", command=chamCong)
btnhandien.grid(column =2, row =4)  

bttrain.place(x=200,y=200)
btnhandien.place(x=350,y=200)
btlaydulieu.place(x=50,y=200)

win.mainloop()
















