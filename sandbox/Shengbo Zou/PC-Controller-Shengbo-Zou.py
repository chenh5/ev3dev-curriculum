#!/usr/bin/env python3
"""  Author: Shengbo Zou
"""  # Done: 1. PUT YOUR NAME IN THE ABOVE LINE.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
key_status = {'Up': False, 'Down': False, 'Left': False, 'Right': False, 'w': False, 's': False}


def pressed(event):
    key_status[event.keysym] = True


def released(event):
    key_status[event.keysym] = False


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    speed_scale = ttk.Scale(main_frame)
    speed_scale.grid(row=2, column=1)
    speed_scale.set(0.5)
    speed = speed_scale.get() * 900

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=3, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=4, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=3, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<Escape>', lambda event: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=4, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    for char in ["Up", "Down", "Left", "Right", "w", "s"]:
        root.bind("<KeyPress-%s>" % char, pressed)
        root.bind("<KeyRelease-%s>" % char, released)

    left_speed = int(speed)
    right_speed = int(speed)
    free_move(root, mqtt_client, left_speed, right_speed, speed_scale)
    root.mainloop()


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shut_down")
    mqtt_client.close()
    exit()


def send_stop(mqtt_client):
    print('stopped')
    mqtt_client.send_message('stop')


def free_move(window, mqtt_client, left_speed, right_speed, speed_scale):

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
    elif key_status["w"] is True:
        speed_scale.set(speed_scale.get() + 0.01)
        left_speed = int(speed_scale.get()) * 900
        right_speed = int(speed_scale.get()) * 900
    elif key_status["s"] is True:
        speed_scale.set(speed_scale.get() - 0.01)
        left_speed = int(speed_scale.get()) * 900
        right_speed = int(speed_scale.get()) * 900
    else:
        mqtt_client.send_message('stop')
    window.after(10, lambda: free_move(window, mqtt_client, left_speed, right_speed, speed_scale))

main()
