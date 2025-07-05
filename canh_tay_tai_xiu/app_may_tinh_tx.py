import cv2
import numpy as np
from gtts import gTTS
import pygame
import os
import threading
import tkinter as tk

dot_count = 0  # Tổng số chấm toàn cục

def digital_zoom(frame, zoom_factor=1):
    h, w = frame.shape[:2]
    new_w, new_h = w // zoom_factor, h // zoom_factor
    start_x = (w - new_w) // 2
    start_y = (h - new_h) // 2
    cropped = frame[start_y:start_y + new_h, start_x:start_x + new_w]
    zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
    return zoomed

def speak_vi(text, filename="speak.mp3"):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(filename)

def speak_result():
    if 11 <= dot_count <= 17:
        speak_vi("Tài")
    elif dot_count < 11 and dot_count > 0:
        speak_vi("Xỉu")
    else:
        speak_vi("Không rõ kết quả")

def read_dice():
    global dot_count
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera!")
        return

    prev_dot_count = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        zoomed_frame = digital_zoom(frame, zoom_factor=3)
        gray = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        current_count = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 80 < area < 2000:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter == 0:
                    continue
                circularity = 4 * np.pi * area / (perimeter ** 2)
                if circularity > 0.6:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(zoomed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    current_count += 1

        dot_count = current_count

        cv2.putText(zoomed_frame, f"So cham: {dot_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Nhan dien xuc xac (da fix size)", zoomed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_camera_thread():
    t = threading.Thread(target=read_dice, daemon=True)
    t.start()

def create_gui():
    root = tk.Tk()
    root.title("Xúc Xắc Tài Xỉu")
    root.geometry("300x150")

    label = tk.Label(root, text="Nhấn nút để đọc kết quả:", font=("Arial", 12))
    label.pack(pady=10)

    btn = tk.Button(root, text="Đọc kết quả", font=("Arial", 14), command=lambda: threading.Thread(target=speak_result).start())
    btn.pack(pady=10)

    root.mainloop()

# Khởi động camera xử lý song song
start_camera_thread()

# Giao diện người dùng
create_gui()
