import os
import time

import requests


BASE_URL = 'https://www.1secmail.com/api/v1/'


def generate_mails(count=1):
    work_url = f'{BASE_URL}?action=genRandomMailbox&count={count}'
    r = requests.get(work_url).json()
    return r[0]


def check_mail(email: str):
    username, domain = email.split('@')
    work_url = f'{BASE_URL}?action=getMessages&login={username}&domain={domain}'
    r = requests.get(work_url).json()
    count_mail = len(r)

    if count_mail == 0:
        print('[INFO] Почтовый ящик пуст!')
    else:
        mails = []

        for i in r:
            for k, v in i.items():
                if k == 'id':
                    mails.append(v)
        print(f'[+] У вас {count_mail} сообщений!')

        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, 'mails')

        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        for i in mails:
            read_msg = f'{BASE_URL}?action=readMessage&login={username}&domain={domain}&id={i}'
            print(read_msg)
            r = requests.get(read_msg).json()

            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            text = r.get('textBody')
            attachments = r.get('attachments')
            if attachments != 0:
                download_link = (f'{BASE_URL}?action=download&login={username}&domain={domain}&id={i}&file={attachments[0]["filename"]}')
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


def main():
    mail = generate_mails(1)
    print(mail)

    while True:
        check_mail(mail)
        time.sleep(15)


if __name__ == '__main__':
    main()
