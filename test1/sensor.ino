#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4; // Averaging size
byte rates[RATE_SIZE]; // Array of BPM readings
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute;
int beatAvg;

#define TRIG_PIN 2
#define ECHO_PIN 3

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30102 not found. Check wiring/power.");
    while (1);
  }

  particleSensor.setup(); // Use default settings
  particleSensor.setPulseAmplitudeRed(0x1F); // Red LED
  particleSensor.setPulseAmplitudeIR(0x1F);  // IR LED

  // Serial.println("Place your finger on the sensor...");
}

void loop() {

  long duration;
  float distance;

  // Trigger pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo time
  duration = pulseIn(ECHO_PIN, HIGH);

  // Convert to distance (cm)
  distance =( duration * 0.034 / 2)/100;
  int weight =75;
  int bmi = weight/(distance*distance);

  long irValue = particleSensor.getIR(); // Read IR value

  if (irValue > 50000) { // Ensure finger is on sensor
    // if (checkForBeat(irValue))
     {
      long delta = millis() - lastBeat;
      lastBeat = millis();

      beatsPerMinute = 60 / (delta / 1000.0);

      if (beatsPerMinute < 255 && beatsPerMinute > 20) {
        rates[rateSpot++] = (byte)beatsPerMinute;
        rateSpot %= RATE_SIZE;

        // Average BPM
        beatAvg = 0;
        for (byte x = 0; x < RATE_SIZE; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }
    }

    float tempC = particleSensor.readTemperature();
    float tempF = particleSensor.readTemperatureF();

    float spo2Estimate = map(irValue, 50000, 120000, 85, 100); // Rough estimate

    // Serial.print("{'IR': "); Serial.print(irValue);
    Serial.print("{'BPM': "); Serial.print(beatsPerMinute, 1);
    // Serial.print(", 'Avg_BPM': "); Serial.print(beatAvg);
    Serial.print(", 'Temp_F': "); Serial.print(tempF, 1);
    Serial.print(", 'SpO2': "); Serial.print(spo2Estimate);
    Serial.print(", 'BMI': "); Serial.print(bmi);
    Serial.println("}");

  } else {
  //  Serial.print("{'IR': 0");
    Serial.print("{'BPM': 0");
    // Serial.print(", 'Avg_BPM': 0");
    Serial.print(", 'Temp_F': 0"); 
    Serial.print(", 'SpO2': 0"); 
    Serial.print(", 'BMI': 0"); 
    Serial.println("}");
  }

  delay(1000); // Adjust to 250 for more real-time
}
