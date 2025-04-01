int receivedNumber = 0;

void nhanDuLieuDieuKhien(){
    if (Serial.available()) {  // Kiểm tra dữ liệu có trong buffer
      String data = Serial.readStringUntil('\n');  // Đọc đến khi gặp ký tự xuống dòng
      receivedNumber = data.toInt();  // Chuyển đổi chuỗi thành số nguyên

      // Kiểm tra nếu số là số lẻ -> Bật LED, ngược lại tắt LED
      if (receivedNumber % 2 == 1) {
          digitalWrite(LED_BUILTIN, HIGH);
      } else {
          digitalWrite(LED_BUILTIN, LOW);
      }
  }
}

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  nhanDuLieuDieuKhien();
}
