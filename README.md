# A climate monitor for my greenhouse

## Hardware
- ESP8266 based board (in my case, the Nodelink D1, based on the ESP12)
 - [Nodeline D1 schematic](https://s3.amazonaws.com/linksprite/Linknode+D1/LinkNode-D1-sch.pdf)
- Temp/RH sensors like the DHT22

## Software
- micropython 1.19.1 (at time of writing)
 - built-in sensor support for [DHT](https://docs.micropython.org/en/latest/esp8266/quickref.html#dht-driver)
- a micropython webserver like [nanoweb](https://github.com/hugokernel/micropython-nanoweb)
- [BIPES](http://bipes.net.br/ide/) is a nice IDE for working with web-attached micropython boards like the ESP8266 ones

# NOTES

Just gluing things together in the REPL:
```
from machine import Pin
from machine import Timer
from machine import RTC
import dht

d = dht.DHT22(Pin(14))
tim = Timer(-1)
rtc = RTC()

tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:print([t, rtc.datetime(), d.measure(), d.temperature(), d.humidity()]))
```


