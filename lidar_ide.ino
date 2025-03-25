#include <Wire.h>
#include <Adafruit_VL53L0X.h>

Adafruit_VL53L0X lidar;

void setup() {
    Serial.begin(9600);  // Nastavi serijsko komunikacijo
    Wire.begin();        // Inicializiraj I2C komunikacijo

    if (!lidar.begin()) {
        Serial.println("Napaka: Senzor ni zaznan!");
        while (1);  // Ustavi program
    }
    Serial.println("Senzor VL53L0X pripravljen.");
}

void loop() {
    VL53L0X_RangingMeasurementData_t measure;
    
    lidar.rangingTest(&measure, false);

    if (measure.RangeStatus != 4) {  // Če je meritev veljavna
        Serial.println(measure.RangeMilliMeter / 10.0);  // Pretvori mm v cm
    } else {
        Serial.println("Meritev ni veljavna");
    }

    delay(100);  // Počakaj 500 ms pred naslednjo meritvijo
}
