import bs4
import requests
from colorama import Fore
from jarviscli import entrypoint


@entrypoint
def __call__(self, jarvis, s):
    """
    Runs a basic search and returns the default answer provided by google.
    Google's default answers all have a class contaning BNeawe, s3v9rd, or
    orAP7Wnd, so we can just run a google query and parse the results

    example: google What is the Large Hadron Collider?
    """
    jarvis.say(search(s), Fore.BLUE)


def search(question):
    query = '+'.join(question.split(' '))
    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    google_answers = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})
    for answer in google_answers:
        if answer.text:
            return parse_result(answer.text)

    first_answers = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})
    for answer in first_answers:
        if answer.text:
            return parse_result(answer.text)

    all_div = soup.find_all("div")
    google_answer_keys = ['BNeawe', 's3v9rd', 'AP7Wnd', 'iBp4i']

    for div in all_div:
        for key in google_answer_keys:
            if key in div:
                return parse_result(div.text)

    return 'No Answers Found'


def parse_result(result):
    result = result.split('\n')[0]
    if result.endswith('Wikipedia'):
        result = result[:result.find('Wikipedia')]
    result += '\n'

    return result
