import uasyncio as asyncio
from nanoweb import Nanoweb
from dht import DHT22
from machine import Pin

sensor = DHT22(Pin(14))

naw = Nanoweb(80)

@naw.route("/ping")
async def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")

@naw.route("/data.json")
async def data(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    sensor.measure() # it's probably not wise to have this blocking here. instead we should poll the sensor and this should simply report the most recent value and date stamp or some such
    await request.write('{"temp": %f, "RH": %f}' % (sensor.temperature(), sensor.humidity()))

loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()
