import datetime
import email
import imaplib
import json
import os
import time

import pyttsx3


# from datetime import datetime
# Reconhecimento de voz e Sintetização de voz


class Checktarefas:
    Lista_emails = []

    def __init__(self):
        data_atual = datetime.date.today()
        hoje = data_atual.strftime('%d/%m/%Y')  # %H:%M

        # gravação de logs
        nome_operacao = 'Iniciando a verificação da SAPHIRA' + ' ' + str(hoje)
        self.escrever_log(nome_operacao)

        # falainicial = 'verificação programada da SAPHIRA. Vou verificar os e-mails e integrar as Tarefas'
        falainicial = 'Verificação programada da SAPHIRA.'
        self.speak(falainicial, 1, 45)
        # time.sleep(2)
        # falainicial = 'Vou verificar os e-mails e integrar as Tarefas'
        # self.speak(falainicial, 1, 45)

        EMAIL = 'masilva.arcs@gmail.com'
        PASSWORD = 'qgfmayjkjndeeuat'  # -- Senha de app que foi gerada para a SAPHIRA
        SERVER = 'imap.gmail.com'
        Checktarefas.Lista_emails = []

        pasta = os.path.abspath(os.path.dirname(__file__)) + '\data'
        if os.path.isdir(pasta):  # vendo se este diretorio ja existe
            # gravação de logs
            nome_operacao = 'Pasta ' + pasta + ' Ja existe no caminho' + ' ' + str(hoje)
            pass
        else:
            os.mkdir(pasta)  # aqui criamos a pasta caso nao exista
            print('Pasta ' + pasta + ' criada com sucesso!')

            # gravação de logs
            nome_operacao = 'Pasta ' + pasta + ' criada com sucesso em' + ' ' + str(hoje)

        self.escrever_log(nome_operacao)

        # abriremos uma conex�o com SSL com o servidor de emails
        # logando e navegando para a inbox
        self.mail = imaplib.IMAP4_SSL(SERVER)
        self.mail.login(EMAIL, PASSWORD)
        # selecionamos a caixa de entrada neste caso
        # mas qualquer outra caixa pode ser selecionada
        self.mail.select('inbox')

        # gravação de logs
        nome_operacao = 'self_mail_select(_inbox_) em' + ' ' + str(hoje)
        self.escrever_log(nome_operacao)

        if self.mail.state == 'SELECTED':
            # self.speak('Tive de fazer umas coisinhas antes', 1, 45)
            # time.sleep(1)
            # falaConexaoEmail = 'Estou agora conectada com o Servidor de E-mails!'
            # print('-- ' + falaConexaoEmail + '--')
            # self.speak(falaConexaoEmail, 1, 45)
            # time.sleep(2)

            # gravação de logs
            nome_operacao = 'Conectou com E-mail em' + ' ' + str(hoje)
            self.escrever_log(nome_operacao)

    def escrever_json(self, lista):
        with open('data\\tarefas.json', 'w', encoding='iso-8859-1') as f:
            json.dump(lista, f)

    def carregar_json(arquivo):
        with open('data\\tarefas.json', 'r', encoding='iso-8859-1') as f:
            return json.load(f)

    def escrever_txt(self, lista):
        with open('data\\tarefas.txt', 'w', encoding='utf-8') as f:
            for nome in lista:
                f.write(nome + '\n')

    def escrever_log(self, lista):
        with open('data\\processos_log_a.txt', 'w', encoding='utf-8') as f:
            for nome in lista:
                f.write(nome + '\n')

    def carregar_txt(self):
        with open('data\\tarefas.txt', 'r', encoding='utf-8') as f:
            return f.readlines()

    def speak(self, ptext, pidvoz, pnrate):
        # Sintese de fala
        # engine = pyttsx3.init()
        engine = pyttsx3.init(driverName='sapi5')
        rate = engine.getProperty('rate')

        if pnrate == 200:
            engine.setProperty('rate', pnrate)
        else:
            engine.setProperty('rate', rate - pnrate)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[pidvoz].id)
        engine.say(str(ptext))
        engine.runAndWait()

    def PesquisarEmails(self):
        try:
            data_atual = datetime.date.today()
            hoje = data_atual.strftime('%d/%m/%Y')  # %H:%M

            # EMAIL = 'masilva.arcs@gmail.com'
            # PASSWORD = 'qgfmayjkjndeeuat'  # -- Senha de app que foi gerada para a SAPHIRA
            # SERVER = 'imap.gmail.com'
            # Considerando pegar os últimos 5 dias para pesquisa das datas
            # datapesq = (datetime.date.today() - datetime.timedelta(5)).strftime("%d-%b-%Y")

            # Considerando pegar os �ltimos 10 dias para pesquisa das datas
            datapesq = (datetime.date.today() - datetime.timedelta(10)).strftime("%d-%b-%Y")

            # abriremos uma conexão com SSL com o servidor de emails
            # logando e navegando para a inbox
            # mail = imaplib.IMAP4_SSL(SERVER)
            # mail.login(EMAIL, PASSWORD)
            # selecionamos a caixa de entrada neste caso
            # mas qualquer outra caixa pode ser selecionada
            # mail.select('inbox')

            # faremos uma busca com o critério ALL para pegar
            # todos os emails da inbox, esta busca retorna
            # o status da operação e uma lista com
            # os ids dos emails
            # ------ Comentado para testes - Marcos status, data = mail.search(None, 'ALL')
            # status, data = mail.search(None, 'UNSEEN', '(FROM "Marcos Santos da Silva" SUBJECT "Planilha")')
            status, data = self.mail.search(None,
                                            'UNSEEN',
                                            # '(SENTSINCE {0})'.format(datapesq),
                                            '(FROM {0} SUBJECT "##Tarefa:")'.format("masilva.arcs@gmail.com".strip()))
            ids = data[0].split()
            dadosEmails = data

            # data � uma lista com ids em blocos de bytes separados
            # por espa�o neste formato: [b'1 2 3', b'4 5 6']
            # ent�o para separar os ids primeiramente criaremos
            # uma lista vazia
            mail_ids = []
            unread = []
            # e em seguida iteramos pelo data separando os blocos
            # de bytes e concatenando a lista resultante com nossa
            # lista inicial
            for block in data:
                # a função split chamada sem nenhum par�metro
                # transforma texto ou bytes em listas usando como
                # ponto de divis�o o espa�o em branco:
                # b'1 2 3'.split() => [b'1', b'2', b'3']
                mail_ids += block.split()

            qtde_emails = len(mail_ids)
            # agora para cada id baixaremos o email
            # e extrairemos seu conte�do
            for num in mail_ids:
                # a função fetch baixa o email passando id e o formato
                # em que voc� deseja que a mensagem venha
                status, data = self.mail.fetch(num, '(RFC822)')

                # data no formato '(RFC822)' vem em uma lista com a
                # tupla onde o conte�do est� e o byte de fechamento b')'
                # por isso vamos iterar pelo data extraindo a tupla
                for response_part in data:
                    # se for a tupla a extra�mos o conte�do
                    if isinstance(response_part, tuple):
                        # o primeiro elemento da tupla � o cabe�alho
                        # de formatação e o segundo elemento possu� o
                        # conte�do que queremos extrair
                        # Comentado para testes de acentuação message = email.message_from_bytes(response_part[1])
                        # message = self.parse_message(self, response_part[1])
                        message = email.message_from_bytes(response_part[1])
                        mail_from = message['from']
                        mail_subject = message['subject']
                        # se o conte�do for texto text/plain que � o
                        # texto puro n�s extra�mos

                        # Faz a marcação de leitura do e-mail processado
                        unread.append(email.message_from_bytes(response_part[1]))
                        self.mail.store(num, '+FLAGS', '\\Seen')

                        # agora para o texto do email precisamos de um
                        # pouco mais de trabalho pois ele pode vir em texto puro
                        # ou em multipart, se for texto puro � s� ir para o
                        # else e extra�-lo do payload, caso contr�rio temos que
                        # separar o que � anexo e extrair somente o texto
                        if message.is_multipart():
                            mail_content = ''

                            # no caso do multipart vem junto com o email
                            # anexos e outras vers�es do mesmo email em
                            # diferentes formatos como texto imagem e html
                            # para isso vamos andar pelo payload do email
                            msg = ''
                            for part in message.get_payload():
                                if part.get_content_type() == 'multipart/alternative':

                                    mail_content = part.get_payload()

                                elif part.get_content_type() == 'text/plain':
                                    # se o conte�do for texto text/plain que � o
                                    # texto puro n�s extra�mos

                                    mail_content += part.get_payload()

                                elif part.get_content_type() == 'image/png':
                                    pass
                                else:
                                    bytes = part.get_payload(decode=True)
                                    charset = part.get_content_charset('iso-8859-1')
                                    # charset = part.get_content_charset('utf-8')
                                    msg = bytes.decode(charset, 'replace')
                                    if type(msg) is bytes:
                                        msg = str(msg)
                                    print(msg)
                        # message.is_multipart() = False
                        # A Saphira-Tarefador foi ajustado para enviar somente como texto normal/formatado(Markdown).
                        else:
                            msg = ''
                            mail_content = ''
                            bytes = message.get_payload(decode=True)
                            charset = message.get_content_charset('iso-8859-1')
                            # charset = message.get_content_charset('utf-8')
                            msg = bytes.decode(charset, 'replace')
                            if type(msg) is bytes:
                                msg = str(msg)
                                print(msg)
                                mail_content += msg
                            else:
                                if msg != '':
                                    mail_content += msg
                                else:
                                    mail_content += message.get_payload()

                        # Exemplo:
                        #       <ID> 1235478 - Teste de inclus�o de tarefa e envio de e-mail - Com acentuação</ID>
                        # Montagem do Assunto (isso pode mudar dependendo de onde foi enviado o e-mail)
                        # testes = 'Montagem do Assunto (isso pode mudar dependendo de onde foi enviado o e-mail)'
                        # testes += '<ID> 1235478 - Teste de inclus�o de tarefa e envio de e-mail - Com acentuação</ID>'
                        montagem = mail_content
                        pos1 = montagem.find('<ID> ')
                        pos2 = montagem.find('</ID>')
                        if pos1 > 0 and pos2 > 0:
                            pos1 += 5
                        assunto = montagem[pos1:pos2]
                        nome = mail_from.split(' <')
                        email_de_nome_pessoa = nome[0].strip()
                        email_de = nome[1][:-1].strip()  # pega o e-mail (precisa tirar o �ltimo caracter pois � ">"

                        # Exclui do conte�do do card o t�tulo da tarefa. Fiz desta forma pra evitar o controle dos
                        # espa�os em branco
                        conteudo = mail_content.replace(assunto, '')
                        conteudo = conteudo.replace('<ID>', '')
                        conteudo = conteudo.replace('</ID>', '').strip()

                        # gravação de logs
                        nome_operacao = 'mail_from: ' + mail_from + ' ' + str(hoje)
                        nome_operacao += '\n' + 'email_de_nome_pessoa: ' + email_de_nome_pessoa
                        nome_operacao += '\n' + 'email_de: ' + email_de
                        self.escrever_log(nome_operacao)

                        # nomeaplicativo = 'Verificador de E-mails'
                        minha_tarefa = {"Titulo": assunto,
                                        "De": email_de_nome_pessoa,
                                        "E-mail": email_de,
                                        "Conteudo": conteudo}

                        # self.escrever_json(self, minha_tarefa)
                        Checktarefas.Lista_emails.append(minha_tarefa)

                        # gravação de logs
                        # nome_operacao = 'Checktarefas.Lista_emails.append(minha_tarefa): ' \
                        #                + str(minha_tarefa) + ' ' + str(hoje)
                        # self.escrever_log(nome_operacao)

                        # print('Esse � o E-mail {}'.format(qtde_emails))
                        # print(f'From: {mail_from}')
                        # print(f'Subject: {mail_subject}')
                        # O conte�do n�o interessa num primeiro momento, pois a Saphira ir� ler Quem enviou e o Assunto.
                        # print(f'Content: {mail_content}')
        finally:
            data_atual = datetime.date.today()
            hoje = data_atual.strftime('%d/%m/%Y')  # %H:%M

            if self.mail.state == 'SELECTED':
                self.mail.close()
                print('-- Verificação de E-mails encerrada! --')

                # gravação de logs
                nome_operacao = 'Verificação de E-mails encerrada' + ' ' + str(hoje)
                self.escrever_log(nome_operacao)

            if self.mail.state != 'LOGOUT':
                self.mail.logout()
                print('-- Encerrou a conexão com a conta de E-mail! --')

                # gravação de logs
                nome_operacao = 'Realizei o Logout da conta de E-mail' + ' ' + str(hoje)
                self.escrever_log(nome_operacao)

            fala_1 = 'Verificação de E-mails encerrada.'
            # fala_2 = 'Encerrei a conex�o com a conta de E-mail!'
            self.speak(fala_1, 1, 45)
            # time.sleep(2)
            # self.speak(fala_2, 1, 45)
            # Faz a gravação do Json para o controle das importa��es
            self.escrever_json(Checktarefas.Lista_emails)

            # gravação de logs
            # nome_operacao = 'gravação do Json para o controle das importa��es' + ' ' + str(hoje)
            # self.escrever_log(nome_operacao)
