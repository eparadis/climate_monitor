from umqtt.simple import MQTTClient
import ubinascii
import time
from dht import DHT22
from machine import Pin, ADC, reset, unique_id
from math import log
from vpd import vpd_kpa
import gc

sensor = DHT22(Pin(14))
adc = ADC(0)

def light_units(x):
  linear = 100.0 * x / 1023.0
  logarithmic = log(linear + 1) * 21.6 # arbitrary constant that looked good
  return logarithmic

def c_to_f(c):
  return c * 9.0 / 5.0 + 32

# MQTT server to connect to
SERVER = "192.168.0.69"
CLIENT_ID = ubinascii.hexlify(unique_id())

# the topic names
temp_tn = b"sensors/greenhouse/temperature"
rh_tn = b"sensors/greenhouse/humidity/relative"
light_tn = b"sensors/greenhouse/light"
vpd_tn = b"sensors/greenhouse/vapor_pressure_difference"

def main():
  print('sleeping 5')
  time.sleep(5)

  print('getting client')
  c = MQTTClient(CLIENT_ID, SERVER)

  # read the sensors
  print('reading sensor')
  sensor.measure()
  temp = c_to_f(sensor.temperature())
  rh = sensor.humidity()
  light = light_units(adc.read())
  vpd = vpd_kpa(temp, rh)

  try:
    print('connecting')
    c.connect()
  except Exception as e:
    print('exception connection!')
    print(e)
    return
  print('publishing')
  c.publish(temp_tn, str(temp))
  c.publish(rh_tn, str(rh))
  c.publish(light_tn, str(light))
  c.publish(vpd_tn, str(vpd))
  print('disconnecting')
  c.disconnect()

  print('sleeping')
  time.sleep(60*2 - 5)
  print('')

def run():
  try:
    main()
  except Exception as e:
    print('outer exception in run()')
    print(e)
  finally:
    print('resetting in 3')
    time.sleep(3)
    reset()

