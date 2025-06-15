#include <stdio.h>
#define max(a, b) ((a) > (b) ? (a) : (b))

int main()
{
    short a = 1200;
    short b = 7;
    unsigned int rpm_limit = 100;

    short i = 0, j = 0;
    char a_flag = 0, b_flag = 0;
    unsigned int pulse_width = 150000;
    unsigned int now, next;
    short a_rpm = rpm_limit*a/max(a, b);
    short b_rpm = rpm_limit*b/max(a, b);
  
//   Serial.print("data ");
//   Serial.print(a);
//   Serial.print(' ');
//   Serial.print(b);
//   Serial.print(' ');
//   Serial.print(a_rpm);
//   Serial.print(' ');
//   Serial.print(b_rpm);
//   Serial.print(' ');
//   Serial.print(max(pulse_width*a/a_rpm, pulse_width*b/b_rpm));
//   Serial.print(' ');
//   Serial.print(((unsigned long)a+1)*b);
//   Serial.print(' ');
//   Serial.print(((unsigned long)b+1)*a);
//   Serial.print(' ');
//   Serial.print(pulse_width*(a+1)/a_rpm);
//   Serial.print(' ');
//   Serial.println(pulse_width*(b+1)/b_rpm);

  while (i < a*2 || j < b*2)
  {
    now = max((float)pulse_width*i*max(a, b)/(rpm_limit*a), (float)pulse_width*j*max(a, b)/(rpm_limit*b));
    if (((unsigned long)i+1)*b < ((unsigned long)j+1)*a)
    {
      next = (float)pulse_width*(i+1)*max(a, b)/(rpm_limit*a);
      i++;
      printf("i %d\n", next);
    }
    else if (((unsigned long)i+1)*b == ((unsigned long)j+1)*a)
    {
      next = (float)pulse_width*(i+1)*max(a, b)/(rpm_limit*a);
      i++;
      j++;
      printf("i j %d\n", next);
    }
    else
    {
      next = (float)pulse_width*(j+1)*max(a, b)/(rpm_limit*b);
      j++;
      printf("j %d\n", next);
    }
  }
  if (i != a*2 || j != b*2)
  {
    // Serial.print("step error : ");
    // Serial.print(a);
    // Serial.print(' ');
    // Serial.print(b);
    // Serial.print(' ');
    // Serial.print(i);
    // Serial.print(' ');
    // Serial.println(j);
  }
}