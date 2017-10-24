//there are two things to edit (how to process when 'R' is passed and terminating when the experiment ends)
//there should be some delay before passing "M"

#include <LiquidCrystal.h>
#include <Time.h>

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

String inString = "";
int exp_dur = 1200; //in seconds
int laser_dur_rem = 10  ; //in seconds

//T or F
int start_counting = 0;
int set_total_time = 0;
int start_counting_laser = 0;
int waiting_pulse = 0;

//Set Numbers
int sec_delay = 5;
int niter = 10;
int laser_on;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Waiting to start");
  lcd.setCursor(0, 1);
  lcd.print("the experiment..");
}


void loop() {
  // Read serial input
  
  while (Serial.available() > 0) {
    int inChar = Serial.read();

    // if we encounter a number
    if (isDigit(inChar)) {
      inString += (char)inChar;
    }

    // if it's a letter: Test if it's
    //S Start counting down
    //T Set total time
    if (inChar == 'S') {
      start_counting = 1;
    } else if (inChar == 'T') {
      set_total_time = 1;
    } else if (inChar == '\n') {
      process_input();
      inString = "";
    }
  }
}

void process_input() {
  if (start_counting == 1) {
    start_counting = 0;
    count_down();
  }
  if (set_total_time == 1) {
    exp_dur = inString.toInt();
    set_total_time = 0;
  }
}

void count_down() {
  unsigned long start_ms = millis();
  unsigned long lstart_ms = millis();
  unsigned long current_ms = start_ms;
  unsigned long previous_ms = current_ms;
  unsigned long ms2s = 1000;
  unsigned long s2m = 60;
  unsigned long m2h = 60;
  int disp_time_left = 1;
  lcd.clear();

  while ((current_ms - start_ms) < exp_dur*ms2s) {
    current_ms = millis();
    if (disp_time_left == 1) {
      lcd.home();
      lcd.print("Time Until End:");
      lcd.setCursor(0, 1);
      lcd.print((exp_dur*ms2s - (current_ms - start_ms)) / ms2s / s2m);
      lcd.print(" min");
      delay(5000);
      lcd.clear();
      if (waiting_pulse == 1) {
        current_ms = millis();
        if ((laser_dur_rem*ms2s - (current_ms - lstart_ms)) / ms2s <= 10) {
          waiting_pulse = 0;
        } else {
          current_ms = millis();
          lcd.home();
          lcd.print("Time Until Next");
          lcd.setCursor(0, 1);
          lcd.print("Pulse: ");
          lcd.print((laser_dur_rem*ms2s - (current_ms - lstart_ms)) / ms2s / s2m);
          lcd.print(" min");
          delay(5000);
          lcd.clear();
        }
      } else {
        while (Serial.available() > 0) {
          int inChar = Serial.read();
          // if we encounter a number
          if (isDigit(inChar)) {
            inString += (char)inChar;
            }
          //M Start counting down
          if (inChar == 'M') {
            start_counting_laser = 1;
          } else if (inChar == '\n') {
            process_input2();
            inString = "";
            lstart_ms = millis();
          }
        }
      }
    }
  }
  lcd.print("Experiment ended");
  lcd.setCursor(0, 1);
  lcd.print("Move avi & param");
}
void process_input2() {
  unsigned long lstart_ms = 0;
  if (start_counting_laser == 1) {
    laser_dur_rem = inString.toInt();
    start_counting_laser = 0;
    waiting_pulse = 1;
    }
  }

