import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- MODELO FÍSICO Y CONTROLADORES (Igual al ejemplo anterior) ---
M, B = 1.0, 0.5
def planta(t, x, u):
    return [x[1], (u - B * x[1]) / M]

def controlador_P(error):
    return 4.0 * error  # Kp = 4

def controlador_PID(error, error_acumulado, derivada):
    return (15.0 * error) + (8.0 * error_acumulado) + (4.0 * derivada)

# --- SIMULADOR MODIFICADO PARA EXTRAER LA FUERZA EN EL TIEMPO ---
def simular_sistema(controlador_tipo, setpoint=5.0, t_max=8.0):
    memoria = {"tiempo_ant": 0.0, "error_ant": setpoint, "integral": 0.0}
    historial_tiempo = []
    historial_u = []  # Para guardar la fuerza aplicada en el tiempo

    def lazo_cerrado(t, x):
        error = setpoint - x[0]
        dt = t - memoria["tiempo_ant"]
        
        if dt > 0:
            memoria["integral"] += error * dt
            derivada = (error - memoria["error_ant"]) / dt
        else:
            derivada = 0.0
            
        memoria["tiempo_ant"], memoria["error_ant"] = t, error
        
        # Selección de controlador
        if controlador_tipo == 'P':
            u = controlador_P(error)
        elif controlador_tipo == 'PID':
            u = controlador_PID(error, memoria["integral"], derivada)
        
        u = np.clip(u, -20.0, 20.0) # Saturación del motor
        
        # Guardamos los datos temporales de la fuerza
        historial_tiempo.append(t)
        historial_u.append(u)
        
        return planta(t, x, u)

    t_eval = np.linspace(0, t_max, 500)
    sol = solve_ivp(lazo_cerrado, [0, t_max], [0.0, 0.0], t_eval=t_eval)
    
    # Sincronizar historial de fuerza con los puntos exactos de t_eval
    u_interp = np.interp(sol.t, historial_tiempo, historial_u)
    
    return sol.t, sol.y[0], u_interp

# --- EJECUTAR SIMULACIONES ---
t, pos_P, u_P = simular_sistema('P')
t, pos_PID, u_PID = simular_sistema('PID')

# --- CONFIGURACIÓN DE LAS GRÁFICAS TEMPORALES ---
plt.figure(figsize=(12, 6))

# Gráfica Superior: Evolución de la Posición en el tiempo
plt.subplot(2, 1, 1)
plt.axhline(5.0, color='red', linestyle='--', label='Objetivo (5 metros)')
plt.plot(t, pos_P, label='Control Proporcional (P)', color='orange', linewidth=2)
plt.plot(t, pos_PID, label='Control PID', color='blue', linewidth=2)
plt.title('Análisis Temporal del Sistema de Control')
plt.ylabel('Posición (m)')
plt.grid(True)
plt.legend()

# Gráfica Inferior: Evolución del Esfuerzo del Motor (u) en el tiempo
plt.subplot(2, 1, 2)
plt.plot(t, u_P, color='orange', linestyle='--', label='Esfuerzo Motor P')
plt.plot(t, u_PID, color='blue', linestyle='--', label='Esfuerzo Motor PID')
plt.ylabel('Fuerza Actuador (N)')
plt.xlabel('Tiempo (segundos)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
