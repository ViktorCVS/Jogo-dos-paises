from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import numpy as np
import base_dados_paises
import os
import pickle
import locale
import functools

locale.setlocale(locale.LC_ALL, 'pt_BR')

diretorio = os.getcwd()

control   = 0
control_2 = 0

gerador = np.random.default_rng()

status_seq = True

rL = {'Brasil':27,'as':13,'ac':23,'an':4,'af':56,'eu':60,'oc':18,'aa':54}

respostas = base_dados_paises.respostas
regiao_aleatoria=0

try:
    with open('pontos.pkl', 'rb') as f:
        pontuacao=pickle.load(f)
except:
    pontuacao = [0,0,0,0,0,0,0,0,0]
    with open('pontos.pkl', 'wb') as f:
        pickle.dump(pontuacao,f)

try:
    with open('pref.pkl', 'rb') as f:
        pref=pickle.load(f)
except:
    pref = [1,1,0,0,'Bandeira e Local','Aleatório']
    with open('pref.pkl', 'wb') as f:
        pickle.dump(pref,f)

pont_media = []
erro_medio = []

def on_config_change(*args):
    pref = [var_independente.get(),var_fantasmas.get(),var_salvar.get(),var_embar.get(),cbb_modo.get(),cbb_tipo.get()]
    with open('pref.pkl', 'wb') as f:
        pickle.dump(pref,f)

def ciclo():

    pais_aleatorio_f()
    confirmar()


def informa():

    top = Toplevel(janela)
    top.geometry("290x320+600+300")
    top.title("Informações")
    top.iconbitmap(diretorio+r'\ícone\world.ico')
    top.attributes('-topmost', 'true')
    top.resizable(False,False)

    lb_informacao_1 = Label(top, text='\n* Use a acentuação e pontuação correta!')
    lb_informacao_1.place(x=10,y=10)
    lb_informacao_2 = Label(top, text='\n* O nome dos países sempre em português!')
    lb_informacao_2.place(x=10,y=50)
    lb_informacao_3 = Label(top, text='\n* Capitais podem ser escritas tanto em português\n quanto na língua local!',justify="left")
    lb_informacao_3.place(x=10,y=90)
    lb_informacao_4 = Label(top, text='\n* As respostas podem ser escritas maiúsculas,\n minúsculas ou de forma mista!',justify="left")
    lb_informacao_4.place(x=10,y=150)
    lb_informacao_4 = Label(top, text='\n* Países declarados independentes estão ativados\n por definição, podendo ser desativados em\n configurações!',justify="left")
    lb_informacao_4.place(x=10,y=200)
    lb_informacao_5 = Label(top, text='\n* Palestina Livre!',justify="left")
    lb_informacao_5.place(x=10,y=270)
    

binario = 0
def marcar_tudo():

    global binario

    if binario > 1:

        binario = 0

    if binario == 1:

        var_brasil.set(1)
        var_am_sul.set(1)
        var_am_central.set(1)
        var_am_norte.set(1)
        var_africa.set(1)
        var_europa.set(1)
        var_oceania.set(1)
        var_asia.set(1)

    elif binario == 0:
        
        var_brasil.set(0)
        var_am_sul.set(0)
        var_am_central.set(0)
        var_am_norte.set(0)
        var_africa.set(0)
        var_europa.set(0)
        var_oceania.set(0)
        var_asia.set(0)

    binario+=1


def muda_menu():

    global control
    global control_2

    global status

    global regiao

    global status_seq

    Tabs.select(tab_menu)
    
    if not var_salvar.get():
    
        control   = 0
        control_2 = 0

        status_seq = True

    else:

        if status==1 or status==0:

            if control_2>0:
                control_2-=1
            if control_2==0 and control>0:
                control-=1
                control_2=rL[regiao[control]]

                
def muda_config():

    Tabs.select(tab_configuracao)

def muda_paises():

    if not var_brasil.get() and not var_am_sul.get() and not var_am_central.get() and not var_am_norte.get() and not var_africa.get() and not var_europa.get() and not var_oceania.get() and not var_asia.get():

        top = Toplevel(janela)
        top.geometry("260x70+600+300")
        top.title("Erro de seleção")
        top.iconbitmap(diretorio+r'\ícone\world.ico')
        top.attributes('-topmost', 'true')
        top.resizable(False,False)

        lb_informacao_1 = Label(top, text='Selecione alguma região!')
        lb_informacao_1.place(x=60,y=20)


    elif not var_salvar.get() or status==0 or status==1:
        Tabs.select(tab_paises)
        pais_aleatorio_f()


    elif status==2 and var_salvar.get():
        Tabs.select(tab_paises)
        confirmar()

