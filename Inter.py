
import sensor, image, time, math, cpufreq, pyb
from pyb import LED

cpufreq.set_frequency(216)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((120,120))
sensor.skip_frames(time = 2000)
sensor.set_contrast(3)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

LED(1).on()
pyb.delay(300)
LED(2).on()
pyb.delay(300)
LED(3).on()

min_degreeV = 0
max_degreeV = 5

minDegreeH = 88
maxDegreeH = 94

min_degreeS = 95
max_degreeS = 112

###########################################################################

def buscarNegros():

    c = 0

    for blob in img.find_blobs([(0,100)], pixels_threshold = 300, area_threshold=2700, merge=True):

        #print(blob.area())

        if blob.area() < 13000 and 30 <= blob.cy() <= 77 and  40 <= blob.cx() <= 80:

            c = blob.count()

            img.draw_rectangle(blob.rect(), color = [0, 0, 0], thickness = 4)

            #print("Centro en x: ", blob.cx(), "Centro en y: ", blob.cy())

            img.draw_cross(blob.cx(), blob.cy(),  color = [0, 0, 0], thickness = 2, size = 5)

            bulto = blob.rect()

            #print(bulto)

            if c > 0:

                return True, bulto
    else:

        bulto = (0,0,120,120)

        return False, bulto

##########################################################################

def buscarLineasVerticales(bulto):

    vL = 0

    for l in img.find_lines(roi = bulto, threshold = 2000, theta_margin = 20, rho_margin = 20, x_stride = 1):

        if min_degreeV <= l.theta() <= max_degreeV:

            img.draw_line(l.line(), color = (0, 0, 0), thickness = 4)

            #print(l)

            vL += 1

        if(vL > 1):

            return True
    else:

        return False

###############################################################################

def buscarLineasHorizontales(bulto):

    bulto = (bulto[0], bulto[1] + math.floor(bulto[3] / 5), bulto[2], bulto[1] + math.ceil(bulto[3] / 2))

    hL = 0

    for t in img.find_line_segments(roi = bulto , merge_distance = 30, max_theta_diff = 15):

        if minDegreeH <= t.theta() <= maxDegreeH and math.floor(bulto[2] / 2)  <= t.length() <= bulto[2]:

                img.draw_line(t.line(), color = (0, 0, 0), thickness = 5)

                #print(t)

                hL += 1

                if (hL > 0):

                    return True
    else:

        return False

##################################################################################

def buscarDiagonales(bulto):

    dL = 0

    for l in img.find_line_segments(roi = bulto ,merge_distance = 40, max_theta_diff = 12):

        if min_degreeS <= l.theta() <= max_degreeS and 30 <= l.length() <= 80: #cambiar por blob

            img.draw_line(l.line(), color = (0, 0, 0), thickness = 4)

            #print(l)

            dL += 1

        if dL > 0:

            return True

    else:

        return False

####################################################################################

def buscarCirculos(bulto):

    ci = 0

    for c in img.find_circles(roi = bulto, threshold = 3000, x_margin = 30, y_margin = 30, r_margin = 30,
            r_min = math.floor(bulto[2] * 0.3), r_max = bulto[2], r_step = 2):

        img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 0), thickness = 4)

        #print(c)

        ci += 1

        if ci > 0:

            return True

    else:

        return False

#contadorDeImagenesEncontradas =

########################### LOOP ####################################################

while(True):

    '''LED(1).on()
    LED(2).on()
    LED(3).on()'''

    funcionBuscarNegros = False

    clock.tick()

    img = sensor.snapshot()

    img.laplacian(2, mul = 0.0065 , sharpen=True)
    #img.dilate(1)

    funcionBuscarNegros = buscarNegros()

    if funcionBuscarNegros[0] == True:
        # Tomas otros 4 snapshots

        # Analizas los 5 juntos
        #LED(1).on()
        #LED(2).on()
        #LED(3).on()

        bulto = funcionBuscarNegros[1]

        LineasVerticales = buscarLineasVerticales(bulto)

        if LineasVerticales == True:

            LineasHorizontales = buscarLineasHorizontales(bulto)

            if LineasHorizontales == True:

                LED(1).on()
                LED(2).off()
                LED(3).off()
                print('H')
                #pyb.delay(5000)

            else:

                LED(1).off()
                LED(2).off()
                LED(3).on()
                print('U')
                #pyb.delay(5000)

        else:

            funcionBuscarDiagonales = buscarDiagonales(bulto)

            if funcionBuscarDiagonales == True:

                funcionBuscarCirculos = buscarCirculos(bulto)

                if funcionBuscarCirculos == True:

                    LED(1).off()
                    LED(2).on()
                    LED(3).off()
                    print('S')
                    #pyb.delay(5000)

    '''elif funcionBuscarNegros[0] == False:

        LineasVerticales = buscarLineasVerticales((0,0,120,120))

        if LineasVerticales == True:

            LED(1).off()
            LED(2).off()
            LED(3).on()
            print('U')
            #pyb.delay(2000)

        else:

            LED(1).off()
            LED(2).off()
            LED(3).off()'''

    #print(clock.fps())
    #print('F')
    #print()

    #if funcionBuscarNegros[0] == True:

        #LED(1).off()
        #LED(2).off()
        #LED(3).on()

# Mejorar la deteccion de bultos en la U

# Funcion buscar diagonales en roi para la s más pequeña

#sacar una media de los pixeles 0-255 y ponerlo actualizar umbrales con base a eso
