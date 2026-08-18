
##Retiro en valor futuro: gasto mensual, 
def valor_futuro(valor_presente , inflacion, tiempo):
    total = valor_presente * (1+inflacion)**tiempo
    return total
    
def valor_anual(valor):
    return valor*12

def retiro_anual_4(valor):
    return valor*25


if __name__ == '__main__':

    #Parametros
    inflacion_promedio = 0.04
    tiempo = 30
    valor_presente = [i*1000 for i in range(8,52,2)]

    #Calculo de valor futuro
    valor_anual_array = [valor_anual(i) for i in valor_presente] 
    valor_futuro_array = [valor_futuro(i, inflacion_promedio,tiempo) for i in valor_anual_array]
    retiro_anual_4_array = [retiro_anual_4(i) for i in valor_futuro_array]

    print(retiro_anual_4_array)
    
