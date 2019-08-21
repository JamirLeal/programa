import sensor, image, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.set_windowing((100, 60))
sensor.skip_frames(time = 2000) # Let new settings take affect.

led = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)

sensor.skip_frames(time = 6000) # Give the user time to get ready.

print("You're on camera!")
sensor.snapshot().save("exampleNUEVOH2EF.jpg") # or "example.bmp" (or others)

pyb.LED(BLUE_LED_PIN).off()
print("Done! Reset the camera to see the saved image.")
