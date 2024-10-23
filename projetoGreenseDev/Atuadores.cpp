#include "Atuadores.h"

bool exaustorOn = false;
unsigned long startTime = 0;
unsigned long previousMillis = 0; // Armazena o momento do último toggle do LED
int ledPin = 2; // Pino do LED



/*
void Atuadores::ledPainel12(int hora) {
    bool start = (hora >= 0);
    bool end = (hora < 12);

    if (start && end) {
        digitalWrite(2, LOW);
     //   digitalWrite(5, HIGH);
        Serial.print(", Painel12: 1");
    }
    else {
        digitalWrite(2, HIGH);
    //    digitalWrite(5, HIGH);
        Serial.print(", Painel12: 0");
    }
}
*/

void Atuadores::agendaPainel() {
  if (hs == 12) {
    ledPainel(12UL * 60UL * 60UL * 1000UL);
  } else if (hs == 8) {
    ledPainel(8UL * 60UL * 60UL * 1000UL);
  } else if (hs == 6) {
    ledPainel(6UL * 60UL * 60UL * 1000UL);
  } else {
    digitalWrite(ledPin, LOW);
    Serial.print(", Painel: -1");
  }
}
  






void Atuadores::ledPainel(unsigned long tempo) {
    unsigned long currentMillis = millis(); // Obtém o tempo atual

    // Verifica se o tempo decorrido desde o último toggle é maior ou igual ao intervalo
    if (currentMillis - previousMillis >= tempo) {
        // Salva o tempo do último toggle
        previousMillis = currentMillis;
        // Alterna o estado do LED
        if (digitalRead(ledPin) == LOW) {
            digitalWrite(ledPin, HIGH);
        } else {
            digitalWrite(ledPin, LOW);
        }
    }

      // Alterna o estado do LED
        if (digitalRead(ledPin) == LOW) {
            Serial.print(", Painel12: 1");
        } else {
            Serial.print(", Painel12: 0");
        }




    
}
/*
void Atuadores::ledPainel6(int hora) {
    bool start1 = (hora >= 0);
    bool end1 = (hora < 6);
    bool start2 = (hora >= 12);
    bool end2 = (hora < 18);

    if (start1 && end1){
        digitalWrite(2, LOW);
     //   digitalWrite(5, HIGH);
        Serial.print(", Painel6: 1");
    }

    if (start2 && end2) {
        digitalWrite(2, LOW);
      //  digitalWrite(5, HIGH);
        Serial.print(", Painel6: 1");
    }

    if (!(start1 && end1) && !(start2 && end2)) {
        digitalWrite(2, HIGH);
       // digitalWrite(5, HIGH);
        Serial.print(", Painel6: 0");
    }
}


void Atuadores::ledPainel0() {
    digitalWrite(2, HIGH);
  //  digitalWrite(5, HIGH);
    Serial.print(", Painel0: 0");
}
*/

void Atuadores::exaustor(Sensores& sensor) {
    int temperature = sensor.readTemperature();
    int humidity = sensor.readHumidity();
    bool cond = ((temperature >= tp) || (humidity > hd));
    unsigned long currentTime = millis();

    if (cond) {
        digitalWrite(3, LOW);
        Serial.print(", Exaustor: 1");
        exaustorOn = true;
        startTime = currentTime;
    } else {
        if (exaustorOn && currentTime - startTime >= 60000) {
            digitalWrite(3, HIGH);
            Serial.print(", Exaustor: 0");
            exaustorOn = false;
        } else if (exaustorOn && currentTime - startTime <= 60000) {
            Serial.print(", Exaustor: 1");
        } else {
            Serial.print(", Exaustor: 0");
        }
    }
}


bool Atuadores::acionarBomba1(int botaoPin1, bool borda_descida_1, int boiaPin1, int bombaPin1, int soloUmid) {
    if ((digitalRead(botaoPin1) == LOW && !borda_descida_1 && digitalRead(boiaPin1) == HIGH) || (soloUmid < 70 && digitalRead(boiaPin1) == HIGH)) {
            digitalWrite(bombaPin1, LOW);
            borda_descida_1 = true;
        }
        if ((digitalRead(boiaPin1) == LOW)) {
            digitalWrite(bombaPin1, HIGH);
            borda_descida_1 = false;
        }

   Serial.print(", BombaBaixa: ");
   Serial.print(borda_descida_1);
   delay(100);
   return borda_descida_1;
}


bool Atuadores::acionarBomba2(bool borda_descida_2, int boiaPin2, int bombaPin2, int boiaPin1) {
    if (digitalRead(boiaPin1) == LOW) {
        digitalWrite(bombaPin2, LOW);
        borda_descida_2 = true;
    }
    if (digitalRead(boiaPin2) == HIGH) {
        digitalWrite(bombaPin2, HIGH);
        borda_descida_2 = false;
    }
   Serial.print(", BombaAlta: ");
   Serial.println(borda_descida_2);
   delay(100);
   return borda_descida_2;
}




void Atuadores::desligaBomba() {
    digitalWrite(4, HIGH);
    digitalWrite(5, HIGH);
    delay(100);
}
