import random
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm
from rembg import remove
#from numba import jit



#def mascara (img):

    #imagen = remove(img) #Esta linea quita el fondo de la imagen que se le envie 
    
    #entrada = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #La imagen retornada se pasa al espacio de color de escala de  grises 
    
    
    #ret3, inverse_mask1 = cv2.threshold(entrada,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) # se realiza una segmentacion automatica mediante el algoritmo otsu para quedarse con la maracara del objeto existente en la imagens
    
    #cnts,_ = cv2.findContours(inverse_mask1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # se buscan todos los contornos existente con la finalidad de encontrar su rectangulo que lo rode 
    
    #max = [] # variable para quedarse con los contornos mas grandes que se encuentren en la imagen 
    
    #for i in range(0,len(cnts)): #for que realiza la tarea de buscar los contornos mas grande que se encuentran en la imagen 
    	#x,y,w,h = cv2.boundingRect(cnts[i]) # se busca las coordenadas de rectangulo que enciera al controno inesimo que se encuentra en la imagen 
    	#if (w >= 70 and h>=80): # Este es el filtro que hace el descartar los contornos que no cumplan que el width sea mayor o igual de 70 y hight mayor o igual que 80
        	#max.append(i) #Guarda el indice de controno que cumple con esta condicion 

    #x,y,w,h = cv2.boundingRect(cnts[max[0]]) # se calcula las coordenadas del rectangulo que 
    
    #imagen = imagen[y:y+h , x:x+w]
    #inverse_mask1 = inverse_mask1[y:y+h , x:x+w]
    
    #return imagen,inverse_mask1

def xyxytoxyhw(coordenadas,Sw):

    x = int((coordenadas[0]*640)-(Sw/2))
    y = int((coordenadas[1]*640)-(Sw/2))
    w = int(coordenadas[2]*640)
    h = int(coordenadas[3]*640)
    
    return x,y,w,h
    
def Coordenadas(x,y,Sw,Sh,Tw,Th):
    
    if (x+Sw/2)>=640:
        x_center = 1 
    else:
        x_center = (x+Sw/2)/Tw
    
    if (y+Sh/2) >=640:
        y_center = 1
    else:
        y_center = (y+Sh/2)/Th
    	
    w = Sw/Tw
    h = Sh/Th
    
    return x_center, y_center, w, h
      

def Cambio_fondo (imagen,mask,Ntomates,porsize):
    
    
    size = int(640*porsize)

    res = cv2.resize(imagen, dsize=(size, size), interpolation=cv2.INTER_CUBIC)
    mask = cv2.resize(mask, dsize=(size, size), interpolation=cv2.INTER_CUBIC)
    
    coord = []
    
    rectangulos=[]
    
    here = os.getcwd() # esto se quedaria fijo para poder entrar y salir sin perden el origen donde esta el archivo que corre los el codigo principal
    list1=os.listdir(os.path.join(here,"fondos"))
    
    ran = random.randint(0,(len(list1)-1))
    
    fondo = cv2.imread(os.path.join(here,"fondos",list1[ran]))


    im_pil1 = Image.fromarray(res)
        
    img1 = np.zeros((640,640,3),np.uint8)
    fondoim = Image.fromarray(img1)

    mas_pil1=Image.fromarray(mask)
    fondo_mask=np.zeros((640,640,3),np.uint8)
    mask1=Image.fromarray(fondo_mask)

    for i in range(0,Ntomates):
        x1 = random.randint(0, 640-size)
        y1 = random.randint(0, 640-size)
        fondoim.paste(im_pil1,(x1, y1))
        mask1.paste(mas_pil1,(x1 , y1))
        x,y,w,h = Coordenadas(x1,y1,res.shape[0],res.shape[1],640,640)
        rectangulos.append(x)
        rectangulos.append(y)
        rectangulos.append(w)
        rectangulos.append(h)
        coord.append(rectangulos)
        rectangulos=[]


    n = np.asarray(fondoim)
    img = cv2.cvtColor(n,cv2.COLOR_RGB2BGR)


    n1=np.asarray(mask1)
    img4= cv2.cvtColor(n1,cv2.COLOR_RGB2GRAY)

    mask_inv1 = cv2.bitwise_not(img4) # se realiza una inversion de la mascara para poder hacer la operacion de elimianr parte de la imagen donde estaran ubucados los tomates 
    msk_inv1 = mask_inv1.astype('uint8')

    fondo1 = cv2.resize(fondo, dsize=(640, 640), interpolation=cv2.INTER_CUBIC) # se ridemensiona la imagen que sera de fondo a un tamaño de 640 x 640 pixeles que sera el tamaño de la imagen modificada 
    fondo1 = fondo1.astype('uint8')

    op2=cv2.bitwise_and(fondo1 , fondo1, mask=msk_inv1) # se hace la operacion de eliminara parte de la imagen donde se encuentras los tomates que se colocaran mediante la mascara
    op2=cv2.cvtColor(op2,cv2.COLOR_RGB2BGR)

    imagen_trans = img+op2
    
    return msk_inv1,imagen_trans,coord


