#include "Configs.h"
#include "Sensores.h"
#include "Atuadores.h"
//#include <avr/wdt.h>

bool borda_descida_1 = false;
bool borda_descida_2 = false;


// Declarando objetos:
Configs config;

Atuadores atuador_painel; 
Atuadores atuador_exaustor;
Atuadores atuador_rega;

//Variáveis:
#define pinSensorA A0   
int pinDHT = 10; // sensor umidade e temperatura do ar;
int pinThermistor = 3; // sensor temperatura solo;
int mark, hs, tp, hd;
int soloUmid;
String param = "in 30 60 12"; // temp, umid, painel;

const int botaoPin1 =  6; //rega
const int bombaPin1 = 4;
const int boiaPin1 = 8; // boia1

const int botaoPin2 =  11; //rega
const int bombaPin2 = 5;
const int boiaPin2 = 9; // boia2

const int devolverAguaPin = 11;
Sensores sensor(pinDHT, pinThermistor); // precisa ser declarado depois das variáveis;


void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  
  pinMode(botaoPin1, INPUT);
  pinMode(bombaPin1, OUTPUT);
  pinMode(boiaPin1, INPUT); 

  pinMode(botaoPin2, INPUT);
  pinMode(bombaPin2, OUTPUT);
  pinMode(boiaPin2, INPUT); 
  
  digitalWrite(3, HIGH);
  atuador_rega.desligaBomba();
  sensor.beginDHT();
  //wdt_enable(WDTO_2S);

}

  
void loop() {

  //Configurações iniciais:
  config.digitalClockDisplay(); // HH:MM:SS DD/MM/YYYY
  config.readSerialData(); // leitura e impressão dos parâmetros;


  atuador_painel.agendaPainel(); 
  
  //Atuadores:
  atuador_exaustor.exaustor(sensor); // passa um objeto da classe Sensor para medir temp e umidade do ar;

  //Sensores:
  sensor.printTempAndHumAr(); // leitura e impressão da temperatura e umidade do ar;
  sensor.soloTemp(); // leitura e impressão da temperatura do solo;
  soloUmid = sensor.soloUmidade(); // leitura e impressão da umidade do solo;
  
  sensor.boiaBaixa();
  sensor.boiaAlta();

  borda_descida_1 = atuador_rega.acionarBomba1(botaoPin1, borda_descida_1, boiaPin1, bombaPin1, soloUmid); 
  borda_descida_2 = atuador_rega.acionarBomba2(borda_descida_2, boiaPin2, bombaPin2, boiaPin1); 
  //Serial.println(soloUmid);  

  //wdt_reset();
  delay(2000);
}