def teclado():

    if status==2:

        pais_aleatorio_f()

    else:

        confirmar()
   
status = 0

def pais_aleatorio_f():

    global status_seq

    global status

    status = 1

    global img_bandeira
    global img_loc

    global lb_bandeira
    global lb_loc
    global regiao_aleatoria

    global regiao
    global paises

    global pais_aleatorio
    
    global control
    global control_2

    b_proximo.configure(state=DISABLED)

    lb_correto['text']=''
    lb_qcorreto['text']=''
    lb_errado['text']=''
    lb_pergunta['text']=''

    e_pais.delete(0, END)
    e_capital.delete(0, END)
    e_continente.delete(0, END)

    e_pais.focus()

    if status_seq:

        regiao = []

        if var_brasil.get():

            regiao.append('Brasil')

        if var_am_sul.get():

            regiao.append('as')

        if var_am_central.get():

            regiao.append('ac')

        if var_am_norte.get():

            regiao.append('an')

        if var_africa.get():

            regiao.append('af')

        if var_europa.get():

            regiao.append('eu')

        if var_oceania.get():

            regiao.append('oc')

        if var_asia.get():

            regiao.append('aa')

    if cbb_tipo.get() == 'Aleatório':

        regiao_aleatoria = gerador.choice(regiao)
        paises = os.listdir(diretorio+f'\\bandeiras\\{regiao_aleatoria}')

        while(True):
            
            pais_aleatorio = gerador.choice(paises)
            if pais_aleatorio.split('.')[0] in base_dados_paises.respostas_independentes.keys() and var_independente.get():

                break

            elif pais_aleatorio.split('.')[0] in base_dados_paises.respostas_fantasmas.keys() and var_fantasmas.get():

                break

            elif pais_aleatorio.split('.')[0] not in base_dados_paises.respostas_fantasmas.keys() or pais_aleatorio.split('.')[0] not in base_dados_paises.respostas_independentes.keys():

                break
                
        
        control=0
        control_2=0

    else:

        if status_seq and not var_embar.get():
            
            regiao_aleatoria = regiao[control]
            paises = os.listdir(diretorio+f'\\bandeiras\\{regiao_aleatoria}')
            paises = sorted(paises,key=functools.cmp_to_key(locale.strcoll))

        elif status_seq and var_embar.get():

            gerador.shuffle(regiao)
            regiao_aleatoria = regiao[control]
            paises = os.listdir(diretorio+f'\\bandeiras\\{regiao_aleatoria}')
            gerador.shuffle(paises)

        while(True):
            
            pais_aleatorio = paises[control_2]

            if pais_aleatorio.split('.')[0] in base_dados_paises.respostas_independentes.keys() and not var_independente.get():
                
                control_2+=1

            elif pais_aleatorio.split('.')[0] in base_dados_paises.respostas_fantasmas.keys() and not var_fantasmas.get():

                control_2+=1

            else:
 
                break
        
        control_2+=1
        if(control_2==len(paises)):
            control_2=0
            control+=1
        if(control==len(regiao)):
            control=0

    status_seq = False
    img_bandeira = Image.open(diretorio+f'\\bandeiras\\{regiao_aleatoria}\\{pais_aleatorio}')
    dim_img = list(img_bandeira.size)
    proporcao = dim_img[1]/dim_img[0]
    img_bandeira = img_bandeira.resize((280,round(280*proporcao)), Image.LANCZOS)
    img_bandeira= ImageTk.PhotoImage(img_bandeira)
    
    img_loc = Image.open(diretorio+f'\\local\\{regiao_aleatoria}\\{pais_aleatorio}')
    img_loc = img_loc.resize((300,300), Image.LANCZOS)
    img_loc= ImageTk.PhotoImage(img_loc)

    if cbb_modo.get()=='Bandeira e Local':

        lb_bandeira['image']=img_bandeira
        lb_loc['image']=img_loc

    elif cbb_modo.get()=='Bandeira apenas':

        lb_bandeira['image']=img_bandeira
        lb_loc['image']=''

    elif cbb_modo.get()=='Local apenas':

        lb_bandeira['image']=''
        lb_loc['image']=img_loc    

    if regiao_aleatoria == 'Brasil':

        lb_pergunta['text']="Qual é o estado, sua capital e sua região, respectivamente?"
        lb_pais['text']='Estado:'
        lb_regiao['text']='Região:'
        lb_pergunta.lift()

    else:

        lb_pergunta['text']="Qual é o país, sua capital e seu continente, respectivamente?"
        lb_pais['text']='País:'
        lb_regiao['text']='Continente:'
        lb_pergunta.lift()


    b_confirmar.configure(state=NORMAL)

        
