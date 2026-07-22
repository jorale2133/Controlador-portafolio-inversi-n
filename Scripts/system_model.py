import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math 

##Ecuación diferencial resuelta
def step_response(t, R, alpha, y_inicial):
    return  (alpha/R)*(math.exp(R*t) - 1) + y_inicial*math.exp(R*t) 

def model_points(tiempo, R, alpha, y_inicial):
    solutions = []
    t_eval = np.linspace(0, tiempo, 30)
    
    for i in t_eval:
        solutions.append(step_response(i, R, alpha=alpha, y_inicial=y_inicial))
    return t_eval, solutions

##Modelo de la ecuación diferencial
def model_system(t, y, R,  u_func):
    return R*y + u_func(t)

## Entradas 
def exp_function(t, alpha, inflation):
    return alpha * np.exp(inflation*t)

def step_function(t, alpha):
    return alpha

def ramp_function(t, alpha):
    return alpha*t


def simulate_model(tiempo=30, delta_t = 30, Rendimiento=0.1, y_inicial=0, alpha=100, select_input=0, inflation=0.04):

    y0= [y_inicial]
    t_span = (0,tiempo) ##Tiempo en años
    t_eval = np.linspace(0, tiempo, delta_t) #generate a delta-t
    
    if select_input == 0:
        input_system = lambda t: 0.0
    elif select_input == 1:
        input_system = lambda t: step_function(t, alpha)
    elif select_input ==2:
        input_system = lambda t: ramp_function(t, alpha)
    elif select_input == 3:
        input_system = lambda t: exp_function(t,alpha, inflation)

    solution = solve_ivp( model_system, t_span, y0, t_eval=t_eval,args=(Rendimiento, input_system))
    
    return solution


if __name__ == "__main__":
    
    Rendimiento = 0.09
    tiempo = 30 #En años
    alpha = 100
    y_inicial = 0

    t , s = model_points(tiempo, Rendimiento, alpha=alpha, y_inicial=y_inicial)

    solutions = simulate_model(tiempo, Rendimiento=Rendimiento, alpha=alpha, y_inicial=y_inicial, select_input=2)

    print(solutions)

    fig, ax = plt.subplots()
    ax.grid(True)

    ax.plot(solutions.t, solutions.y[0],)
    
    ax.plot(solutions.t[-1], solutions.y[0][-1], 'd')
    ax.text(solutions.t[-1], solutions.y[0][-1], f'{solutions.y[0][-1]}')
    
    rampa = [ ramp_function(i, alpha) for i in solutions.t ]
    ax.plot(solutions.t, rampa)

    ax.plot
    plt.show()


