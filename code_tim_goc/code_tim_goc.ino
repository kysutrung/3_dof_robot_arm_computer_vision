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
  baseServo.write(123); //quay tay sang trái
}

void quayTaySangPhai(){
  baseServo.write(20); //quay tay sang phải
}

void nangTayLen(){
  updown1Servo.write(10); //cánh tay ngẩng lên trời
  updown2Servo.write(0); //cánh tay ngẩng lên trời
}

void haCanhTayXuong1(){
  updown1Servo.write(100); 
  updown2Servo.write(30);  
}

void haCanhTayXuong2(){
  updown1Servo.write(90); 
  updown2Servo.write(15);  
}

void quayVeGoc(){
  nangTayLen();
  moTayGap();
  delay(1000);
  baseServo.write(70);
}

void nhatMauDoOViTri1(){
  quayVeGoc();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  dongTayGap();
  delay(1000);
  nangTayLen();
  quayTaySangPhai();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  moTayGap();
  delay(1000);
  quayVeGoc();
}

void nhatMauDoOViTri2(){
  quayVeGoc();
  delay(1000);
  haCanhTayXuong2();
  delay(1000);
  dongTayGap();
  delay(1000);
  nangTayLen();
  quayTaySangPhai();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  moTayGap();
  delay(1000);
  quayVeGoc();
}

void nhatMauXanhOViTri1(){
  quayVeGoc();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  dongTayGap();
  delay(1000);
  nangTayLen();
  quayTaySangTrai();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  moTayGap();
  delay(1000);
  quayVeGoc();
}

void nhatMauXanhOViTri2(){
  quayVeGoc();
  delay(1000);
  haCanhTayXuong2();
  delay(1000);
  dongTayGap();
  delay(1000);
  nangTayLen();
  quayTaySangTrai();
  delay(1000);
  haCanhTayXuong1();
  delay(1000);
  moTayGap();
  delay(1000);
  quayVeGoc();
}


void setup() {
  updown2Servo.attach(7);
  updown1Servo.attach(8);
  baseServo.attach(9);    
  gripperServo.attach(10);    

  nhatMauDoOViTri2();
  delay(1000);
  nhatMauXanhOViTri1();
}

void loop() {
  // Không cần làm gì trong loop
}
