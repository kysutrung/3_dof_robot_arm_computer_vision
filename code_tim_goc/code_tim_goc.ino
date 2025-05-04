#include <Servo.h>

Servo baseServo;
Servo gripperServo;
Servo updown1Servo;
Servo updown2Servo;


void dongTayGap(){
  gripperServo.write(175); //đóng tay gắp hết cỡ
}

void moTayGap(){
  gripperServo.write(135); //mở tay gắp hết cỡ
}

void quayTaySangTrai(){
  baseServo.write(120); //quay tay sang trái
}

void quayTaySangPhai(){
  baseServo.write(20); //quay tay sang phải
}

void nangTayLen(){
  updown1Servo.write(10); //cánh tay ngẩng lên trời
  updown2Servo.write(0); //cánh tay ngẩng lên trời
}

void haCanhTayXuong(){
  updown1Servo.write(100); 
  updown2Servo.write(30);  
}

void quayVeGoc(){
  nangTayLen();
  moTayGap();
  baseServo.write(70);
}

void setup() {
  updown2Servo.attach(7);
  updown1Servo.attach(8);
  baseServo.attach(9);    
  gripperServo.attach(10);    

  quayVeGoc();
  delay(1000);
  haCanhTayXuong();
  delay(1000);
  dongTayGap();
  delay(1000);
  nangTayLen();
  quayTaySangTrai();
  delay(1000);
  moTayGap();
}

void loop() {
  // Không cần làm gì trong loop
}
