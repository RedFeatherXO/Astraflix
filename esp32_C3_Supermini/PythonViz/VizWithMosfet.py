import serial
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import numpy as np
from collections import deque

# Configuration
WINDOW_SIZE = 200  # Number of samples to display
PORT = 'COM9'
BAUD_RATE = 250000

class MPU6050Visualizer:
    def __init__(self):
        # Initialize serial connection
        self.ser = serial.Serial(PORT, BAUD_RATE, timeout=0.01)
        time.sleep(2)  # Wait for connection to establish
        
        # Initialize data structures
        self.acc_x = deque(maxlen=WINDOW_SIZE)
        self.acc_y = deque(maxlen=WINDOW_SIZE)
        self.acc_z = deque(maxlen=WINDOW_SIZE)
        self.gyro_x = deque(maxlen=WINDOW_SIZE)
        self.gyro_y = deque(maxlen=WINDOW_SIZE)
        self.gyro_z = deque(maxlen=WINDOW_SIZE)
        
        # Initialize PWM control values
        self.pwm_values = {
            'A0': 0,
            'A1': 0,
            'A2': 0,
            'A3': 0
        }
        
        # Setup GUI
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        
        # Create acceleration plot
        self.acc_plot = pg.PlotWidget(title="Acceleration")
        self.acc_plot.setLabel('left', 'Acceleration', 'm/s²')
        self.acc_plot.setLabel('bottom', 'Samples')
        self.acc_plot.addLegend()
        self.acc_lines = {
            'x': self.acc_plot.plot(pen='r', name='X'),
            'y': self.acc_plot.plot(pen='g', name='Y'),
            'z': self.acc_plot.plot(pen='b', name='Z')
        }
        
        # Create gyroscope plot
        self.gyro_plot = pg.PlotWidget(title="Gyroscope")
        self.gyro_plot.setLabel('left', 'Angular Velocity', 'rad/s')
        self.gyro_plot.setLabel('bottom', 'Samples')
        self.gyro_plot.addLegend()
        self.gyro_lines = {
            'x': self.gyro_plot.plot(pen='r', name='X'),
            'y': self.gyro_plot.plot(pen='g', name='Y'),
            'z': self.gyro_plot.plot(pen='b', name='Z')
        }
        
        # Create PWM control widget
        self.pwm_widget = QtWidgets.QWidget()
        self.pwm_layout = QtWidgets.QHBoxLayout(self.pwm_widget)
        
        # Create slider for PWM control
        self.pwm_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pwm_slider.setMinimum(0)
        self.pwm_slider.setMaximum(255)
        self.pwm_slider.valueChanged.connect(self.update_pwm)
        
        # Create labels for PWM values
        self.pwm_labels = {}
        for pin in ['A0', 'A1', 'A2', 'A3']:
            label = QtWidgets.QLabel(f"{pin}: 0")
            self.pwm_labels[pin] = label
            self.pwm_layout.addWidget(label)
        
        # Add widgets to layout
        self.layout.addWidget(self.acc_plot)
        self.layout.addWidget(self.gyro_plot)
        self.layout.addWidget(self.pwm_widget)
        self.layout.addWidget(self.pwm_slider)
        
        # Setup window
        self.window.setWindowTitle("MPU6050 Data Visualizer with PWM Control")
        self.window.resize(800, 800)
        self.window.show()
        
        # Setup timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # Update every 10ms
        
    def update_pwm(self):
        pwm_value = self.pwm_slider.value()
        
        # Calculate PWM values for each pin
        self.pwm_values['A0'] = pwm_value
        self.pwm_values['A1'] = int(pwm_value) #* 0.075)
        self.pwm_values['A2'] = int(pwm_value) #* 0.05)
        self.pwm_values['A3'] = int(pwm_value) #* 0.01)
        
        # Update labels
        for pin, value in self.pwm_values.items():
            self.pwm_labels[pin].setText(f"{pin}: {value}")
        
        # Send PWM values over serial
        pwm_command = f"PWM,{self.pwm_values['A0']},{self.pwm_values['A1']},{self.pwm_values['A2']},{self.pwm_values['A3']}\n"
        self.ser.write(pwm_command.encode())
        
    def update(self):
        try:
            # Read data from serial
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                # Parse the CSV data
                data = line.split(',')
                if len(data) == 6:
                    # Update data queues
                    self.acc_x.append(float(data[0]))
                    self.acc_y.append(float(data[1]))
                    self.acc_z.append(float(data[2]))
                    self.gyro_x.append(float(data[3]))
                    self.gyro_y.append(float(data[4]))
                    self.gyro_z.append(float(data[5]))
                    
                    # Update plots
                    self.acc_lines['x'].setData(list(self.acc_x))
                    self.acc_lines['y'].setData(list(self.acc_y))
                    self.acc_lines['z'].setData(list(self.acc_z))
                    
                    self.gyro_lines['x'].setData(list(self.gyro_x))
                    self.gyro_lines['y'].setData(list(self.gyro_y))
                    self.gyro_lines['z'].setData(list(self.gyro_z))
        
        except Exception as e:
            print(f"Error: {e}")
    
    def run(self):
        """Start the application"""
        self.app.exec_()
    
    def cleanup(self):
        """Clean up resources"""
        self.ser.close()

if __name__ == "__main__":
    try:
        visualizer = MPU6050Visualizer()
        visualizer.run()
    finally:
        visualizer.cleanup()