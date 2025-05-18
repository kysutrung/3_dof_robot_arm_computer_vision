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

void nhatMauDoOViTriB(){
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

void nhatMauDoOViTriA(){
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

void nhatMauXanhOViTriB(){
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

void nhatMauXanhOViTriA(){
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
  Serial.begin(9600);
  updown2Servo.attach(7);
  updown1Servo.attach(8);
  baseServo.attach(9);    
  gripperServo.attach(10);    

  quayVeGoc();
}

void loop() {
  if (Serial.available()) {
    int code = Serial.parseInt();
    if(code == 1){
      nhatMauXanhOViTriA();
    }
    if(code == 2){
      nhatMauDoOViTriA();
    }
    if(code == 3){
      nhatMauXanhOViTriB();
    }
    if(code == 4){
      nhatMauDoOViTriB();
    }
    if(code == 5){
      nhatMauDoOViTriB();
      delay(1000);
      nhatMauXanhOViTriA();
    }
    if(code == 6){
      nhatMauXanhOViTriB();
      delay(1000);
      nhatMauDoOViTriA();
    }
  }
}
