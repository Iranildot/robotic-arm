# Robotic Arm Control Application
This Python application provides a graphical user interface (GUI) for controlling a robotic arm using an Arduino microcontroller. Developed with the customtkinter library for a modern interface, it allows users to easily connect to and control a robotic arm via serial communication.

## Key Features

- **Arduino Connection:** Automatically detects available USB ports and establishes a serial connection with the connected Arduino board.
- **Real-Time Control:** Use on-screen buttons or keyboard inputs to move the robotic arm in different directions and operate the gripper.
- **Customizable Settings:** Adjust the angle step size for precise movement control of the robotic arm's servos.
- **Responsive UI:** Visual feedback for user actions, including button presses and Arduino connection status.
- **Error Handling:** Includes an alert system to notify users of connection issues or other errors.
- **Continuous Monitoring:** Periodically checks for connected devices and updates the interface accordingly.

## Technologies Used

- **CustomTkinter:** Provides a modern, customizable UI framework for the application's interface.
- **PIL (Pillow):** Handles image processing for icons and visual elements.
- **Serial Communication:** Facilitates data exchange between the application and the Arduino board to control the robotic arm.

## How to Run

- Ensure that your Arduino is connected to your computer via USB.
- Run the application (App) from the main script.
- Use the interface to connect to the Arduino and control the robotic arm.
  
This application is ideal for hobbyists and developers looking to create or enhance a robotic arm control system with a user-friendly interface.

## How the app looks like

![image](https://github.com/user-attachments/assets/45da2cea-2eb4-46d3-8a20-b55aa383b324)

