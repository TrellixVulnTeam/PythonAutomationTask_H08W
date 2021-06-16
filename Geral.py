from datetime import time
import time

import pyttsx3
from plyer import notification
from plyer.utils import platform

from unicodedata import normalize


class voz_saphira:
    def speak(ptext, pidvoz=1, pnrate=200):
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
        engine.say(ptext)
        engine.runAndWait()


class TextUtil:
    """
    Classe com métodos para tratamento de texto
    """

    def removerCaracteresEspeciais(self, text):
        """
        Método para remover caracteres especiais do texto
        """
        return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

class Notification:

    # def notify(self, titulo, msg, nomeapp, tempo=7, alerta_simples=True, path_icon=''):
    def notify(self, title='', message='', app_name='', app_icon='',
               timeout=10, ticker='', toast=False):
        """
        Parameters:

        title (str) – Title of the notification
        message (str) – Message of the notification
        app_name (str) – Name of the app launching this notification
        app_icon (str) – Icon to be displayed along with the message
        timeout (int) – time to display the message for, defaults to 10
        ticker (str) – text to display on status bar as the notification arrives
        toast (bool) – simple Android message instead of full notification
        """
        return notify(self,
            title=title, message=message,
            app_icon=app_icon, app_name=app_name,
            timeout=timeout, ticker=ticker, toast=toast
        )
