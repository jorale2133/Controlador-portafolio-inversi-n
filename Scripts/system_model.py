import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math 

##Ecuación diferencial resuelta
def step_response(t, R, alpha, y_inicial):
    return  (alpha/R)*(math.exp(R*t) - 1) + y_inicial*math.exp(R*t) 
##Respueta a la rampa
def ramp_response(t, R, alpha, y_inicial):
    return y_inicial*math.exp(R*t) + (alpha / R**2)*math.exp(R*t) - (alpha/R)*t
## Ecuación diferencial rampa + escalon base
def ramp_step_response(t, R, alpha, base, y_inicial):
    return (y_inicial + base/R + alpha/R**2)*math.exp(R*t) - (base/R + alpha/R**2) -  (alpha/R)*t  

def model_points(tiempo, R, alpha, y_inicial):
    solutions = []
    t_eval = np.linspace(0, tiempo, 30)
    
    for i in t_eval:
        solutions.append(step_response(i, R, alpha=alpha, y_inicial=y_inicial))
    return t_eval, solutions

##Modelo de la ecuación diferencial
def model_system(t, y, R,  u_func):
    return R*y + u_func(t)

## Entradas U(t)
def exp_function(t, alpha, inflation):
    return alpha * np.exp(inflation*t)

def step_function(t, alpha):
    return alpha

def ramp_function(t, alpha, escalon_base):
    return alpha*t + escalon_base 

##Solve diferential equation.
def simulate_model(tiempo=30, delta_t = 30, Rendimiento=0.1, y_inicial=0, alpha=100, select_input=0, inflation=0.04):

    y0= [y_inicial]
    t_span = (0,tiempo) ##Tiempo en años
    t_eval = np.linspace(0, tiempo, delta_t) #generate a delta-t
    
    if select_input == 0:
        input_system = lambda t: 0.0
    elif select_input == 1:
        input_system = lambda t: step_function(t, alpha)
    elif select_input == 2:
        input_system = lambda t: ramp_function(t, alpha)
    elif select_input == 3:
        input_system = lambda t: exp_function(t,alpha, inflation)

    solution = solve_ivp( model_system, t_span, y0, t_eval=t_eval,args=(Rendimiento, input_system))
    
    return solution


if __name__ == "__main__":
    
    Rendimiento = 0.09
    tiempo = 30 #En años
    y_inicial = 100
    alpha = 100


    t , s = model_points(tiempo, Rendimiento, alpha=alpha, y_inicial=y_inicial)

    solutions_zero = simulate_model(tiempo, Rendimiento=Rendimiento, alpha=alpha, y_inicial=10000 , select_input=0)
    
    solutions_step = simulate_model(tiempo, Rendimiento=Rendimiento, alpha=alpha, y_inicial=y_inicial, select_input=1)
    solutions_ramp = simulate_model(tiempo, Rendimiento=Rendimiento, alpha=alpha, y_inicial=y_inicial, select_input=2)
    solutions_exp = simulate_model(tiempo, Rendimiento=Rendimiento, alpha= y_inicial, y_inicial=y_inicial, select_input=3)


    fig, ax = plt.subplots(2,1)
    
    ax[0].grid(True)
    ax[1].grid(True)

    ##Gráfica de soluciones
    ax[0].plot(solutions_zero.t, solutions_zero.y[0], 'black', linestyle = 'dotted')
    ax[0].plot(solutions_step.t, solutions_step.y[0], 'green')
    ax[0].plot(solutions_ramp.t, solutions_ramp.y[0], 'red')
    ax[0].plot(solutions_exp.t, solutions_exp.y[0], 'blue')


    ax[0].plot(solutions_zero.t[-1], solutions_zero.y[0][-1], 'd')
    ax[0].text(solutions_zero.t[-1], solutions_zero.y[0][-1], f'{solutions_zero.y[0][-1]}')

    ##Graficas de entradas    
    escalon = [ step_function(i, alpha) + y_inicial for i in t ]
    rampa = [ ramp_function(i, alpha) + y_inicial for i in t ]
    exponencial = [ exp_function(i, alpha, 0.1)-alpha + y_inicial for i in t ]

    ax[1].plot( t, rampa, 'red', linestyle = 'dotted')
    ax[1].plot( t, escalon, 'green', linestyle = 'dotted')
    ax[1].plot( t, exponencial, 'blue', linestyle = 'dotted')

    plt.show()


