#include <Servo.h>

Servo myservo;  // Servo 객체 생성

int pos = 0;    // 서보모터의 현재 각도

void setup() {
  myservo.attach(A0);  // 서보모터를 9번 핀에 연결
}

void loop() {
  // for (pos = 0; pos <= 180; pos += 1) { // 0도에서 180도까지 회전
  //   myservo.write(pos);                 // 서보모터를 지정된 각도로 회전
  //   delay(15);                          // 각도 변경 후 잠시 대기
  // }
  delay(1000);
  myservo.write(180);
  // myservo.write(0);
  delay(1000);
  myservo.write(0);
  // for (pos = 180; pos >= 0; pos -= 1) { // 180도에서 0도까지 회전
  //   myservo.write(pos);                 // 서보모터를 지정된 각도로 회전
  //   delay(15);                          // 각도 변경 후 잠시 대기
  // }
}
