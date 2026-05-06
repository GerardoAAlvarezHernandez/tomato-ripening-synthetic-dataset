import argparse
from utils.callbacks import Callbacks
import sys
import os
from pathlib import Path
from dataload2 import Dataset
import shutil 
import numpy
import random
import numpy as np
import time
import pandas as pd
from numpy import random

Generaciones = 10
Pc = 0.85
Pm = 0.1

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def genGtip(): #Esta funcion genera la poblacion inicial para el algortimo genetico
    gen = []
    poblacion = []
        
    for i in range(0,10):
        gen.append(random.uniform(0.5,0.9)) # anterior 0.3 - 07
        gen.append(random.randint(1,5))
        gen.append(random.uniform(0, 0.7)) # anterior 0 y 1
        gen.append(random.uniform(0.4, 1))   # anterior 0 y 1
        gen.append(random.normal(loc=0.2, scale=0.05))
        poblacion.append(gen)
        gen=[]
    return poblacion


def Fitness(poblacion,opt): #Esta funcion calcula el valor de fitness, para este caso es la metrica map50
    path = 'datasets/Tomates'
    n = os.getcwd()

    fitness = []

    carpetas_run=os.listdir(os.path.join(n,"runs","train"))

    for i in range(0,len(carpetas_run)):
        shutil.rmtree(os.path.join(n,"runs","train",carpetas_run[i]))

    for i in range(0,len(poblacion)):
        l1 = Dataset(path,poblacion[i])
        dest = shutil.move(os.path.join(n,"datasets"),n[:33]) 
        comando = "python train.py --img "+str(opt.imgsz)+" --batch "+str(opt.batch_size)+" --epochs "+str(opt.epochs)+" --data "+ str(opt.data)+" --weights "+str(opt.weights)+" --cache --hyp "+str(opt.hyp)
        os.system(comando)
        if i == 0:
            f = os.path.join(n,"runs","train","exp","results.csv")
            with open(f, newline='') as File:
                reader = numpy.loadtxt(File,delimiter=",",skiprows=1)
                fitness.append(reader[(opt.epochs)-1][6])
        else:
            f = os.path.join(n,"runs","train","exp"+str(i+1),"results.csv")
            with open(f, newline='') as File:
                reader = numpy.loadtxt(File,delimiter=",",skiprows=1)
                fitness.append(reader[(opt.epochs)-1][6])
        
        reg = shutil.move(os.path.join(n[:33],"datasets"),n)
        list1 = os.listdir(os.path.join(n,"datasets","Tomates new","images","train"))
        list2 = os.listdir(os.path.join(n,"datasets","Tomates new","labels","train"))
        for i in range(0,len(list2)):
            os.remove(os.path.join(n,"datasets","Tomates new","images","train",list1[i]))
            os.remove(os.path.join(n,"datasets","Tomates new","labels","train",list2[i]))
        os.remove(os.path.join(n,"datasets","Tomates new","labels","train.cache"))
        os.remove(os.path.join(n,"datasets","Tomates new","labels","val.cache"))
    
    return fitness

def Mutacion (Hijo1,Hijo2,Pm): # Funcion que realiza la mutacion mediante probabilidades ponderadas
    Aleatorio_hijo1 = []
    
    for i in range(0,len(Hijo1)):
        ran = random.uniform(0,1)
        Aleatorio_hijo1.append(ran)
    
    hijo1_mut = []
    
    for j in range(0,len(Aleatorio_hijo1)):
        if(Aleatorio_hijo1[j] < Pm):
            if j == 0:
                hijo1_mut.append(random.uniform(0.5,0.9)) #antes 0.3 y 0.7
            elif j == 1:
                hijo1_mut.append(random.randint(1,5))
            elif j == 2:
                hijo1_mut.append(random.uniform(0,0.7))
            elif j == 3:
                hijo1_mut.append(random.uniform(0.4,1))
            elif j == 4:
                hijo1_mut.append(random.normal(loc=0.2, scale=0.05))
        else:
            hijo1_mut.append(Hijo1[j])
        
    Aleatorio_hijo2 = []
    
    for i in range(0,len(Hijo2)):
        ran = random.uniform(0,1)
        Aleatorio_hijo2.append(ran)
    
    hijo2_mut = []
    
    for f in range(0,len(Aleatorio_hijo2)):
        if(Aleatorio_hijo2[f] < Pm):
            if f == 0:
                hijo2_mut.append(random.uniform(0.3,0.7))
            elif f == 1:
                hijo2_mut.append(random.randint(1,5)) 
            elif f == 2:
                hijo2_mut.append(random.uniform(0,0.7))
            elif f == 3:
                hijo2_mut.append(random.uniform(0.4,1))
            elif f == 4:
                hijo2_mut.append(random.normal(loc=0.2, scale=0.05))
        else:
            hijo2_mut.append(Hijo2[f])
            
    return hijo1_mut , hijo2_mut

