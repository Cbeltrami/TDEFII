import serial
import time
from tkinter import *

global ser, reconnect, distancia, velocidade0, lb_StatusGeral, aceleracao
global delay, tempob, tempoev, nciclos, problema_valores, posicao_status, problema_valores2, erroaccelA, erroaccelB, erroaccelC
global accelA, accelB, accelC, propA, propB, propC, tipoA, tipoB, tipoC, ativacao, tfinal, aviso

tfinal = 0
delay = 0 
tempob = 0 
tempoev = 0 
nciclos = 0
posicao_status = 0
distancia = 0
ativacao = 0
aviso = 0
aceleracao = 'Desativada.'
accelA = 'Insira um valor.'
accelB = 'Insira um valor.'
accelC = 'Insira um valor.'
propA = 'Insira um valor.'
propB = 'Insira um valor.'
propC = 'Insira um valor.'
problema_valores2 = 1
problema_valores = 1

##########################################################################################
def conectar():	
	global ser, reconnect
	com = 'COM1'
	rcnn= 0
	while int(com[3]) <= 12:
		try:
			ser = serial.Serial(com, 9600, timeout=1)
			reconnect = 0
			break
		except:
			com = com[:3] + str(int(com[3])+1)
			rcnn = rcnn + 1
		if rcnn == 36:
			reconnect = 1
			break	
##########################################################################################
def conexao():
	global reconnect, connect_status, lb_connect_status

	janela_connect = Tk()
	janela_connect.title("Conexão serial")
	janela_connect.iconbitmap('ico.ico')
	
	lb_connect_S = Label(janela_connect, text='Status da conexão')
	lb_connect_S.place(x=97, y=20)

	bt_connect = Button(janela_connect,  width=25, height=3, text = "Reconectar", command = lambda: reconectar(janela_connect))
	bt_connect.place(x=50, y=50)
	if reconnect == 0:		
		bt_connect["text"] = "Reconectar"
	if reconnect == 1:
		bt_connect["text"] = "Conectar"
	
	lb_connect_status = Label(janela_connect, text= "", justify = LEFT)
	lb_connect_status.place(x=50, y=110)
	connect_status = info_connect(janela_connect) ##### FUNÇÃO INFOCONNECT
	janela_connect.geometry("280x220+200+200")
	janela_connect.mainloop()
##########################################################################################
def info_connect(janela_connect):	
	global ser, connect_status, lb_connect_status, reconnect, janela
	
	if reconnect == 1:
		connect_status = 'Sem conexão'
		janela.title("LEe- Dip Coating - Dispositivo não conectado")
		try:
			janela3.title("Módulo avançado - Dispositivo não conectado")
		except:
			pass		

	if reconnect == 0:
		connect_status = 'Conectado à porta ' + str(ser.port) + "\nBaudrate: " + str(ser.baudrate) + "\nBytesize: " + str(ser.bytesize) + "\nParity: " + str(ser.parity) + "\nStopbits" + str(ser.stopbits) + "\nTimeout: " + str(ser.timeout)
		janela.title("LEe- Dip Coating")
		try:
			janela3.title("Módulo avançado")
		except:
			pass

	lb_connect_status["text"] = connect_status
##########################################################################################
def reconectar(janela_connect):
	conectar()
	info_connect(janela_connect)
##########################################################################################
def informar():

	janela_info = Tk()
	janela_info.title("Dip Coating LEe- Informações:")
	janela_info.iconbitmap('ico.ico')
	
	lb_informar1 = Label(janela_info, justify = LEFT, font= "TkDefaultFont 10 bold", text='Dispositivo Dip Coating LEe-')
	lb_informar1.place(x=97, y=20)

	lb_informar_t = Label(janela_info, justify = LEFT, text='Este dispositivo foi projetado especialmente para deposições de filmes\nfinos poliméricos para o uso interno do laboratório de Espectroscopia\nde Elétrons (LEe-) da Universidade Federal do Rio Grande do Sul (UFRGS)\nsem qualquer fim lucrativo. Use-o por sua própria conta e risco.')
	lb_informar_t.place(x=30, y=50)

	lb_informar2 = Label(janela_info, justify = LEFT, font= "TkDefaultFont 9 bold", text='Dip Coating clássico:')
	lb_informar2.place(x=30, y=125)

	lb_informar3 = Label(janela_info, justify = LEFT, text='Velocidade máxima: 2264 \u03BCm/s\nVelocidade mínima: 54 \u03BCm/s\nTempo máximo de banho: 9999 s\nTempo máximo de evaporação: 9999 s\nNúmero máximo de ciclos: 9999')
	lb_informar3.place(x=30, y=150)

	lb_informar4 = Label(janela_info, justify = LEFT, font= "TkDefaultFont 9 bold", text='Dip Coating avançado:')
	lb_informar4.place(x=30, y=240)

	lb_informar5 = Label(janela_info, justify = LEFT, text='Aceleração máxima aceita: 9999.99 \u03BCm/s²\nPercentuais somente aceitam valores inteiros entre 0 a 100 cuja soma\ndeve dar 100, pois são referentes a divisões do trajetório.')
	lb_informar5.place(x=30, y=265)

	lb_informar6 = Label(janela_info, justify = LEFT, font= "TkDefaultFont 10 bold", text='Desenvolvedores:')
	lb_informar6.place(x=97, y=330)

	lb_informar7 = Label(janela_info, justify = LEFT, text='Eng. Carlos Ballardin Beltrami\nContato: carlosballardinbeltrami@gmail.com\n\nDr. Jonder Morais\nContato: jonder@if.ufrgs.br')
	lb_informar7.place(x=30, y=360)

	#justify = LEFT
	janela_info.geometry("440x460+200+200")
	janela_info.mainloop()
