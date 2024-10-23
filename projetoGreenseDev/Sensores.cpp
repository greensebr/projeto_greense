#include "Sensores.h"

void Sensores::beginDHT() {
    dht.begin();
}


int Sensores::readTemperature() {
    int temperature = round(dht.readTemperature());

    if (isnan(temperature)) {
      //  printError(temperature, -1);
        return -1;
        temperature = 30;
    }
    return temperature;
}


int Sensores::readHumidity() {
    int humidity;
    int humidityParcial;
    const int nAmostras = 50;
    int soma = 0;

    for (int i = 0; i < nAmostras; i++){
        humidityParcial = dht.readHumidity();
        if (isnan(humidityParcial)) {
          humidityParcial = 40;
        }
      
        soma += humidityParcial;
        delay(10);
    }

    humidity = round(soma / nAmostras);
    
    if (isnan(humidity)) {
      //  printError(-1, humidity);
       // return -1;
        humidity = 40;
    }
    return humidity;
}


void Sensores::printTempAndHumAr() {
    int temperature = readTemperature();
    if (isnan(temperature)) {
        temperature =  30;
    }
    int humidity = readHumidity();
    if (isnan(humidity)) {
        humidity =  80;
    }
    

    Serial.print(", TempAmb: ");
    Serial.print(temperature);
    Serial.print("°C, UmidAmb: ");
    Serial.print(humidity);
    Serial.print("%");
}


void Sensores::printError(int temperature, int humidity) {
    Serial.print("Error: ");

 //   if (temperature == DHT::ERROR_TIMEOUT || temperature == DHT::ERROR_CHECKSUM) {
 //       Serial.print("Temperature Reading ");
 //   }

 //   if (humidity == DHT::ERROR_TIMEOUT || humidity == DHT::ERROR_CHECKSUM) {
 //       Serial.print("Humidity Reading ");
 //   }
    Serial.println("Error");
}


/*void Sensores::soloTemp() {
    const int nAmostras = 5;
    int soma = 0;
    for (int i = 0; i < nAmostras; i++){
        soma += analogRead(ThermistorPin);
        delay(10);
    }

    int Vo = soma / nAmostras;

    float R2 = 10000 * (1023.0 / (float)Vo - 1.0);
    float logR2 = log(R2);
    float T = (1.0 / (1.009249522e-03 + 2.378405444e-04*logR2 + 2.019202697e-07*logR2*logR2*logR2));
    int Tc = round(T - 273.15);

    Serial.print(", TempSolo: ");
    Serial.print(Tc);
}
*/

void Sensores::soloTemp(){
    int valor_analogico;
    const int nAmostras = 5;
    int soma = 0;

    for (int i = 0; i < nAmostras; i++){
        soma += analogRead(ThermistorPin);
        delay(10);
    }

    valor_analogico = soma / nAmostras;

    

    int Tc = map(valor_analogico, 406/2, 443, 2*32, 27); 
    //Serial.print("°C, UmidSolo: ");
    //Serial.print(valor_convertido);
    //Serial.print("%");
    if (isnan(Tc)) {
        Tc =  -1;
    }
    Serial.print(", TempSolo: ");
    Serial.print(Tc);
}

int Sensores::soloUmidade(){
    int valor_analogico;
    const int nAmostras = 5;
    int soma = 0;

    for (int i = 0; i < nAmostras; i++){
        soma += analogRead(pinSensorA);
        delay(10);
    }

    valor_analogico = soma / nAmostras;

    int valor_convertido = map(valor_analogico, 1023, 600, 0, 100); 

    if (isnan(valor_convertido)) {
        valor_convertido =  -1;
    }
    
    Serial.print("°C, UmidSolo: ");
    Serial.print(valor_convertido);
    Serial.print("%");
    return valor_convertido;
}


void Sensores::boiaAlta() {
    int estadoBoia = digitalRead(boiaPin1);

    Serial.print(", BoiaAlta: ");
    Serial.print(!estadoBoia);
    delay(100);
}

void Sensores::boiaBaixa() {
    int estadoBoia = digitalRead(boiaPin2);

    Serial.print(", BoiaBaixa: ");
    Serial.print(!estadoBoia);
}
