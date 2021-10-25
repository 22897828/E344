//assigning ADC pins
int batteryADC = A10;
int supplyADC = A9;
int ldrADC = A0;
int currentADC = A1;
int chargePin = 2;
int pwmPin = 11;

//declaring data variables
float batteryVal = 0;
float supplyVal = 0;
float currentVal = 0;
byte ldrVal = 0;

int pwm = 0;
bool overCharge = true;
String receive = "OV1"; 


void setup() {
  Serial.begin(9600);
  pinMode(chargePin, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(ldrADC, INPUT);
  pinMode(supplyADC, INPUT);
  pinMode(batteryADC, INPUT);
  pinMode(currentADC, INPUT);
}

void loop() {
  //processing ADC data
  currentVal = (((float)analogRead(currentADC))/1023)*600 - 150;
  batteryVal = (((float)analogRead(batteryADC))/1023)*2 + 5.5;
  supplyVal = (((float)analogRead(supplyADC))/1023)*23.3;
  ldrVal = (int)((((float)analogRead(ldrADC))/1023)*100);
  
  //read serial input and set overcharge bool
  while(Serial.available() > 0){
    receive = Serial.readStringUntil('\n');
  }
  
  if(receive == "OV1"){
    overCharge = true;
    digitalWrite(chargePin, HIGH);
  }
  if(receive == "OV0"){
    overCharge = false;
    digitalWrite(chargePin, LOW);
  }

  if(receive != "OV0" && receive != "OV1" && receive != "aaa"){
    pwm = (int)(255*((float)((receive[0] - 48 - 1)*100 + (receive[1] - 48)*10 + (receive[2] - 48)))/100);
    analogWrite(pwmPin, pwm);
    receive = "aaa";
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


  delay(100);
   
}
