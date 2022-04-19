uint32_t X,Y,Z;
uint8_t X_LS, X_MS, Y_LS, Y_MS, Z_LS, Z_MS;
int i = 0;

void setup()
{
    Serial.begin(9600); // Serial Port at 9600 baud
    Serial.setTimeout(100); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt() 
}

void loop()
{ 
  X = analogRead(A0); // X raw data divided by 4 gives 0 - 255
  Y = analogRead(A1); // -------------------------------------
  Z = analogRead(A2); // -------------------------------------

//  X = 65535;
//  Y = 65535;
//  Z = 65535;

//  X_LS = X /4;
//  Y_LS = Y /4;
//  Z_LS = Z /4;

  //X = 65535;
  X_LS = X & 0xFF;
  X_MS = ((X & 0xFF00) >> 8) | 0xF0;
  Y_LS = Y & 0xFF;
  Y_MS = ((Y & 0xFF00) >> 8) | 0xF0;
  Z_LS = Z & 0xFF;
  Z_MS = ((Z & 0xFF00) >> 8) | 0xF0;

  uint8_t len = 6;
  
  Serial.print(char(X_LS));
  Serial.print(char(X_MS));
  Serial.print(char(Y_LS));
  Serial.print(char(Y_MS));
  Serial.print(char(Z_LS));
  Serial.print(char(Z_MS));
  Serial.print('\n');
  delay(1);

/*
  sprintf(Array, "%u",X_LS);
  sprintf(Array + 1, "%u",X_MS);
  sprintf(Array + 2, "%u",Y_LS);
  sprintf(Array + 3, "%u",Y_MS);
  sprintf(Array + 4, "%u",Z_LS);
  sprintf(Array + 5, "%u",Z_MS);

  for(int i = 0; i < 6; i++)
  {
    Serial.print(Array[i]);
    delay(10);
  }
  Serial.print('\n');
  */
}
