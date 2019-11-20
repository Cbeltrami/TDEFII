//DECLARAÇÕES:

//PARÂMETROS DA DEPOSIÇÃO
int tempob=0, tempoev=0, nciclos=0, accel = -1;
double velocidade0, delaytime = 0.00;
// Dummy variable
int NOP;

//COMUNICAÇÃO SERIAL:
//char Acel_status;
///////////////// Aceleração
double AccelA = 0.00, AccelB = 0.00, AccelC = 0.00;
float PropA = 1.00, PropB = 0.00, PropC = 0.00;
char tipoA = 'L', tipoB = 'L', tipoC = 'L';  

//SERIAL SWITCH
int val;

//SWITCH FÍSICO
int Switch = 13;
//BOTOES
int down = A4;
int up = A5;

//FLAGS
int pronto = 10;
int parado = 11;
int operacao = 12;

//MOTOR
int max_speed = 2;
int Vmax = 760;
int v_subir = 2; //função subir
int phaseA=A3;
int phaseB=A2;
int phaseC=A1;
int phaseD=A0;

//POSICIONADOR
long signed int posicao_garra = 0;
int total_passos=0;

//7 SEGMENTOS
int a = 9; //ok
int b = 7; //ok
int c = 6; //ok
int d = 3; //ok
int e = 8; //ok
int f = 5; //ok
int g = 4; //ok

//AÇÃO
int breaker = 0;

void setup() {
Serial.begin(9600);
//Setup SWITCH
pinMode(Switch, INPUT);
//Setup MOTOR
pinMode(phaseA,OUTPUT);
pinMode(phaseB,OUTPUT);
pinMode(phaseC,OUTPUT);
pinMode(phaseD,OUTPUT);
//Setup FLAGS
pinMode(pronto, OUTPUT);
pinMode(operacao, OUTPUT);
pinMode(parado, OUTPUT);
//Setup BOTÕES
pinMode(up, INPUT);
pinMode(down, INPUT);
//Setup 7 SEGMENTOS
pinMode(a,OUTPUT);
pinMode(b,OUTPUT);
pinMode(c,OUTPUT);
pinMode(d,OUTPUT);
pinMode(e,OUTPUT);
pinMode(f,OUTPUT);
pinMode(g,OUTPUT);

f_7seg_apaga();
digitalWrite(pronto,HIGH);
delay(200);
digitalWrite(pronto,LOW);

//Interrupt Service Routine
attachInterrupt(digitalPinToInterrupt(2), PARADA, RISING);
}

void loop() {
/// INÍCIO /// LOOP
val = Serial.read();

if(val == 'S'){if(total_passos>0){subir(Vmax);}motor_apaga();val = 0;}
if(val == 'D'){if(total_passos>0){descer(Vmax);}motor_apaga();val = 0;}
if(val == 'P'){digitalWrite(pronto,LOW);motor_apaga();val = 0;}      //Se está aqui já está parado OK

if(val == 'R'){receber();val = 0;}    //Receber dados OK
if(val == 'A'){receberAccel();val = 0;}
if(val == 'H'){posicionar();motor_apaga();val = 0;} //Posicionar sistema mecânico OK
if(val == 'K'){accel = accel*(-1);val = 0; Serial.println(accel);}         // Aceleração -1: Desativada - Aceleração 1: Ativada

if(val == 'G')
{
  digitalWrite(operacao,HIGH);  
  if(accel == -1){Dip_coating_classico(delaytime, tempob, tempoev, nciclos);}  //TROCAR PARA ACELERADO!!!!!
  if(accel == 1){Dip_coating_acelerado(velocidade0);}val = 0;
  motor_apaga();
  f_7seg_apaga();
  digitalWrite(operacao,LOW);
  digitalWrite(pronto,HIGH);}   //DEIXAR COMO ESTÁ
  
while(digitalRead(Switch) == HIGH)
{Controle_manual();}
//// FIM //// LOOP
}
/////////////////////////////////////////////////////////////////////////////
////////////////////////    INTERRUPT          //////////////////////////////
/////////////////////////////////////////////////////////////////////////////
//Interrupt Service Routine - botão de emergência
void PARADA()
{
detachInterrupt(digitalPinToInterrupt(2));
motor_apaga();
digitalWrite(parado,HIGH);
while(digitalRead(up)== LOW & digitalRead(down) == LOW)
  {
  NOP = 1; //Operação sem sentido, apenas para manter o loop;
  }
digitalWrite(parado,LOW);
attachInterrupt(digitalPinToInterrupt(2), PARADA, RISING);}
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
/// FUNÇÔES
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
int Controle_manual()
{
  digitalWrite(operacao,HIGH);
  while(digitalRead(Switch) == HIGH)
  {
  if(digitalRead(up) == HIGH){MotorUp_Manual(Vmax);}
  if(digitalRead(down) == HIGH){MotorDown_Manual(Vmax);}   
  motor_apaga();
  }
  digitalWrite(operacao,LOW);
}
/////////////////////////////////////////////////////////////////////////////
int subir(int motor_delay)
{    
while(posicao_garra < total_passos)
    { 
    PassoA();  
    delay_meu(motor_delay);
    posicao_garra++;    
    
    PassoB();
    delay_meu(motor_delay);
    posicao_garra++;
            
    PassoC();
    delay_meu(motor_delay);
    posicao_garra++;
        
    PassoD();
    posicao_garra++;
    delay_meu(motor_delay);
    val=Serial.read();
    if(val == 'P'){return;}}}
