import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Follow a line")
    print("--------------------------------------------")
    ev3.Sound.speak("Follow a line").wait()

    # TODO: 4: After running the code set the default white and black levels to a better initial guess.
    #   Once you have the values hardcoded to resonable numbers here you don't really need the w and b commands below.

    white_level = 100
    black_level = 0
    robot = robo.Snatch3r()

    robot.arm_calibration()


    print("Follow the line until the touch sensor is pressed.")
    follow_the_line(robot, white_level, black_level)


    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

    ev3.Sound.speak("Beep at hands")
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()



    # Note, it is assumed that you have a touch_sensor property on the Snatch3r class.
    # Presumably you added this in the digital_inputs unit, if not add it now so that
    # the code below works to monitor the touch_sensor.

    while not robot.touch_sensor.is_pressed:
        # Done: 2. Implement the module as described in the opening comment block.
        # It is recommended that you add to your Snatch3r class's constructor the ir_sensor, as shown
        #   self.ir_sensor = ev3.InfraredSensor()
        #   assert self.ir_sensor
        # Then here you can use a command like robot.ir_sensor.proximity
        if robot.ir_sensor.proximity < 10:
            ev3.Sound.beep()
            time.sleep(1.5)
        time.sleep(0.1)


def follow_the_line(robot, white_level, black_level):
    """
    The robot follows the black line until the touch sensor is pressed.
    You will need a black line track to test your code
    When the touch sensor is pressed, line following ends, the robot stops, and control is returned to main.

    Type hints:
      :type robot: robo.Snatch3r
      :type white_level: int
      :type black_level: int
    """
    the_time_robot_pick_up_the_object = 0
    while True:

        if robot.color_sensor.reflected_light_intensity > black_level + 0.2 * white_level:
            init_col = robot.color_sensor.reflected_light_intensity
            robot.constant_moving(300, -300)
            time.sleep(0.2)
            robot.stop()
            if robot.color_sensor.reflected_light_intensity < init_col:
                robot.constant_moving(300, -300)
                time.sleep(0.2)
                robot.stop()
            else:
                robot.constant_moving(-300, 300)
                time.sleep(0.4)
                robot.stop()
        else:
            robot.constant_moving(300, 300)

        if robot.ir_sensor.proximity < 5 and the_time_robot_pick_up_the_object == 0:
            ev3.Sound.beep()
            time.sleep(1)
            robot.stop()
            robot.arm_up()
            the_time_robot_pick_up_the_object = time.time()


        if time.time() - the_time_robot_pick_up_the_object > 30 and the_time_robot_pick_up_the_object != 0:
            robot.stop()
            robot.arm_down()

            while(1):
                print("GoodBye")
                time.sleep(1)



    # TODO: 5. Use the calibrated values for white and black to calculate a light threshold to determine if your robot
    # should drive straight or turn to the right.  You will need to test and refine your code until it works well.
    # Optional extra - For a harder challenge could you drive on the black line and handle left or right turns?


# TODO: 6. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.
#
# Observations you should make, following a black line would be easier with 2 sensors (one on each side of the line),
# but it can be done with only a single sensor.  There are also optimizations that could be made to follow the line
# faster and more smoothly.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
