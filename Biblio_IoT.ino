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

void setup() {
  Serial.begin(9600);

  SPI.begin(); // init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) 
  {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }

  //Display setup:
  lcd.init();                    //initialize
  lcd.backlight();               //turn on backlight
  lcd.print("Biblio IoT"); //display startup message

  //LED setup:
  pinMode(GREENLED, OUTPUT);
  pinMode(REDLED, OUTPUT);
  digitalWrite(REDLED, HIGH);
  digitalWrite(GREENLED, LOW);
}

void loop() {
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Look for new cards
    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
      Serial.print(F("Reader "));
      Serial.print(reader);
      // Show some details of the PICC (that is: the tag/card)
      Serial.print(F(": Card UID:"));
      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
      Serial.println();
      /*Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522[reader].PICC_GetType(mfrc522[reader].uid.sak);
      Serial.println(mfrc522[reader].PICC_GetTypeName(piccType));*/
      
      String stringa="";
      char c='\n';

      delay(28); //waiting python script
      
      while(stringa==""){
            stringa = Serial.readStringUntil(c);
      }
      if (stringa == "OK"){
        digitalWrite(GREENLED, HIGH);
        digitalWrite(REDLED, LOW);

        lcd.clear();            //Clear display
        lcd.setCursor(0, 0);    //Write on the first row
        if (reader == 0)
        {
          lcd.print("Benvenuto,"); //Print title on external display
        }
        else if (reader == 1) {
          lcd.print("Arrivederci,"); //Print title on external display
        }
        
        lcd.setCursor(0, 1);    //Write on the second row
        dump_byte_array_to_lcd(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
      }

      delay(800);

      lcd.clear(); //reset display
      lcd.setCursor(0, 0);

      digitalWrite(REDLED, HIGH);
      digitalWrite(GREENLED, LOW);

      // Halt PICC
      mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
    } 
  }
}

// Helper routine to dump a byte array as hex values to Serial.
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
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