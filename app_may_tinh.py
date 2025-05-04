import cv2
import numpy as np
import serial
import time
import tkinter as tk

try:
    ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)
    time.sleep(2)
    print("Serial kết nối thành công")
except:
    print("Lỗi: Không thể kết nối với Serial. Kiểm tra cổng COM")


var_meo_meo = 0  


lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])


cap = cv2.VideoCapture(0)

def send_serial():
    if ser.is_open:
        ser.write(f"{var_meo_meo}\n".encode())
        print(f"Đã gửi: {var_meo_meo}")
    else:
        print("Serial chưa mở!")

def detect_color():
    global var_meo_meo

    ret, frame = cap.read()
    if not ret:
        print("Không nhận được hình ảnh từ camera")
        root.after(100, detect_color)
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    detected_red = False
    detected_blue = False

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_red:
        if cv2.contourArea(contour) > 1000:
            detected_red = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Red Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_blue:
        if cv2.contourArea(contour) > 1000:
            detected_blue = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'Blue Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if detected_red:
        var_meo_meo = 1
    elif detected_blue:
        var_meo_meo = 2
    else:
        var_meo_meo = 0

    cv2.imshow('Camera', frame)
    root.after(10, detect_color)

root = tk.Tk()
root.title("3 DOF Robotic Arm Control App")
root.geometry("360x150")

btn_send = tk.Button(
    root, 
    text="BẮT ĐẦU GẮP", 
    command=send_serial, 
    font=("Arial", 16, "bold"),  # Cỡ chữ lớn hơn, in đậm
    bg="red",                 # Đổi màu nền thành cam
    fg="white",                  # Chữ màu trắng
    padx=20,                     # Tăng chiều rộng của nút
    pady=10,                     # Tăng chiều cao của nút
    borderwidth=5,               # Độ dày viền nút
    relief="raised"              # Hiệu ứng 3D nổi
)
btn_send.pack(pady=30)

detect_color()

root.mainloop()

cap.release()
cv2.destroyAllWindows()
ser.close()