def confirmar():

    global status
    status = 2

    global pais_aleatorio
   
    lb_correto['text']=''
    lb_qcorreto['text']=''
    lb_errado['text']=''
    lb_pergunta['text']=''


    pais_aleatorio = pais_aleatorio.split('.')[0]

    pais_resposta = e_pais.get()
    capital_resposta = e_capital.get()
    continente_resposta = e_continente.get()
    
    acerto = 0
    pontuacao[5]=pontuacao[5]+1

    pont_media.append(0)
    erro_medio.append(1)

    if pais_resposta.upper() in [local.upper() for local in respostas[pais_aleatorio][0]]:

        acerto += 1
        
        pontuacao[0]=round(pontuacao[0]+0.35,2)
        pontuacao[5]=round(pontuacao[5]-0.35,2)

        pont_media[-1]=pont_media[-1]+0.35
        if(len(pont_media)==241):
            pont_media.pop(0)

        erro_medio[-1]=erro_medio[-1]-0.35
        if(len(erro_medio)==241):
            erro_medio.pop(0)

    if capital_resposta.upper() in [local.upper() for local in respostas[pais_aleatorio][1]]:

        acerto += 1
        
        pontuacao[0]=round(pontuacao[0]+0.5,2)
        pontuacao[5]=round(pontuacao[5]-0.5,2)

        pont_media[-1]=pont_media[-1]+0.5
        if(len(pont_media)==241):
            pont_media.pop(0)

        erro_medio[-1]=erro_medio[-1]-0.5
        if(len(erro_medio)==241):
            erro_medio.pop(0)


    if continente_resposta.upper() in [local.upper() for local in respostas[pais_aleatorio][2]]:

        acerto += 1
        
        pontuacao[0]=round(pontuacao[0]+0.15,2)
        pontuacao[5]=round(pontuacao[5]-0.15,2)

        pont_media[-1]=pont_media[-1]+0.15
        if(len(pont_media)==241):
            pont_media.pop(0)

        erro_medio[-1]=erro_medio[-1]-0.15
        if(len(erro_medio)==241):
            erro_medio.pop(0)

    

    if acerto == 3:

        lb_correto['text']="Resposta certa!"
        lb_correto.lift()

        pontuacao[-1]=pontuacao[-1]+1
        if(pontuacao[-1]>pontuacao[1]):
            pontuacao[1]=pontuacao[-1]

    elif acerto == 0:

        lb_errado['text']=f"Respostas erradas! As respostas certas são {respostas[pais_aleatorio][0][0]}, {respostas[pais_aleatorio][1][0]}, {respostas[pais_aleatorio][2][0]}."
        lb_errado.lift()
        
        pontuacao[-1]=0

    else:

        lb_qcorreto['text']=f"Resposta quase certa! As respostas certas são {respostas[pais_aleatorio][0][0]}, {respostas[pais_aleatorio][1][0]}, {respostas[pais_aleatorio][2][0]}."
        lb_qcorreto.lift()

        pontuacao[-1]=0
    
    aproveitamento = pontuacao[0]/(pontuacao[0]+pontuacao[5])
    pontuacao[2] = round(aproveitamento,4)
    pontuacao[3] = round(sum(pont_media),2)
    aproveitamento_m = sum(pont_media)/len(pont_media)
    pontuacao[4] = round(aproveitamento_m,4)
    pontuacao[6] = round(sum(erro_medio),2)
    b_confirmar.configure(state=DISABLED)
    b_proximo.configure(state=NORMAL)

    with open('pontos.pkl', 'wb') as f:
        pickle.dump(pontuacao, f)
        

# ------------------------------ DEFINIÇÃO

janela = Tk()
janela.title("Treino de Países")

janela.geometry("850x850+570+110")

janela.iconbitmap(diretorio+r'\ícone\world.ico')

style = ttk.Style(janela)
style.layout('Tabless.TNotebook.Tab', [])

Tabs = ttk.Notebook(janela, style="Tabless.TNotebook")
Tabs.pack(side='top',expand=1,fill='both')

tab_menu = Frame(Tabs,borderwidth=0,highlightthickness = 0)
Tabs.add(tab_menu,text="Menu")

tab_paises = Frame(Tabs,borderwidth=0,highlightthickness = 0)
Tabs.add(tab_paises,text="Paises")

tab_configuracao = Frame(Tabs,borderwidth=0,highlightthickness = 0)
Tabs.add(tab_configuracao,text="Configuração")

# ------------------------------ MENU

