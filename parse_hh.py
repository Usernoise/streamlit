import requests
from bs4 import BeautifulSoup


def get_html(url: str):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"},
        )
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    try:
        title = soup.find("h1", {"data-qa": "vacancy-title"}).text.strip()
    except AttributeError:
        title = "Не указано"

    try:
        salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"}).text.strip()
    except AttributeError:
        salary = "Не указано"

    try:
        experience = soup.find("span", {"data-qa": "vacancy-experience"}).text.strip()
    except AttributeError:
        experience = "Не указано"

    try:
        employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"}).text.strip()
    except AttributeError:
        employment_mode = "Не указано"

    try:
        company = soup.find("a", {"data-qa": "vacancy-company-name"}).text.strip()
    except AttributeError:
        company = "Не указано"

    try:
        location = soup.find("p", {"data-qa": "vacancy-view-location"}).text.strip()
    except AttributeError:
        location = "Не указано"

    try:
        description = soup.find("div", {"data-qa": "vacancy-description"}).text.strip()
    except AttributeError:
        description = "Не указано"

    skills = [
        skill.text.strip()
        for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})
    ]

    # Формирование строки в формате Markdown
    markdown = f"# {title}\n\n"
    markdown += f"**Компания:** {company}\n"
    markdown += f"**Зарплата:** {salary}\n"
    markdown += f"**Опыт работы:** {experience}\n"
    markdown += f"**Тип занятости и режим работы:** {employment_mode}\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += "## Описание вакансии\n"
    markdown += f"{description}\n\n"
    markdown += "## Ключевые навыки\n"
    markdown += "- " + "\n- ".join(skills) + "\n"


    return markdown.strip()


def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        name = soup.find('h2', {'data-qa': 'bloko-header-1'}).text.strip()
    except AttributeError:
        name = "Не указано"

    try:
        gender_age = soup.find('p').text.strip()
    except AttributeError:
        gender_age = "Не указано"

    try:
        location = soup.find('span', {'data-qa': 'resume-personal-address'}).text.strip()
    except AttributeError:
        location = "Не указано"

    try:
        job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).text.strip()
    except AttributeError:
        job_title = "Не указано"

    try:
        job_status = soup.find('span', {'data-qa': 'job-search-status'}).text.strip()
    except AttributeError:
        job_status = "Не указано"

    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    if experience_section:
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        experiences = []
        for item in experience_items:
            try:
                period = item.find('div', class_='bloko-column_s-2').text.strip()
                duration = item.find('div', class_='bloko-text').text.strip()
                period = period.replace(duration, f" ({duration})")
                company = item.find('div', class_='bloko-text_strong').text.strip()
                position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
                description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
                experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")
            except AttributeError:
                continue
    else:
        experiences = ["Опыт работы не найден"]

    try:
        skills_section = soup.find('div', {'data-qa': 'skills-table'})
        skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]
    except AttributeError:
        skills = ["Не указаны"]

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown



def get_candidate_info(url: str):
    response = get_html(url)
    if response:
        return extract_candidate_data(response.text)
    return None


def get_job_description(url: str):
    response = get_html(url)
    if response:
        return extract_vacancy_data(response.text)
    return None