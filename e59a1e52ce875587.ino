#include <WiFi.h>
#include "time.h"
int analogPin = 25;
int analogPin2 = 26;
int analogPin3 = 27;
int ledPin = 18;
int ledPin2 = 19;
int ledPin3 = 5;
int room =0;
int room2 =0;
int room3 =0;
int stateus_room=0;
int stateus_room2=0;
int stateus_room3=0;
const char* ssid     = ".";
const char* password = "whawha23";

const char* ntpServer = " time2.navy.mi.th";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 3600;

void setup(){
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  
  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  printLocalTime();

  //disconnect WiFi as it's no longer needed
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
}

void loop(){
  delay(1000);
  printLocalTime();
  room = analogRead(analogPin);
  room2 = analogRead(analogPin2);
  room3 = analogRead(analogPin3);
  Serial.print("room = ");
  Serial.println(room);

  if (room < 3500) { 
      digitalWrite(ledPin, HIGH); 
      stateus_room=1;
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
     }
  else{
      digitalWrite(ledPin,LOW);
      stateus_room=0;
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
   }
      
   if (room2 < 3500) { 
      digitalWrite(ledPin2, HIGH); 
      stateus_room2=1;
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
    }
  else{
      digitalWrite(ledPin2,LOW);
      stateus_room2=0;
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
  }  
  if (room3 < 3500) { 
      digitalWrite(ledPin3, HIGH); 
      stateus_room3=1;
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
    }
  else{
      digitalWrite(ledPin3,LOW);
      stateus_room3=0; 
      //ใส่ส่วนที่ส่งหาbackendส่งstateusและเวลา 
  }

}

void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y  int(%H)+7:%M:%S");
  Serial.println();
}
