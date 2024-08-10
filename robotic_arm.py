from customtkinter import *
from PIL import Image
import time
from serial_connection import *

set_widget_scaling(1.3)

class App(CTk):
    def __init__(self):
        super().__init__()
        # MAIN WINDOW SETTINGS
        self.configure(fg_color="#777777")
        self.title("Robotic arm app")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # DEFINING ARDUINO'S VARIABLES
        self.serial_connection = SerialConnection()
        self.ports = self.serial_connection.check_available_ports()["ports"]
        self.arduino = None
        self.key = None
        
        self.window = None
        
        self.drawer_frame = CTkScrollableFrame(self, fg_color="#111111", width=260, corner_radius=0)
        self.drawer_frame.grid(sticky="NS")
        
        # ARDUINO CONTROLS
        arduino_settings_frame = CTkFrame(self.drawer_frame, fg_color="#333333")
        arduino_settings_frame.grid(padx=20, pady=(20, 0), sticky="EW")
        
        self.connected_arduino_label = CTkLabel(arduino_settings_frame, 
                                                text="ARDUINO COTROLS", 
                                                font=("helvetica", 14, "bold"), 
                                                text_color="#FFFFFF",
                                                compound="right",
                                                image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
        self.connected_arduino_label.grid(row=0, column=0, padx=(10, 0), pady=10, columnspan=2, sticky="W")
        
        # ARDUINO BOARD COMBOBOX
        CTkLabel(arduino_settings_frame, 
                 text="ARDUINO BOARD", 
                 text_color="#FFFFFF").grid(row=1, column=0, padx=10, pady=(0, 20), sticky="W")
        self.arduino_board_combobox = CTkComboBox(arduino_settings_frame, 
                                                  values=[""],
                                                  width=100,
                                                  state="readonly",
                                                  command=self.connect_arduino)
        self.arduino_board_combobox.grid(row=1, column=1, padx=(0, 10), pady=(0, 20))
        self.arduino_board_combobox.set(self.arduino_board_combobox._values[0])
        
        # ARDUINO CONTROLS
        servos_settings_frame = CTkFrame(self.drawer_frame, fg_color="#333333")
        servos_settings_frame.grid(padx=20, pady=(20, 0), sticky="EW")
        
        self.servo_settings_label = CTkLabel(servos_settings_frame, 
                                             text="SERVOS SETTINGS", 
                                             font=("helvetica", 14, "bold"), 
                                             text_color="#FFFFFF",
                                             compound="right",
                                             image=CTkImage(light_image=Image.open("./icons/settings.png")))
        self.servo_settings_label.grid(row=0, column=0, padx=(10, 0), pady=10, columnspan=2, sticky="W")
        
        # SERVOS' SETTINGS
        CTkLabel(servos_settings_frame,
                 text="ANGLE STEP",
                 text_color="#FFFFFF").grid(row=1, column=0, padx=10, pady=(0, 20), sticky="W")
        
        # SERVOS' SETTINGS COMBOBOX
        self.angle_step_combobox = CTkComboBox(servos_settings_frame, 
                                               values=["1°", "2°", "3°"],
                                               width=100,
                                               state="readonly",
                                               command=None)
        self.angle_step_combobox.grid(row=1, column=1, padx=(0, 10), pady=(0, 20))
        self.angle_step_combobox.set(self.angle_step_combobox._values[0])
        
        # DASHBOARD FRAME
        self.dashboard_frame = CTkFrame(self, fg_color="#DDDDDD", corner_radius=0)
        self.dashboard_frame.rowconfigure(0, weight=1)
        self.dashboard_frame.columnconfigure((0, 1), weight=1)
        self.dashboard_frame.grid(row=0, column=1, sticky="NSEW")
        
        # CREATING DASHBOARD LEFT BUTTONS FRAME
        self.gripper_frame = CTkFrame(self.dashboard_frame,
                                      fg_color="#AAAAAA",
                                      corner_radius=200,
                                      border_width=5,
                                      border_color="#111111",
                                      width=150,
                                      height=150)
        self.gripper_frame.grid(row=0, column=0, padx=(40, 10), pady=40, sticky="E")
        
        CTkLabel(self.gripper_frame,
                 text="",
                 font=("helvetica", 25, "bold", "italic"),
                 compound="right",
                 image=CTkImage(light_image=Image.open("./icons/end_effector.png"), size=(50, 50)),
                 text_color="#111111").grid(rowspan=4, columnspan=4)
        
        # CREATING BUTTONS THAT MOVES THE ROBOTIC ARM UP AND DOWN OR OPEN AND CLOSE THE THE GRIPPER
        self.up_button = CTkButton(self.gripper_frame,
                                   text="W",
                                   font=("helvetica", 20, "bold"),
                                   fg_color="#555555",
                                   hover_color="#111111",
                                   width=50,
                                   height=50,
                                   command=lambda: self.send_to_serial("W"))
        self.up_button.grid(row=1, column=1, pady=(42, 35))
        
        self.open_button = CTkButton(self.gripper_frame,
                                     text="A",
                                     font=("helvetica", 20, "bold"),
                                     fg_color="#555555",
                                     hover_color="#111111",
                                     width=50,
                                     height=50,
                                     command=lambda: self.send_to_serial("A"))
        self.open_button.grid(row=1, column=0, padx=(38, 10), rowspan=2)
        
        self.close_button = CTkButton(self.gripper_frame,
                                      text="D",
                                      font=("helvetica", 20, "bold"),
                                      fg_color="#555555",
                                      hover_color="#111111",
                                      width=50,
                                      height=50,
                                      command=lambda: self.send_to_serial("D"))
        self.close_button.grid(row=1, column=2, padx=(10, 38), rowspan=2)
        
        self.down_button = CTkButton(self.gripper_frame,
                                     text="S",
                                     font=("helvetica", 20, "bold"),
                                     fg_color="#555555",
                                     hover_color="#111111",
                                     width=50,
                                     height=50,
                                     command=lambda: self.send_to_serial("S"))
        self.down_button.grid(row=2, column=1, pady=(35, 42))

        # CREATING DASHBOARD RIGHT BUTTONS FRAME
        self.rotation_frame = CTkFrame(self.dashboard_frame,
                                       fg_color="#AAAAAA",
                                       corner_radius=200,
                                       border_width=5,
                                       border_color="#111111",
                                       width=150,
                                       height=150)
        self.rotation_frame.grid(row=0, column=1, padx=(0, 40), sticky="W")
        
        CTkLabel(self.rotation_frame,
                 text="",
                 font=("helvetica", 25, "bold", "italic"),
                 compound="right",
                 image=CTkImage(light_image=Image.open("./icons/rotate.png"), size=(50, 50)),
                 text_color="#111111").grid(rowspan=4, columnspan=4)
        
        # CREATING BUTTONS THAT MOVE THE ROBOTIC ARM LEFT AND RIGHT OR FOWARD AND BACKWARD        
        self.forward_button = CTkButton(self.rotation_frame,
                                   text="",
                                   font=("helvetica", 20, "bold"),
                                   fg_color="#555555",
                                   hover_color="#111111",
                                   width=50,
                                   height=50,
                                   image=CTkImage(light_image=Image.open("./icons/forward.png"), size=(38, 38)),
                                   command=lambda: self.send_to_serial("UP"))
        self.forward_button.grid(row=1, column=1, pady=(42, 35))
        
        self.left_button = CTkButton(self.rotation_frame,
                                     text="",
                                     font=("helvetica", 20, "bold"),
                                     fg_color="#555555",
                                     hover_color="#111111",
                                     width=50,
                                     height=50,
                                     image=CTkImage(light_image=Image.open("./icons/left.png"), size=(38, 38)),
                                     command=lambda: self.send_to_serial("LEFT"))
        self.left_button.grid(row=1, column=0, padx=(38, 10), rowspan=2)
        
        self.right_button = CTkButton(self.rotation_frame,
                                      text="",
                                      font=("helvetica", 20, "bold"),
                                      fg_color="#555555",
                                      hover_color="#111111",
                                      width=50,
                                      height=50,
                                      image=CTkImage(light_image=Image.open("./icons/right.png"), size=(38, 38)),
                                      command=lambda: self.send_to_serial("RIGHT"))
        self.right_button.grid(row=1, column=2, padx=(10, 38), rowspan=2)
        
        self.backward_button = CTkButton(self.rotation_frame,
                                     text="",
                                     font=("helvetica", 20, "bold"),
                                     fg_color="#555555",
                                     hover_color="#111111",
                                     width=50,
                                     height=50,
                                     image=CTkImage(light_image=Image.open("./icons/backward.png"), size=(38, 38)),
                                     command=lambda: self.send_to_serial("DOWN"))
        self.backward_button.grid(row=2, column=1, pady=(35, 42))
        
        # BINDING KEYBOARD EVENTS
        self.bind("<Key>", self.key_events)
        self.bind("<KeyRelease>", self.key_events)
        
        # BINDING BUTTONS EVENTS 
        self.up_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("W"))
        self.open_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("A"))
        self.close_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("D"))
        self.down_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("S"))
        self.forward_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("UP"))
        self.left_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("LEFT"))
        self.right_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("RIGHT"))
        self.backward_button.bind("<ButtonPress-1>", lambda event: self.mouse_call("DOWN"))
        self.up_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.open_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.close_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.down_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.forward_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.left_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.right_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.backward_button.bind("<ButtonRelease-1>", lambda event: self.mouse_call(None))
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.mouse_events()
        
        self.checking_divices()
        
        self.mainloop()
    
    # WHEN THE USER CLICK THE MOUSE LEFT BUTTON
    def mouse_call(self, key):
        
        self.key = key
        
    # CALLS THE EVENT WEHN A GUI BUTTON IS PRESSED
    def mouse_events(self):
        
        if self.key != None:
            self.send_to_serial(self.key)
            
        self.update()
        self.after(10, self.mouse_events)
        
    
    # CALLS A EVENT WHEN A KEY IS PRESSED
    def key_events(self, event):
        
        self.key = event.keysym.upper()
        
        # BUTTON PRESS
        if event.type == "2":
            
            if self.key == "W":
                self.up_button.configure(fg_color="#111111")
            if self.key == "A":
                self.open_button.configure(fg_color="#111111")
            if self.key == "D":
                self.close_button.configure(fg_color="#111111")
            if self.key == "S":
                self.down_button.configure(fg_color="#111111")
            if self.key == "UP":
                self.forward_button.configure(fg_color="#111111")
            if self.key == "LEFT":
                self.left_button.configure(fg_color="#111111")
            if self.key == "RIGHT":
                self.right_button.configure(fg_color="#111111")
            if self.key == "DOWN":
                self.backward_button.configure(fg_color="#111111")
            
        # BUTTON RELEASE
        if event.type == "3":
            if self.key == "W":
                self.up_button.configure(fg_color="#555555")
            if self.key == "A":
                self.open_button.configure(fg_color="#555555")
            if self.key == "D":
                self.close_button.configure(fg_color="#555555")
            if self.key == "S":
                self.down_button.configure(fg_color="#555555")
            if self.key == "UP":
                self.forward_button.configure(fg_color="#555555")
            if self.key == "LEFT":
                self.left_button.configure(fg_color="#555555")
            if self.key == "RIGHT":
                self.right_button.configure(fg_color="#555555")
            if self.key == "DOWN":
                self.backward_button.configure(fg_color="#555555")
                
            self.key = None
        
    # SEND THE DATA TO ARDUINO
    def send_to_serial(self, key):
        
        if self.arduino != None:
            if self.arduino.is_open:
                self.arduino.write(f"{key}:{self.angle_step_combobox.get().replace("°", "")}:".encode())
                
                    
    # TO STABILISH SERIAL CONNECTION
    def connect_arduino(self, event) -> None:
        if self.arduino != None:
            if self.arduino.is_open:
                self.serial_connection.end(self.arduino)
        
        self.arduino = self.serial_connection.start(self.arduino_board_combobox.get())
        
        time.sleep(1)
        
        if self.arduino != None:
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb.png")))
        else:
            self.arduino_board_combobox.set(value=[])
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
            self.alert_window("ARDUINO CONNECTION FAILED")

        
    # TO CHECK IF THERE ARE ARDUINOS CONNECTED TO THE USB PORTS ON USER'S COMPUTER
    def checking_divices(self) -> None:               
        
        # GETTING THE PORT
        self.ports = self.serial_connection.check_available_ports()["ports"]
        # PUT THE PORTS INTO COMBOBOX VALUES
        self.arduino_board_combobox.configure(values=self.ports)
        
        if self.arduino_board_combobox.get() not in self.ports:
            self.arduino_board_combobox.set(value=[])
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
            self.arduino = None

        # CHECKS THE USB PORTS EACH 2 SECONDS
        self.after(1000, self.checking_divices)
    
    # TO STOP THE SONG LOOP WHEN THE APP WINDOW CLOSE
    def cancel(self) -> None:
        if self.arduino != None:
            if self.arduino.is_open:
                self.serial_connection.end(self.arduino)

        self.quit()
    
    # WHEN RAISES AN ERROR
    def alert_window(self, message:str) -> None:
        # DELETE A MAPPED TOP WINDOW WHEN IT EXITS
        if self.window != None:
            if self.window.winfo_ismapped:
                self.window.destroy()
            self.window = None
            
        # CREATE A TOP WINDOW
        self.window = CTkToplevel(self)
        self.window.attributes('-topmost', True)
        self.window.geometry("+200+200")
        self.window.resizable(False, False)
        self.window.title("Alert")
        
        self.window_frame = CTkFrame(self.window,
                                     fg_color="#111111",
                                     corner_radius=0)
        self.window_frame.grid()
        
        # ERROR MESSAGE
        CTkLabel(self.window_frame,
                 text=message,
                 text_color="#FFFFFF").grid(padx=30, pady=(20, 5))
        
        # CONFIRM BUTTON
        CTkButton(self.window_frame,
                  text="OK",
                  fg_color="#008833",
                  hover_color="#006611",
                  command=lambda: self.window.destroy()).grid(padx=30, pady=(5, 20), columnspan=2, sticky="EW")
        
if __name__ == "__main__":
    App()