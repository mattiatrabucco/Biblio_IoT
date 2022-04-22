#include <SPI.h>
#include <MFRC522.h>



#define GREENLED 3
#define REDLED 2


#define SS_PIN 40
#define RST_PIN 5
#define SCK_PIN 52
#define MOSI_PIN 51
#define MISO_PIN 50

#define SS1_PIN 42

#define NR_OF_READERS   2

byte ssPins[] = {SS_PIN, SS1_PIN};
MFRC522 mfrc522[NR_OF_READERS];


void setup() {
  Serial.begin(9600);
  SPI.begin(); // init SPI bus
    for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }
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
      Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522[reader].PICC_GetType(mfrc522[reader].uid.sak);
      Serial.println(mfrc522[reader].PICC_GetTypeName(piccType));
      
      char c='\n';
      String stringa="";
      //ASPETTO RISPOSTA DA MAINPY
      
      //if(Serial.available()) {
      while(stringa==""){
            stringa = Serial.readStringUntil(c);
            //Serial.println(stringa);
      }
      if (stringa == "OK\n"){
        digitalWrite(GREENLED, HIGH);
        digitalWrite(REDLED, LOW);
      }
      delay(3000);
      digitalWrite(REDLED, HIGH);
      digitalWrite(GREENLED, LOW);
      // Halt PICC
      mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
    } //if (mfrc522[reader].PICC_IsNewC
  } //for(uint8_t reader  

}

/**
 * Helper routine to dump a byte array as hex values to Serial.
 */
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