/////////////////////////////////////////////////////////////////////////////
int descer(int motor_delay)
{    
while(posicao_garra > 0)
    { 
    PassoD();  
    delay_meu(motor_delay);
    posicao_garra--;    
    
    PassoC();
    delay_meu(motor_delay);
    posicao_garra--;
            
    PassoB();
    delay_meu(motor_delay);
    posicao_garra--;
        
    PassoA();
    delay_meu(motor_delay);
    posicao_garra--;
    val=Serial.read();
    if(val == 'P'){return;}}}
/////////////////////////////////////////////////////////////////////////////
int MotorUp_Manual(int motor_delay)
{
    if(digitalRead(up) == HIGH){
    PassoA();
    delay_meu(motor_delay);}
    if(digitalRead(up) == HIGH){
    PassoB();
    delay_meu(motor_delay);}
    if(digitalRead(up) == HIGH){    
    PassoC();
    delay_meu(motor_delay);}
    if(digitalRead(up) == HIGH){
    PassoD();
    delay_meu(motor_delay);}}
/////////////////////////////////////////////////////////////////////////////
int MotorDown_Manual(int motor_delay) 
{
    if(digitalRead(down) == HIGH){
    PassoD();
    delay_meu(motor_delay);}
    if(digitalRead(down) == HIGH){
    PassoC();
    delay_meu(motor_delay);}
    if(digitalRead(down) == HIGH){
    PassoB();
    delay_meu(motor_delay);}
    if(digitalRead(down) == HIGH){
    PassoA();
    delay_meu(motor_delay);}}
/////////////////////////////////////////////////////////////////////////////
int motor_apaga()
{digitalWrite(phaseA,LOW);
 digitalWrite(phaseB,LOW);
 digitalWrite(phaseC,LOW);
 digitalWrite(phaseD,LOW);} 
