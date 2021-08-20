import smbus
import time

def get_fTemp():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    return(str(round(fTemp, 2)))

def get_humidity():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return(str(round(humidity, 2)))