img_config = Image.open(diretorio+f'\\ícone\\config.png')
img_config = img_config.resize((20,20), Image.LANCZOS)
img_config = ImageTk.PhotoImage(img_config)


lb_intro = Label(tab_menu, text="Bem vindo ao programa de aprendizado de países.",font=('Arial',14))
lb_intro.pack(pady=(30,0))

bt_marcar= Button(tab_menu,width=20,text="Marcar/Desmarcar",command=marcar_tudo)
bt_marcar.place(relx=0.5,x=-80,y=320+100)

bt_comeco = Button(tab_menu,width=20,text="Começar",command=muda_paises)
bt_comeco.place(relx=0.5,x=-80,y=320+150)

bt_sair = Button(tab_menu,width=20,text="Sair",command=janela.destroy)
bt_sair.place(relx=0.5,x=-80,y=320+200)

bt_config = Button(tab_menu,width=30,height=30,image=img_config,command=muda_config)
bt_config.place(x=10,y=10)

helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
bt_info = Button(tab_menu,width=3,text='i',font=helv36,command=informa)
bt_info.place(relx=1,rely=1,x=-50,y=-50)


var_brasil=IntVar()
var_am_sul=IntVar()
var_am_central=IntVar()
var_am_norte=IntVar()
var_africa=IntVar()
var_europa=IntVar()
var_oceania=IntVar()
var_asia=IntVar()


cb_brasil = Checkbutton(tab_menu, text='Brasil',variable=var_brasil)
cb_brasil.place(relx=0.5,x=-40,y=100+50)

cb_am_sul = Checkbutton(tab_menu, text='América do Sul',variable=var_am_sul)
cb_am_sul.place(relx=0.5,x=-40,y=120+50)
cb_am_sul.select()

cb_am_central = Checkbutton(tab_menu, text='América Central',variable=var_am_central)
cb_am_central.place(relx=0.5,x=-40,y=140+50)
cb_am_central.select()

cb_am_norte = Checkbutton(tab_menu, text='América do Norte',variable=var_am_norte)
cb_am_norte.place(relx=0.5,x=-40,y=160+50)
cb_am_norte.select()

cb_africa = Checkbutton(tab_menu, text='África',variable=var_africa)
cb_africa.place(relx=0.5,x=-40,y=180+50)
cb_africa.select()

cb_europa = Checkbutton(tab_menu, text='Europa',variable=var_europa)
cb_europa.place(relx=0.5,x=-40,y=200+50)
cb_europa.select()

cb_oceania = Checkbutton(tab_menu, text='Oceania',variable=var_oceania)
cb_oceania.place(relx=0.5,x=-40,y=220+50)
cb_oceania.select()

cb_asia = Checkbutton(tab_menu, text='Ásia',variable=var_asia)
cb_asia.place(relx=0.5,x=-40,y=240+50)
cb_asia.select()

lb_versao = Label(tab_menu, text="V1.7b.nb")
lb_versao.place(rely=1,x=1,y=-20)


# ------------------------------ JOGO


lb_bandeira = Label(tab_paises)
lb_loc = Label(tab_paises)

lb_jogo = Label(tab_paises, text="Você iniciou o programa de aprendizado de países",font=('Arial',14))
lb_jogo.place(relx=0.5,x=-200,y=20)

lb_pergunta = Label(tab_paises)

e_pais = Entry(tab_paises,width=40)
e_capital = Entry(tab_paises,width=40)
e_continente = Entry(tab_paises,width=40)


lb_pais = Label(tab_paises, text="")
lb_capital = Label(tab_paises, text="Capital:")
lb_regiao = Label(tab_paises, text="")

lb_pergunta = Label(tab_paises, text='',font=('Arial',10))

lb_correto = Label(tab_paises,font=('Arial',10))
lb_qcorreto = Label(tab_paises,font=('Arial',10))
lb_errado = Label(tab_paises,font=('Arial',10))

b_confirmar = Button(tab_paises,width=20,text="Confirmar",command=confirmar)

b_proximo = Button(tab_paises,width=20,text="Próximo",command=pais_aleatorio_f)
b_proximo.configure(state=DISABLED)

b_menu = Button(tab_paises,width=20,text="Menu",command=muda_menu)


# ------------------------------ Configuração

pos = 50

b_menu_config = Button(tab_configuracao,width=20,text="Menu",command=muda_menu)

var_independente=IntVar()
cb_independente = Checkbutton(tab_configuracao, text='Habilitar países declarados independentes',variable=var_independente)
cb_independente.place(relx=0.5,x=-120,y=2*pos)
if pref[0] == 1:
    cb_independente.select()
var_independente.trace('w',on_config_change)

