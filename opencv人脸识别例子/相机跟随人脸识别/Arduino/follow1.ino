#include <Servo.h>
 
Servo s;
int degree = 90;
 
void setup()
{
    Serial.begin(115200);
    s.attach(9);
}
 
void loop()
{
    if(Serial.available())
    {
        int cmd = Serial.read();
        if(cmd == 'a')
        {
            degree++;
            if(degree >= 180)
                degree = 180;
            s.write(degree);
        }
        else if(cmd == 'b')
        {
            degree--;
            if(degree <= 0)
                degree = 0;
            s.write(degree);
        }
        else
            Serial.println("Press a/b to turn the camrea!");
    }
}
