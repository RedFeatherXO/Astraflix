import serial
import time
from vpython import box, vector, rate

# Seriellen Port öffnen (Passe die Portnummer an)
ser = serial.Serial('COM9', 250000, timeout=0.01)
time.sleep(2)  # Warte auf die Verbindung

# Erstelle ein 3D-Modell (z. B. ein Quader für den ESP32)
model = box(size=vector(1, 0.2, 0.5), color=vector(0, 1, 0))

try:
    while True:
        # Lese eine Zeile von den Sensordaten
        line = ser.readline().decode('utf-8').strip()
        print(line)
        # if line:
        #     # Splitte die Zeile nach Kommata und extrahiere die Werte
        #     data = line.split(',')
        #     if len(data) == 6:
        #         try:
        #             ax, ay, az = float(data[0]), float(data[1]), float(data[2])
        #             gx, gy, gz = float(data[3]), float(data[4]), float(data[5])

        #             # Berechne Ausrichtung oder Update der Modellposition
        #             model.axis = vector(ax, ay, az)  # Beispielhafte Anwendung der Daten

        #             # Visuelle Aktualisierung
        #             rate(30)  # Refresh rate
        #         except ValueError as e:
        #             print(f"Fehler bei der Konvertierung der Daten: {e}")

finally:
    ser.close()