##########################################################################################
def set1():
	global ser
	global problema_valores, reconnect, lb_StatusGeral
	global aceleracao, delay, tempob, tempoev, nciclos

	if reconnect != 0:
		lb_StatusGeral["text"] = "Conectar dispositivo."
		return
	captura()
	if problema_valores != 0:
		lb_StatusGeral["text"] = "Inserir valores válidos"
		return
	enviar()
	if problema_valores != 0:
		lb_StatusGeral["text"] = "Problemas de comunicação.\nClique em Set novamente! \nCaso o erro persistir, feche programas abertos ou reconecte."
		bt_set["bg"] = "yellow"
		bt_go["bg"] = "red"
		lb_ValoresPlaca["text"] = ('Problema de recepção')
		return
	else:
		lb_StatusGeral["text"] = "Aguardando instruções.\nPronto para iniciar.\nPrepare o substrato."
		bt_set["bg"] = "green"		
		bt_go["bg"] = "green"
		lb_ValoresPlaca["text"] = ('Valores recebidos na placa:\n  - Velocidade: ' + str(delay) + '\n' + ' - Aceleração: ' + aceleracao + '\n' + " - Tempo banho: " + str(tempob) + '\n' + ' - Tempo de evaporação: ' + str(tempoev) + '\n'  + ' - Número de ciclos: ' + str(nciclos))
##########################################################################################
def captura():
	global delay, tempob, tempoev, nciclos, problema_valores, velocidade0

	delay = delay_en.get() # float
	tempob = tempob_en.get() # int
	tempoev = tempoev_en.get() # int
	nciclos = nciclos_en.get() # int

	problema_valores = 0	#Flag caso houver valor inválido
	indice = 1
	lista_valores = [0, tempob, tempoev, nciclos]
	for valor in lista_valores[1:]:
		try:
			valor = int(valor)
			if valor <10000 and valor >=0:
				lista_valores[indice] = valor
			else:
				lista_valores[indice] = "Valor inválido"
				problema_valores += 1
		except:
			lista_valores[indice] = "Valor inválido"
			problema_valores += 1
		indice += 1

	indice = 0
	try:
		delay = int(delay)
		if delay <= 2264 and delay >= 54:
			lista_valores[0] = delay
		else:
			lista_valores[0] = "Valor inválido"
			problema_valores += 1
	except:
			lista_valores[0] = "Valor inválido"
			problema_valores += 1

	lb_delay_status["text"] = lista_valores[0]
	lb_tempob_status["text"] = lista_valores[1]
	lb_tempoev_status["text"] = lista_valores[2]
	lb_nciclos_status["text"] = lista_valores[3]
##########################################################################################
def enviar():
	global ser, delay, tempob, tempoev, nciclos, problema_valores
	problema_valores = 0

	ini1 = ":::"	#4 valores
	ini2 = ":::"
	end1 = ":::"
	end2 = ":::"
			
	delay_s = str(delay).zfill(4)
	tempob_s = str(tempob).zfill(4)
	tempoev_s = str(tempoev).zfill(4)
	nciclos_s = str(nciclos).zfill(4)

	data_train = delay_s+tempob_s+tempoev_s+nciclos_s
	data_train = ini1 + ini2 + data_train + end1 + end2
	data_train = list(data_train)
	
	time.sleep(2) #Estritamente necessário (por algum motivo (?))
	data_station = [] #Local onde serão recebidos os dados
	ser.write("R".encode())

	for x in data_train:
		ser.write(str(x).encode())

	time.sleep(0.3)
	x=0
	while(x<=3):
		y = ser.readline()
		y = y.rstrip()
		try:
			y = y.decode("utf-8")
			data_station.append(y)
			x+=1
		except:
			pass

	u = int(data_station[0]) # delay
	v = int(data_station[1]) # tempob
	w = int(data_station[2]) # tempoev
	y = int(data_station[3]) # nciclos

	if(u==int(delay) and v==int(tempob) and w==int(tempoev) and y==int(nciclos)):
		problema_valores = 0
	else:
		problema_valores += 1
##########################################################################################


