
import sensor, image, time, pyb

sensor.reset()
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_windowing((120,120))
sensor.skip_frames(time = 2000)

clock = time.clock()
led2 = pyb.LED(2)

min_degreeS = 95
max_degreeS = 112

def buscarDiagonales():
    dL = 0
    for l in img.find_line_segments(merge_distance = 40, max_theta_diff =10):
        if (min_degreeS <= l.theta() <= max_degreeS and 30 <= l.length() <= 80):
            #img.draw_line(l.line(), color = (0, 0, 0), thickness = 4)
            #print(l)
            dL += 1
        if(dL > 0):
            return True
    else:
        return False

def buscarCirculos():
    ci = 0
    for c in img.find_circles(threshold = 3000, x_margin = 30, y_margin = 30, r_margin = 30,
            r_min = 20, r_max = 40, r_step = 2):
        #img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 0), thickness = 4)
        #print(c)
        ci += 1
        if(ci > 0):
            return True
    else:
        return False

while(True):
        clock.tick()
        img = sensor.snapshot()
        img.laplacian(2, mul = 0.0065 , sharpen=True)

        if(buscarDiagonales() == True):
            if(buscarCirculos() == True):
                #print('S')
                led2.on()
        else:
            #print('F')
            led2.off()
