from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

# Program
right_motor = Motor(Port.D, positive_direction=Direction.CLOCKWISE)
left_motor = Motor(Port.C, positive_direction=Direction.CLOCKWISE)

# Define the drive base
motors = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=525)
gyro = GyroSensor(Port.S2)

# Set the volume
ev3.speaker.set_volume(10)

target_speed = 0
tilt_threshold = 1
Kp = 30

# Adjust Kp with ev3 buttons
def on_up_button():
    global Kp
    ev3.speaker.beep(100)
    Kp += 1
    ev3.screen.clear()
    ev3.screen.print(Kp)

def on_down_button():
    global Kp
    ev3.speaker.beep(250)
    Kp -= 1
    ev3.screen.clear()
    ev3.screen.print(Kp)

def on_enter_button():
    ev3.speaker.beep(500)
    gyro.reset_angle(0)


# Balancing loop
while True:
    if Button.UP in ev3.buttons.pressed():
        on_up_button()
    if Button.DOWN in ev3.buttons.pressed():
        on_down_button()
    if Button.CENTER in ev3.buttons.pressed():
        on_enter_button()

    # Get current angle
    current_tilt = gyro.angle()
    error = 0 - current_tilt
    # Adjust the angle of the robot
    if abs(error) > tilt_threshold:
        P = Kp * error * -1
        adjusted_speed = target_speed + P
        motors.drive(adjusted_speed, 0)
    else:
        motors.stop()

    print([current_tilt])
    
    # Update every 10 ms
    wait(10)