var_fantasmas=IntVar()
cb_fantasma = Checkbutton(tab_configuracao, text='Habilitar países extintos',variable=var_fantasmas)
cb_fantasma.place(relx=0.5,x=-120,y=3*pos)
if pref[1] == 1:
    cb_fantasma.select()
var_fantasmas.trace('w',on_config_change)

var_salvar=IntVar()
cb_salvar = Checkbutton(tab_configuracao, text='Salvar no modo sequencial',variable=var_salvar)
cb_salvar.place(relx=0.5,x=-120,y=4*pos)
if pref[2] == 1:
    cb_salvar.select()
var_salvar.trace('w',on_config_change)

var_embar=IntVar()
cb_embar = Checkbutton(tab_configuracao, text='Embaralhar o modo sequencial',variable=var_embar)
cb_embar.place(relx=0.5,x=-120,y=5*pos)
if pref[3] == 1:
    cb_embar.select()
var_embar.trace('w',on_config_change)

cbb_modo = ttk.Combobox(tab_configuracao, values=["Bandeira e Local", "Bandeira apenas", "Local apenas"])
cbb_modo.place(relx=0.5,x=-115,y=6*pos)
if pref[4] == 'Bandeira e Local':
    cbb_modo.current(0)
elif pref[4] == 'Bandeira apenas':
    cbb_modo.current(1)
else:
    cbb_modo.current(2)
cbb_modo.bind("<<ComboboxSelected>>", lambda event: on_config_change())

lb_configuracao = Label(tab_configuracao, text="Modo de jogo")
lb_configuracao.place(relx=0.5,x=35,y=6*pos-2)

cbb_tipo = ttk.Combobox(tab_configuracao, values=["Aleatório", "Sequencial"])
cbb_tipo.place(relx=0.5,x=-115,y=7*pos)
if pref[5] == 'Aleatório':
    cbb_tipo.current(0)
else:
    cbb_tipo.current(1)
cbb_tipo.bind("<<ComboboxSelected>>", lambda event: on_config_change())

lb_configuracao = Label(tab_configuracao, text="Tipo de jogo")
lb_configuracao.place(relx=0.5,x=35,y=7*pos-2)


def nova_pos(event):

    try:

        if cbb_modo.get()=='Bandeira e Local':

            lb_bandeira.place(x=(janela.winfo_width()-lb_bandeira.winfo_reqwidth()-lb_loc.winfo_reqwidth())/3,y=150)
            lb_loc.place(x=2*((janela.winfo_width()-lb_bandeira.winfo_reqwidth()-lb_loc.winfo_reqwidth())/3)+lb_bandeira.winfo_reqwidth(),y=100)

        elif cbb_modo.get()=='Bandeira apenas':

            lb_bandeira.place(x=(janela.winfo_width()-lb_bandeira.winfo_reqwidth())/2,y=150)

        elif cbb_modo.get()=='Local apenas':

            lb_loc.place(x=(janela.winfo_width()-lb_loc.winfo_reqwidth())/2,y=100)

        e_continente.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2,y=580+40)
        e_capital.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2,y=480+50+40)
        e_pais.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2,y=480+40)
        
        if regiao_aleatoria == 'Brasil':
            lb_pais.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2-47,y=516)
            lb_regiao.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2-50,y=617)
        else:
            lb_pais.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2-35,y=516)
            lb_regiao.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2-70,y=617)
            
        lb_capital.place(x=(janela.winfo_width()-e_pais.winfo_reqwidth())/2-50,y=567)

        lb_pergunta.place(x=(janela.winfo_width()-lb_pergunta.winfo_reqwidth())/2,y=460)

        b_confirmar.place(x=(janela.winfo_width()-b_confirmar.winfo_reqwidth())/2,y=640+40)
        b_proximo.place(x=(janela.winfo_width()-b_confirmar.winfo_reqwidth())/2,y=690+40)
        b_menu.place(x=(janela.winfo_width()-b_confirmar.winfo_reqwidth())/2,y=740+40)
        b_menu_config.place(x=(janela.winfo_width()-b_confirmar.winfo_reqwidth())/2,y=740+40)
        
        lb_correto.place(x=(janela.winfo_width()-lb_correto.winfo_reqwidth())/2,y=460)
        lb_qcorreto.place(x=(janela.winfo_width()-lb_qcorreto.winfo_reqwidth())/2,y=460)
        lb_errado.place(x=(janela.winfo_width()-lb_errado.winfo_reqwidth())/2,y=460)

    except:

        pass


#janela.resizable(False,False)
janela.bind("<Configure>", nova_pos)
janela.bind('<Return>',lambda event:teclado())
janela.mainloop()
