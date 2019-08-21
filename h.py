import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((120,120))
sensor.skip_frames(time = 2000)
clock = time.clock()
led = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)

min_degreeH = 0
max_degreeH = 5

minDegreeV = 88
maxDegreeV = 94

low_threshold = (0, 100)

def buscarLineasVerticales():

    vL = 0

    for l in img.find_lines(threshold = 2000, theta_margin = 20, rho_margin = 20, x_stride = 1):
        if (min_degreeH <= l.theta() <= max_degreeH):
            #img.draw_line(l.line(), color = (0, 0, 0), thickness = 4)
            #print(l)
            vL += 1

        if(vL > 1):
            return True
    else:
        return False

def buscarLineasHorizontales():
    hL = 0

    for t in img.find_line_segments(merge_distance = 30, max_theta_diff = 10):
        if (minDegreeV <= t.theta() <= maxDegreeV) and (34 <= t.length() <= 84):
                #img.draw_line(t.line(), color = (0, 0, 0), thickness = 5)
                #print(t)
            hL += 1

            if (hL > 0):
                return True
    else:
        return False

while(True):

    clock.tick()

    img = sensor.snapshot()
    img.laplacian(2, mul = 0.0065 , sharpen=True)

    if(buscarLineasVerticales() == True):

        if(buscarLineasHorizontales() == True):
            #print('H')
            led2.on()

    else:
       # print("Lineas verticales: ", vL, " Lineas horizontales: ", hL)
        led2.off()

# 2.1 / 4 para sacar la longitud aprox de la linea horizontal


