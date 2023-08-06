#!/usr/bin/env python
# coding: utf-8
    
def printLinha(msg):
    '''
        Printing of a dividing line, containing an explanation str.
    '''
    texto = str(f'-=< {msg} >=-')
    tam = len(texto)
    print(f'{"-":^}' * tam)
    print(f'{texto:^{tam}}')
    print(f'{"-":^}' * tam)


def printLis(lista):
    '''
        Printing lists where indexes and values are shown.
    '''
    from time import sleep
    printLinha('Lista')
    for k, v in enumerate(lista):
        print(f'{k} -> {v}')


def printDic(dicionario):
    '''
        Dictionary printing, showing the keys and values of the items.
    '''
    printLinha('Dicionário')
    for kk, vv in dicionario.items():
        print(f'{kk} -> {vv}')
        if str(type(vv))[8:12] == 'list':
            printLis(vv)
            print('-'*10)


def timeProcess():
    '''
        Returns a tuple containing the time and date when the file was loaded.
    '''
    from datetime import datetime
    hora = str(f'{datetime.now().hour}h{datetime.now().minute}m{datetime.now().second}s')
    data = str(f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}')
    return hora, data


def setup_img_save(fonte = 15):
    '''
        Sets image parameters to default size 15.

            font.size
            legend.fontsize
            axes.labelsize
            axes.titlesize
            xtick.labelsize
            ytick.labelsize
    '''
    import matplotlib.pyplot as plt
    params = {
            'font.size': fonte,
            'legend.fontsize': fonte,
            'axes.labelsize': fonte,
            'axes.titlesize': fonte,
            'xtick.labelsize': fonte,
            'ytick.labelsize': fonte
    }
    plt.rcParams.update(params)
    
    
def img_save(campo, g=0, dpi=300, date='0000-0-0'):
    '''
        Saving png images with date.
    '''
    import matplotlib.pyplot as plt
    import os
    if campo:
        try:
            os.mkdir('figure')
        except OSError:
            print ("Creation of the directory figure failed")
        else:
            print ("Directory figure successfully created")
        # g += 1
        plt.savefig('figure/0'+str(g)+'-'+date+'.png', dpi=dpi, bbox_inches='tight')
        print('Save')
    else:
        print('Not save')
    plt.show()


def mask_corr_graphic(inic: int):
    '''
        The function receives an int which is the number of columns in the DataFrame.
        Return a numpy array mask with True and False for correlation plots.
    '''
    import numpy as np
    n = inic
    lista_fim = []
    for num in range(1, inic+1):
        n -= 1
        list_entra = [False]*num + [True]*n
        lista_fim.append(list_entra[:])
    return np.asarray(lista_fim)


def structured_confusion(test, prevision):
    '''
        Function to comprehensively organize and print a confusion matrix with two categories.
        
        Parameters:
        test => list-like with the original test values
        prevision => list-like with the values predicted by the model
    '''
    import pandas as pd
    from sklearn.metrics import confusion_matrix
    confu_print = pd.DataFrame(
        data=confusion_matrix(test, prevision),
        index=['Pred Pos','Pred Neg'],
        columns=['Meas Pos','Meas Neg'],
    )
    return confu_print


def meus_uteis():
    '''
        Prints the particular functions.
    '''
    lista_importes = [
        "printLinha()",
        "printLis()",
        "printDic()",
        "timeProcess()",
        "import_started()",
        "img_save()",
        "setup_img_save()",
        "mask_corr_graphic()",
        "structured_confusion()",
    ]
    printLis(lista_importes)


# def import_started():
#     '''
#         Returns a list containing automatic imports when loading Anaconda.
#     '''
#     lista_importes = [
#         "import os",
#         "import joblib",
#         "import random",
#         "import numpy as np",
#         "import pandas as pd",
#         "import seaborn as sns",
#         "import matplotlib.pyplot as plt",
#         "from meus.printer import *",
#         "from datetime import datetime",
#         "import statistics as stat",
#     ]
#     printLis(lista_importes)
