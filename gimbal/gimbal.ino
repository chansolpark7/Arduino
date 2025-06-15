#include <Wire.h>
#include <math.h>
#include <Servo.h>

const int MPU = 0x68;
Servo myservo1;
Servo myservo2;
Servo myservo3;

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
  myservo1.attach(11);
  myservo2.attach(10);
  myservo3.attach(9);
}

float noise(int x)
{
  int n = x;
  n = (n<<13) ^ n;
  int nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff;
  Serial.println(nn);
  return 1 - ((float)nn / 1073741824);
}

float bezier_interpolate(float a, float b, float c, float t)
{
  return (1-t)*(1-t)*a + 2*t*(1-t)*b + t*t*c;
}
float bezier_noise(float x)
{
  float v = 0;
  int octave = 3;
  for (int i=0; i<octave; i++)
  {
    int int_x = (int)x;
    // Serial.println(x-int_x);
    float y2 = noise(int_x);
    float y1 = (noise(int_x-1)+y2)/2;
    float y3 = (noise(int_x+1)+y2)/2;
    float d = 1;
    for (int j = 0; j < i; j++) d *= 2;
    v += bezier_interpolate(y1, y2, y3, x-int_x) / d;
    x *= 2;
  }
  return v;
}

void loop() {
  float a = 0.95;
  int t = 50;
  float time = (float)millis()/1000;
  delay(t);
  get6050();
  ax = (float)AcX/16384*9.8;
  ay = (float)AcY/16384*9.8;
  az = (float)AcZ/16384*9.8;
  gx = (float)GyX/131 * 1 / t *3.14;
  gy = (float)GyY/131 * 1 / t * 3.14;
  gz = (float)GyZ/131 * 1 / t * 3.14;
  x = atan(ay/sqrt(ax*ax+az*az))*180/3.14;
  y = -atan(ax/sqrt(ay*ay+az*az))*180/3.14;
  fx = (fx+gx)*a+x*(1-a);
  fy = (fy+gy)*a+y*(1-a);
  fz = fz+gz;
  if (fz > 0) fz = fz - 0.05;
  else fz = fz + 0.05;
  Serial.print(fx);
  Serial.print('\t');
  Serial.print(fy);
  Serial.print('\t');
  Serial.print(fz);
  Serial.print("\t\t\t");
  Serial.print(ax);
  Serial.print('\t');
  Serial.print(ay);
  Serial.print('\t');
  Serial.println(az);
  myservo1.write(fx+90);
  myservo2.write(fy+90);
  myservo3.write(fz+90);
  // float random_x = bezier_noise(time+3000);
  // float random_y = bezier_noise(time+5000);
  // float random_z = bezier_noise(time);
  // Serial.print(random_x);
  // Serial.print('\t');
  // Serial.print(random_y);
  // Serial.print('\t');
  // Serial.print(random_z);
  // Serial.print('\n');
  // Serial.print(noise(int(time)));

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