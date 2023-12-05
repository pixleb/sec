from .basic_mailer import Main

class NotifyUser:
    def __init__(self, receiver: str, password: str) -> None:
        self.subject: str = 'Получение пользовательского доступа к панели WeWatch'
        self.text: str = f'''
            Ваш пароль от пользовательской панели WeWatch: {password}
        '''
        Main().send_mail(receiver, self.subject, self.text)