##########################################################################################
def go():
	global problema_valores, problema_valores2, posicao_status, aviso, tfinal, distancia, delay, tempob, tempoev, nciclos

	if problema_valores != 0:
		return

	if problema_valores2 != 0 and ativacao == 1:
		lb_StatusGeral["text"] = "Verificar aceleração."
		return

	if posicao_status != 2:
		lb_StatusGeral["text"] = "Determinar ponto de máximo e mínimo.\nBotão posicionar."
		return

	if aviso == 1 and ativacao == -1:
		aviso = 0
		aviso_aceleracao()
		return
	
	if ativacao == 1:
		simularaccel(0)
	else: #if ativacao <= 0:
		tfinal = round((distancia/256), 4)/(delay/1000)
	
	t = ( float(tfinal) + float(tempob) + float(tempoev) + float(round((distancia/256) , 4)/(1.9531)) ) * float(nciclos)
	horas = int(t//3600)
	minutos = int(round(((t % 3600)/3600)*60))
	segundos = int(round((((t % 3600)/3600)*60 % 1)*60))

	t = time.localtime()
	lb_StatusGeral["text"] = "Deposição iniciada."
	lb_Mensagens["text"] = 'Deposição iniciada às ' + str(t[3]) + 'h e ' + str(t[4]) + 'min do dia ' + str(t[2]) + '/' + str(t[1]) + '/' + str(t[0]) + '.   O processo levará aproximadamente ' +  str(horas) + 'h, ' + str(minutos) + 'min e ' + str(segundos) + 's'
	ser.write("G".encode()) #Processo inciado

	separador = "-----------------------------------------------------------------------------------\n"
	parametros = "Velocidade: "+str(delay)+" um/s Tempo de banho: "+str(tempob)+" s Tempo de evaporação: "+str(tempoev)+" s Número de ciclos: "+str(nciclos)+"\n" 
	horario = str(time.asctime()) + "\n"
	trajeto = "Tamanho do trajeto: " + str(distancia) + " mm     "
	tempototal = "Tempo de deposição: " + str(horas) + ":" + str(minutos) + ":" + str(segundos) + "\n"
	if ativacao > 0:
		tipo = 'Dip coating acelerado\n'	
		parametros = parametros + "Aceleração A: "+str(accelA)+" um/s² Proporção: "+str(propA)+"% Tipo: "+tipoA
		parametros = parametros + "\nAceleração B: "+str(accelB)+" um/s² Proporção: "+str(propB)+"% Tipo: "+tipoB
		parametros = parametros + "\nAceleração C: "+str(accelC)+" um/s² Proporção: "+str(propC)+"% Tipo: "+tipoC + "\n"
	else:
		tipo = 'Dip coating clássico\n'

	log = horario + "Processo iniciado: " + tipo + trajeto + tempototal + parametros + separador

	try:
		fl = open("LEe- Dip Coating - histórico de uso/Histórico.txt", "r")
		fl.close()
		fl = open("LEe- Dip Coating - histórico de uso/Histórico.txt", "a+")
		fl.write(log)
	except:
		fl = open("LEe- Dip Coating - histórico de uso/Histórico.txt", "a+")
		fl.write("*****************************************************************************\n")
		fl.write("                        ")
		fl.write(str(time.asctime()) + "\nArquivo de histórico não encontrado, foi movido ou deletado da pasta original\nNovo arquivo gerado.\n")
		fl.write("*****************************************************************************\n")
		fl.write(log)
	fl.close()
	
##########################################################################################
def posicionar():

	if reconnect == 1:
		lb_StatusGeral["text"] = 'Conectar dispositivo.'
		return

	global posicao_status, bt_top, bt_down
		
	ser.write("H".encode())
	lb_Mensagens["text"]  = 'Definindo posições. Para interroper o processo clique em Parar'
	posicao_status = 0

	janela2 = Tk()
	janela2.title("Ajuste de posição")
	janela2.iconbitmap('ico.ico')

	lb_top = Label(janela2, text='Ponto A')
	lb_top.place(x=20, y=20)
	bt_top = Button(janela2, text = "Fixar", width=25, command = lambda: Top(janela2))
	bt_top.place(x=20, y=50)

	lb_down = Label(janela2, text='Ponto B')
	lb_down.place(x=20, y=80)
	bt_down = Button(janela2, text = "Fixar", width=25, command = lambda: Down(janela2))
	bt_down.place(x=20, y=110)
		
	lb_info_posicionar = Label(janela2, text='Utilizar botões físicos para posicionar')
	lb_info_posicionar.place(x=20, y=140)

	janela2.geometry("225x200+200+200")
	janela2.mainloop()
##########################################################################################
def Top(janela2):
	global bt_top, posicao_status, distancia
	if  bt_top["bg"] != "green":
		ser.write("Q".encode())
		bt_top["text"] = "Fixado"
		bt_top["bg"] = "green"
		posicao_status = posicao_status + 1
	elif bt_top["bg"] == "green":
		pass
	if posicao_status == 2:
		time.sleep(0.1)
		distancia = ler()
		lb_Mensagens["text"]  = 'Posições definidas. Percurso: ' + str(round(distancia/256 , 4)) + ' mm.'
		janela2.destroy()
##########################################################################################
def	Down(janela2):
	global bt_down, posicao_status, distancia
	if bt_down["bg"] != "green":
		ser.write("W".encode())
		bt_down["text"] = "Fixado"
		bt_down["bg"] = "green"
		posicao_status = posicao_status + 1
	elif bt_down["bg"] == "green":
		pass 
	if posicao_status == 2:
		time.sleep(0.1)
		distancia = ler()
		lb_Mensagens["text"]  = 'Posições definidas. Percurso: ' + str(round(distancia/256 , 4)) + ' mm.'
		janela2.destroy()
##########################################################################################
def ler():
	ser.write("B".encode())
	y = ser.readline()
	y = y.rstrip()
	try:
		y = y.decode("utf-8")
	except:
		y = 0
	y = int(y)
	return y
##########################################################################################
def	subir():
	global posicao_status
	if posicao_status == 2:
		lb_ManualStatus["text"] = "Mover substrato para o ponto máximo."
		ser.write("S".encode())	
	else:
		lb_StatusGeral["text"] = "Defina as posições do porta-amostras."
##########################################################################################
def descer():
	global posicao_status
	if posicao_status == 2:
		lb_ManualStatus["text"] = "Mover substrato para o ponto mínimo."
		ser.write("D".encode())
	else:
		lb_StatusGeral["text"] = "Defina as posições do porta-amostras."
##########################################################################################
def parar():
	ser.write("P".encode())
	if (lb_ManualStatus["text"] == ""):
		lb_ManualStatus["text"] = "Parado."
	elif (lb_ManualStatus["text"] == "Parado."):
		lb_ManualStatus["text"] = ""
	else:
		lb_ManualStatus["text"] = "Parado."

	lb_StatusGeral["text"] = "Aguardando instruções."
	lb_Mensagens["text"] = ""
##########################################################################################
def prev_func(janela_pred):
	global veloc_pred, Tempo_pred, Ciclos_pred, Temperatura_pred, Humidade_pred, Percurso_pred, secagem_pred

	lb_results_pred = Label(janela_pred, font= "TkDefaultFont 8 bold", justify = LEFT, text='')
	lb_results_pred.place(x=10, y=320)
	
	Velocidade_p = veloc_pred.get()
	Tempo_p = Tempo_pred.get()
	Ciclos_p = Ciclos_pred.get()
	Temperatura_p = Temperatura_pred.get()
	Humidade_p = Humidade_pred.get()
	Percurso_p = Percurso_pred.get()
	secagem_p = secagem_pred.get()
	
	try:
		Velocidade_p = float(Velocidade_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	try:
		Tempo_p = float(Tempo_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return
	
	try:
		Ciclos_p = float(Ciclos_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	try:
		Temperatura_p = float(Temperatura_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	try:
		Humidade_p = float(Humidade_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	try:
		Percurso_p = float(Percurso_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	try:
		secagem_p = float(secagem_p)
	except:
		lb_results_pred['text'] = '   Insira valores válidos.'
		return

	import pandas as pd
	from sklearn.neighbors import KNeighborsRegressor
	import numpy as np

	T_Caixa = 0
	T_Direta = 0
	T_i = secagem_p
	T_f = secagem_p
	data = pd.read_csv("bd.csv", sep=',')
	y_col = 'Espessura'
	feature_cols = [x for x in data.columns if x != y_col]
	X_data = data[feature_cols]
	y_data = data[y_col]
	knn = KNeighborsRegressor(n_neighbors = 5, weights = 'distance')
	knn = knn.fit(X_data, y_data)

	d_pred = np.array([[Velocidade_p], [Tempo_p], [Ciclos_p], [Temperatura_p], [Humidade_p], [Percurso_p], [T_Caixa], [T_Direta], [T_i], [T_f]])
	predict_data = pd.DataFrame({'Velocidade': d_pred[0], 'Tempo': d_pred[1], 'Ciclos': d_pred[2], 'Temperatura': d_pred[3],
	 'Humidade': d_pred[4], 'Percurso': d_pred[5], 'T_Caixa': d_pred[6], 'T_Direta': d_pred[7], 'T_i': d_pred[8],	'T_f': d_pred[9]})

	pred = knn.predict(predict_data)
	pred = pred.round(3)
	
	text_predresult = 'Resultado:   ' + str(pred[0]) + ' nm\n   Solução: Polivinilpirrolidona + água.\n   Concentração: 0.72 mol/L.'
	lb_results_pred['text'] = text_predresult

##########################################################################################
def simulador():
	global veloc_pred, Tempo_pred, Ciclos_pred, Temperatura_pred, Humidade_pred, Percurso_pred, secagem_pred

	janela_pred = Tk()
	janela_pred.title("Previsor de espessuras")

	lb_pred1 = Label(janela_pred, font= "TkDefaultFont 11 bold",  text='Previsor de espessuras')
	lb_pred1.place(x=87, y=20)
	lb_pred2 = Label(janela_pred, font= "TkDefaultFont 10 bold",  text='Insira os dados abaixo')
	lb_pred2.place(x=99, y=40)

	veloc_pred = Entry(janela_pred)
	veloc_pred.place(x=210, y=80)
	lb_veloc_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Velocidade (\u03BCm/s):')
	lb_veloc_pred.place(x=10, y=80)

	Tempo_pred = Entry(janela_pred)
	Tempo_pred.place(x=210, y=110)
	lb_Tempo_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Tempo de secagem (s):')
	lb_Tempo_pred.place(x=10, y=110)

	Ciclos_pred = Entry(janela_pred)
	Ciclos_pred.place(x=210, y=140)
	lb_Ciclos_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Ciclos (s):')
	lb_Ciclos_pred.place(x=10, y=140)

	Temperatura_pred = Entry(janela_pred)
	Temperatura_pred.place(x=210, y=170)
	lb_Temperatura_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Temperatura externa (°C):')
	lb_Temperatura_pred.place(x=10, y=170)

	Humidade_pred = Entry(janela_pred)
	Humidade_pred.place(x=210, y=200)
	lb_Temperatura_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Humidade do ar (%):')
	lb_Temperatura_pred.place(x=10, y=200)

	Percurso_pred = Entry(janela_pred)
	Percurso_pred.place(x=210, y=230)
	lb_Percurso_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Percurso do porta-amostras (mm):')
	lb_Percurso_pred.place(x=10, y=230)

	secagem_pred = Entry(janela_pred)
	secagem_pred.place(x=210, y=260)
	lb_secagem_pred = Label(janela_pred, font= "TkDefaultFont 8 bold",  text='Temperatura de secagem (°C):')
	lb_secagem_pred.place(x=10, y=260)

	bt_predict = Button(janela_pred,  width=40, text = "Prever espessura", command = lambda: prev_func(janela_pred))
	bt_predict.place(x=28, y=290)

	janela_pred.geometry("350x400+200+200")
	janela_pred.mainloop()

##########################################################################################
def dipcoating_aceleration():

	global bt_acelerationA, bt_acelerationA2, bt_acelerationB, bt_acelerationB2, bt_acelerationC, bt_acelerationC2
	global lb_text_janela3A, lb_text_janela3B, lb_text_janela3C, lb_text_janela3C_status, bt_enviaraccel
	global accelA, propA, tipoA, accelB, propB, tipoB, accelC, propC, tipoC, erroaccelA, erroaccelB, erroaccelC
	erroaccelA = 0
	erroaccelB = 0
	erroaccelC = 0
	janela3 = Tk()
	janela3.iconbitmap('ico.ico')

	if reconnect == 1:
		janela3.title("Módulo avançado - Dispositivo não conectado")
	elif reconnect == 0:
		janela3.title("Módulo avançado")

	######

	lb_infoacel = Label(janela3, text='Aceleração (\u03BCm/s²):')
	lb_infoacel.place(x=100, y=50)

	lb_acelerationA = Label(janela3, text='Topo:')
	lb_acelerationA.place(x=60, y=80)
	acelerationA_en = Entry(janela3)
	acelerationA_en.place(x=100, y=80)

	lb_acelerationB = Label(janela3, text='Meio:')
	lb_acelerationB.place(x=60, y=110)
	acelerationB_en = Entry(janela3)
	acelerationB_en.place(x=100, y=110)

	lb_acelerationC = Label(janela3, text='Fim:')
	lb_acelerationC.place(x=60, y=140)
	acelerationC_en = Entry(janela3)
	acelerationC_en.place(x=100, y=140)

	bt_enviaraccel = Button(janela3, text = 'Enviar valores', width=25, command = set2)
	bt_enviaraccel.place(x=60, y=170)

	######

	lb_infoacel2 = Label(janela3, text='Percentual do trajeto (%):')
	lb_infoacel2.place(x=310, y=50)

	lb_propA = Label(janela3, text='Proporção:')
	lb_propA.place(x=240, y=80)
	propA_en = Entry(janela3)
	propA_en.place(x=310, y=80)

	lb_propB = Label(janela3, text='Proporção:')
	lb_propB.place(x=240, y=110)
	propB_en = Entry(janela3)
	propB_en.place(x=310, y=110)

	lb_propC = Label(janela3, text='Proporção:')
	lb_propC.place(x=240, y=140)
	propC_en = Entry(janela3)
	propC_en.place(x=310, y=140)

	bt_simularaccel = Button(janela3, text = 'Simular movimento', width=25, command = lambda: simularaccel(1))
	bt_simularaccel.place(x=250, y=170) 

	#######

	bt_acelerationA = Button(janela3, text = "Linear", width=25, command = lambda: Aaccel('Linear', acelerationA_en.get(), propA_en.get()) ) # alterar a cor do bt
	bt_acelerationA.place(x=450, y=80)
	bt_acelerationA2 = Button(janela3, text = "Exponencial", width=25, command = lambda: Aaccel('Exponencial', acelerationA_en.get(), propA_en.get()) )
	bt_acelerationA2.place(x=645, y=80)

	bt_acelerationB = Button(janela3, text = "Linear", width=25, command = lambda: Baccel('Linear', acelerationB_en.get(), propB_en.get()) ) 
	bt_acelerationB.place(x=450, y=110)
	bt_acelerationB2 = Button(janela3, text = "Exponencial", width=25, command = lambda: Baccel('Exponencial', acelerationB_en.get(), propB_en.get()) ) 
	bt_acelerationB2.place(x=645, y=110)

	bt_acelerationC = Button(janela3, text = "Linear", width=25, command = lambda: Caccel('Linear', acelerationC_en.get(), propC_en.get()) )
	bt_acelerationC.place(x=450, y=140)
	bt_acelerationC2 = Button(janela3, text = "Exponencial", width=25, command = lambda: Caccel('Exponencial', acelerationC_en.get(), propC_en.get()) )
	bt_acelerationC2.place(x=645, y=140)

	#######

	lb_text_janela3A = Label(janela3, text='Aceleração: ' + str(accelA) + ' Proporção: ' + str(propA))
	lb_text_janela3A.place(x=450, y=170)
	lb_text_janela3B = Label(janela3, text='Aceleração: ' + str(accelB) + ' Proporção: ' + str(propB))
	lb_text_janela3B.place(x=450, y=190)
	lb_text_janela3C = Label(janela3, text='Aceleração: ' + str(accelC) + ' Proporção: ' + str(propC))
	lb_text_janela3C.place(x=450, y=210)
	lb_text_janela3C_status = Label(janela3, text='Aguardando instruções.')
	lb_text_janela3C_status.place(x=450, y=240)
	
	janela3.geometry("900x294+200+200")
	janela3.mainloop()
##########################################################################################
def set2():
	global erroaccelA, erroaccelB, erroaccelC, reconnect, aviso, ativacao, bt_enviaraccel
	global propA, propB, propC

	if reconnect != 0:
		lb_text_janela3C["text"] = 'Conectar dispositivo'
		return

	if erroaccelA == 1 or erroaccelB == 1 or erroaccelC == 1:
		lb_text_janela3C_status["text"] = 'Corrigir valores de aceleração.'
		return

	if (propA+propB+propC) != 100:
		lb_text_janela3C_status["text"] = 'Corrigir valores de poporção. Soma diferente de 100'
		return

	enviarAccel()
	if problema_valores2 == 0:
		lb_text_janela3C_status["text"] = 'Valores enviados para o dispositivo.'
		bt_enviaraccel["bg"] = 'green'
		aviso = 1
		ativacao = -1

	else:
		lb_text_janela3C_status["text"] = 'Problemas de recepção, envie os valores novamente.'
		bt_enviaraccel["bg"] = 'red'
##########################################################################################
def Aaccel(tipo,accel, prop):
	global erroaccelA, accelA, propA, tipoA
	erroaccelA = 0
	if tipo == 'Linear':
		bt_acelerationA["bg"] = 'green'
		bt_acelerationA2["bg"] = 'red'
		tipoA = 'L'
	elif tipo == 'Exponencial':
		bt_acelerationA["bg"] = 'red'
		bt_acelerationA2["bg"] = 'green'
		tipoA = 'E'
	
	try:
		accelA = float(accel)
		if accelA > -10000 and accelA < 10000:
			accelA = round(accelA, 2)
		else:
			erroaccelA = 1
			accelA = 'Valor inválido'
	except:
		erroaccelA = 1
		accelA = 'Valor inválido'

	try:
		propA = int(prop)
		if propA >= 0 and propA <= 100:
			pass
		else:
			erroaccelA = 1
			propA = 'Valor inválido'
	except:
		erroaccelA = 1
		propA = 'Valor inválido'
		
	lb_text_janela3A["text"] = 'Aceleração: ' + str(accelA) + ' Proporção: ' + str(propA)	

def Baccel(tipo,accel, prop):
	global erroaccelB, accelB, propB, tipoB
	erroaccelB = 0
	if tipo == 'Linear':
		bt_acelerationB["bg"] = 'green'
		bt_acelerationB2["bg"] = 'red'
		tipoB = 'L'
	elif tipo == 'Exponencial':
		bt_acelerationB["bg"] = 'red'
		bt_acelerationB2["bg"] = 'green'
		tipoB = 'E'
	try:
		accelB = float(accel)
		if accelB > -10000 and accelB < 10000:
			accelB = round(accelB, 2)
		else:
			erroaccelB = 1
			accelB = 'Valor inválido'
	except:
		erroaccelB = 1
		accelB = 'Valor inválido'

	try:
		propB = int(prop)
		if propB >= 0 and propB <= 100:
			pass
		else:
			erroaccelB = 1
			propB = 'Valor inválido'
	except:
		erroaccelB = 1
		propB = 'Valor inválido'
		
	lb_text_janela3B["text"] = 'Aceleração: ' + str(accelB) + ' Proporção: ' + str(propB)	

def Caccel(tipo,accel, prop):
	global erroaccelC, accelC, propC, tipoC
	erroaccelC = 0
	if tipo == 'Linear':
		bt_acelerationC["bg"] = 'green'
		bt_acelerationC2["bg"] = 'red'
		tipoC = 'L'
	elif tipo == 'Exponencial':
		bt_acelerationC["bg"] = 'red'
		bt_acelerationC2["bg"] = 'green'
		tipoC = 'E'
	try:
		accelC = float(accel)
		if accelC > -10000 and accelC < 10000:
			accelC = round(accelC, 2)
		else:
			erroaccelC = 1
			accelC = 'Valor inválido'
	except:
		erroaccelC = 1
		accelC = 'Valor inválido'

	try:
		propC = int(prop)
		if propC >= 0 and propC <= 100:
			pass
		else:
			erroaccelC = 1
			propC = 'Valor inválido'
	except:
		erroaccelC = 1
		propC = 'Valor inválido'
		
	lb_text_janela3C["text"] = 'Aceleração: ' + str(accelC) + ' Proporção: ' + str(propC)	
##########################################################################################
def enviarAccel():
	global ser, problema_valores2, accelA, accelB, accelC, propA, propB, propC, tipoA, tipoB, tipoC
	
	problema_valores2 = 0

	ini1 = ":::"
	ini2 = ":::"
	end1 = ":::"
	end2 = ":::"

	aA = int(accelA*100)
	aB = int(accelB*100)
	aC = int(accelC*100)
	
	data = []
	parametros = [aA, aB, aC]
	
	for dado in parametros:
		if dado < 0:
			dado = str(dado)[1:]
			dado = '-' + dado.zfill(6)
		else:
			dado = str(dado).zfill(7)		
		data.append(dado)

	aA = data[0]
	aB = data[1]
	aC = data[2]
	pA = str(propA).zfill(3)
	pB = str(propB).zfill(3)
	pC = str(propC).zfill(3)	
	tA = tipoA
	tB = tipoB
	tC = tipoC
	data_train = aA+aB+aC+pA+pB+pC+tA+tB+tC
	data_train_test = data_train
	data_train = ini1 + ini2 + data_train + end1 + end2
	data_train = list(data_train)
	
	############################################################## começa o envio!
	data_station = [] #Local onde serão recebidos os dados
	ser.write("A".encode())

	for x in data_train:
		ser.write(str(x).encode())

	time.sleep(0.3)
	x=0
	while(x <= (len(data_train) - len(ini1+ini2+end1+end2) - 1)):
		y = ser.readline()
		y = y.rstrip()
		try:
			y = y.decode("utf-8")
			data_station.append(y)
			x+=1
		except:
			pass

			  #SINAL			M 				  C 				D 				  U 			  .	/d 				  /c
	aA_test = data_station[0] + data_station[1] + data_station[2] + data_station[3] + data_station[4] + data_station[5] + data_station[6] 
	aB_test = data_station[7] + data_station[8] + data_station[9] + data_station[10] + data_station[11] + data_station[12] + data_station[13]
	aC_test = data_station[14] + data_station[15] + data_station[16] + data_station[17] + data_station[18] + data_station[19] + data_station[20]
			  #C 				 D   				U
	pA_test = data_station[21] + data_station[22] + data_station[23]
	pB_test = data_station[24] + data_station[25] + data_station[26]
	pC_test = data_station[27] + data_station[28] + data_station[29]
			  #Char
	tA_test = data_station[30]
	tB_test = data_station[31]
	tC_test = data_station[32]

	problema_valores2 = 1
	if aA_test == aA and aB_test == aB and aC_test == aC and pA_test == pA and pB_test == pB and pC_test == pC and tA_test == tA and tB_test == tB and tC_test == tC:
		problema_valores2 = 0			
##########################################################################################
def simularaccel(plot):

	global accelA, accelB, accelC, propA, propB, propC, tipoA, tipoB, tipoC, delay, distancia, tfinal
	import math

	if distancia == 0:
		lb_text_janela3C_status["text"] = 'Definir percurso do porta-amostras.'
		return

	if (propA + propB + propC) != 100:
		lb_text_janela3C_status["text"] = 'Corrigir valores de poporção. Soma diferente de 100'
		return

	velocidade0 = delay/1000
	v = velocidade0
	x = 3.906250/velocidade0
	t = 0
	passo = 1
	aAA = accelA/1000
	aBB = accelB/1000
	aCC = accelC/1000

	velocidades_quant = []
	tempo_quant = []
	percurso_quant = []
	accel_quant = []

	propAA = propA/100
	propBB = propB/100
	propCC = propC/100

	distanciaA = propAA*distancia
	distanciaB = propBB*distancia + distanciaA
	distanciaC = propCC*distancia + distanciaB

	#tempo_quant.append(0)
	#velocidades_quant.append(0)
	#percurso_quant.append(0)
	#accel_quant.append(0)
	######################### Parte A:

	if tipoA == 'L':
		while(passo <= distanciaA):
			
			t += (x/1000) #s
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0 + aAA*t)

			if x < 0:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)

			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			else:	
				accel_quant.append(aAA)						
			
			v = 3.906250/x  #mm/s

	if tipoA == 'E':
		while(passo <= distanciaA):
			t += (x/1000) #s
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0*math.exp(aAA*t))

			if x > 73:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			else:	
				accel_quant.append(velocidade0*aAA*math.exp(aAA*t))					
			
			v = 3.906250/x  #mm/s

	try:
		velocidade0 = v
	except:
		pass
	######################### Parte B:
	t2 = 0
	if tipoB == 'L':
		while(passo <= distanciaB):
			
			t += (x/1000) #s
			t2 += (x/1000)
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0 + aBB*t2)

			if x <= 0:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)

			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)

			else:	
				accel_quant.append(aBB)						
			
			v = 3.906250/x  #mm/s

	if tipoB == 'E':
		while(passo <= distanciaB):
			t += (x/1000) #s
			t2 += (x/1000)
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0*math.exp(aBB*t2))

			if x > 73:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			else:	
				accel_quant.append(velocidade0*aBB*math.exp(aBB*t2))					
			
			v = 3.906250/x  #mm/s

	try:
		velocidade0 = v
	except:
		pass	
	######################### Parte C:
	t2 = 0
	if tipoC == 'L':
		while(passo <= distanciaC):
			
			t += (x/1000) #s
			t2 += (x/1000)
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0 + aCC*t2)

			if x <= 0:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)				
			else:	
				accel_quant.append(aCC)						
			
			v = 3.906250/x  #mm/s		

	if tipoC == 'E':
		while(passo <= distanciaC):
			t += (x/1000) #s
			t2 += (x/1000)
			tempo_quant.append(t)
			velocidades_quant.append(v)
			percurso_quant.append(passo/256)
			
			passo += 1			
			
			x = 3.906250/(velocidade0*math.exp(aCC*t2))

			if x > 73:
				x = 73
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			elif x < 1.725:
				x = 1.725
				accel_quant.append(0)
				while(passo <= distanciaA):
					t += (x/1000) #s
					tempo_quant.append(t)
					velocidades_quant.append(v)
					percurso_quant.append(passo/256)
					passo += 1
					accel_quant.append(0)
			else:	
				accel_quant.append(velocidade0*aCC*math.exp(aCC*t2))					
			
			v = 3.906250/x  #mm/s	

	tfinal = t
	######################### PLOT:
	if plot == 1:
		import matplotlib.pyplot as pl
		pl.figure(figsize=(11, 5.7), num='Simulação da movimentação do sistema mecânico (porta-amostras)', facecolor = 'grey', edgecolor = 'grey')
		pl.subplots_adjust(top=0.96, left= 0.06, right= 0.98, wspace= 0.25)

		pl.subplot(221)
		pl.title('')
		pl.plot(tempo_quant, velocidades_quant, color='blue')
		pl.xlabel('Tempo (s)')
		pl.ylabel('Velocidade (mm/s)')
		pl.xlim(0, t)

		pl.subplot(222)
		pl.title('')
		pl.plot(percurso_quant, velocidades_quant, color='blue')
		pl.xlabel('Distância percorrida (mm)')
		pl.ylabel('Velocidade (mm/s)')
		pl.xlim(0, percurso_quant[len(percurso_quant)-1])

		pl.subplot(223)
		pl.title('')
		pl.plot(tempo_quant, percurso_quant, color='blue')
		pl.xlabel('Tempo (s)')
		pl.ylabel('Distância percorrida (mm)')
		pl.xlim(0, t)

		pl.subplot(224)
		pl.title('')
		pl.plot(tempo_quant, accel_quant, color='blue')
		pl.xlabel('Tempo (s)')
		pl.ylabel('Aceleração (mm/s²)')
		pl.xlim(0, t)

		pl.show()
	else:
		return
