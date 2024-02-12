import speech_recognition
import sounddevice
from playsound import playsound
import pexpect 
import re
import os

sr = speech_recognition.Recognizer() 
sr.pause_threshold=1 
durations=0.7 
ID_mic=5 
rec=0 
result = "" 
child = pexpect.spawn('pacmd set-default-sink \'1\'') 
x = ''
y = '' 
R = ['0','1','2','3','4','5','6','7','8','9', 
			'а','б','в','г','д','е','ё','ж','з','и', 'й',
			'к','л','м', 'н', 'о','п','р','с','т','у','ф',
			'х','ц','ч','ш','щ','ъ', 'ы', 'ь', 'э', 'ю', 'я',
			':',' ', '-', '+', '*', '/']
braille = ['101100 ','010000 ','010100 ','110000 ','111000 ','010010 ','110100 ','111100 ','011100 ','100100 ', 
			'010000 ','010100 ','101110 ','111100 ','111000 ','011000 ','010010 ','101100 ','011011 ','100100 ', '110111 ',
			'010001 ','010101 ','110001 ','111001 ','011001 ','110101 ','011101 ','100101 ','101101 ','010011 ', '110100 ',
			'011100 ','110000 ','111101 ','011010 ','110011 ','011111 ', '100111 ', '101111 ', '100110 ', '011110 ', '110110 ',
			'001100', 'n', '000101', '001110', '010001', '001100']

def Recognize_command(): 
    with speech_recognition.Microphone(ID_mic) as mic: 
       sr.adjust_for_ambient_noise(source=mic, duration=durations) 
       playsound('audio/start.wav')
       audio = sr.listen(source=mic)
       playsound('audio/stop.wav')
       try:
          query = sr.recognize_google(audio_data=audio, language='ru-RU').lower() 
          if '.' in query:
             query = query.replace(".", " точка ")
       except speech_recognition.UnknownValueError:
          query = ('Error1') 
       return query 

def Braille2RU(BrailleText) :
    x = ''.join([R[braille.index(fi)] for ch in BrailleText for fi in braille if ch == fi])
    return x
   
def RUSSIAN2Braiile(russianText) :
    y = ''.join([braille[R.index(fi)] for ch in russianText for fi in R if ch == fi])
    return y

while true: 
   query = Recognize_command() 
   if rec==0:
      match query: 
         case 'записать' | 'запись' | 'записываем':
            rec=1
            query = ""
            result = "")
         case 'печать' | 'напечатать':
            e = RUSSIAN2Braiile(result)
            r = open(('/home/orangepi/bot/text.txt','w', encoding='utf-8').write(e)
            os.system("Cfile")
         case 'выключить' | 'выход':
            exit() 
   if rec==1:
      if "Error1" in query:
         query = re.compile('(\s*)Error1(\s*)').sub('\\1''\\2', query)
      if "стоп" in query:
         query = re.compile('(\s*)стоп(\s*)').sub('\\1''\\2', query)
         result = result + ' ' + query
         rec=0
      elif "stop" in query:
         query = re.compile('(\s*)stop(\s*)').sub('\\1''\\2', query)
         result = result + ' ' + query
         rec=0
      else:
         if query != '':
            result = result + ' ' + query
