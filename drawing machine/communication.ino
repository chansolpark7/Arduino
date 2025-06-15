int data;
String input_string;
char input[20];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
    input_string = Serial.readStringUntil('\n');
    input_string.toCharArray(input, sizeof(input));
    sscanf(input, "%d", &data);
    Serial.println(data);
  }
}