def ocolusion (imagen , Ntomates, coordenadas, porcentaje,porsize):
    
    size = int(porsize*640)

    img_colo12 = imagen.astype('uint8') #imagene original donde estan los toamtes ya colocados 
  
    img1 = np.zeros((640,640,3),np.uint8)
    img1 = Image.fromarray(img1) 

    img2 = np.zeros((640,640,3),np.uint8)
    img2 = Image.fromarray(img2) 
    
    h= cv2.imread(os.path.join("mascaras","hoja_sinfonda.jpg"))
    hm=cv2.imread(os.path.join("mascaras","MASK_HOJA.jpg"))
    
    h = cv2.resize(h, dsize=(size, size), interpolation=cv2.INTER_CUBIC)
    hm = cv2.resize(hm, dsize=(size, size), interpolation=cv2.INTER_CUBIC)

    hoja1 = Image.fromarray(h)
    hoja = Image.fromarray(hm) 

    can_tap = (1-porcentaje)

    for i in range(0,Ntomates):
        x1,y1,_,h1 = xyxytoxyhw(coordenadas[i],size)
        img1.paste(hoja,(x1,y1+int(h1*can_tap)))
        img2.paste(hoja1,(x1,y1+int(h1*can_tap)))

    n1=np.asarray(img1)
    n2=np.asarray(img2)
    	
    img4_1 = cv2.cvtColor(n2,cv2.COLOR_RGB2BGR)
    img4 =  cv2.cvtColor(n1,cv2.COLOR_RGB2GRAY)
    	
    op2=cv2.bitwise_and(img_colo12,img_colo12,mask=cv2.bitwise_not(img4))
    op2=cv2.cvtColor(op2,cv2.COLOR_RGB2BGR)
    	
    f1=op2+img4_1

    return f1

    
