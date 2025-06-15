#include <Servo.h>

#define steps_a 2
#define dir_a 3
#define steps_b 4
#define dir_b 5

#define ms1 10
#define ms2 9
#define ms3 8

#define a_cw 0
#define a_ccw 1
#define b_cw 0
#define b_ccw 1
#define motor_enable 7

#define pen_pin 6
#define pen_up 0
#define pen_down 50

#define mm_per_step 0.2
#define rpm_limit 240UL
#define pulse_width 150000UL
#define x_max 1300
#define y_max 600

int step_mode = 4;
int micro_step_list[] = {1, 2, 4, 8, 16};
int ms1_value[] = {LOW, HIGH, LOW, HIGH, HIGH};
int ms2_value[] = {LOW, LOW, HIGH, HIGH, HIGH};
int ms3_value[] = {LOW, LOW, LOW, LOW, HIGH};

int x = 0;
int y = 0;
int is_pen_down;

String input_string = "";

Servo pen_servo;

// state 0 up
// state 1 down
void set_pen(int state)
{
  is_pen_down = state;
  if (state == 0) // up
  {
    // pen_servo.write(0);
    // delay(200);
    pen_servo.write(pen_up);
  }
  else // down
  {
    pen_servo.write(pen_down);
  }
}

void move_a(int a)
{
  unsigned int delay_time = pulse_width / rpm_limit;
  digitalWrite(steps_a, LOW);
  for (int i=0; i<a; i++)
  {
    delayMicroseconds(delay_time);
    digitalWrite(steps_a, HIGH);
    delayMicroseconds(delay_time);
    digitalWrite(steps_a, LOW);
  }
}

void move_b(int b)
{
  unsigned int delay_time = pulse_width / rpm_limit;
  digitalWrite(steps_b, LOW);
  for (int i=0; i<b; i++)
  {
    delayMicroseconds(delay_time);
    digitalWrite(steps_b, HIGH);
    delayMicroseconds(delay_time);
    digitalWrite(steps_b, LOW);
  }
}

void move(int dx, int dy)
{
  int a = dx-dy;
  int b = dx+dy;

  if (a >= 0) digitalWrite(dir_a, a_cw);
  else digitalWrite(dir_a, a_ccw);
  if (b >= 0) digitalWrite(dir_b, b_cw);
  else digitalWrite(dir_b, b_ccw);
  a = abs(a);
  b = abs(b);
  if (a == 0 && b == 0) return;
  else if (a == 0)
  {
    move_b(b);
    return;
  }
  else if (b == 0)
  {
    move_a(a);
    return;
  }
  
  int i = 0, j = 0;
  char a_flag = 0, b_flag = 0;
  unsigned long now, next;
  int a_rpm = rpm_limit*a/max(a, b);
  int b_rpm = rpm_limit*b/max(a, b);
  
  // Serial.print("data ");
  // Serial.print(a);
  // Serial.print(' ');
  // Serial.print(b);
  // Serial.print(' ');
  // Serial.print(a_rpm);
  // Serial.print(' ');
  // Serial.print(b_rpm);
  // Serial.print(' ');
  // Serial.print(max(pulse_width*a/a_rpm, pulse_width*b/b_rpm));
  // Serial.print(' ');
  // Serial.print(((unsigned long)a+1)*b);
  // Serial.print(' ');
  // Serial.print(((unsigned long)b+1)*a);
  // Serial.print(' ');
  // Serial.print(pulse_width*(a+1)/a_rpm);
  // Serial.print(' ');
  // Serial.println(pulse_width*(b+1)/b_rpm);

  while (i < a*2 || j < b*2)
  {
    now = max((float)pulse_width*i*max(a, b)/(rpm_limit*a), (float)pulse_width*j*max(a, b)/(rpm_limit*b));
    if (((unsigned long)i+1)*b < ((unsigned long)j+1)*a)
    {
      next = (float)pulse_width*(i+1)*max(a, b)/(rpm_limit*a);
      delayMicroseconds(next-now);
      i++;
      a_flag = !a_flag;
      digitalWrite(steps_a, a_flag);
    }
    else if (((unsigned long)i+1)*b == ((unsigned long)j+1)*a)
    {
      next = (float)pulse_width*(i+1)*max(a, b)/(rpm_limit*a);
      delayMicroseconds(next-now);
      i++;
      j++;
      a_flag = !a_flag;
      b_flag = !b_flag;
      digitalWrite(steps_a, a_flag);
      digitalWrite(steps_b, b_flag);
    }
    else
    {
      next = (float)pulse_width*(j+1)*max(a, b)/(rpm_limit*b);
      delayMicroseconds(next-now);
      j++;
      b_flag = !b_flag;
      digitalWrite(steps_b, b_flag);
    }
  }
  if (i != a*2 || j != b*2)
  {
    Serial.print("step error : ");
    Serial.print(a);
    Serial.print(' ');
    Serial.print(b);
    Serial.print(' ');
    Serial.print(i);
    Serial.print(' ');
    Serial.println(j);
  }
}