##########################################################################################
def ativar_aceleracao():
	global ativacao, delay, tempob, tempoev, nciclos, reconnect
	
	if reconnect != 0:
		lb_StatusGeral["text"] = "Conectar dispositivo."
		return

	if ativacao == 0:
		lb_StatusGeral["text"] = "Definir aceleração."
		return

	ser.write("K".encode()) #Definir letra!
	ativacao = ativacao*(-1)
	resposta = ler()

	if resposta == ativacao:
		pass
	else:
		ativacao = ativacao*(-1)
		lb_StatusGeral["text"] = "Ativação não confirmada.\nPor favor tente novamente."
		return

	if ativacao > 0:
		aceleracao = 'Ativada.'
		lb_ValoresPlaca["text"] = ('Valores recebidos na placa:\n  - Velocidade: ' + str(delay) + '\n' + ' - Aceleração: ' + aceleracao + '\n' + " - Tempo banho: " + str(tempob) + '\n' + ' - Tempo de evaporação: ' + str(tempoev) + '\n'  + ' - Número de ciclos: ' + str(nciclos))
		bt_aceleracao["bg"] = 'green'
		bt_aceleracao["text"] = 'Desativar aceleração'
		lb_StatusGeral["text"] = "Aceleração ativada."
	else:
		aceleracao = 'Desativada.'
		lb_ValoresPlaca["text"] = ('Valores recebidos na placa:\n  - Velocidade: ' + str(delay) + '\n' + ' - Aceleração: ' + aceleracao + '\n' + " - Tempo banho: " + str(tempob) + '\n' + ' - Tempo de evaporação: ' + str(tempoev) + '\n'  + ' - Número de ciclos: ' + str(nciclos))
		bt_aceleracao["bg"] = 'red'
		bt_aceleracao["text"] = 'Ativar aceleração'
		lb_StatusGeral["text"] = "Aceleração Desativada."
