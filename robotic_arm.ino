#include <Servo.h>

#define OPEN_CLOSE_PIN 3
#define UP_DOWN_PIN 5
#define LEFT_RIGHT_PIN 6
#define FORWARD_BACKWARD_PIN 9

struct {
  Servo openClose;
  Servo upDown;
  Servo leftRight;
  Servo forwardBacward;
} RoboticArm;

struct {
  int open_close = 0;
  int up_down = 0;
  int left_right = 0;
  int forward_backward = 0;
} ServosAngle;

struct {
  int open_close[2] = {50, 130};
  int up_down[2] = {50, 130};
  int left_right[2] = {0, 180};
  int forward_backward[2] = {80, 150};
} ServosBounds;

String key = "";
int angle_step = 0;

void setup() {
  Serial.begin(9600);

  RoboticArm.openClose.attach(OPEN_CLOSE_PIN);
  RoboticArm.upDown.attach(UP_DOWN_PIN);
  RoboticArm.leftRight.attach(LEFT_RIGHT_PIN);
  RoboticArm.forwardBacward.attach(FORWARD_BACKWARD_PIN);

  RoboticArm.openClose.write(ServosBounds.open_close[0]);
  RoboticArm.upDown.write(ServosBounds.up_down[0]);
  RoboticArm.leftRight.write(ServosBounds.left_right[0]);
  RoboticArm.forwardBacward.write(ServosBounds.forward_backward[0]);

}

void loop() {
  if (Serial.available()){

    key = Serial.readStringUntil(':');
    angle_step = Serial.readStringUntil(':').toInt();

    if (key.equals("W")){

      ServosAngle.up_down += angle_step;

      if (ServosAngle.up_down > ServosBounds.up_down[1]){
        ServosAngle.up_down = ServosBounds.up_down[1];
      }
  
      RoboticArm.upDown.write(ServosAngle.up_down);

    } else if (key.equals("A")){

      ServosAngle.open_close -= angle_step;

      if (ServosAngle.open_close < ServosBounds.open_close[0]){
        ServosAngle.open_close = ServosBounds.open_close[0];
      }
      
      RoboticArm.openClose.write(ServosAngle.open_close);

    } else if (key.equals("D")){

      ServosAngle.open_close += angle_step;

      if (ServosAngle.open_close > ServosBounds.open_close[1]){
        ServosAngle.open_close = ServosBounds.open_close[1];
      }
      
      RoboticArm.openClose.write(ServosAngle.open_close);

    } else if (key.equals("S")){
      
      ServosAngle.up_down -= angle_step;

      if (ServosAngle.up_down < ServosBounds.up_down[0]){
        ServosAngle.up_down = ServosBounds.up_down[0];
      }
      
      RoboticArm.upDown.write(ServosAngle.up_down);
      
    } else if (key.equals("UP")){
      
      ServosAngle.forward_backward += angle_step;

      if (ServosAngle.forward_backward > ServosBounds.forward_backward[1]){
        ServosAngle.forward_backward = ServosBounds.forward_backward[1];
      }
      
      RoboticArm.forwardBacward.write(ServosAngle.forward_backward);

    } else if (key.equals("LEFT")){

      ServosAngle.left_right += angle_step;

      if (ServosAngle.left_right < ServosBounds.left_right[0]){
        ServosAngle.left_right = ServosBounds.left_right[0];
      }

      RoboticArm.leftRight.write(ServosAngle.left_right);

    } else if (key.equals("RIGHT")){
      
      ServosAngle.left_right -= angle_step;

      if (ServosAngle.left_right > ServosBounds.left_right[1]){
        ServosAngle.left_right = ServosBounds.left_right[1];
      }

      RoboticArm.leftRight.write(ServosAngle.left_right);

    } else if (key.equals("DOWN")){
      
      ServosAngle.forward_backward -= angle_step;

      if (ServosAngle.forward_backward < ServosBounds.forward_backward[0]){
        ServosAngle.forward_backward = ServosBounds.forward_backward[0];
      }

      RoboticArm.forwardBacward.write(ServosAngle.forward_backward);

    }

  }
}
