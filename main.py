import time, sensor, image, pyb
from image import SEARCH_EX, SEARCH_DS
from pyb import Pin, Timer
from pyb import UART
uart = UART(3,9600, timeout_char = 1000)
# Reset sensor
led = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)
sensor.reset()

# Set sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
# Max resolution for template matching with SEARCH_EX is QQVGA
sensor.set_framesize(sensor.QQVGA)
# You can set windowing to reduce the search image.
#sensor.set_windowing(((640-80)//2, (480-60)//2, 80, 60))
sensor.set_pixformat(sensor.GRAYSCALE) # Configuramos escala de grises

# Load template.
# Template should be a small (eg. 32x32 pixels) grayscale image.
templateH = image.Image("/exampleH1.pgm") # Abrimos archivo H
templateS = image.Image("/exampleS1.pgm") # Abrimos archivo S
templateU = image.Image("/exampleU1.pgm") # Abrimos archivo U
tim = Timer(4, freq=1000) # Frequency in Hz
clock = time.clock()

# Run template matching
while (True):
    clock.tick()
    img = sensor.snapshot()
    r = img.find_template(templateH, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    p = img.find_template(templateS, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    q = img.find_template(templateU, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r:
        img.draw_rectangle(r)
        print('H')
        uart.write("%d\n"% 5)

    elif p:
        img.draw_rectangle(p)
        print('S')
        uart.write("%d\n"% 4)

    elif q:
        img.draw_rectangle(q)
        print('U')
        uart.write("%d\n"% 3)

    else:
        print("No_se_reconoce_nada")
