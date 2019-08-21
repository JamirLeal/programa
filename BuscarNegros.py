
import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320,240))
sensor.set_contrast(3)
sensor.set_auto_exposure(False)
sensor.skip_frames(time = 2000)

clock = time.clock()

led = pyb.LED(1)

#Area debe ser mayor a 3000, y menor a 13000

def actualizarThresholds():

    if 160 <= img.get_statistics().mean():
        valorDeseado = img.get_statistics().lq() - math.floor(img.get_statistics().stdev() / 2)
    else :
        valorDeseado = img.get_statistics().lq() + 15

    return valorDeseado

def buscarNegros(valorDeseado):
    c = 0
    for blob in img.find_blobs([(0,valorDeseado)], pixels_threshold = 30, area_threshold=2700, merge=True):
        #print(blob.area())
        if(blob.area() < 13000 and 20 <= blob.cy() <= 77 and 30 <= blob.cx() <= 80):
            c = blob.count()
            #img.draw_rectangle(blob.rect(), color = [0, 0, 0], thickness = 4)
            #img.draw_cross(blob.cx(), blob.cy(),  color = [0, 0, 0], thickness = 4)
            #print(blob.cx(), " " ,blob.cy())
            bulto = blob.rect()
            if(c > 0):
                return True, bulto
    else:
        bulto = (0,0,0,0)
        return False, bulto

while(True):

    clock.tick()

    img = sensor.snapshot()

    #img.dilate(1)

    #img.laplacian(2, mul = 0.0065 , sharpen=True)

    valorDeseado = actualizarThresholds()

    funcionBuscarNegros = buscarNegros(valorDeseado)

    if(funcionBuscarNegros[0] == True):

        bultoR = funcionBuscarNegros[1]

        img.draw_rectangle(bultoR[0], bultoR[1], bultoR[2], bultoR[3], color= [0,0,0], thickness = 4)
        print(bultoR)

        print(img.get_statistics())

        #print("")

        led.on()

    else:

        led.off()

''' Y muy arriba lejos = 71 cerca = 76
 Y en el centro lejos = 46 cerca = 52
 Y muy abajo lejos = 34 cerca = 34
 img.draw_rectangle(blob.rect(), color = [0, 0, 0], thickness = 4)
 img.draw_cross(blob.cx(), blob.cy(),  color = [0, 0, 0], thickness = 4)
 print(blob.area()) '''

#print("Centro x: ", blob.cx(), " Centro y: ", blob.cy())