/////////////////////////////////////////////////////////////////////////////
int receber()
{
char T[24];
int contador_serial,x_serial;
float V[5];
int n_vars = 24; //25 - 1
int i=0;
//int delaytime, tempob, tempoev, nciclos;
for(contador_serial=0;contador_serial<=n_vars;contador_serial++)
{x_serial=0;
while(x_serial!=1){
if(Serial.available() > 0) 
  {T[contador_serial] = Serial.read();
  break;}}}

for(contador_serial=0;contador_serial<=n_vars;contador_serial++)
{  
if(T[contador_serial]!= ':' and i<=3 and i>=0)
{V[i] = (T[contador_serial] - '0')*1000 + (T[contador_serial+1] - '0')*100 + (T[contador_serial+2] - '0')*10 + (T[contador_serial+3] - '0');
i++; contador_serial=contador_serial+3;}
}

for(contador_serial=0;contador_serial<=3;contador_serial++)  
{Serial.println(int(V[contador_serial]));}

delaytime = V[0];
tempob = V[1];
tempoev = V[2];
nciclos = V[3];
velocidade0 = delaytime/1000.0;
delaytime = 3.906250/velocidade0;
}    // Não mexer. Funciona.
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
int receberAccel()  
{
digitalWrite(operacao,HIGH);
char T[45], R[45];
int contador_serial,x_serial;
int n_vars = 45; //27 - 1
int i=0;

for(contador_serial=0;contador_serial<=n_vars-1;contador_serial++)
{x_serial=0;
while(x_serial!=1){
if(Serial.available() > 0) 
  {T[contador_serial] = Serial.read();
  //delay(300);
  break;}}}

for(contador_serial=0;contador_serial<=n_vars-1;contador_serial++)  
{
  if( T[contador_serial] != ':')
  {
    R[i] = T[contador_serial];
    Serial.println(R[i]);
    i++;
  } }

  AccelA = (R[1]-'0') + (R[2]-'0')/10.0 + (R[3]-'0')/100.0 + (R[4]-'0')/1000.0 + (R[5]-'0')/10000.0 + (R[6]-'0')/100000.0;
  if(R[0] == '-'){AccelA = AccelA*(-1);}
  
  AccelB = (R[8]-'0') + (R[9]-'0')/10.0 + (R[10]-'0')/100.0 + (R[11]-'0')/1000.0 + (R[12]-'0')/10000.0 + (R[13]-'0')/100000.0;
  if(R[7] == '-'){AccelB = AccelB*(-1);}

  AccelC = (R[15]-'0') + (R[16]-'0')/10.0 + (R[17]-'0')/100.0 + (R[18]-'0')/1000.0 + (R[19]-'0')/10000.0 + (R[20]-'0')/100000.0;
  if(R[14] == '-'){AccelC = AccelC*(-1);}
  
  PropA = (R[21]-'0')*100.0 + (R[22]-'0')*10.0 + (R[23]-'0');
  PropA = PropA/100;

  PropB = (R[24]-'0')*100.0 + (R[25]-'0')*10.0 + (R[26]-'0');
  PropB = PropB/100;

  PropC = (R[27]-'0')*100.0 + (R[28]-'0')*10.0 + (R[29]-'0');
  PropC = PropC/100;

  tipoA = R[30];
  tipoB = R[31];
  tipoC = R[32];
  digitalWrite(operacao,LOW);
}
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
int posicionar()
{int PontoA, PontoB, controleA, controleB, AB; 
int PontoA_fixado = 0;
int PontoB_fixado = 0;
int controle_posicao = 1;
posicao_garra = 0;
digitalWrite(operacao,HIGH);

while(PontoA_fixado <= 0 or PontoB_fixado <= 0)
{ 
  val = Serial.read();
  if(val == 'Q'){PontoA_fixado = 1;controleA = controle_posicao;controle_posicao++;PontoA=posicao_garra;}
  if(val == 'W'){PontoB_fixado = 1;controleB = controle_posicao;controle_posicao++;PontoB=posicao_garra;}
  if(val == 'P'){digitalWrite(operacao,LOW); return;}
  val = 'N';
  MotorUp_ManualPosicionar(Vmax);
  MotorDown_ManualPosicionar(Vmax);
  motor_apaga();}
    
  total_passos = abs(PontoA - PontoB);  
  
  if(controleA > controleB and PontoA > PontoB){posicao_garra = total_passos;} //Garra em cima                   
  if(controleA > controleB and PontoB > PontoA){posicao_garra = 0;}            //Garra em baixo 
  
  if(controleB > controleA and PontoB > PontoA){posicao_garra = total_passos;} //Garra em cima                    
  if(controleB > controleA and PontoA > PontoB){posicao_garra = 0;}            //Garra em baixo

  AB = 0;
  while(AB!=1){
  if(Serial.available() > 0) 
  {val = Serial.read();  break;}} 
  if(val == 'B')
  {Serial.println(total_passos);}

digitalWrite(operacao,LOW);}
/////////////////////////////////////////////////////////////////////////////
int MotorDown_ManualPosicionar(int motor_delay)
{   if(digitalRead(down) == HIGH){
    PassoD();
    delay_meu(motor_delay);
    posicao_garra--;}
    if(digitalRead(down) == HIGH){
    PassoC();
    delay_meu(motor_delay);
    posicao_garra--;}
    if(digitalRead(down) == HIGH){    
    PassoB();
    delay_meu(motor_delay);
    posicao_garra--;}
    if(digitalRead(down) == HIGH){
    PassoA();
    delay_meu(motor_delay);
    posicao_garra--;}}
