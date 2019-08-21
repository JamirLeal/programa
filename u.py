
import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((120,120))
sensor.skip_frames(time = 2000)
clock = time.clock()

min_degree = 0
max_degree = 7

minDegree = 85
maxDegree = 95
led = pyb.LED(3)
low_threshold = (0, 100)

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.laplacian(2, mul = 0.0065 , sharpen=True)

    vL = 0
    ci = 0

    for l in img.find_lines(threshold = 2000, theta_margin = 20, rho_margin = 20, x_stride = 2):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (0, 0, 0), thickness = 4)
            print(l)
            vL += 1
        if(vL > 1):
            break

    if(vL > 1):
        for c in img.find_circles(threshold = 2000, x_margin = 20, y_margin = 20, r_margin = 20,
                    r_min = 30, r_max = 40, r_step = 10):
                 if(c.magnitude()>2800):
                    #img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 0))
                    #print(c)
                    ci += 1

    if(vL > 1 and ci > 0):
        led.on()
        print('U')
    else:
        print('FF?')
        led.off()
# Para H 2 lineas verticales - 1 linea horizontal
# Para S una linea a 100 grados dos circulos
# Para U 2 lineas verticales un circulo o más
