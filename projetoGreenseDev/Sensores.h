#ifndef Sensores_h
#define Sensores_h

#include "Arduino.h"
#include "DHT.h"
#include "Thermistor.h"

// Definições das constantes
#define DHTPIN 10     // Pino digital conectado ao sensor DHT
#define DHTTYPE DHT22 // Tipo do sensor DHT (DHT22 ou similar)

extern int tp;
extern int hd;
extern int pinSensorA;

class Sensores {
public:
    // Construtor da classe Sensores
    Sensores(int pinDHT, int pinThermistor) : dht(pinDHT, DHTTYPE), ThermistorPin(pinThermistor) {}

    // Métodos públicos da classe Sensores
    int readTemperature();
    int readHumidity();
    void printTempAndHumAr();
    void soloTemp();
    int soloUmidade();
    void beginDHT();
    void boiaAlta();
    void boiaBaixa();
    

private:
    DHT dht;           // Objeto DHT para o sensor
    
    int ThermistorPin; // Pino do termistor
    int pinSensorA;    // Pino do sensor A (não utilizado nesta versão)

    // Método privado para imprimir erro
    static void printError(int temperature, int humidity);
    const int boiaPin1 = 8; // Pino da boia 1
    const int boiaPin2 = 9; // Pino da boia 2
};

#endif
