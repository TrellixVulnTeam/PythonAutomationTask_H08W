import json
import json as js

import requests


class trello:

    # Criando a classe da API do Trello
    # utiliza o token que criei manualmente
    def __init__(self):
        self.key = 'd4b335be9dcbd55a5aa4831868d8cea7'
        self.token = 'b9852e24e3ce4d711b980ce5f9e0f4bb7940300db2cc2e2291136efcee97109a'
        self.board = '5f51478b0c68d72b6fd23471'  # - Todas as Tarefas -Estavam em Backlog?
        self.limit = 200

        self.auth = {'key': self.key,
                     'token': self.token}
        self.url = "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application/json"
        }

    # Grava um arquivo Json com o resultado/retorno da consulta na API
    def escrever_json(self, lista, nomearq):
        with open('data\\' + nomearq + '.json', 'w') as f:
            # json.dump(lista, f)
            # comentado para testes abaxo json.dump(lista, f, sort_keys=True, indent=4)
            json.dump(lista, f, sort_keys=True, indent=4, separators=(",", ": "))

    # Retorna as principais informações do Quadro: "- Todas as Tarefas -Estavam em Backlog?"
    def getBoard(self):
        url = "https://api.trello.com/1/boards/" + self.board

        querystring = {"actions": "all", "boardStars": "none", "cards": "none", "card_pluginData": "false",
                       "checklists": "none", "customFields": "false",
                       "fields": "name,desc,descData,closed,idOrganization,pinned,url,shortUrl,prefs,labelNames",
                       "lists": "open", "members": "none", "memberships": "none", "membersInvited": "none",
                       "membersInvited_fields": "all", "pluginData": "false", "organization": "false",
                       "organization_pluginData": "false", "myPrefs": "false", "tags": "false", "key": self.key,
                       "token": self.token}

        response = requests.request("GET", url, params=querystring)

        print(response.text)

    # Lista todas as tarefas para o quadro “- Todas as Tarefas -Estavam em Backlog?”
    def getCards(self):
        url = 'https://api.trello.com/1/boards/' + self.board + '/cards/?limit=' + str(
            self.limit) + '&fields=name&members=true&member_fields=fullName&key=' + self.key + '&token=' + self.token

        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }

        call = requests.get(url, headers=headers)
        dic = js.loads(call.text)
        self.escrever_json(dic, 'tarefas_em_Backlog')

        print(dic)

    # Detalhamento da tarefa
    def getCardID(self):
        """
        "id": "5f525bc935da213f6bd05973",
        "members": [],
        "name": "170591-Erro de Serial no processo de estorno de notas"
        """

        self.idCard = '5f525bc935da213f6bd05973'

        url = 'https://trello.com/1/boards/{0}/cards/{1}?key={2}&token={3}'.format(self.board, self.idCard, self.key,
                                                                                   self.token)

        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }

        call = requests.get(url, headers=headers)
        dic = js.loads(call.text)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        self.escrever_json(dic, 'consulta_tarefa_em_Backlog')
        print(json.dumps(json.loads(dic), sort_keys=True, indent=4, separators=(",", ": ")))

        # print(dic)

    # Pessoas que estão alocadas em uma determinada tarefa
    def getMember(self):
        self.member = '5dd284b9baf8127a4f2cac82'

        url = "https://api.trello.com/1/members/" + self.member

        querystring = {"boardBackgrounds": "none", "boardsInvited_fields": "name,closed,idOrganization,pinned",
                       "boardStars": "false", "cards": "none", "customBoardBackgrounds": "none", "customEmoji": "none",
                       "customStickers": "none", "fields": "all", "organizations": "none", "organization_fields": "all",
                       "organization_paid_account": "false", "organizationsInvited": "none",
                       "organizationsInvited_fields": "all", "paid_account": "false", "savedSearches": "false",
                       "tokens": "none", "key": self.key, "token": self.token}

        response = requests.request("GET", url, params=querystring)

        print(response.text)
        self.escrever_json(response.text, 'visao_geral_quadro')

        # Pessoas que estão alocadas em uma determinada tarefa

    def postNewcard(self, id_list, desc_tarefa):
        # This code sample uses the 'requests' library:
        # http://docs.python-requests.org

        url = "https://api.trello.com/1/cards"

        nome_ativ = desc_tarefa["Titulo"]
        descricao_ativ = desc_tarefa["Conteudo"]

        query = {
            "key": self.key,
            "token": self.token,
            # 'idList': '60243b824ac00d58fc2d6f5b',
            "idList": id_list,
            "name": nome_ativ,
            "desc": descricao_ativ
        }

        response = requests.request(
            "POST",
            url,
            params=query
        )

        # print(response.text)
        self.escrever_json(response.text, 'Nova_tarefa_em_Backlog')

    # Não alterar essa rotina
    def add_board(self, board_name):
        "Add board using board name"
        result_flag = False
        self.payload = self.auth.copy()
        self.payload['name'] = board_name
        self.payload['defaultLists'] = "false"
        url = self.url + "/boards/"
        response = requests.post(url=url, data=self.payload)
        if response.status_code == 200:
            result_flag = True

        return result_flag

    def search_board(self, me_procura, id_board):

        url = "https://api.trello.com/1/search"

        if id_board != '':
            querystring = {"query": me_procura,
                           "key": self.key,
                           "token": self.token,
                           "idBoard": id_board
                           }
        else:
            querystring = {"query": me_procura,
                           "key": self.key,
                           "token": self.token
                           }

        response = requests.request("GET", url, params=querystring)
        # print(response)
        board_id = ""
        print(response.json())
        if response.json()["boards"]:
            board_id = response.json()["boards"][0]["id"]
            print('ID da Board {0} = {1}'.format(me_procura, board_id))
        return board_id

    def create_new_list(self, nome_lista, id_board):
        url = "https://api.trello.com/1/lists"

        query = {"query": nome_lista,
                 "key": self.key,
                 "token": self.token,
                 "name": nome_lista,
                 "idBoard": id_board
                 }

        response = requests.request("POST", url, params=query)

        if response.status_code == 200:
            if response.json()["id"]:
                list_id = response.json()["id"]
                print('ID da Lista {0} = {1}'.format(nome_lista, list_id))
                return list_id
            else:
                return ''
        else:
            return ''

    def find_list(self, id_board, list_name):
        """ Return list specified by board_name/list_name"""
        url = "https://api.trello.com/1/boards/" + id_board + "/lists"

        query = {"key": self.key,
                 "token": self.token,
                 "filter": "open"
                 }

        headers = {
            "Accept": "application/json"
        }

        response = requests.request("GET", url, headers=headers, params=query)

        # print(response)
        board_id = ""
        # print(response.json())
        if response.status_code == 200:
            print(response.json())
            dic = js.loads(response.text)
            if response.json():
                id_lista = dic[0]["id"]
                nome_lista = dic[0]["name"][:23]  # Nome da lista sem o horário
                if id_lista != '':
                    if nome_lista == list_name:
                        print('ID da Lista {0} = {1}'.format(list_name, id_lista))
                        return id_lista
                    else:
                        return ''
                else:
                    return ''
            else:
                return ''
        else:
            return ''
