from machine import ADC, I2C, Pin, Timer
import ssd1306
import time
import math
import writer
import courier20
import json

pot1pin = 26
pot2pin = 27
displayscl = 1
displaysda = 0

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

def load_data():
    try:
        with open("data_log.txt", "r") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []

def save_data():
    with open("data_log.txt", "w") as f:
        json.dump(data_log, f)

data_log = load_data()

def adc_to_per(adc_value, adc_max=65535):
    normalized = adc_value / adc_max
    adjusted = (normalized ** 11) * 100
    return min(max(adjusted, 0), 100)

pot1 = ADC(pot1pin)
pot2 = ADC(pot2pin)

i2c = machine.I2C(0, scl=machine.Pin(displayscl), sda=machine.Pin(displaysda), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
wri = writer.Writer(oled, courier20)

count = 0

while True:
  pot1value = adc_to_per(pot1.read_u16())
  pot2value = adc_to_per(pot2.read_u16())
  oled.fill(0)
  wri.set_textpos(oled, 10, 10)
  wri.printstring(f"{pot1value:.2f}%, {pot2value:.2f}%")
  oled.show()
  
  data_log.append((pot1value, pot2value))
  
  count += 1
  if count == 10:
      save_data()
      count = 0
  
  time.sleep(0.1)
