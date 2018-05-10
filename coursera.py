import requests
from bs4 import BeautifulSoup
import random
from openpyxl import Workbook
import argparse


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--output_file_path',
        help='Enter the full path of output file or its name only.'
    )
    arguments = parser.parse_args()
    return arguments


def download_course_info(courses_info_url):
    print('send request...')
    coursera_response = requests.get(courses_info_url)
    course_info = coursera_response.text
    print('got response')
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


def get_course_info_from_html(page):
    bs_object = BeautifulSoup(page, 'html.parser')
    course_title = bs_object.find(
        'h1',
        class_='title display-3-text'
    ).get_text()
    language = bs_object.find('div', class_='rc-Language').get_text()
    start_date = bs_object.find('div', id='start-date-string').get_text()
    week_items = bs_object.find('div', class_='rc-WeekView')
    if week_items:
        weeks_number = len(week_items.contents)
    if not week_items:
        weeks_number = None
    course_mark_html_item = bs_object.find(
            'div',
            class_='ratings-text headline-2-text'
        )
    if course_mark_html_item:
        course_mean_mark = course_mark_html_item.span.get_text()
    if not course_mark_html_item:
        course_mean_mark = None
    course_info_dict = {
        'course_title': course_title,
        'course_language': language,
        'course_start_date': start_date,
        'course_duration': weeks_number,
        'course_mean_mark': course_mean_mark
    }
    return course_info_dict


def get_all_courses_list(courses_links):
    course_list = []
    for course_link in courses_links:
        course_page = download_course_info(course_link)
        course_info = get_course_info_from_html(course_page)
        course_list.append(course_info)
    return course_list


def set_column_names(table):
    column_names = [
        'Course Name', 'Language', 'Start Date', 'Weeks Number', 'Course Mean Mark'
    ]
    table.append(column_names)


def set_course_info(table, course_dict):
    course_title = course_dict['course_title']
    course_language = course_dict['course_language']
    course_start_date = course_dict['course_start_date']
    course_duration = course_dict['course_duration']
    course_mean_mark = course_dict['course_mean_mark']
    course_features = (
        course_title,
        course_language,
        course_start_date,
        course_duration,
        course_mean_mark,
    )
    table.append(course_features)


def get_output_path(file_path):
    if not file_path:
        return 'courses_info.xlsx'
    return file_path


def output_courses_info_to_xlsx(path, courses_info):
    workbook = Workbook()
    worksheet = workbook.active
    set_column_names(worksheet)
    for course in courses_info:
        set_course_info(worksheet, course)
    output_file_path = path
    if not output_file_path:
        output_file_path = 'courses_info.xlsx'
    workbook.save(output_file_path)


if __name__ == '__main__':
    number_of_coursers = 20
    coursera_info_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    console_arguments = get_console_arguments()
    file_path = console_arguments.output_file_path
    courses_xml_info = download_course_info(coursera_info_url)
    list_of_course_links = get_links_of_random_courses(
        courses_xml_info,
        number_of_coursers
    )
    all_courses_info = get_all_courses_list(list_of_course_links)
    output_courses_info_to_xlsx(file_path, all_courses_info)
