import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata


run_count = 0


# Kobler deg opp mot Adafruit dashboarded ditt
ADAFRUIT_IO_USERNAME = "jonasvm"
ADAFRUIT_IO_KEY = "aio_rAGU920FogaDN09yn38bbHBf3hXo"



# Lager en klient som kommuniserer med adafruit-kontoen.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



# Starter opp firmata kommunikasjonen med Arduino.
board = pyfirmata.Arduino('COM3')
it = pyfirmata.util.Iterator(board)
it.start()



# Setter opp digital pinne 4, til være output.
digital_output = board.get_pin('d:4:o')
# setter opp analog pinne 0 til input
analog_input = board.get_pin('a:0:i')
# Setter opp digital pinne 2, til være output.
digital_output2 = board.get_pin('d:2:o')
# Setter opp digital pinne 12, til være output.
digital_output3 = board.get_pin('d:12:o')

try:
    digital = aio.feeds('digital')
    analog = aio.feeds('analog') # ser etter feeds "digital" og "analog" og printer "error hvis den ikke finner de
except RequestError:
    print ("error")
   
while True:
# Teller og sender en counter til en feed som heter 'counter' på adafruit.
    print('Sending count:', run_count)
    run_count += 1
    aio.send_data('counter', run_count)

    # Leser analog input og sender dataen til "analog" feeden på Adafruit
    analog_value = analog_input.read()
    if analog_value is not None:
      aio.send_data('analog', analog_value) 
      print('analog: ', analog_value)
    time.sleep(0.01)

 
    # Leser verdi fra en feed med navn 'digital' p adafruit.
    data = aio.receive(digital.key)
    print('Data: ', data.value)
    # Dersom feed vi leser fra adafruit er på, skal utgangen være aktiv.
    # Dersom den ikke er på, skal den vræe av.
    if data.value == "ON":
        digital_output.write(True)
    else:
        digital_output.write(False)

    if analog_value >0.5:
        digital_output2.write(True)
        digital_output3.write(False)
    else:
        digital_output2.write(False)
        digital_output3.write(True)
    time.sleep(3)
