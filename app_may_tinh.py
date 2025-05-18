import cv2
import numpy as np
import serial
import time
import threading
import tkinter as tk

# === Cấu hình Serial ===
SERIAL_PORT = 'COM15'  # Thay đổi theo cổng Arduino
BAUD_RATE = 9600

# === Giao diện chính ===
root = tk.Tk()
root.title("Robot Vision Control")
root.geometry("300x120")

ser = None
last_sent_code = -1
latest_code = 0
latest_label = "Chưa có dữ liệu"

cap = cv2.VideoCapture(0)

def find_center(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))
    return centers

def detect_case(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([130, 255, 255])

    red_mask = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    red_centers = find_center(red_mask)
    blue_centers = find_center(blue_mask)

    width = frame.shape[1]
    mid = width // 2

    labels = []

    for cx, cy in red_centers:
        if cx < mid:
            labels.append("A:Red")
        else:
            labels.append("B:Red")

    for cx, cy in blue_centers:
        if cx < mid:
            labels.append("A:Blue")
        else:
            labels.append("B:Blue")

    # Mã trạng thái
    code = 0
    if labels == []:
        code = 0
    elif labels == ["A:Blue"]:
        code = 1
    elif labels == ["A:Red"]:
        code = 2
    elif labels == ["B:Blue"]:
        code = 3
    elif labels == ["B:Red"]:
        code = 4
    elif "A:Blue" in labels and "B:Red" in labels:
        code = 5
    elif "A:Red" in labels and "B:Blue" in labels:
        code = 6

    return ", ".join(labels) if labels else "No Object", code

def vision_loop():
    global latest_code, latest_label
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        latest_label, latest_code = detect_case(frame)

        cv2.putText(frame, f"{latest_label} ({latest_code})", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Camera - Nhan dien", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

def send_once():
    global last_sent_code
    try:
        if ser is None or not ser.is_open:
            print("[Lỗi] Chưa kết nối với Arduino!")
            return

        if latest_code != last_sent_code:
            ser.write(f"{latest_code}\n".encode())
            print(f"[GỬI] Mã mới: {latest_code} ({latest_label})")
            last_sent_code = latest_code
        else:
            print("[BỎ QUA] Mã đã gửi trước đó, không gửi lại.")
    except Exception as e:
        print("[Lỗi gửi]", e)

def connect_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"[KẾT NỐI] Arduino tại {SERIAL_PORT}")
        btn_send.config(state='normal')
    except:
        print(f"[Lỗi kết nối] Không thể mở cổng {SERIAL_PORT}")

# Nút giao diện
btn_connect = tk.Button(root, text="Kết nối tay gắp", font=('Arial', 12), command=connect_serial)
btn_connect.pack(pady=10)

btn_send = tk.Button(root, text="Bắt đầu gắp", font=('Arial', 12), command=send_once, state='disabled')
btn_send.pack(pady=10)

# Bắt đầu luồng camera
vision_thread = threading.Thread(target=vision_loop, daemon=True)
vision_thread.start()

# Chạy giao diện
root.mainloop()
