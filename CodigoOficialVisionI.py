import time, sensor, image, pyb
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

HA = image.Image("/exampleHF1.pgm")
HB = image.Image("/exampleHF2.pgm")
HC = image.Image("/exampleHF3.pgm")

SA = image.Image("/exampleSF1.pgm")
SB = image.Image("/exampleSF2.pgm")
SC = image.Image("/exampleSF3.pgm")

UA = image.Image("/exampleUF1.pgm")
UC = image.Image("/exampleUF3.pgm")

tim = Timer(4, freq=1000)
clock = time.clock()

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

    ha = img.find_template(HA, 0.9, step=4, search=SEARCH_EX)
    hb = img.find_template(HB, 0.85, step=4, search=SEARCH_EX)
    hc = img.find_template(HC, 0.9, step=4, search=SEARCH_EX)

    sa = img.find_template(SA, 0.8, step=4, search=SEARCH_EX)
    sb = img.find_template(SB, 0.8, step=4, search=SEARCH_EX)
    sc = img.find_template(SC, 0.8, step=4, search=SEARCH_EX)

    ua = img.find_template(UA, 0.80, step=4, search=SEARCH_EX)
    uc = img.find_template(UC, 0.80, step=4, search=SEARCH_EX)

    if ha:
        uart.write("%d\n"% 6)
        pyb.delay(20)
        led.on()
        led2.off()
        led3.off()

    elif hb:
        uart.write("%d\n"% 6)
        pyb.delay(20)
        led.on()
        led2.off()
        led3.off()

    elif hc:
        uart.write("%d\n"% 6)
        pyb.delay(20)
        led.on()
        led2.off()
        led3.off()

    elif sa:
        uart.write("%d\n"% 5)
        pyb.delay(20)
        led.off()
        led2.on()
        led3.off()

    elif sb:
        uart.write("%d\n"% 5)
        pyb.delay(20)
        led.off()
        led2.on()
        led3.off()

    elif sc:
        uart.write("%d\n"% 5)
        pyb.delay(20)
        led.off()
        led2.on()
        led3.off()

    elif ua:
        uart.write("%d\n"% 4)
        pyb.delay(20)
        led.off()
        led2.off()
        led3.on()

    elif uc:
        uart.write("%d\n"% 4)
        pyb.delay(20)
        led.off()
        led2.off()
        led3.on()

    else:
        led.off()
        led2.off()
        led3.off()
        for blob in img.find_blobs([thresholds], pixels_threshold= 300, area_threshold=100, merge=True):

            c = blob.count()

            if(c > 0):
                print(blob.pixels())

                uart.write("%d\n"% 9)
                print(blob.cx())
                pyb.delay(20)
                led.on()
                led2.on()
                led3.off()
                break
