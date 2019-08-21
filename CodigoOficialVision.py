import time, sensor, image, pyb
from image import SEARCH_EX, SEARCH_DS
from pyb import Pin, Timer
from pyb import UART
uart = UART(3,9600, timeout_char = 1000)
# Reset sensor
led = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)
thresholds = (0, 55) #Rangos negro

sensor.reset()

# Set sensor settings
# Max resolution for template matching with SEARCH_EX is QQVGA
sensor.set_framesize(sensor.QQVGA)
# You can set windowing to reduce the search image.
#sensor.set_windowing(((640-80)//2, (480-60)//2, 80, 60))
sensor.set_pixformat(sensor.GRAYSCALE) # Configuramos escala de grises
sensor.skip_frames(time = 100)

# Load template.
# Template should be a small (eg. 32x32 pixels) grayscale image.
templateH1 = image.Image("/exampleH1.pgm") # Abrimos archivo H1
templateH2 = image.Image("/exampleH2.pgm") # Abrimos archivo H2
templateH3 = image.Image("/exampleH3.pgm") # Abrimos archivo H3

templateS1 = image.Image("/exampleS1.pgm") # Abrimos archivo S1
templateS2 = image.Image("/exampleS2.pgm") # Abrimos archivo S3
templateS3 = image.Image("/exampleS3.pgm") # Abrimos archivo S3

templateU1 = image.Image("/exampleU1.pgm") # Abrimos archivo U1
templateU3 = image.Image("/exampleU3.pgm") # Abrimos archivo U3

tim = Timer(4, freq=1000) # Frequency in Hz
clock = time.clock()

# Run template matching
while (True):
    clock.tick()

    img = sensor.snapshot()

    rp = img.find_template(templateH1, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    rt = img.find_template(templateH2, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    rq = img.find_template(templateH3, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))

    tp = img.find_template(templateS1, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    tt = img.find_template(templateS2, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    tq = img.find_template(templateS3, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))

    zt = img.find_template(templateU1, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    zq = img.find_template(templateU3, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))

    if rp:
        img.draw_rectangle(rp)
        print('H')
        uart.write("%d\n"% 2)

    elif rt:
        img.draw_rectangle(rt)
        print('H')
        uart.write("%d\n"% 2)
    elif rq:
        img.draw_rectangle(rq)
        print('H')
        uart.write("%d\n"% 2)

    elif tp:
        img.draw_rectangle(tp)
        print('S')
        uart.write("%d\n"% 1)
    elif tt:
        img.draw_rectangle(tt)
        print('S')
        uart.write("%d\n"% 1)
    elif tq:
        img.draw_rectangle(tq)
        print('S')
        uart.write("%d\n"% 1)

    elif zt:
        img.draw_rectangle(zt)
        print('U')
        uart.write("%d\n"% 0)
    elif zq:
        img.draw_rectangle(zq)
        print('U')
        uart.write("%d\n"% 0)

    else:
        for blob in img.find_blobs([thresholds], pixels_threshold= 100, area_threshold=100, merge=True):
           img.draw_rectangle(blob.rect())
           img.draw_cross(blob.cx(), blob.cy())
           c = blob.count()
           if(c > 0):
                  print("Alejate_Mas", c)
                  print(blob.pixels())
                  break


