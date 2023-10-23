import os
import time

import requests


BASE_URL = 'https://www.1secmail.com/api/v1/'


def generate_mails(count=1):
    work_url = f'{BASE_URL}?action=genRandomMailbox&count={count}'
    r = requests.get(work_url).json()
    return r[0]


def check_mail(email: str):
    # Разбиваем email на имя пользователя и домен
    username, domain = email.split('@')

    # Формируем URL для запроса сообщений
    work_url = f'{BASE_URL}?action=getMessages&login={username}&domain={domain}'

    # Отправляем GET-запрос и получаем ответ в формате JSON
    r = requests.get(work_url).json()

    # Проверяем количество сообщений
    count_mail = len(r)

    if count_mail == 0:
        print('[INFO] Почтовый ящик пуст!')
    else:
        mails = []

        for i in r:
            # Используем метод items() для итерации по ключам и значениям словаря
            for k, v in i.items():
                if k == 'id':
                    mails.append(v)
        print(f'[+] У вас {count_mail} сообщений!')

        # Создаем директорию для сохранения почты, если её нет
        final_dir = os.path.join(os.getcwd(), 'mails')
        os.makedirs(final_dir, exist_ok=True)

        for i in mails:
            # Формируем URL для чтения сообщения
            read_msg = f'{BASE_URL}?action=readMessage&login={username}&domain={domain}&id={i}'
            r = requests.get(read_msg).json()

            sender = f'Отправитель: {r.get("from")}'
            subject = f'Тема: {r.get("subject")}'
            date = f'Дата: {r.get("date")}'
            text = f'Текст: {r.get("textBody")}'
            attachments = r.get('attachments')
            download_link = ''

            if attachments:  # Проверяем наличие вложений
                download_link = f'Ссылка для скачивания: {BASE_URL}?action=download&login={username}&domain={domain}&id={i}&file={attachments[0]["filename"]}'

            mail_file_path = os.path.join(final_dir, f'{i}.txt')
            gen_mail_lines = [
                sender,
                subject,
                date,
                text,
                download_link
            ]
            with open(mail_file_path, 'w', encoding='UTF-8') as file:
                for line in gen_mail_lines:
                    file.write(f'{line}\n')


def delete_mail(email):
    url = 'https://www.1secmail.com/mailbox'
    username, domain = email.split('@')
    data = {
        'action': 'deleteMailbox',
        'login': f'{username}',
        'domain': f'{domain}'
    }
    r = requests.post(url=url, data=data)
    print(f'[X] Почтовый адрес {email} - удален!')

def main():
    try:
        mail = generate_mails(1)
        print(mail)

        while True:
            check_mail(mail)
            time.sleep(15)
    except(KeyboardInterrupt):
        print('Давай пока!!!')
        delete_mail(mail)


if __name__ == '__main__':
    main()
