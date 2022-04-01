import tkinter
from tkinter import *
from tkinter import ttk

# importando bibliotecas
from PIL import Image, ImageTk

import requests
from datetime import datetime

import pytz
import pycountry_convert as pc

################# cores ###############
co0 = "#444466"  # Preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul


fundo_dia="#6cc4cc"
fundo_noite="#484f60"
fundo_tarde = "#bfb86d"

fundo = fundo_dia

janela = Tk()
janela.title('')
janela.geometry('320x350')
janela.configure(bg=fundo)

#title
janela.title("Clima Tempo")

#icon in a Tkinter app
icone = Image.open('images/temperature-control.png')
photo = ImageTk.PhotoImage(icone)
janela.wm_iconphoto(False, photo)

#will disable max/min tab of window
janela.resizable(0,0)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

frame_top = Frame(janela, width=320, height=50,bg=co1, pady=0, padx=0, relief="flat",)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300,bg=fundo, pady=12, padx=0, relief="flat",)
frame_corpo.grid(row=2, column=0, sticky=NW)

style = ttk.Style(frame_top)
style.theme_use("clam")

global imagem

#Função que retorna as informações
def informacao():
    #Aqui a chave da API do openweathermap.org
    chave = ''
    cidade = e_local.get()
    api_link = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang=PT'.format(cidade,chave)

    #HTTP request
    r=requests.get(api_link)
    #convert the data in 'r' into dictionary
    data=r.json()
    
    print(data)
    

    # --- Dados do Json retornado ---
    cidade2 = data['name']
    temperatura = int(data['main']['feels_like'])
    tempo = data["main"]["temp"]
    umidade = data["main"]["humidity"]
    velocidade = data["wind"]["speed"]
    descricao = data["weather"][0]["description"]
   
    # zona , pais, horas 
    pais_codigo = data['sys']['country']
    
    zona_fuso=pytz.country_timezones[pais_codigo]
    
    # --- pais ---
    pais = pytz.country_names[pais_codigo]
    
    # --- data ---
    zona = pytz.timezone(zona_fuso[0]) 
    zona_horas = datetime.now(zona)
    zona_horas = zona_horas.strftime("%d/%m/%Y | %H:%M:%S %p")
    

    
    # Retorna o continente do Pais
    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continent_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continent_codigo)
        return pais_continente_nome
    
    continente= pais_para_continente(pais)
    
    # passando as informações na labels
    l_cidade['text'] = cidade2 + " - " + pais + " / "+ continente
    
    l_data['text'] = zona_horas
    l_temperatura['text'] = int(temperatura)
    l_temperatura_simbol['text'] = '°C'
    l_temperatura_nome['text'] = 'Celsius'
    l_umidade['text'] = "Umidade : "+ str(umidade) + '%'
    l_velocidade['text'] = "Velocidade do vento : "+ str(velocidade)
    l_descricao['text'] = descricao
    
    # apresentado sol e lua
    
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")
    
    global imagem
    
    zona_periodo = int(zona_periodo)
    if zona_periodo <= 5:
        imagem = Image.open('images/lua.png')
        fundo = fundo_noite
    elif zona_periodo <= 11:
        imagem = Image.open('images/sol_dia.png')
        fundo = fundo_dia
    elif zona_periodo <= 17:
        imagem = Image.open('images/sol_tarde.png')
        fundo = fundo_tarde
    elif zona_periodo <= 23:
        imagem = Image.open('images/lua.png')
        fundo= fundo_noite
    else: 
        pass
    
    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_corpo,image=imagem, compound=LEFT,  bg=fundo, fg="white",font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
    l_icon.place(x=162, y=50)
    
    
    janela.configure(bg=fundo)
    frame_top.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)
    
    l_cidade['bg'] = fundo
    l_data['bg'] = fundo
    l_temperatura['bg'] = fundo
    l_temperatura_simbol['bg'] = fundo
    l_temperatura_nome['bg'] = fundo
    l_umidade['bg'] = fundo
    l_velocidade['bg'] = fundo
    l_descricao['bg'] = fundo



#Configurando frame TOP

e_local= Entry(frame_top,width=20, justify='left',font=("",14),highlightthickness=1,relief="solid")
e_local.place(x=15, y=10)

b_ver = Button(frame_top, command=informacao, text="Ver Clima", height=1, bg=co1, fg=co2,font=('Ivy 9 bold'), relief=RAISED, overrelief=RIDGE)
b_ver.place(x=250, y=10)

#Configurando frame Corpo

l_cidade = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 14 '), bg=fundo, fg=co1)
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_data.place(x=10, y=54)

l_temperatura = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 38 '), bg=fundo, fg=co1)
l_temperatura.place(x=10, y=100)

l_temperatura_simbol = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 bold '), bg=fundo, fg=co1)
l_temperatura_simbol.place(x=85, y=110)

l_temperatura_nome = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 8 '), bg=fundo, fg=co1)
l_temperatura_nome.place(x=85, y=140)

l_umidade = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_umidade.place(x=10, y=184)

l_velocidade = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_velocidade.place(x=10, y=212)

l_descricao = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_descricao.place(x=170, y=190)

l_descricao = Label(frame_corpo, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_descricao.place(x=170, y=190)

janela.mainloop()
