import serial
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Seriellen Port öffnen
ser = serial.Serial('COM9', 250000, timeout=0.01)
time.sleep(2)  # Warte auf die Verbindung

# Erstelle eine 3D-Achse
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialisiere die Datenarrays
x_data, y_data, z_data = [0], [0], [0]  # Anfangswerte, damit der Plot nicht leer ist

# Initialisiere das Streudiagramm
scatter = ax.scatter(x_data, y_data, z_data)

# Funktion zum Aktualisieren des Plots
def update_plot():
    scatter._offsets3d = (x_data, y_data, z_data)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.001)  # Update alle 10ms

try:
    while True:
        # Lese eine Zeile von den Sensordaten
        line = ser.readline().decode('utf-8').strip()
        if line:
            # Splitte die Zeile nach Kommata und extrahiere die Werte
            data = line.split(',')
            if len(data) == 6:
                ax_val, ay_val, az_val = float(data[0]), float(data[1]), float(data[2])
                gx_val, gy_val, gz_val = float(data[3]), float(data[4]), float(data[5])

                # Debug-Ausgabe der Daten
                print(f"ax: {ax_val}, ay: {ay_val}, az: {az_val}")

                # Füge die neuen Werte zu den Listen hinzu
                x_data.append(ax_val)
                y_data.append(ay_val)
                z_data.append(az_val)

                # Begrenze die Datenpunkte (optional)
                max_points = 100
                if len(x_data) > max_points:
                    x_data.pop(0)
                    y_data.pop(0)
                    z_data.pop(0)

                # Aktualisiere die Visualisierung
                update_plot()

finally:
    ser.close()