void move_to(int to_x, int to_y)
{
  if (to_x < 0) to_x = 0;
  if (to_x > x_max*micro_step_list[step_mode]) to_x = x_max*micro_step_list[step_mode];
  if (to_y < 0) to_y = 0;
  if (to_y > y_max*micro_step_list[step_mode]) to_y = y_max*micro_step_list[step_mode];
  move(to_x-x, to_y-y);
  x = to_x;
  y = to_y;
}

void readline(char string[], int size)
{
  input_string = "";
  char input_c;
  while (1)
  {
    if (Serial.available())
    {
      input_c = (char)Serial.read();
      input_string += input_c;
      if (input_c == '\n') break;
    }
  }
  input_string.toCharArray(string, size);
  // Serial.println(input_string);
}

void setup(){
  Serial.begin(9600);
  pinMode(steps_a, OUTPUT);
  pinMode(dir_a, OUTPUT);
  pinMode(steps_b, OUTPUT);
  pinMode(dir_b, OUTPUT);
  pinMode(ms1, OUTPUT);
  pinMode(ms2, OUTPUT);
  pinMode(ms3, OUTPUT);
  pinMode(motor_enable, OUTPUT);

  pen_servo.attach(pen_pin);
  set_pen(0);
  
  digitalWrite(ms1, ms1_value[step_mode]);
  digitalWrite(ms2, ms2_value[step_mode]);
  digitalWrite(ms3, ms3_value[step_mode]);
  digitalWrite(motor_enable, LOW);

  // delay(5000);//////////////////////
}

int i =0;
int command, result;
char input[20];
void loop()
{
  if(Serial.available())
  {
    // String input_string;
    // input_string = Serial.readStringUntil('\n');
    // input_string.toCharArray(input, sizeof(input));
    readline(input, sizeof(input));
    result = sscanf(input, "%d", &command);
    if (result == 1)
    {
      switch (command)
      {
        case 0:
          Serial.println("complete");
          x = 0;
          y = 0;
          break;
        case 1:
          Serial.println("complete");
          set_pen(0);
          break;
        case 2:
          Serial.println("complete");
          set_pen(1);
          break;
        case 3:
          Serial.println("complete");
          int to_x, to_y;
          while (1)
          {
            if (Serial.available() != 0) break;
          }
          // input_string = Serial.readStringUntil('\n');
          // input_string.toCharArray(input, sizeof(input));
          readline(input, sizeof(input));
          result = sscanf(input, "%d %d", &to_x, &to_y);
          if (result == 2)
          {
            Serial.println("complete");
            move_to(to_x, to_y);
          }
          else
          {
            Serial.println("move_to error");
            Serial.println(input_string);
          }
          break;
        case 4:
          Serial.println("complete");
          digitalWrite(motor_enable, HIGH);
          break;
        case 5:
          Serial.println("complete");
          digitalWrite(motor_enable, LOW);
          break;
        case 6:
          Serial.println("complete");
          Serial.print(x);
          Serial.print(' ');
          Serial.println(y);
          break;
        default:
          Serial.println("command error");
          Serial.println(input_string);
      }
      // Serial.println(i);
      // i++;
    }
  }
}