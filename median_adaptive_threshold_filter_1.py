# Median Adaptive Threshold Filter Example
#
# This example shows off median filtering with adaptive thresholding.
# When median(threshold=True) the median() method adaptive thresholds the image
# by comparing the median of the pixels around a pixel, minus an offset, with that pixel.

import sensor, image, time

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    img.median(1, percentile=1, threshold=True, offset = 18, invert=True)

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
