#!/usr/bin/env python3



import tkinter
from tkinter import ttk
import PIL
from PIL import ImageTk
import mqtt_remote_method_calls as com



def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()


    photo = ImageTk.PhotoImage(file="./bg.gif")
    photo1 = ImageTk.PhotoImage(file="./bg1.gif")
    photo2 = ImageTk.PhotoImage(file="./bg2.gif")
    photo3 = ImageTk.PhotoImage(file="./bg3.gif")
    photo4 = ImageTk.PhotoImage(file="./bgs.gif")

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "300")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "300")
    right_speed_entry.grid(row=1, column=2)

    # Done: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.

    forward_button = ttk.Button(main_frame, text="Forward", image=photo)
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry.get(), right_speed_entry.get()))

    left_button = ttk.Button(main_frame, text="Left", image=photo1)
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_turning_left(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    root.bind('<Left>', lambda event: send_turning_left(mqtt_client, left_speed_entry.get(), right_speed_entry.get()))
    # left_button and '<Left>' key

    stop_button = ttk.Button(main_frame, text="Stop", image=photo4)
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event:send_stop(mqtt_client))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(main_frame, text="Right", image=photo2)
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_turning_right(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    root.bind('<Right>', lambda event: send_turning_right(mqtt_client, left_speed_entry.get(), right_speed_entry.get()))
    # right_button and '<Right>' key

    back_button = ttk.Button(main_frame, text="Back", image=photo3)
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_backward(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    root.bind('<Down>', lambda event: send_backward(mqtt_client, left_speed_entry.get(), right_speed_entry.get()))
    # back_button and '<Down>' key

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    x_button = ttk.Button(main_frame, text="Factory")
    x_button.grid(row=5,column=2)
    x_button['command'] = lambda: mqtt_client.send_message('run_file', [])

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=3)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    root.bind()


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
        mqtt_client.send_message("shut_down")
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
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
