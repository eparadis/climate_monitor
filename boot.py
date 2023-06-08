# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()

# run our webserver by default. use CTRL-C in the webrepl to stop it
#import webserver

# run our mqtt client by default. use CTRL-C in the webrepl to stop it
import mqtt
