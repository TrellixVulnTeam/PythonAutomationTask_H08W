# pyinstaller --hidden-import=pyttsx3.drivers.sapi5 --noconfirm integrador.py

import time
from sys import platform

import schedule
from datetime import datetime

# from Geral import Notification
import Geral
from apiTrello import trello
from check_emails import Checktarefas
from win10toast import ToastNotifier


def FazerIntegracao():
    # path_icon = 'img\woman-5854291_1920.' + ('ico' if platform == 'win' else 'png')
    path_icon = 'img\woman-5854291_1920.ico'

    InitEmails = Checktarefas()
    listaGeral = InitEmails.PesquisarEmails()
    tarefas = InitEmails.Lista_emails
    # tarefas = Lista.PesquisarEmails()
    if len(tarefas) == 0:
        pass
    else:
        APITrello = trello()

        # APITrello.getMember()     # Funcionando OK (visao_geral_quadro)
        # APITrello.getCards()      # Funcionando OK (tarefas_em_Backlog)
        # APITrello.getCardID()     # Funcionando OK (consulta_tarefa_em_Backlog)
        # --- Trabalhando nisso ainda...
        # APITrello.putNewcard()
        # APITrello.putCard()
        # ---
        # APITrello.add_board('Integrados pela Saphira')  # Funcionando OK

        # APITrello.search_board('Integrados pela Saphira')  # Funcionando OK

        # Verifica se o quadro: 'Integrados pela Saphira' já existe.
        # Se já existe, pega o ID e vai para as próximas validações

        id_quadro_Integrados_Saphira = APITrello.search_board('Integrados pela Saphira', '')
        if id_quadro_Integrados_Saphira != '':
            print('Quadro já existente id: {}'.format(id_quadro_Integrados_Saphira))
        else:
            print('- Vamos criar o Quadro! - ')
            APITrello.add_board('Integrados pela Saphira')  # Funcionando OK
            id_quadro_Integrados_Saphira = APITrello.search_board('Integrados pela Saphira', '')

        data_atual = datetime.today()
        hoje = data_atual.strftime('%d/%m/%Y')  # %H:%M
        nome_lista = "Integrado em"
        nome_lista += ' ' + str(hoje)

        id_lista = APITrello.find_list(id_quadro_Integrados_Saphira, nome_lista)

        if id_lista != '':
            print('Lista de hoje já foi integrada')
        else:
            if id_quadro_Integrados_Saphira != '':
                print('- Vamos criar a lista de hoje! -')
                # OK - Funcionando corretamente - Cria a Lista de cartões do dia

                hoje = data_atual.strftime('%d/%m/%Y %H:%M')  # Data completa com o Horário
                nome_lista = "Integrado em"
                nome_lista += ' ' + str(hoje)
                id_lista = APITrello.create_new_list(nome_lista, id_quadro_Integrados_Saphira)
                if id_lista != '':
                    falaListaCriada = 'Lista do dia criada com sucesso!'
                    print('-> ' + falaListaCriada)
                    InitEmails.speak(falaListaCriada, 1, 45)
                    time.sleep(2)

                    titulo = 'Criação diária de Lista'
                    msg = 'Lista Criada: ' + nome_lista
                    nameApp = 'Integração com Trello'
                    toaster = ToastNotifier()
                    toaster.show_toast(titulo,
                                       msg,
                                       icon_path=path_icon,
                                       duration=5,
                                       threaded=True)
                    # Wait for threaded notification to finish
                    while toaster.notification_active():
                        time.sleep(0.2)

                    print('------ Notificação exibida ------')
                else:
                    print('Houve algum problema (create_new_list) - fale com o Mestre!')
            else:
                print('Houve algum problema (id_quadro_Integrados_Saphira) - fale com o Mestre!')

        # Agora será feita a criação dos cartões usando a Lista e Existente ou a Nova que foi Criada
        if id_lista != '':
            # APITrello.postNewcard(id_lista)
            if tarefas != '':
                toaster = ToastNotifier()
                for i in tarefas:
                    APITrello.postNewcard(id_lista, i)
                    titulo = i["Titulo"]
                    msg = i["Conteudo"][0:50]
                    toaster.show_toast(titulo,
                                       msg,
                                       icon_path=path_icon,
                                       duration=10,
                                       threaded=True)
                    # Wait for threaded notification to finish
                    while toaster.notification_active():
                        time.sleep(0.2)
            if len(tarefas) > 1:
                msg_saphira = str(len(tarefas)) + ' tarefas foram importadas'
            else:
                msg_saphira = str(len(tarefas)) + ' tarefa foi importada'
            Geral.voz_saphira.speak(ptext=msg_saphira, pnrate=50)
            tarefas = ''
        else:
            # print('Houve algum problema (postNewcard) - fale com o Mestre!')
            msg_saphira = 'Nenhuma tarefa foi importada'
            Geral.voz_saphira.speak(ptext=msg_saphira, pnrate=50)


# Faz a integração e depois repete a cada 60 minutos
FazerIntegracao()
# Executa a cada 60 minutos (faz a conexão com o G-mail e realiza a importação das Novas tarefas para o Trello)
schedule.every(60).minutes.do(FazerIntegracao)
while True:
    schedule.run_pending()
    time.sleep(1)