/////////////////////////////////////////////////////////////////////////////
int MotorUp_ManualPosicionar(int motor_delay)
{
    if(digitalRead(up) == HIGH){
    PassoA();
    delay_meu(motor_delay);
    posicao_garra++;}
    if(digitalRead(up) == HIGH){
    PassoB();
    delay_meu(motor_delay);
    posicao_garra++;}
    if(digitalRead(up) == HIGH){
    PassoC();
    delay_meu(motor_delay);
    posicao_garra++;}
    if(digitalRead(up) == HIGH){
    PassoD();
    delay_meu(motor_delay);
    posicao_garra++;}}
/////////////////////////////////////////////////////////////////////////////
int espera(int espera1)
{int espera2; 
  //for(espera2 = 0; espera2<=espera1*60; espera2++) //#minutos
  for(espera2 = 0; espera2<=espera1; espera2++)     //#segundos
  {delay(999);
    val=Serial.read();
    if(val == 'P'){breaker = 1; return;}}}
/////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////    
int Dip_coating_classico(double m_delay, int tbanho, int tevapo, int ciclos)
{ int Ciclo_dip = 0;
  breaker = 0; 
    
  while(Ciclo_dip < ciclos)
  {  
  f_7seg(ciclos - Ciclo_dip);  
  MotorDown_Automatico(760);       //Descer()
  motor_apaga();
  if(breaker>0){return;} //Abort
  
  espera(tbanho);                       //Banho()
  if(breaker>0){return;} //Abort
  
  MotorUp_Automatico(m_delay);   //Sabir()
  motor_apaga();
  if(breaker>0){return;} //Abort
  
  espera(tevapo);                       //Evaporar()
  if(breaker>0){return;} //Abort
  f_7seg_apaga();
  Ciclo_dip++;}}                      
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int Dip_coating_acelerado(double v0)
{
int Ciclo_dip = 0;
int dist_A, dist_B, dist_C;
double v;

//m_speed = velocidade0

dist_A = total_passos*PropA;
dist_B = total_passos*PropB + dist_A;
dist_C = total_passos*PropC + dist_B;

breaker = 0;

while(Ciclo_dip < nciclos)
  {
  v = v0; 
  f_7seg(nciclos - Ciclo_dip);

  MotorDown_Automatico(760);      //Descer()
  motor_apaga();
  if(breaker>0){return;} //Abort
  //////////////////////////////////////////////////////////////////////////////////// 
  
  espera(tempob);                       //Banho()
  if(breaker>0){return;}         //Abort
  //////////////////////////////////////////////////////// 

  if(tipoA == 'L'){v = MotorUp_AutomaticoALinear(v, AccelA, dist_A);}
  else{v = MotorUp_AutomaticoAexp(v, AccelA, dist_A);}
  motor_apaga();
  if(breaker>0){return;}      
  
  if(tipoB == 'L'){v = MotorUp_AutomaticoALinear(v, AccelB, dist_B);}
  else{v = MotorUp_AutomaticoAexp(v, AccelB, dist_B);}
  motor_apaga();
  if(breaker>0){return;}
  
  if(tipoC == 'L'){v = MotorUp_AutomaticoALinear(v, AccelC, dist_C);}
  else{v = MotorUp_AutomaticoAexp(v, AccelC, dist_C);}
  motor_apaga();
  if(breaker>0){return;}
  ////////////////////////////////////////////////////////

  espera(tempoev);                       //Evaporar()
  if(breaker>0){return;}          //Abort

  f_7seg_apaga();
  Ciclo_dip++;}}       
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int delay_meu(unsigned long tempo)
{
  int val;
  unsigned long ccc;
  ccc = 0;
  
  while(ccc<=tempo)
{ val = Serial.read();
  if(val == 'P'){breaker = 1; return;}
  ccc++;}}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
