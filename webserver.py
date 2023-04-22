import uasyncio as asyncio
from nanoweb import Nanoweb
from dht import DHT22
from machine import Pin, ADC
from vpd import vpd_kpa
from math import log

sensor = DHT22(Pin(14))
adc = ADC(0)

naw = Nanoweb(80)

def c_to_f(c):
  return c * 9.0 / 5.0 + 32

def light_units(x):
  linear = 100.0 * x / 1023.0
  logarithmic = log(linear + 1) * 21.6 # arbitrary constant that looked good
  return logarithmic

@naw.route("/ping")
async def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")

@naw.route("/mem_info")
async def memory_info(request):
    from micropython import mem_info
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write(mem_info())

@naw.route("/data.json")
async def data(request):
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    sensor.measure() # it's probably not wise to have this blocking here. instead we should poll the sensor and this should simply report the most recent value and date stamp or some such
    temp = c_to_f(sensor.temperature())
    rh = sensor.humidity()
    light = light_units(adc.read())
    vpd = vpd_kpa(temp, rh)
    fields = (temp, rh, light, vpd)
    await request.write('{"temp": %f, "RH": %f, "light": %f, "vpd": %f}\r\n' % fields)

loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()
