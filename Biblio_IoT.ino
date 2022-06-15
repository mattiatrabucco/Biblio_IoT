#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>

#define GREENLED 3
#define REDLED 2

#define SS_PIN 40
#define RST_PIN 5
#define SCK_PIN 52
#define MOSI_PIN 51
#define MISO_PIN 50

#define SS1_PIN 42

#define NR_OF_READERS 2

//RFID reader requirements
byte ssPins[] = {SS1_PIN, SS_PIN};
MFRC522 mfrc522[NR_OF_READERS];

//Display requirements
LiquidCrystal_I2C lcd(0x27, 16, 2);

//Variabile usata per controllare i dati a intervalli regolari
unsigned long display_millis, bridge_millis;

//FSM states
int ser_state, f_ser_state;

//In order to wait the python script
bool var_state;

//Saves the current reader ID
uint8_t cur_reader;

void setup() {
  Serial.begin(9600);

  SPI.begin(); // init SPI bus

  //Var setup
  bridge_millis = display_millis = millis();
  ser_state = f_ser_state = 0;
  var_state = true;
  cur_reader = 0;

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) 
  {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    // Serial.print(F("Reader "));
    // Serial.print(reader);
    // Serial.print(F(": "));
    // mfrc522[reader].PCD_DumpVersionToSerial();
    // delay(1000);
  }

  //Display setup:
  lcd.init();                    //initialize
  lcd.backlight();               //turn on backlight
  lcd.print("Biblio IoT");       //display startup message

  //LED setup:
  pinMode(GREENLED, OUTPUT);
  pinMode(REDLED, OUTPUT);
  digitalWrite(REDLED, HIGH);
  digitalWrite(GREENLED, LOW);
}

void loop() {


  if ((millis() - bridge_millis > 200) && !var_state) {
    bridge_millis = millis();

    uint8_t status_code = status_read();
      if (status_code == 1){
        digitalWrite(GREENLED, HIGH);
        digitalWrite(REDLED, LOW);

        display_millis = millis();

        lcd.clear();            //Clear display
        lcd.setCursor(0, 0);    //Write on the first row
        
        if (cur_reader == 0)
        {
          lcd.print("Benvenuto,"); //Print title on external display
        }
        else if (cur_reader == 1) {
          lcd.print("Arrivederci,"); //Print title on external display
        }
        
        lcd.setCursor(0, 1);    //Write on the second row
        dump_byte_array_to_lcd(mfrc522[cur_reader].uid.uidByte, mfrc522[cur_reader].uid.size);
      }
      else if (status_code == 2) {
        display_millis = millis();

        lcd.clear();            //Clear display
        lcd.setCursor(0, 0);    //Write on the first row
        lcd.print("Errore");    //Print title on external display
      }
    
    var_state = true; //we can now turn back on reading
  }

  if (millis() - display_millis > 3000) {
    display_millis = millis();

    lcd.clear(); //reset display
    lcd.setCursor(0, 0);

    digitalWrite(REDLED, HIGH); //restore LEDs
    digitalWrite(GREENLED, LOW);
  }

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Look for new cards
    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial() && var_state) {
      
      Serial.print(reader);
      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size); //send card ID to serial
      Serial.write(0xFF);
      
      // In order to wait the python script  
      var_state = false;
      cur_reader = reader;

      // Halt PICC
      mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
    } 
  }
}

uint8_t status_read(){
  while(Serial.available()){
    uint8_t c = Serial.read();
    f_ser_state = 0;
    if(c == 'O' && ser_state == 0)  f_ser_state = 1;
    if(c == 'N' && ser_state == 0)  f_ser_state = 3;
    if(c == 'K' && ser_state == 1)  f_ser_state = 2;
    if(c == 'O' && ser_state == 3)  f_ser_state = 4;
    ser_state = f_ser_state ;
  }
  if(ser_state == 2) {
    f_ser_state = ser_state = 0;
    return 1; //OK
  }
  if(ser_state == 4) {
    f_ser_state = ser_state = 0;
    return 2; //NO
  }
  return 0;
}

// Helper routine to dump a byte array as hex values to Serial.
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? "0" : "");
    Serial.print(buffer[i], HEX);
  }
}

// Helper routine to dump a byte array as hex values to LCD display.
void dump_byte_array_to_lcd(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    lcd.print(buffer[i] < 0x10 ? " 0" : " ");
    lcd.print(buffer[i], HEX);
  }
}