##########################################################################################
def aviso_aceleracao():
		janela_aviso = Tk()
		janela_aviso.title("Dip Coating LEe- Aviso!")
		janela_aviso.iconbitmap('ico.ico')

		lb_aviso = Label(janela_aviso, justify = CENTER, font= "TkDefaultFont 12 bold", text = 'Atenção!', foreground="red")
		lb_aviso.place(x=105, y=20)
		lb_aviso = Label(janela_aviso, justify = CENTER, text = 'Aceleração configurada, mas desativada!\nAtive caso deseje utilizá-la.')
		lb_aviso.place(x=30, y=50)

		janela_aviso.geometry("280x100+400+200")
		janela_aviso.mainloop()
##########################################################################################
##########################################################################################

### Início

conectar()
janela = Tk()
janela.iconbitmap('ico.ico')
if reconnect == 1:
	janela.title("LEe- Dip Coating - Dispositivo não conectado")
elif reconnect == 0:
	janela.title("LEe- Dip Coating")
##########################################################################################

#Labels estéticos

lb_ControlesManuais = Label(janela, font= "TkDefaultFont 10 bold", text='Controles manuais:')
lb_ControlesManuais.place(x=95, y=50)

lb_Parametros = Label(janela, font= "TkDefaultFont 10 bold",  text='Parâmetros:')
lb_Parametros.place(x=519, y=20)