double MotorUp_AutomaticoAexp(double v0, float acel_const, int posicao)
{
double t = 0.00;
double m_delay, v;
m_delay = 3.906250/v0;

while(posicao_garra <= posicao)
  {
  //////////////////////////////////////////////////////////////////////////////
  PassoA();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0*exp(acel_const*t));
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}

  if(acel_const < 0 and  m_delay > 73)
  {
  m_delay = 73;  
  while(posicao_garra <= posicao)
  {
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if(acel_const > 0 and  m_delay < 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoB();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0*exp(acel_const*t));

  if(acel_const < 0 and  m_delay >= 73)
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if(acel_const > 0 and  m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoC();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0*exp(acel_const*t));
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}

  if(acel_const < 0 and  m_delay >= 73)
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if(acel_const > 0 and  m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoD();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0*exp(acel_const*t));

  if(acel_const < 0 and  m_delay >= 73)
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if(acel_const > 0 and  m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}}
  //////////////////////////////////////////////////////////////////////////////
  v = 3.906250/m_delay;
  return v;}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
double MotorUp_AutomaticoALinear(double v0, double acel_const, int posicao)
{
double t = 0.00;
double m_delay, v;
m_delay = 3.906250/v0;

while(posicao_garra <= posicao)
  {
  //////////////////////////////////////////////////////////////////////////////
  PassoA();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0 + acel_const*t);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  
  if (acel_const < 0 and (m_delay <= 0 or m_delay >= 73))
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000); 
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if (acel_const > 0 and m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoB();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0 + acel_const*t);

  if (acel_const < 0 and (m_delay <= 0 or m_delay >= 73))
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if (acel_const > 0 and m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoC();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0 + acel_const*t);
  val=Serial.read();
  if(val == 'P'){breaker = 1; return;}

  if (acel_const < 0 and (m_delay <= 0 or m_delay >= 73))
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if (acel_const > 0 and m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  //////////////////////////////////////////////////////////////////////////////
  PassoD();
  delay_meu(int((m_delay - 0.004531)/0.002264));
  posicao_garra++;
  t = t + (m_delay/1000);
  m_delay = 3.906250/(v0 + acel_const*t);

  if (acel_const < 0 and (m_delay <= 0 or m_delay >= 73))
   {
  m_delay = 73;  
  while(posicao_garra <= posicao)
   {
  PassoA(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}
  PassoC(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(32242); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}
  
  if (acel_const > 0 and m_delay <= 1.725)
   {
  m_delay = 1.725;
  while(posicao_garra <= posicao)
   {
  PassoA(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoB(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoC(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  PassoD(); delay_meu(760); posicao_garra++; t = t + (m_delay/1000);
  val=Serial.read(); if(val == 'P'){breaker = 1; return;}}}}
  //////////////////////////////////////////////////////////////////////////////
  v = 3.906250/m_delay;
  return v;}
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int MotorDown_Automatico(int motor_delay)
{
while(posicao_garra > 0)
    {PassoD();
    delay_meu(motor_delay);
    posicao_garra--;
    if(posicao_garra==0){return;}
    PassoC();
    delay_meu(motor_delay);
    posicao_garra--;
    if(posicao_garra==0){return;}
    PassoB();
    delay_meu(motor_delay);
    posicao_garra--;
    if(posicao_garra==0){return;}
    PassoA();
    delay_meu(motor_delay);
    posicao_garra--;
    val=Serial.read();
    if(val == 'P'){breaker = 1; return;}}}
/////////////////////////////////////////////////////////////////////////////
int MotorUp_Automatico(double m_delay)
{
int delay_const;
delay_const = (m_delay - 0.004531)/0.002264;

while(posicao_garra < total_passos)
    {PassoA();
    delay_meu(delay_const);
    posicao_garra++;
    if(posicao_garra==total_passos){return;}
    PassoB();
    delay_meu(delay_const);
    posicao_garra++;
    if(posicao_garra==total_passos){return;}
    val=Serial.read(); if(val == 'P'){breaker = 1; return;}
    PassoC();
    delay_meu(delay_const);
    posicao_garra++;
    if(posicao_garra==total_passos){return;}
    PassoD();
    delay_meu(delay_const);
    posicao_garra++;
    val=Serial.read();if(val == 'P'){breaker = 1; return;}}}
/////////////////////////////////////////////////////////////////////////////
int PassoA()
{   digitalWrite(phaseA,HIGH);
    digitalWrite(phaseB,LOW);
    digitalWrite(phaseC,LOW);
    digitalWrite(phaseD,HIGH);}
/////////////////////////////////////////////////////////////////////////////
int PassoB()
{   digitalWrite(phaseA,LOW);
    digitalWrite(phaseB,LOW);
    digitalWrite(phaseC,HIGH);
    digitalWrite(phaseD,HIGH);}
/////////////////////////////////////////////////////////////////////////////
int PassoC()
{   digitalWrite(phaseA,LOW);
    digitalWrite(phaseB,HIGH);
    digitalWrite(phaseC,HIGH);
    digitalWrite(phaseD,LOW);}
/////////////////////////////////////////////////////////////////////////////
int PassoD()
{   digitalWrite(phaseA,HIGH);
    digitalWrite(phaseB,HIGH);
    digitalWrite(phaseC,LOW);
    digitalWrite(phaseD,LOW);}
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
int f_7seg(int valor)
{
  f_7seg_apaga();
  if(valor == 0)
{
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,LOW);
digitalWrite(f,LOW);
digitalWrite(g,HIGH);
}
  
  if(valor == 1)
  {
digitalWrite(a,HIGH);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,HIGH);
digitalWrite(e,HIGH);
digitalWrite(f,HIGH);
digitalWrite(g,HIGH);
}
  if(valor == 2)
  {
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,HIGH);
digitalWrite(d,LOW);
digitalWrite(e,LOW);
digitalWrite(f,HIGH);
digitalWrite(g,LOW);
}
  if(valor == 3)
  {
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,HIGH);
digitalWrite(f,HIGH);
digitalWrite(g,LOW);
}
  if(valor == 4)
  {
digitalWrite(a,HIGH);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,HIGH);
digitalWrite(e,HIGH);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}
  if(valor == 5)
  {
digitalWrite(a,LOW);
digitalWrite(b,HIGH);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,HIGH);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}
  if(valor == 6)
  {
digitalWrite(a,LOW);
digitalWrite(b,HIGH);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,LOW);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}
  if(valor == 7)
  {
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,HIGH);
digitalWrite(e,HIGH);
digitalWrite(f,LOW);
digitalWrite(g,HIGH);
}
  if(valor == 8)
  {
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,LOW);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}
  if(valor == 9)
  {
digitalWrite(a,LOW);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,LOW);
digitalWrite(e,HIGH);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}
  if(valor >= 10)
  {
digitalWrite(a,HIGH);
digitalWrite(b,LOW);
digitalWrite(c,LOW);
digitalWrite(d,HIGH);
digitalWrite(e,LOW);
digitalWrite(f,LOW);
digitalWrite(g,LOW);
}return;}
/////////////////////////////////////////////////////////////////////////////
int f_7seg_apaga()
{
 // Apaga tudo 
digitalWrite(a,HIGH);
digitalWrite(b,HIGH);
digitalWrite(c,HIGH);
digitalWrite(d,HIGH);
digitalWrite(e,HIGH);
digitalWrite(f,HIGH);
digitalWrite(g,HIGH); 
return;}
/////////////////////////////////////////////////////////////////////////////
