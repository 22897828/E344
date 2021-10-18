//Teo 22897828

//assigning ADC pins
int batteryADC = A10;
int supplyADC = A9;
int ldrADC = A0;
int currentADC = A1;

//declaring data variables
float batteryVal = 0;
float supplyVal = 0;
float currentVal = 0;
byte ldrVal = 0;
bool overCharge = true;
String command = "OV1"; 


void setup() {
  Serial.begin(9600);
}

void loop() {
  //processing ADC data
  currentVal = (((float)analogRead(currentADC))/1023)*600 - 150;
  batteryVal = (((float)analogRead(batteryADC))/1023)*2 + 5.5;
  supplyVal = (((float)analogRead(supplyADC))/1023)*23.3;
  ldrVal = (int)((((float)analogRead(ldrADC))/1023)*100);
  
  //read serial input and set overcharge bool
  if(Serial.read() > 0){
  command = Serial.readString();
  if(command[2] == 1){
    overCharge = true;
  }
  if(command[2] == 0){
    overCharge = false;
  }
  }


  Serial.print(overCharge);
  Serial.print(",");
  Serial.print(batteryVal);
  Serial.print(",");
  Serial.print(supplyVal);
  Serial.print(",");
  Serial.print(currentVal);
  Serial.print(",");
  Serial.print(ldrVal);
  Serial.println();


  delay(1000);
   
}