lb_ProcessoAutomatico = Label(janela, font= "TkDefaultFont 10 bold",  text='Processo automático:')
lb_ProcessoAutomatico.place(x=905, y=50)

lb_Movimento = Label(janela, text='Movimento (\u03BCm/s):')
lb_Movimento.place(x=335, y=50)

lb_Velocidade = Label(janela, text='Velocidade:')
lb_Velocidade.place(x=280, y=80)

#lb_Aceleracao = Label(janela, text='Aceleração:')
#lb_Aceleracao.place(x=280, y=110)

lb_tempos = Label(janela, text='Tempos (s):')
lb_tempos.place(x=678, y=50)

lb_Banho = Label(janela, text='Banho:')
lb_Banho.place(x=580, y=80)

lb_Evaporacao = Label(janela, text='Evaporação:')
lb_Evaporacao.place(x=580, y=110)

lb_Repeticoes = Label(janela, text='Repetições (número):')
lb_Repeticoes.place(x=505, y=135)

lb_Ciclos = Label(janela, text='Ciclos:')
lb_Ciclos.place(x=430, y=160)


### Entradas

delay_en = Entry(janela)
delay_en.place(x=355, y=80)

tempob_en = Entry(janela)
tempob_en.place(x=655, y=80)

tempoev_en = Entry(janela)
tempoev_en.place(x=655, y=110)

