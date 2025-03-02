from machine import Pin
import time

# Configurar el pin del sensor
sensor_pin = 34  # GPIO14
encoder = Pin(sensor_pin, Pin.IN, Pin.PULL_UP)

# Variables globales
pulsos = 0
ultimo_tiempo = time.ticks_ms()

# Función de interrupción
def contar_pulsos(pin):
    global pulsos
    pulsos += 1

# Configurar interrupción
encoder.irq(trigger=Pin.IRQ_FALLING, handler=contar_pulsos)

# Configuración del disco encoder
PULSOS_POR_REVOLUCION = 20  # Ajusta según el disco del encoder

while True:
    tiempo_actual = time.ticks_ms()
    delta_tiempo = time.ticks_diff(tiempo_actual, ultimo_tiempo) / 1000  # Segundos

    if delta_tiempo >= 1:  # Medir cada 1 segundo
        rpm = (pulsos / PULSOS_POR_REVOLUCION) * 60
        #print("Velocidad:", rpm, "RPM")
        print( pulsos)
        
        # Reiniciar contador
        #pulsos = 0
        ultimo_tiempo = tiempo_actual

    time.sleep(0.1)