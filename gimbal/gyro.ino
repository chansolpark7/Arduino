#include <Wire.h>
#include <math.h>

const int MPU = 0x68;

int AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
int xpos;
int ypos;
float ax, ay, az, gx, gy, gz;
float fx = 0, fy = 0, fz = 0;

float x = 0;
float y = 0;
float z = 0;
float a = 0;

int low = -16383;
int high = 16383;

void setup() {
  Serial.begin(9600);

  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}


void loop() {
  float a = 0.95;
  int t = 50;
  delay(t);
  get6050();
  // ypos=map(AcX,-16383,16383,0,180);
  // xpos=map(AcY,-16383,16383,180,0);


  //     Serial.print("xpos");
  //     Serial.print(xpos);
  //     Serial.print(",  ");
  //     Serial.print("ypos");
  //     Serial.println(ypos);

  // gx = map(GyX, low, high, 0, 180);
  // gy = map(GyY, low, high, 0, 180);
  // Serial.print(gx);
  // Serial.print(", ");
  // Serial.println(gy);
  // Serial.print(AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ);
  // Serial.println(AcX);
  // Serial.println(AcY);
  // Serial.println(AcZ);
  // Serial.println(GyX);
  // Serial.println(GyY);
  // Serial.println(GyZ);
  // Serial.println();
  ax = (float)AcX/16384*9.8;
  ay = (float)AcY/16384*9.8;
  az = (float)AcZ/16384*9.8;
  gx = (float)GyX/131 * 1 / t *3.14;
  gy = (float)GyY/131 * 1 / t * 3.14;
  gz = (float)GyZ/131 * 1 / t * 3.14;
  x = atan(ay/sqrt(ax*ax+az*az))*180/3.14; // degree
  y = -atan(ax/sqrt(ay*ay+az*az))*180/3.14; // degree
  fx = (fx+gx)*a+x*(1-a);
  fy = (fy+gy)*a+y*(1-a);
  // fx = fx+gx;
  // fy = fy+gy;
  fz = fz+gz;
  // Serial.print(x);
  // Serial.print(' ');
  // Serial.print(y);
  // Serial.print(' ');

  // Serial.print(fx);
  // Serial.print(' ');
  // Serial.print(fy);
  // Serial.print(' ');
  // Serial.println(fz);

  // Serial.print(gx);
  // Serial.print(' ');
  // Serial.print(gy);
  // Serial.print(' ');
  // Serial.println(gz);

  Serial.print(ax);
  Serial.print(' ');
  Serial.print(ay);
  Serial.print(' ');
  Serial.println(az);
}
void get6050() {

  Wire.beginTransmission(MPU);

  Wire.write(0x3B);

  Wire.endTransmission(false);

  Wire.requestFrom(MPU, 14, true);

  AcX = Wire.read() << 8 | Wire.read();

  AcY = Wire.read() << 8 | Wire.read();

  AcZ = Wire.read() << 8 | Wire.read();

  Tmp = Wire.read() << 8 | Wire.read();

  GyX = Wire.read() << 8 | Wire.read();

  GyY = Wire.read() << 8 | Wire.read();

  GyZ = Wire.read() << 8 | Wire.read();
}