def Dataset (path , MatrizTnaform):
    
    list2=os.listdir(os.path.join(path,"images","train")) # estos se leeran primero
    
    origen = os.getcwd()
    
    imagenes_originales=[]
    
    for i in range(0,len(list2)):
        imagenes_originales.append(cv2.imread(os.path.join(path,"images","train",list2[i])))
    
    loop = tqdm(total = len(list2), position=0 , leave=False)

    for i in range(0,len(list2)):
        
        g=os.path.splitext(list2[i])
        
        loop.set_description("Loading data augmentation...".format(i))
        loop.update(1)
        #print(g[0])
        imagen = imagenes_originales[i]
        
        prob_fondo = random.uniform(0 , 1)
        
        if(prob_fondo < MatrizTnaform[0]):

            imSin_fondo = cv2.imread(os.path.join("mascaras","mask",g[0]+"_sinfondo.jpg")) 
            mascara1 = cv2.imread(os.path.join("mascaras","mask",g[0]+"mask.jpg"))
            
            #s =random.uniform(MatrizTnaform[4],MatrizTnaform[4]+0.1) #primera iteracion haciendo variar el tamano del tomate desde el valor del gen 5 y gen5+0.5 en una distibucion uniforme
            
            s =random.uniform(5/640,MatrizTnaform[4]+0.1)
            
            if s<=(1/640):
            	s=(5/640)
            else:
            	s=s
                        
            mask, imagen_trans, coordenadas= Cambio_fondo(imSin_fondo , mascara1 , MatrizTnaform[1],s)
            
            #print(coordenadas)
            
            prob_oculusion = random.uniform(0 , 1)
            
            if(prob_oculusion < MatrizTnaform [2]):
                final_image = ocolusion (imagen_trans , MatrizTnaform[1] , coordenadas , MatrizTnaform[3],s)
                fichero = open(os.path.join(origen,"datasets","Tomates","labels","train",g[0]+'.txt'))
                os.chdir(os.path.join(origen,"datasets","Tomates new","images","train"))
                name=g[0]+'.jpg'
                cv2.imwrite(name,final_image)
                os.chdir(origen)
                name=g[0]+'.txt'
                os.chdir(os.path.join(origen,"datasets","Tomates new","labels","train"))
                file = open(name, "w")
                clase=fichero.read()

                for j in range(0,MatrizTnaform[1]):
                    file.write(clase[0])
                    file.write(" ")
                    file.write(" " + str(coordenadas[j][0]) + " " + str(coordenadas[j][1]) + " " + str(coordenadas[j][2]) + " " + str(coordenadas[j][3])) 
                    file.write('\n')
                
                file.close()
                os.chdir(origen)
            
            else:
                final_image = imagen_trans
                os.chdir(os.path.join(origen,"datasets","Tomates new","images","train"))
                fichero = open(os.path.join(origen,"datasets","Tomates","labels","train",g[0]+'.txt'))
                name=g[0]+'.jpg'
                cv2.imwrite(name, cv2.cvtColor(final_image,cv2.COLOR_RGB2BGR) )
                os.chdir(origen)
                name=g[0]+'.txt'
                os.chdir(os.path.join(origen,"datasets","Tomates new","labels","train"))
                file = open(name, "w")
                clase=fichero.read()

                for z in range(0,int(MatrizTnaform[1])):
                    file.write(clase[0])
                    file.write(" ")
                    file.write(" " + str(coordenadas[z][0]) + " " + str(coordenadas[z][1]) + " " + str(coordenadas[z][2]) + " " + str(coordenadas[z][3])) 
                    file.write('\n')
                
                file.close()
                os.chdir(origen)

        else:
            
            final_image = cv2.resize(imagen, dsize=(640, 640), interpolation=cv2.INTER_CUBIC)
            imagen1 = remove(final_image)
            entrada = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
            ret3, inverse_mask1 = cv2.threshold(entrada,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) # se realiza una segmentacion automatica mediante el algoritmo otsu
            cnts,_ = cv2.findContours(inverse_mask1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            max = []

            for i in range(0,len(cnts)):
                x,y,w,h = cv2.boundingRect(cnts[i])
                if (w >= 70 and h>=80):
                    max.append(i)
    	    
            x,y,w,h = cv2.boundingRect(cnts[max[0]])
            
            x_center, y_center, w1, h1 = Coordenadas(x,y,w,h,640,640)
    	    
            fichero = open(os.path.join(origen,"datasets","Tomates","labels","train",g[0]+'.txt'))
            os.chdir(os.path.join(origen,"datasets","Tomates new","images","train"))
            name=g[0]+'.jpg'
            cv2.imwrite(name,final_image)
            os.chdir(origen)
            name=g[0]+'.txt'
            os.chdir(os.path.join(origen,"datasets","Tomates new","labels","train"))
            file = open(name, "w") 
            file.write(fichero.read()[0])
            file.write(" ")
            file.write(" " + str(x_center) + " " + str(y_center) + " " + str(w1) + " " + str(h1)) 
            file.write('\n')
            file.close()
            os.chdir(origen)
	
    
    loop.close()
    return  list2

