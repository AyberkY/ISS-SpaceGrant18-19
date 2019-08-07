# Simple demo of sending and recieving data with the RFM95 LoRa radio.
import adafruit_rfm9x
import board
import busio
import digitalio
import time

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
                        # module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

#Create text file to store data
air_data = open("air_data.txt", "w+")

def fakeData():
    time = 1
    lat = 2
    long = 3
    dist = 4
    rssi = rfm9x.rssi #this one ain't fake
    return(time,lat,long,dist,rssi)

counter = 0
while True:
    init_time = time.time()
    counter = counter + 1 #remove once we have live data
    if counter > 1:
        break
    print("Round {0}".format(counter))

    Time, Lat, Long, Dist, RSSI = fakeData()
    air_data.write("Time: {0} \nLatitude: {1} \nLongitude: {2} \nDistance: {3} \nRSSI: {4} \n\n".format(Time,Lat,Long,Dist,RSSI))

    # Send a packet.  Note you can only send a packet up to 252 bytes in length.
    # This is a limitation of the radio packet size, so if you need to send larger
    # amounts of data you will need to break it into smaller send calls.  Each send
    # call will wait for the previous one to finish before continuing.
    rfm9x.send(bytes("Time: {0} \nLatitude: {1} \nLongitude: {2} \nDistance: {3} \nRSSI: {4} \n\n".format(Time,Lat,Long,Dist,RSSI),"utf-8"))
    print('Sent data!')
    print("Duration to send data: " + str(time.time() - init_time) + " seconds")

    # Wait to receive packets.  Note that this library can't receive data at a fast
    # rate, in fact it can only receive and process one 252 byte packet at a time.
    # This means you should only use this for low bandwidth scenarios, like sending
    # and receiving a single message at a time.

    # time.sleep(.1)
