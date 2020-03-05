##Las funciones fueron tomadas y modificadas del ejemploGasolinera
import simpy
import random
import numpy
import matplotlib.pyplot as plt

def proceso(nombre,env,tiempo,espacio,RAM):
    global totalT  
    global tiempos
    global desviacion

    #Se crea el proceso
    yield env.timeout(tiempo)
    #Tiempo que le toma al proceso llegar
    tiempoInicial = env.now
    #Se establece la memoria que se utilizara y la cantidad de instrucciones
    memoria = random.randint(1,10)
    instrucciones = random.randint(1, 10)
    print ('%s proceso inicia en tiempo %f necesita %d de memoria  y tiene %e instrucciones'  % (nombre,tiempoInicial,memoria, instrucciones))

    #Se define ir a la cola
    with RAM.get(instrucciones) as turno:
        print(nombre, "tiemp: ", env.now)
        yield turno
        #Si tiene mas de dos instrucciones
        while instrucciones>2:
            with espacio.request() as simular:
                yield simular
                instrucciones = instrucciones-3
                yield env.timeout(1)
                print(nombre,  "tiempo: ", env.now)
            io = random.randint(1,2)
            if(io == 2):
                yield env.timeout(1)
         #Si se tienen menos de tres       
        if instrucciones<3:
            yield env.timeout(1)
        RAM.put(memoria)

    #Espacio a usar del cpu
    with espacio.request() as turno:
        yield turno 
        yield env.timeout(instrucciones)
        print ('%s proceso termina a las %f' % (nombre, env.now))
    TOTAL = env.now - tiempoInicial
    tiempos.append(TOTAL)
    print ('%s se tardo %f' % (nombre, TOTAL))
    totalT = totalT + TOTAL


desviacion1=list()
promedios1=list()
desviacion2=list()
promedios2=list()
desviacion3=list()
promedios3=list()
CantidadProcesos=[25,50,100,150,200]
intervalos=[10,5,1]
print("Con intervalos de 10")
for k in CantidadProcesos:
    env = simpy.Environment() #ambiente de simulación
    espacio = simpy.Resource(env,capacity = 1)#Cantidad de CPU
    RAM = simpy.Container(env,capacity= 200, init=200) #Cantidad de RAM
    random.seed(10) # fijar el inicio de random
    tiempos = list()
    totalT = 0
    procesos=k
    for i in range(k): #numero de procesos 
        env.process(proceso('proceso %d'%i,env,random.expovariate(1.0/10),espacio,RAM))

    env.run()  #correr la simulación en tiempo infinito
    promedios1.append(totalT/k)
    desviacion1.append(numpy.std(tiempos))
    print ("tiempo promedio para", k  ,"procesos es: ", totalT/k)
print("Los promedios son: ",promedios1)
print("Las desviaciones estandar son: ",desviacion1)

print("Con intervalos de 5")
for k in CantidadProcesos:
    env = simpy.Environment() #ambiente de simulación
    espacio = simpy.Resource(env,capacity = 1)#Cantidad de CPU
    RAM = simpy.Container(env,capacity= 200, init=200) #Cantidad de RAM
    random.seed(10) # fijar el inicio de random
    tiempos = list()
    totalT = 0
    procesos=k
    for i in range(k): #numero de procesos 
        env.process(proceso('proceso %d'%i,env,random.expovariate(1.0/5),espacio,RAM))

    env.run()  #correr la simulación en tiempo infinito
    promedios2.append(totalT/k)
    desviacion2.append(numpy.std(tiempos))
    print ("tiempo promedio para", k  ,"procesos es: ", totalT/k)
print("Los promedios son: ",promedios2)
print("Las desviaciones estandar son: ",desviacion2)

print("Con intervalos de 1")
for k in CantidadProcesos:
    env = simpy.Environment() #ambiente de simulación
    espacio = simpy.Resource(env,capacity = 1)#Cantidad de CPU
    RAM = simpy.Container(env,capacity= 200, init=200) #Cantidad de RAM
    random.seed(10) # fijar el inicio de random
    tiempos = list()
    totalT = 0
    procesos=k
    for i in range(k): #numero de procesos 
        env.process(proceso('proceso %d'%i,env,random.expovariate(1.0),espacio,RAM))

    env.run()  #correr la simulación en tiempo infinito
    promedios3.append(totalT/k)
    desviacion3.append(numpy.std(tiempos))
    print ("tiempo promedio para", k  ,"procesos es: ", totalT/k)
print("Los promedios son: ",promedios1)
print("Las desviaciones estandar son: ",desviacion1)
plt.plot(CantidadProcesos,promedios1,"ro",color="green")
plt.plot(CantidadProcesos,promedios2,"ro",color="red")
plt.plot(CantidadProcesos,promedios3,"ro",color="blue")
plt.title("Promedios por cantidad de procesos con 200 de memoria")
plt.xlabel("Cantidad de procesos")
plt.ylabel("Promedio")
plt.legend(("Promedios con invervalos de 10","Promedios con invervalos de 5","Promedios con invervalos de 1"),loc="upper left")
plt.show()