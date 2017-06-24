int dataColomnPin=10;
int clkColomnPin=11;
int latchColomnPin=12;
int clearColomnPin=13;
int scanRate=1;
int blinkingSpeed=20;
int delays=0;
#define NOP __asm__ __volatile__ ("nop\n\t")

int initialMatrix [8][8]={ {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1},
                           {1,1,1,1,1,1,1,1} };

int initialMatrix1 [8][8]={ {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0},
                            {0,0,0,0,0,0,0,0} };
                
int matrixLeft[8][8]={ {1,1,1,1,0,0,0,0},
                       {1,1,1,1,0,0,0,0},
                       {1,1,1,1,0,0,0,0},
                       {1,1,1,1,0,0,0,0},
                       {0,0,0,0,0,0,0,0},
                       {0,0,0,0,0,0,0,0},
                       {0,0,0,0,0,0,0,0},
                       {0,0,0,0,0,0,0,0} };
int matrixLeftL[8][8]={{1,1,0,0,0,0,0,0},
                       {1,1,0,0,0,0,0,0},
                       {1,1,0,0,0,0,0,0},
                       {1,1,0,0,0,0,0,0},
                       {1,1,0,0,0,0,0,0},
                       {1,1,0,0,0,0,0,0},
                       {1,1,1,1,1,1,1,1},
                       {1,1,1,1,1,1,1,1} };

int matrixPattern[8][8];
void writeData()
{
      digitalWrite(clkColomnPin,HIGH);
      NOP;
      digitalWrite(clkColomnPin,LOW);
      digitalWrite(latchColomnPin,HIGH);
      NOP;
      digitalWrite(latchColomnPin,LOW);
}
void displayMatrix(int matrix[8][8])
{
  for(int i=0;i<8;i++)
  {
    for(int j=0;j<8;j++)
    {
      digitalWrite(j+2,0);
    }
    for(int j=0;j<8;j++)
    {  
        digitalWrite(j+2,matrix[j][i]);
    }
    if(i==0)
    {
      digitalWrite(dataColomnPin,HIGH);
    }
    else
    {
      digitalWrite(dataColomnPin,LOW);
    }
    writeData();
    delay(scanRate);
  }
  for(int j=0;j<8;j++)
  {
    digitalWrite(j,0);
  }
  digitalWrite(dataColomnPin,LOW);
  writeData();
  delay(scanRate);
}
void blinkPattern(int matrix[8][8])
{
  for(int i=0;i<blinkingSpeed;i++)
  {
    displayMatrix(matrix);
  }
  //for(int i=0;i<2;i++)
  //{
    //displayMatrix(initialMatrix1);
  //}
}
void setup() {
Serial.begin(9600);
  // put your setup code here, to run once:
pinMode(dataColomnPin,OUTPUT);
pinMode(clkColomnPin,OUTPUT);
pinMode(latchColomnPin,OUTPUT);
pinMode(clearColomnPin,OUTPUT);
pinMode(2,OUTPUT);
pinMode(3,OUTPUT);
pinMode(4,OUTPUT);
pinMode(5,OUTPUT);
pinMode(6,OUTPUT);
pinMode(7,OUTPUT);
pinMode(8,OUTPUT);
pinMode(9,OUTPUT);
for(int i=0;i<8;i++)
  for(int j=0;j<8;j++)
    matrixPattern[j][i]=matrixLeft[j][i];
}

void loop() {
  blinkPattern(initialMatrix);
  blinkPattern(matrixPattern);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if(inChar=='1')
      for(int i=0;i<8;i++)
        for(int j=0;j<8;j++)
          matrixPattern[j][i]=matrixLeft[j][i];
    if(inChar=='2')
      for(int i=0;i<8;i++)
        for(int j=0;j<8;j++)
          matrixPattern[j][i]=matrixLeftL[j][i];
    }
}


