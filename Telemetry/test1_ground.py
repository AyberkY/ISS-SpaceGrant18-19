# Simple demo of sending and recieving data with the RFM95 LoRa radio.
import adafruit_rfm9x
import board
import busio
import digitalio

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
ground_data = open("ground_data.txt", "w+")

try:
    while True:
        packet = rfm9x.receive()
        # Optionally change the receive timeout from its default of 0.5 seconds:
        #packet = rfm9x.receive(timeout=5.0)
        # If no packet was received during the timeout then None is returned.
        if packet is None:
            # Packet has not been received
            print('Received nothing! Listening again...')
        else:
            # Received a packet!
            # Print out the raw bytes of the packet:
            #print('Received (raw bytes): {0}'.format(packet))

            # And decode to ASCII text and print it too.  Note that you always
            # receive raw bytes and need to convert to a text format like ASCII
            # if you intend to do string processing on your data.  Make sure the
            # sending side is sending ASCII data before you try to decode!
            packet_text = str(packet, 'ascii')
            print('Received (ASCII): {0}\n'.format(packet_text))

            #Write data to text file
            ground_data.write(packet_text)
            print("Saved data to text file.\n")

            # Also read the RSSI (signal strength) of the last received message and
            # print it.
            rssi = rfm9x.rssi
            print('Received signal strength: {0} dB'.format(rssi))

            break #replace with better way to exit program
except KeyboardInterrupt:
    print("\nending program.")
