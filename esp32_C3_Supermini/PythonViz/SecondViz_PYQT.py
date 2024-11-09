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
        
        # Add plots to layout
        self.layout.addWidget(self.acc_plot)
        self.layout.addWidget(self.gyro_plot)
        
        # Setup window
        self.window.setWindowTitle("MPU6050 Data Visualizer")
        self.window.resize(800, 600)
        self.window.show()
        
        # Setup timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # Update every 10ms
        
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