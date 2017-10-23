#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

String inString = "";
int exp_dur_rem = 0;
int laser_dur_rem = 0;
int start_counting = 0;
int set_total_time = 0;
int niter = 10;
int laser_on;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lcd.begin(16, 2);
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
    //Q Show on LCD
    if (inChar == 'Q') {
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
      laser_dur_rem = inString.toInt(); 
      start_counting = 0;
      count_down();
    }
    if (set_total_time == 1) {
      exp_dur_rem = inString.toInt(); 
      set_total_time = 0;
    }
}

void count_down() {
  unsigned long start_ms = millis();    
  unsigned long current_ms = start_ms;
  unsigned long 5sec_delay = 5;
  unsigned long previous_ms = current_ms;
  int lasertime = 0
  long interval = 5;
  
  while ((current_ms - start_ms) < exp_dur_rem ) {
    current_ms = millis();
    if ((current_ms - previous_ms) >= 5sec_delay) {
      if (lasertime == 0) {
        current_ms = millis();
        lcd.home();
        lcd.print("Time Until Next");
        lcd.setCursor(0,1);
        lcd.print("Pulse: ");
        lcd.print()
        lasertime = 1;
      } else {
        current_ms millis();
        previous_ms = current_ms;
        lasertime = 0;
      }  
    } 
  }
}