from bs4 import BeautifulSoup
import requests
import json
import re
import typing as tp

# constants
search_words = ["scala", "data engineer", "python"] #sys.argv
link = 'https://hh.ru/search/vacancy?text={}&area=1&search_field=name&page={}'
vacancies = []

def filter_with_block_set(words, block_set):
    return list(set.difference(words, block_set))

def _scrap_url(url: str) -> requests.models.Response:
    print('next_page:\t', url)

    # work with parser
    headers = {"User-Agent":"Mozilla/5.0"}
    return requests.get(url = str(url), headers=headers)

def parse_vacancy_description(link:str) -> tp.Union[None, tp.List[str]]:
    # work with parser
    response = _scrap_url(link)
    soup = BeautifulSoup(response.content, "html.parser")
    vacancy_description = soup.select_one('div[data-qa=vacancy-description]').text
    vacancy_words = re.sub(r'[^a-z]', ' ', vacancy_description, flags=re.IGNORECASE).split(' ')
    skills_set = set(map(lambda x: x.lower(), filter(lambda x: x.strip(), vacancy_words)))
    result_set = None if len(skills_set) >= 60 else skills_set
    return result_set

# changes global array - vacancies
def parse_search_results(link: str, search:str, page: int, 
                        max_page_number = None) -> tp.List[object]: 
    # preformat
    search_encoded: str = search.lower().replace(' ', '+')
    formatted_link = link.format(search_encoded,str(page))
    
    print('search_encoded: {} | page: {} | max_page_number: {}'.format(search_encoded,page,max_page_number))
    
    # work with parser
    response = _scrap_url(formatted_link)
    soup = BeautifulSoup(response.content, "html.parser")
    vacancies_items = soup.find_all("div", {"class": "vacancy-serp-item"})
    for item in vacancies_items:
        res_item = parseSearchResult(item)
        res_item['search'] = search
        vacancies.append(res_item)

    if page == 0: # calculate max_page_number
        max_page_number = int(soup.select('a[data-qa=pager-page]')[-1]['href'].split('page=')[1])
    
    if page != max_page_number: # go next page, until max_page_number
        parse_search_results(link, search, page+1, max_page_number)

def parseSearchResult(item) -> dict:
    result = {}

    header_item = item.select_one("a[data-qa=vacancy-serp__vacancy-title]")
    link = header_item['href'].split("?")[0]
    result['link'] = link
    result['title'] = header_item.text.strip()

    # parse skills
    skills_set = parse_vacancy_description(link)
    if skills_set: # if true -> russian vacancy
        filtered_list = filter_with_block_set(skills_set, block_set)
        result['skills'] = filtered_list

    work_schedule_item = item.select_one('div[data-qa=vacancy-serp__vacancy-work-schedule]')
    if work_schedule_item:
        result['work_schedule'] = work_schedule_item.text
    
    compenstaion_item = item.select_one('span[data-qa=vacancy-serp__vacancy-compensation]')
    if compenstaion_item: # salary
        result['compensation'] = compenstaion_item.text.replace("\u202f","") 

    employer_item = item.select_one('a[data-qa=vacancy-serp__vacancy-employer]')
    if employer_item:
        employer = {}
        employer['link'] = "https://hh.ru" + employer_item['href'].split("?")[0]
        employer['name'] = employer_item.text.strip().replace('\xa0','')
        result['employer'] = employer

    return result

# load block_set
with open('blockset.csv','r', encoding='utf-8') as f:
    block_set = set(f.read().splitlines())

# real run
for search_word in search_words:
    parse_search_results(link, search_word, 0)

# saving
with open('target/output', 'w+', encoding='utf8') as f:
    for vacancy in vacancies:
        json.dump(vacancy, f, ensure_ascii=False)
        f.write('\n')