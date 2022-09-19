import os.path
import picamera
import RPi.GPIO as GPIO

launchDetect = False
videoRecorded = False

#Pin definitions
triggerPin = 17

#Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.IN)

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 30
stream = picamera.PiCameraCircularIO(camera, seconds=100)
camera.start_recording(stream, format='h264')

def launch_detected():
    if GPIO.input(triggerPin):
        launchDetect = True
        return launchDetect

for i in range(99):
    if not os.path.exists('video' + str(i) + '.h264'):
        try:
            while not videoRecorded:
                camera.wait_recording(3)
                if launch_detected():
                    camera.wait_recording(90)
                    stream.copy_to('video'+ str(i) + '.h264')
                    camera.stop_recording()
                    videoRecorded = True
        finally:
            if os.path.exists('video' + str(i) + '.h264'):
                os.system("sudo shutdown now")
