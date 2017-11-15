"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time
import os




class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):

        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.arm_motor.connected

        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor

        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy

        self.pwr = ev3.PowerSupply()

        self.running = True


    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    def drive_inches(self, length, speed):
        self.right_motor.run_to_rel_pos(position_sp=length * 90, speed_sp=speed)
        self.left_motor.run_to_rel_pos(position_sp=length * 90, speed_sp=speed)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turning_degrees(self, degrees, speed):
        if degrees > 0:
            self.right_motor.run_to_rel_pos(position_sp=degrees * 4.615384615, speed_sp=speed)
            self.left_motor.run_to_rel_pos(position_sp=-degrees * 4.615384615, speed_sp=speed)
        if degrees < 0:
            self.right_motor.run_to_rel_pos(position_sp=-degrees * 4.615384615, speed_sp=speed)
            self.left_motor.run_to_rel_pos(position_sp=degrees * 4.615384615, speed_sp=speed)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def draw_polygon(self, length, sides, speed):
        degree = 180 -  ((sides - 2) * 180)/sides
        for k in range(abs(sides)):
            self.drive_inches(length, speed)
            if sides > 0:
                self.turning_degrees(-degree, speed)
            if sides < 0:
                self.turning_degrees(degree, speed)

    def arm_calibration(self):
        # arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        # assert arm_motor.connected
        #
        # touch_sensor = ev3.TouchSensor()
        # assert touch_sensor

        self.arm_motor.run_forever(speed_sp=900)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

    def shutdown(self):
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.speak('Goodbye')

    def loop_forever(self):
        self.running = True
        while self.running:
            #   "Self Defense" mode developed by Shengbo Zou
            if self.ir_sensor.proximity < 10:
                self.pinch()
                ev3.Sound.speak("Don't touch me. Now back off").wait()
                time.sleep(1.5)
                self.release()
            time.sleep(0.1)

    def shut_down(self):
        self.running = False

    def constant_moving(self, l_speed, r_speed):
        self.left_motor.run_forever(speed_sp=l_speed)
        self.right_motor.run_forever(speed_sp=r_speed)

    def stop(self):
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def seek_beacon(self):
        seeker = ev3.BeaconSeeker(sensor=self.ir_sensor, channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = seeker.heading
            current_distance = seeker.distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance <= 1:
                        time.sleep(1)
                        self.stop()
                        return True
                    if current_distance > 0:
                        self.constant_moving(forward_speed, forward_speed)
                elif current_heading < 0:
                    self.constant_moving(-turn_speed, turn_speed)
                elif current_heading > 0:
                    self.constant_moving(turn_speed, -turn_speed)
                else:
                    print("Heading too far off")
            time.sleep(0.2)
        print("Abandon ship!")
        self.stop()
        return False

    def pinch(self):
        self.arm_motor.run_forever(speed_sp=900)
        time.sleep(1.5)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def release(self):
        self.arm_motor.run_forever(speed_sp=-900)
        time.sleep(1.5)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def free_moving(self, l_speed, r_speed):
        self.left_motor.run_forever(speed_sp=l_speed)
        self.right_motor.run_forever(speed_sp=r_speed)

    def run_file(self):
        os.system("python follow_move.py");

    def getPower(self):
        self.mqtt.send_message("rcv_pwr_data",[ self.pwr.measured_current, self.pwr.measured_voltage])

