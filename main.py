from machine import I2C, Pin, Timer
import socket
import time

i2c = I2C(scl=Pin(2), sda=Pin(0), freq=400000)
exti = Pin(14, Pin.IN)
tim = Timer(1)

""" rejestry i wartości w kolejności:
- PWR_MGMT_1 Rozpoczęcie pracy czujnika
- SMPRT_DIV Częstotliwość próbkowania = 8k/(1+SMPRT_DIV) = 100 Hz
- ACCEL_CONFIG Zakres: +/- 4g
- INT_EN Przerwanie, gdy wszystkie dane gotowe"""

registers = [(0x6B, b'\x00'),
             (0x19, b'\x4f'),
             (0x1C, b'\x08'),
             (0x38, b'\x01')]
accel_out = 0x3B
slave_addr = 0x68

data = bytearray(6)
data_list = []
const= 4.0 / 32768

def unsigned_to_signed(value):
    if value > 32767:
        return value - 65536
    else:
        return value

def callback_exti(p):
    pass

def callback_tim(t):
    i2c.readfrom_mem_into(slave_addr, accel_out, data)
    ts = time.time()
    acX = unsigned_to_signed(data[0] << 8 | data[1]) * const
    acY = unsigned_to_signed(data[2] << 8 | data[3]) * const
    acZ = unsigned_to_signed(data[4] << 8 | data[5]) * const
    print('ts = ', ts, '| acX = ', acX, ' | acY = ', acY, ' | acZ = ', acZ)
    if len(data_list) >= 100:
        del data_list[0]
    data_list.append((ts, acX, acY, acZ))

if __name__ == "__main__":
    for register in registers:
        i2c.writeto_mem(slave_addr, register[0], register[1])
    time.sleep(1)
    tim.init(period=100, mode=Timer.PERIODIC, callback=callback_tim)
    exti.irq(trigger=Pin.IRQ_FALLING, handler=callback_exti)
