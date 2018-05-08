# 1. с сайта Курсеры взять 20 курсов; +
# 2. со страницы каждого курса взять его х-ки: название, язык, дата начала,
# кол-во недель, средняя оценка;
# 3. Загрузить данные по каждому курсу в файл xlsx.
import requests
from bs4 import BeautifulSoup
import random


def get_console_arguments():
    pass


def download_course_info(courses_info_url):
    print('send request...')
    coursera_response = requests.get(courses_info_url)
    course_info = coursera_response.text
    print('get response')
    return course_info


def get_links_of_random_courses(xml_info_string, coursers_number):
    bs_object = BeautifulSoup(xml_info_string, 'lxml')
    course_links_with_tags = bs_object.find_all('loc')
    random_links_with_tags = random.sample(
        course_links_with_tags,
        coursers_number
    )
    links_of_random_courses = [
        link_with_tags.get_text() for link_with_tags in random_links_with_tags
    ]
    return links_of_random_courses


def get_course_info(page):
    bs_object = BeautifulSoup(page, 'html.parser')
    course_title = bs_object.find(
        'h1',
        class_='title display-3-text'
    ).get_text()
    language = bs_object.find('div', class_='rc-Language').get_text()
    start_date = bs_object.find('div', id='start-date-string').get_text()
    try:
        week_items = bs_object.find('div', class_='rc-WeekView').contents
        weeks_number = len(week_items)
    except AttributeError:
        weeks_number = None
    course_mean_mark = bs_object.find(
        'div',
        class_='ratings-text bt3-hidden-xs'
    ).span.get_text()
    return course_title, language, start_date, weeks_number, course_mean_mark


def get_all_courses_info(courses_links):
    course_list = []
    for course_link in courses_links:
        course_page = download_course_info(course_link)
        course_info = get_course_info(course_page)
        course_list.append(course_info)
    return course_list


def output_courses_info_to_xlsx(path, courses_info):
    pass


if __name__ == '__main__':
    # args = get_console_arguments()
    # file_path = args.file_path
    coursera_info_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    # courses_string_info = download_course_info(coursera_info_url)
    with open('courses.xml', 'r') as xml_file:
        courses_string_info = xml_file.read()
    number_of_coursers = 2
    list_of_course_links = get_links_of_random_courses(
        courses_string_info,
        number_of_coursers
    )
    print(list_of_course_links)
    all_courses_info = get_all_courses_info(list_of_course_links)
    print(all_courses_info)
    file_path = None
    output_courses_info_to_xlsx(file_path, all_courses_info)
