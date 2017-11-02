#!/usr/bin/env python3
"""
This module is the mini-project for the MQTT unit.  This module will be running on your PC and communicating with the
m5_ev3_remote_drive.py module that is running on your EV3 (you have to write that module too, but it's easier).
Only the Tkinter GUI has been made for you.  You will need to implement all of the MQTT communication.  The goal is to
have a program running on your computer that can control the EV3.

You will need to have the following features:
  -- Clickable drive direction buttons to drive forward (up), backwards (down), left, right, and stop (space)
    -- Keyboard shortcut keys that behave the same as clicking the buttons (this has already been wired up for you)
  -- An entry box for the left and right drive motor speeds.
    -- If both become set to 900 all of the drive direction buttons will go fast, for example forward goes 900 900
    -- If both become set to 300 all of the drive direction buttons will go slower, for example reverse goes -300 -300
    -- If 500 then left does -500 500, which causes the robot to spin left (use half speed -250 250 if too fast)
    -- If set differently to say 600 left, 300 right the robot will drive and arc, for example forward goes 600 300
  -- In addition to the drive features there needs to be a clickable button for Arm Up and Arm Down
    -- There also need to be keyboard shortcut for Arm Up (u) and Arm Down (j).  Arm calibration is not required.

  -- Finally you need 2 buttons for ending your program:
    -- Quit, which stops only this program and allows the EV3 program to keep running
    -- Exit, which sends a shutdown message to the EV3, then ends it's own program as well.

You can start by running the code to see the GUI, but don't expect button clicks to do anything useful yet.

Authors: David Fisher and Shengbo Zou
"""  # Done: 1. PUT YOUR NAME IN THE ABOVE LINE.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
key_status = {'Up': False, 'Down': False, 'Left': False, 'Right': False}


def pressed(event):
    key_status[event.keysym] = True


def released(event):
    key_status[event.keysym] = False


def main():
    # Done: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry.get(), right_speed_entry.get())

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_turning_left(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    # left_button and '<Left>' key

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event:send_stop(mqtt_client))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_turning_right(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    # right_button and '<Right>' key

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_backward(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    # back_button and '<Down>' key

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<Escape>', lambda event: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    for char in ["Up", "Down", "Left", "Right"]:
        root.bind("<KeyPress-%s>" % char, pressed)
        root.bind("<KeyRelease-%s>" % char, released)

    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())
    free_move(root, mqtt_client, left_speed, right_speed)
    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# Done: 4. Implement the functions for the drive button callbacks.

# TODO: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def send_forward(mqtt_client, left_speed, right_speed):
    print("going forward:", left_speed, right_speed)
    mqtt_client.send_message('constant_moving', [int(left_speed), int(right_speed)])


def send_backward(mqtt_client, left_speed, right_speed):
    print('going backward:', left_speed, right_speed)
    mqtt_client.send_message('constant_moving', [-int(left_speed), -int(right_speed)])


def send_turning_left(mqtt_client, left_speed, right_speed):
    print('turning left:', left_speed, right_speed)
    mqtt_client.send_message('constant_moving', [-int(left_speed), int(right_speed)])


def send_turning_right(mqtt_client, left_speed, right_speed):
    print('turning right:', left_speed, right_speed)
    mqtt_client.send_message('constant_moving', [int(left_speed), -int(right_speed)])


def send_stop(mqtt_client):
    print('stopped')
    mqtt_client.send_message('stop')


def free_move(window, mqtt_client, left_speed, right_speed):

    if key_status["Up"] is True and key_status["Left"] is True:
        mqtt_client.send_message('free_moving', [0.5 * left_speed, right_speed])
        print("Awesome Move Up-Left")
    elif key_status["Up"] is True and key_status["Right"] is True:
        print("Awesome Move Up-Right")
        mqtt_client.send_message('free_moving', [left_speed, 0.5 * right_speed])
    elif key_status["Down"] is True and key_status["Left"] is True:
        print("Awesome Move Down-Left")
        mqtt_client.send_message('free_moving', [-0.5 * left_speed, -right_speed])
    elif key_status["Down"] is True and key_status["Right"] is True:
        print("Awesome Move Down-Right")
        mqtt_client.send_message('free_moving', [-left_speed, -0.5 * right_speed])
    elif key_status["Up"] is True:
        print("Going Forward")
        mqtt_client.send_message('free_moving', [left_speed, right_speed])
    elif key_status["Down"] is True:
        mqtt_client.send_message('free_moving', [-left_speed, -right_speed])
        print("Going Backward")
    elif key_status["Left"] is True:
        mqtt_client.send_message('free_moving', [-left_speed, right_speed])
        print("Turning Left")
    elif key_status["Right"] is True:
        print("Turning Right")
        mqtt_client.send_message('free_moving', [left_speed, -right_speed])
    else:
        mqtt_client.send_message('stop')
    window.after(50, free_move(window, mqtt_client, left_speed, right_speed))
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
