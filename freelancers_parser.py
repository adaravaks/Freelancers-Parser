import time
import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import json

url_no_page_num = 'https://freelance.habr.com/freelancers?page='
user_agent = UserAgent()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User_agent': user_agent.random
}


def get_freelancers(url_no_page_num, headers):
    freelancers_list_of_dicts = []
    for page_num in range(1, 101):
        req = requests.get(url=(url_no_page_num + str(page_num)), headers=headers)
        with open(f'html_pages/{page_num}_index.html', 'w', encoding='utf8') as file:
            file.write(req.text)

        with open(f'html_pages/{page_num}_index.html', encoding='utf8') as file:
            source = file.read()

        soup = BeautifulSoup(source, 'lxml')
        freelancers_list = soup.find('ul', class_='content-list_freelancers').find_all('li', class_='content-list__item')

        for freelancer in freelancers_list:
            frlncr_dict = {}
            frlncr_broad_info = freelancer.find('article').find('div', class_='user__info')

            frlncr_name = frlncr_broad_info.find('header', class_='user-data').find('div', class_='user-data__title').find('a').text.strip()
            frlncr_dict['Имя'] = frlncr_name

            frlncr_spec = frlncr_broad_info.find('header', class_='user-data').find('div', class_='user-data__title').find('div').text.strip()
            frlncr_dict['Специализация'] = frlncr_spec

            frlncr_ratings = freelancer.find('div', class_='user_rating').find_all('a')
            frlncr_pos_rating = frlncr_ratings[0].text.strip()
            frlncr_neg_rating = frlncr_ratings[1].text.strip()
            frlncr_dict['Позитивные оценки'] = frlncr_pos_rating
            frlncr_dict['Негативные оценки'] = frlncr_neg_rating

            frlncr_price = freelancer.find('div', class_='user__price').find('span').text.strip()
            frlncr_dict['Цена'] = frlncr_price

            frlncr_description = frlncr_broad_info.find('p').text.strip().replace('\n', ' ')
            frlncr_dict['О себе'] = frlncr_description

            frlncr_dict['Проекты'] = 'Проектов нет'
            if frlncr_broad_info.find('div', class_='projects_grid'):  # If freelancer has any projects in his profile
                frlncr_projects_list = frlncr_broad_info.find('div', class_='projects_grid').find_all('a')
                frlncr_projects = []
                for project in frlncr_projects_list:
                    frlncr_projects.append(project.get('title').strip())
                frlncr_dict['Проекты'] = frlncr_projects

            frlncr_tags_list = frlncr_broad_info.find('div', class_='user__tags').find('ul').find_all('li')
            frlncr_tags = []
            for tag in frlncr_tags_list:
                frlncr_tags.append(tag.text.strip())
            frlncr_dict['Теги'] = frlncr_tags

            freelancers_list_of_dicts.append(frlncr_dict)
        print(f'{page_num} итерация завершена')
        time.sleep(2)

    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(freelancers_list_of_dicts, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_freelancers(url_no_page_num, headers)
