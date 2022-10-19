import uasyncio as asyncio
from nanoweb import Nanoweb

naw = Nanoweb(80)
naw.assets_extensions += ('ico',)

@naw.route("/ping")
async def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")

loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()