def Ruleta (fitness): #Esta funcion realiza la seleccion por ruleta 

    Total = 0
    
    ProbaPon = []
    
    Proba =[]

    for f in fitness:
        Total  += f
    
    sumapon = 0
    
    for i in range(0,len(fitness)):
        Proba.append(fitness[i]/Total)
        sumapon += (fitness[i]/Total)
        ProbaPon.append(sumapon)
    
    indix=0
    
    ran = random.uniform(0, 1)
    
    bandera= False 
    
    for p in range(0,len(ProbaPon)):
        if ProbaPon[p] >= ran:
            indix = p
            return indix
            break
    
    return indix

def SelectPadre(poblacion,fit,opt): # esta funcion hace  la seleccion de los padres mediante el metodo de la ruleta

    indice1 = Ruleta(fit)
    
    indice2 = Ruleta(fit)
    
    while indice1==indice2:
        indice2=Ruleta(fit)
    
    Padre1 = poblacion[indice1]
    Padre2 = poblacion[indice2]
    
    return Padre1,Padre2,indice1,indice2

def Cruzapunto (gen1,gen2): # esta funcion realiza la operacion de cruza de 1 punto
    tuple1 = (0, 1, 2, 3, 4)
    
    indice=random.choice(tuple1)
    
    hijo1=[0.0, 0, 0.0, 0.0, 0.0] #Gen [probabilidad de cambio de fondo,# de tomates, probabilidad de ocolusion, porcentaje de ocolucion, tamano del tomate respecto al tamano de la imagen final]
    hijo2=[0.0, 0, 0.0, 0.0, 0.0]

    hijo1[:indice+1]=gen1[:indice+1]
    hijo1[indice+1:]=gen2[indice+1:]
    
    hijo2[:indice+1]=gen2[:indice+1]
    hijo2[indice+1:]=gen1[indice+1:]
    return hijo1,hijo2
    
def torneo (Padre,Hijo,opt,indice,fit): #Esta funcion encuentra el mejor individuo entre el padre y el hijo
    
    round1=[]
    score = 0

    round1.append(Hijo)
    
    fitness = Fitness(round1,opt)

    if(fit[indice] > fitness[0]):
        mejor = Hijo
        score = fitness[0]
    else:
        mejor = Padre
        score = fit[indice]
    
    return mejor,score



def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default=ROOT / 'yolov5s.pt', help='initial weights path')
    parser.add_argument('--cfg', type=str, default='', help='model.yaml path')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='dataset.yaml path')
    parser.add_argument('--hyp', type=str, default=ROOT / 'data/hyps/hyp.scratch-low.yaml', help='hyperparameters path')
    parser.add_argument('--epochs', type=int, default=100, help='total training epochs')
    parser.add_argument('--batch-size', type=int, default=16, help='total batch size for all GPUs, -1 for autobatch')
    parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=640, help='train, val image size (pixels)')
    parser.add_argument('--optimizer', type=str, choices=['SGD', 'Adam', 'AdamW'], default='SGD', help='optimizer')
    
    return parser.parse_known_args()[0] if known else parser.parse_args()
    
def main(opt):

    inicio = time.time()

    poblacion = genGtip()

    print("------------------------------------------------------------Generacion Inicial--------------------------------------------------------------------------")
    print(poblacion)
    
    print("\n")
    file = open("Resultados.txt", "w") 
    file.write("Fitness")
    file.write("                                                                   ")
    file.write("Cromosoma") 
    file.write('\n')

    for j in range(0,Generaciones):
        new_generacion = []
        fitness = Fitness(poblacion,opt)
        
        if(j==0):
            for i in range(0,len(fitness)):
                file.write(str(poblacion[i])+' '+str(fitness[i]))
                file.write('\n')
        
        print('\n')
        
        for k in range (0,int((len(poblacion)/2))):
            padre1,padre2,indice1,indice2 = SelectPadre(poblacion,fitness,opt)
            ran = random.uniform(0,1)  
            if(ran < Pc):
                hijo1,hijo2 = Cruzapunto(padre1,padre2)
                hijo1,hijo2 = Mutacion(hijo1,hijo2,Pm)
                hijo1,fitness1= torneo(padre1,hijo1,opt,indice1,fitness)
                hijo2,fitness2= torneo(padre2,hijo2,opt,indice2,fitness)
                file.write(str(hijo1)+' '+str(fitness1))
                file.write('\n')
                file.write(str(hijo2)+' '+str(fitness2))
                file.write('\n')
            else:
                hijo1=padre1
                hijo2=padre2
                file.write(str(hijo1)+' '+str(fitness[indice1]))
                file.write('\n')
                file.write(str(hijo2)+' '+str(fitness[indice2]))
                file.write('\n')
            new_generacion.append(hijo1)
            new_generacion.append(hijo2)
        file.write('\n')
        Espacio=new_generacion
        print("-------------------------------Generacion "+str(j+1)+"-----------------------------")
        print(Espacio)
        
    file.close()
    print(Espacio)  
    
    fin = time.time()

    print(fin-inicio)
    return 0


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
