import time, sensor, image, pyb, utime
from image import SEARCH_EX, SEARCH_DS
from pyb import Pin, Timer
from pyb import UART
uart = UART(3, 115200)

led = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)

thresholds = (0, 20)

sensor.reset()
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.skip_frames(time = 1000)

Hb = image.Image("/H1DEF.pgm")
Ha = image.Image("/H1sc.pgm")

Sa = image.Image("/S1.pgm")
Sb = image.Image("/S2.pgm")

tim = Timer(4, freq=1000)
clock = time.clock()

c = 0

led.on()
pyb.delay(200)
led.off()
pyb.delay(200)
led2.on()
pyb.delay(200)
led2.off()
pyb.delay(200)
led3.on()
pyb.delay(200)
led3.off()
pyb.delay(200)

while (True):
    clock.tick()

    img = sensor.snapshot()

    ha = img.find_template(Ha, 0.8, step=4, search=SEARCH_EX)
    hb = img.find_template(Hb, 0.8, step=4, search=SEARCH_EX)

    sa = img.find_template(Sa, 0.6, step=4, search=SEARCH_EX)
    sb = img.find_template(Sb, 0.6, step=4, search=SEARCH_EX)

    if ha:
        uart.write("%d\n"% 6)
        print('H1')
        img.draw_rectangle(ha)
        pyb.delay(20)
        led.on()
        led2.off()
        led3.off()
        pyb.delay(50)
        led.off()
        led2.off()
        led3.off()
        pyb.delay(50)

        utime.sleep(20)

    elif hb:
        print('H3')
        uart.write("%d\n"% 6)
        img.draw_rectangle(hA)
        pyb.delay(20)
        led.on()
        led2.off()
        led3.off()
        pyb.delay(50)
        led.off()
        led2.off()
        led3.off()
        pyb.delay(50)

        utime.sleep(20)

    elif sa:
        print('S1')
        uart.write("%d\n"% 5)
        img.draw_rectangle(sa)
        pyb.delay(20)
        led.off()
        led2.on()
        led3.off()
        pyb.delay(50)
        led.off()
        led2.off()
        led3.off()
        pyb.delay(50)

       # utime.sleep(20)

    elif sb:
        print('S3')
        uart.write("%d\n"% 5)
        img.draw_rectangle(sc)
        pyb.delay(20)
        led.off()
        led2.on()
        led3.off()
        pyb.delay(50)
        led.off()
        led2.off()
        led3.off()
        pyb.delay(50)

        #utime.sleep(20)

    else:
        uart.write("%d\n"% 0)
#led.on()
#led2.on()
#led3.on()
