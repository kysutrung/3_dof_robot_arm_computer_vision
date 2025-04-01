import serial
import time

# Cấu hình cổng Serial (Thay đổi theo cổng Arduino của bạn, ví dụ: COM3 trên Windows hoặc /dev/ttyUSB0 trên Linux)
ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)
    
# Khai báo số muốn gửi
number_to_send = 11  # Thay đổi số tùy thích

def send_number(num):
    ser.write(f"{num}\n".encode())  # Gửi số kèm ký tự xuống dòng
    print(f"Sent: {num}")

try:
    while True:
        send_number(number_to_send)  # Gửi số đã khai báo trước
        time.sleep(2)  # Gửi sau mỗi 2 giây
except KeyboardInterrupt:
    print("\nThoát chương trình.")
    ser.close()
