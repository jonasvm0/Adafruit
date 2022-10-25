import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata


run_count = 0


# Sett inn din egen username/key hentet fra "My Key" p dashboard.
ADAFRUIT_IO_USERNAME = "jonasvm"
ADAFRUIT_IO_KEY = "aio_BfEZ04dBuhvZQn68Z7aFEwHtOH5s"



# Lager en klient som kommuniserer med adafruit-kontoen.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



# Starter opp firmata kommunikasjonen med Arduino.
board = pyfirmata.Arduino('COM3')
it = pyfirmata.util.Iterator(board)
it.start()



# Setter opp digital pinne 4, til vre output.
digital_output = board.get_pin('d:4:o')
# Sjekker frst om der er en feed som heter 'digital'
# Dersom ikke lager man en feed som heter 'digital'
analog_input = board.get_pin('a:0:i')

try:
    digital = aio.feeds('digital')
    analog = aio.feeds('analog')
except RequestError:
    print ("error")
   
while True:


# Teller og sender en counter til en feed som heter 'counter' p adafruit.
    print('Sending count:', run_count)
    run_count += 1
    aio.send_data('counter', run_count)

    analog_value = analog_input.read()
    if analog_value is not None:
      aio.send_data('analog', analog_value) 
    time.sleep(0.01)

  
    # Leser verdi fra en feed med navn 'digital' p adafruit.
    data = aio.receive(digital.key)
    print('Data: ', data.value)
    # Dersom feed vi leser fra adafruit er p, skal utgangen vre aktiv.
    # Dersom den ikke er p, skal den vre av.
    if data.value == "ON":
        digital_output.write(True)
    else:
        digital_output.write(False)
    time.sleep(3)
