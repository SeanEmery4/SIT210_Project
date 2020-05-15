// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

// This #include statement was automatically added by the Particle IDE.
#include <HC_SR04.h>

// This #include statement was automatically added by the Particle IDE.
#include <SharpIR.h>

MQTT client("test.mosquitto.org", 1883, callback);

// Method called when a message is received. Not needed
void callback(char* topic, byte* payload, unsigned int length) 
{
}

// distances sensors detect
int F_C_Dist = 0.0; 
char message[4];

//double R_C_Dist = 0.0;

// SHARP distance sensor pin and model
int pin = A1;
int model = 1080;

// Ultrasonic pins not working
//int R_C_trigPin = D5;
//int R_C_echoPin = D4;

// set up sharp sensor with input in and model
SharpIR F_C_rangefinder(pin, model);

// set up ultrasonics with trigger and echo pins and min and max values
//HC_SR04 R_C_rangefinder = HC_SR04(R_C_trigPin, R_C_echoPin, 10, 100);

int getIRDistance()
{
    int distance = F_C_rangefinder.distance();
    if (distance <= 80 && distance >= 10)
    {
        return distance;
    }
    else if (distance > 80)
    {
        return 81;
    }
    else if (distance < 10)
    {
        return 10;
    }
    else
    {
        return distance;
    }
}


void setup() {
    Particle.variable("F_C_Dist", F_C_Dist);
    client.connect("SIT210_SE_MQTT_Arg");
    
}

void loop() {
    
    
    F_C_Dist = getIRDistance();
    
    //int R_C_Dist = R_C_rangefinder.getDistanceCM();
    
    Particle.publish("Front Centre Distance", (String)F_C_Dist, PUBLIC);
    
    //Particle.publish("Rear Centre Distance", (String)R_C_Dist, PUBLIC);
    
    if (client.isConnected())
    {
        
        
        sprintf(message, "%d", F_C_Dist);
        client.publish("F_C_Distance_Log", message);
        
    }
    else
    {
        Particle.publish("ArgonLog", "Client Not Connected");
    }
    
    delay(500);
    
    client.loop();

}