nciclos_en = Entry(janela)
nciclos_en.place(x=505, y=160)

### Labels de Status do dispositivo

lb_StatusGeral = Label(janela, justify = LEFT, text = 'Aguardando instruções.')
lb_StatusGeral.place(x=880, y=140)

lb_ValoresPlaca = Label(janela, justify = LEFT, text= 'Valores na placa:\n - Velocidade: 0\n - Aceleração: Desativada.\n - Tempo banho: 0\n - Tempo de evaporação: 0\n - Número de ciclos: 0')
lb_ValoresPlaca.place(x=880, y=200)

lb_Mensagens = Label(janela, text='Defina as posições do porta-amostras para iniciar uma deposição')
lb_Mensagens.place(x=25, y=272)

lb_ManualStatus = Label(janela)
lb_ManualStatus.place(x=50, y=220)

### Labels Informativos de entradas

lb_delay_status = Label(janela, text='Insira um valor')
lb_delay_status.place(x=470, y=80)

#lb_accel_status = Label(janela, text='Insira um valor')
#lb_accel_status.place(x=470, y=110)

lb_tempob_status = Label(janela, text='Insira um valor')
lb_tempob_status.place(x=770, y=80)

lb_tempoev_status = Label(janela, text='Insira um valor')
lb_tempoev_status.place(x=770, y=110)

