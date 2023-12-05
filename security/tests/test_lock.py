import requests

print('Начинаем запрос...')

http_to = 'http://127.0.0.1:8000/post_lock/'

mac = 'test'
status = 0
power = 45 

print('Целевой адрес: %s' % http_to)
print('MAC адрес: %s' % mac)
print('Статус: %s' % status)
print('Заряд: %s' % power)

r = requests.post(
    http_to, 
    json = {
        'mac': mac,
        'status': status,
        'power': power
    }
)
print('Ответ сервера: ', r.text)
