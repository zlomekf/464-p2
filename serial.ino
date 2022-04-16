char Array[3*sizeof(char)];
char X,Y,Z;

void setup()
{
    Serial.begin(9600); // Serial Port at 9600 baud
    Serial.setTimeout(100); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt() 
}

void loop()
{ 
  X = analogRead(A0) / 4; // X raw data divided by 4 gives 0 - 255
  Y = analogRead(A1) / 4; // -------------------------------------
  Z = analogRead(A2) / 4; // -------------------------------------

  sprintf(Array, "%c",X);
  sprintf(Array + 1, "%c",Y);
  sprintf(Array + 2, "%c",Z);
  for(int i = 0; i < 3; i++)
  {
    Serial.print(Array[i]);
    delay(1);
  }
  Serial.print('\n');
  delay(1);
}