lb_nciclos_status = Label(janela, text='Insira um valor')
lb_nciclos_status.place(x=620, y=160)

### botões 																				#SERIAL KEYS: 	

bt_set = Button(janela, text = "Enviar valores", width=25, command = set1)				#ENVIAR DADOS (E) OK
bt_set.place(x=880, y=80)

bt_go = Button(janela, width=25, text = "Iniciar processo", command = go)				#INICIAR PROCESSO (G)
bt_go.place(x=880, y=110)

bt_info = Button(janela, width=25, text = "Informações", command = informar)				#//
bt_info.place(x=670, y=220)

bt_Conexao = Button(janela, width=25, text = "Conexão", command = conexao)				#//
bt_Conexao.place(x=670, y=190)

bt_Simulador = Button(janela, width=25, text = "Simulador de espessura", command = simulador)		#//
bt_Simulador.place(x=470, y=190)

bt_Simulador = Button(janela, width=25, text = "Dip Coating avançado", command = dipcoating_aceleration)		#//
bt_Simulador.place(x=470, y=220)

bt_Posicao = Button(janela, width=25, text = "Posicionar", command=posicionar)			#POSICIONAR (L) IN:-> Definir ponto A (Q) - Definir ponto B (W) OK
bt_Posicao.place(x=270, y=190)

bt_aceleracao = Button(janela, width=25, text = "Ativar aceleração", command=ativar_aceleracao)			#POSICIONAR (L) IN:-> Definir ponto A (Q) - Definir ponto B (W) OK
bt_aceleracao.place(x=270, y=220)

bt_Subir = Button(janela, width=25, text = "Subir", command=subir)						#SUBIR (S)
bt_Subir.place(x=60, y=80)

bt_Descer = Button(janela, width=25, text = "Descer", command=descer)					#DESCER (D)
bt_Descer.place(x=60, y=110)

bt_Parar = Button(janela, width=25, height=4, text = "Parar", command=parar, bg="red")	#PARAR (P)
bt_Parar.place(x=60, y=145)
##########################################################################################
janela.geometry("1120x294+110+200")
janela.mainloop()
if reconnect == 0:
	ser.close() 
##########################################################################################