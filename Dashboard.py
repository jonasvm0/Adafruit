import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata


run_count = 0


# Sett inn din egen username/key hentet fra "My Key" p dashboard.
ADAFRUIT_IO_USERNAME = "jonasvm"
ADAFRUIT_IO_KEY = "aio_quwZ416qt2CWU4qI9wJfMfjyG11h"



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



try:
    digital = aio.feeds('digital')
except RequestError:
    feed = Feed(name='digital')
    digital = aio.create_feed(feed)
while True:
# Teller og sender en counter til en feed som heter 'counter' p adafruit.
    print('Sending count:', run_count)
    run_count += 1
    aio.send_data('counter', run_count)
    # Leser verdi fra en feed med navn 'digital' p adafruit.
    print(aio.receive(digital.key))
#    data = aio.receive(digital.key)
    print('Data: ', data.value)
    # Dersom feed vi leser fra adafruit er p, skal utgangen vre aktiv.
    # Dersom den ikke er p, skal den vre av.
    if data.value == "ON":
        digital_output.write(True)
    else:
        digital_output.write(False)
    time.sleep(3)
