import basehat
import time
from buildhat import Motor
from basehat import IMUSensor


ultrasonicPin = 22
lineFinderLeft = 26
lineFinderRight = 18

ultra = basehat.UltrasonicSensor(ultrasonicPin)
lineLeft = basehat.LineFinder(lineFinderLeft)
lineRight = basehat.LineFinder(lineFinderRight)

button = basehat.Button(24)

motorLeft = Motor('C')
motorRight = Motor('D')
motorGate = Motor('A')

IMU = IMUSensor()

adder = 0

leftKp = 0.02
leftKi = 0
leftKd = 0
leftWindup = 0

rightKp = .02
rightKi = 0
rightKd = 0
rightWindup = 0

speed = 90

start = False

timeNow = time.time()

def dropOff():
    initial_position = motorGate.get_position()
    while initial_position - motorGate.get_position() < 420:
        motorGate.run_for_degrees(-425, speed=40)

def getUp():
    motorGate.run_for_degrees(400, speed=100)

magValue = 285.0
magSecs = 3

try:
    while True:
        if button.value == 1:
            time.sleep(1)            
            break

    while True:
        # motorLeft.pwm(1)

        # motorLeft.run_PID(Kp = leftKp, Ki = leftKi, Kd = leftKd, windup = leftWindup, speed = speed)
        # motorRight.run_PID(Kp = rightKp, Ki = rightKi, Kd = rightKd, windup = rightWindup, speed = -speed)

        x, y, z = IMU.getMag()
        dist = ultra.getDist

        if dist != None:
            if dist < 5:
                motorLeft.stop()
                motorRight.stop()
        elif dist == None or dist > 5:
        
            if z >= magValue:
                magTime = time.time()
                while time.time() - magTime < magSecs:
                    motorLeft.pwm(.8)
                    motorRight.pwm(-.8)
                motorLeft.stop()
                motorRight.stop()
                dropOff()
                time.sleep(.5)
                # break
            elif (lineLeft.value == 0 and lineRight.value == 0) or (lineLeft.value == 1 and lineRight.value == 1):
                print("straight")
                if (time.time() - timeNow > .8):
                    motorLeft.pwm(1)
                    motorRight.pwm(-1)
                else:
                    motorLeft.pwm(.6)
                    motorRight.pwm(-.6)

            elif lineLeft.value == 1:
                    print("turnleft")
                # while lineRight.value == 0:
                    timeNow = time.time()
                    motorLeft.pwm(-1)
                    motorRight.pwm(-1)

            elif lineRight.value == 1:
                # while lineLeft.value == 0:
                    print("turnright")
                    timeNow = time.time()
                    motorLeft.pwm(1)
                    motorRight.pwm(1)
        if button.value == 1:
            # motorLeft.stop()
            # motorRight.stop()
            # print("stopping")
            # break
            getUp()

except Exception as e:
    motorLeft.stop()
    motorRight.stop()
    print(e)



