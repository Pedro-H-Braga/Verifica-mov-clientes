import glob
import PySimpleGUI as sg
import os 

sg.theme('DarkBrown2') 

layout = [  [sg.Text('VERIFICAR MOVIMENTAÇÕES OCORRIDAS')],            
            [sg.Text('----------------------------------------------------------------------------------------------------')],
            [sg.Text('A seguir informe os caminhos para verificações')],
            [sg.Text('----------------------------------------------------------------------------------------------------')],
            [sg.Text('INFORME A PASTA *COMPARTILHADA* COM O CLIENTE:')], 
            [sg.FolderBrowse('PASTA COMPARTILHADA',key='-compartilhada-')],

            [sg.Text('INFORME A PASTA *INTERNA* DA EMPRESA:')], 
            [sg.FolderBrowse('-------PASTA INTERNA-------',key='-interna-')],
            [sg.Text('----------------------------------------------------------------------------------------------------')],
            [sg.Text('Informe o ano e mês de verificação')],
            [sg.Text('----------------------------------------------------------------------------------------------------')],
            [sg.Text('INFORME NA SEGUINTE FORMATAÇÃO: 202X/2')],
            [sg.InputText(key='-data_ver-')],
            [sg.Text('----------------------------------------------------------------------------------------------------')],
            [sg.Button('Verificar'), sg.Button('Sair')] ]

window = sg.Window('MOVIMENTACAO DE ARQUIVOS DOS CLIENTES', layout)

while True:
    event, values = window.read() 
    if event == sg.WIN_CLOSED or event == 'Sair': 
        break

    evento_compartilhada = values['-compartilhada-']
    evento_interna = values['-interna-']        
    pt_comp = evento_compartilhada
    pt_int = evento_interna

    data_verif = values['-data_ver-'] 
    print(data_verif)

    path_remoto = str(f'{pt_comp}')
    path_local  = str(f'{pt_int}')
    print(path_remoto, '\n', path_local)

    arq_remoto = sorted(list(glob.iglob(path_remoto + f'**/**/{data_verif}*/*', recursive=True)))

    print(arq_remoto)
    pos = 0 
    for nome in arq_remoto: 
       arq_remoto[pos] = nome[len(path_remoto):]
       pos += 1
    
    
    arq_local  = sorted(list(glob.iglob(path_local + f'**/**/{data_verif}*/*', recursive=True)))
    
    print(arq_local)
    pos = 0
    for nome in arq_local: 
       arq_local[pos] = nome[len(path_local):]
       pos += 1
    
    arq_dif    = sorted(list(set(arq_remoto).difference(set(arq_local))))
    
    dif_lista = [] 
    arq_lista = [] 
    lista_recebe_extensoes = []
    extensoes = ['.pdf','.csv','.xlsx','.gsheet']    
    
    txt_dif_montante = open('arquivos_dif.txt','w', encoding='utf-8')
    for posicao_dif in arq_dif:
      txt_dif_montante.write(f'{posicao_dif}\n')
      arq_lista.append(posicao_dif)  
    txt_dif_montante.close()   
    
    txt_final = open('txt_pdf.txt', 'w', encoding='utf-8') 
    for pos in range(0,4):
       for posicao_lista in arq_lista:
          if extensoes[pos] in posicao_lista:
            lista_recebe_extensoes.append(posicao_lista)
            txt_final.write(f'{posicao_lista}\n')
    txt_final.close()
    
    print('MOVIMENTACOES OCORRIDAS')

    cam = os.getcwd()
    os.system(f'{cam}/txt_pdf.txt')        

window.close()