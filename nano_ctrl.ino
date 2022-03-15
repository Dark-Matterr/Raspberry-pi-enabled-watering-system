//pins initialization
int pumpPin = 12;
int soilPower = 2;
int SoilAnalog = A6;

//data variable
String relayTrig = "1";
String soilTrig = "2";

void setup(){
  Serial.begin(115200);
  
  //Digital Pin init
  pinMode(pumpPin, OUTPUT);
  pinMode(soilPower, OUTPUT);
}

void loop(){
  
  //Serial communication in both device init
  if(Serial.available() > 0){
    String serial_data = Serial.readStringUntil('\n');
    if(relayTrig == serial_data){
       relay(); // triggering the relay
    }
    if(soilTrig == serial_data){
      Serial.println("Soil Moisture: "+ String(moistureData(SoilAnalog, soilPower))); // sending data to raspberry pi
    }
    serial_data = "0"; // powering off the digitalpin of relayTrig
  }
}

void relay(){
   digitalWrite(pumpPin, HIGH);
   delay(3000);
   digitalWrite(pumpPin, LOW);
   delay(3000);
   digitalWrite(pumpPin, HIGH);
   delay(3000);
   digitalWrite(pumpPin, LOW);
   delay(3000);
   digitalWrite(pumpPin, HIGH);
   delay(3000);
   digitalWrite(pumpPin, LOW);
   delay(3000);
}

//Getting the soil moisture data
int moistureData(int sensorAnalog, int sensorPower){
   digitalWrite(sensorPower, HIGH);
   delay(10); 
   int data = analogRead(sensorAnalog);
   digitalWrite(soilPower, LOW);
   return data;
}
