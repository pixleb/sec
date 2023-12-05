from .basic_mailer import Main

class NotifyAdmin:
    def __init__(self, receiver: str, password: str) -> None:
        self.subject: str = 'Получение админ-доступа к панели WeWatch'
        self.text: str = f'''
            Ваш пароль от админ-панели WeWatch: {password}
        '''
        Main().send_mail(receiver, self.subject, self.text)
