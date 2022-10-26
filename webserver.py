import uasyncio as asyncio
from nanoweb import Nanoweb
from dht import DHT22
from machine import Pin, ADC

sensor = DHT22(Pin(14))
adc = ADC(0)

naw = Nanoweb(80)

def c_to_f(c):
  return c * 9.0 / 5.0 + 32

def light_units(x):
  # percentage for now
  return 100.0 * x / 1023.0

@naw.route("/ping")
async def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")

@naw.route("/data.json")
async def data(request):
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    sensor.measure() # it's probably not wise to have this blocking here. instead we should poll the sensor and this should simply report the most recent value and date stamp or some such
    await request.write('{"temp": %f, "RH": %f, "light": %f}\r\n' % (c_to_f(sensor.temperature()), sensor.humidity(), light_units(adc.read())))

loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()
