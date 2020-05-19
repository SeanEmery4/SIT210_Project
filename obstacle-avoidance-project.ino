// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

// This #include statement was automatically added by the Particle IDE.
#include <SharpIR.h>

//MQTT object client to free MQTT test broker
MQTT client("test.mosquitto.org", 1883, callback);

// Method called when a message is received. Not needed
void callback(char* topic, byte* payload, unsigned int length) { }

// distances sensor value variable
int F_C_Dist = 0; 

// message to pass to MQTT broker variable
char message[4];

// SHARP distance sensor pin and model
int pin = A1;
int model = 1080;

// set up sharp sensor with input in and model
SharpIR F_C_rangefinder(pin, model);

// Ultrasonic not working
//double R_C_Dist = 0.0;

// Ultrasonic pins - not working
//int R_C_trigPin = D5;
//int R_C_echoPin = D4;

// set up ultrasonics with trigger and echo pins and min and max values - not working
//HC_SR04 R_C_rangefinder = HC_SR04(R_C_trigPin, R_C_echoPin, 10, 100);

// function to return value from sharp sensor between 80 and 10
// greater than 80 means clear, 10 is anything between 0 and 10
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


// set up particle variable and connect to MQTT broker
void setup() {
    Particle.variable("F_C_Dist", F_C_Dist);
    client.connect("SIT210_SE_MQTT_Arg");
    
    //set up message to iniciate for first if statement
    sprintf(message, "%d", F_C_Dist);
}

// continuous loop
void loop() {
    
    // get sensor reading and store in F_C_Dist
    F_C_Dist = getIRDistance();
    
    // publish distance to events tab for viewing and debugging
    //Particle.publish("Front Centre Distance", (String)F_C_Dist, PUBLIC); // for testing
    
    
    // if client is connected to MQTT broker then publish reading to broker, if not publish error
    if (client.isConnected())
    {
        // test to see if F_C_Dist has changed since last loop
        // if not don't publish same value
        if ((String)F_C_Dist != message)
        {
            // if distance has changed publish new value
            sprintf(message, "%d", F_C_Dist);
            client.publish("F_C_Distance_Log", message, true); // true is to retain most recent publish. So if Pi subscribes after latest publish it still gets most recent message
        }
       
    }
    else
    {
        client.publish("F_C_Distance_Log", "Error");
        //Particle.publish("MQTT_Error", "Client Not Connected"); // for testing
    }
    
    delay(100);
   
    client.loop();

}
