// This #include statement was automatically added by the Particle IDE.
#include <SharpIR.h>



// distances sensors detect
double F_C_Dist = 0.0; //may need to be int

//double F_R_Dist = 0.0;
//double R_C_Dist = 0.0;

// SHARP distance sensor pin and model
int pin = A0;
int model = 1080;

// Ultrasonic pins
//int F_L_trigPin = D4;
//int F_L_echoPin = D5;
//int F_R_trigPin = D3;
//int F_R_echoPin = D2;
//int R_C_trigPin = D5;
//int R_C_echoPin = D4;

// set up sharp sensor with input in and model
SharpIR F_C_rangefinder(pin, model);

// set up ultrasonics with trigger and echo pins and min and max values
//HC_SR04 F_L_rangefinder = HC_SR04(F_L_trigPin, F_L_echoPin, 5, 300);
//HC_SR04 F_R_rangefinder = HC_SR04(F_R_trigPin, F_R_echoPin, 5, 300);
//HC_SR04 R_C_rangefinder = HC_SR04(R_C_trigPin, R_C_echoPin, 5, 300);

void setup() {
    Particle.variable("F_C_Dist", F_C_Dist);
    
}

void loop() {
    
    
    F_C_Dist = F_C_rangefinder.distance();
    //F_L_Dist = F_L_rangefinder.getDistanceCM();
    //F_R_Dist = F_R_rangefinder.getDistanceCM();
    //R_C_Dist = R_C_rangefinder.getDistanceCM();
    
    Particle.publish("Front Centre Distance", (String)F_C_Dist, PUBLIC);
    //Particle.publish("Front Left Distance", (String)F_L_Dist, PUBLIC);
    //Particle.publish("Front Right Distance", (String)F_R_Dist, PUBLIC);
    //Particle.publish("Rear Centre Distance", (String)R_C_Dist, PUBLIC);
    
    
    delay(500);

}
