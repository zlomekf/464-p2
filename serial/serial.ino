uint32_t X,Y,Z;
uint8_t X_LS, X_MS, Y_LS, Y_MS, Z_LS, Z_MS;
int i = 0;

uint32_t x_arr[3];
uint32_t  y_arr[3];
uint32_t  z_arr[3];

void setup()
{
    Serial.begin(9600); // Serial Port at 9600 baud
    Serial.setTimeout(100); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt() 
}

void loop()
{ 
  if(i == 3){

    i = 0;
    X = (x_arr[0] + x_arr[1] + x_arr[2])/3;
    Y = (y_arr[0] + y_arr[1] + y_arr[2])/3;
    Z = (z_arr[0] + z_arr[1] + z_arr[2])/3;
    
    X_LS = X & 0xFF;
    X_MS = ((X & 0xFF00) >> 8) | 0xF0;
    Y_LS = Y & 0xFF;
    Y_MS = ((Y & 0xFF00) >> 8) | 0xF0;
    Z_LS = Z & 0xFF;
    Z_MS = ((Z & 0xFF00) >> 8) | 0xF0;
    
    Serial.print(char(X_LS));
    Serial.print(char(X_MS));
    Serial.print(char(Y_LS));
    Serial.print(char(Y_MS));
    Serial.print(char(Z_LS));
    Serial.print(char(Z_MS));
    Serial.print('\n');
    delay(1);
  
  }
  
  x_arr[i] = analogRead(A0); // X raw data divided by 4 gives 0 - 255
  y_arr[i] = analogRead(A1); // -------------------------------------
  z_arr[i] = analogRead(A2); // -------------------------------------

  i = i + 1;
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
