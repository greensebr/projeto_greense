#ifndef Atuadores_h
#define Atuadores_h

#include "Arduino.h"
#include "Sensores.h"

extern int hs;
extern int tp;
extern int hd;

class Atuadores {

    public:
        static void ledPainel(unsigned long tempo);
        static void agendaPainel();
     //   static void ledPainel6(int hora);
     //   static void ledPainel0();
        static void exaustor(Sensores& sensor);
   //     void regar(int soloUmid);
        void desligaBomba();
 //       void boiaAlta();
 //       void boiaBaixa();
        bool acionarBomba1(int botaoPin1, bool borda_descida_1, int boiaPin1, int bombaPin1, int soloUmid);
        bool acionarBomba2(bool borda_descida_2, int boiaPin2, int bombaPin2, int boiaPin1);


    private:
        const int botaoPin = 6; // Pino do botão
        const int devolverAguaPin = 11; // Pino do sensor para devolver água



        

};


#endif
