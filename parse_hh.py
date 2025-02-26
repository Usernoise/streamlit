import requests
from bs4 import BeautifulSoup

# Функция для получения HTML-страницы
def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )

# Извлечение данных вакансии
def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Не указан"

    # Извлечение зарплаты
    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Не указана"

    # Извлечение опыта работы
    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Не указан"

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Не указан"

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Не указана"

    # Извлечение местоположения
    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Не указано"

    # Извлечение описания вакансии
    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Не указано"

    # Извлечение ключевых навыков
    skills = [
        skill.text.strip()
        for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})
    ]

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills) if skills else 'Не указаны'}
"""

    return markdown.strip()

# Извлечение данных кандидата
def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name.text.strip() if name else "Не указано"

    gender_age = soup.find('p')
    gender_age = gender_age.text.strip() if gender_age else "Не указано"

    location = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location.text.strip() if location else "Не указано"

    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title.text.strip() if job_title else "Не указано"

    job_status = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status.text.strip() if job_status else "Не указано"

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experiences = []
    if experience_section:
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        for item in experience_items:
            period = item.find('div', class_='bloko-column_s-2')
            duration = item.find('div', class_='bloko-text')
            period = period.text.strip() if period else "Не указан"
            duration = duration.text.strip() if duration else "Не указано"
            period = period.replace(duration, f" ({duration})")

            company = item.find('div', class_='bloko-text_strong')
            company = company.text.strip() if company else "Не указана"

            position = item.find('div', {'data-qa': 'resume-block-experience-position'})
            position = position.text.strip() if position else "Не указана"

            description = item.find('div', {'data-qa': 'resume-block-experience-description'})
            description = description.text.strip() if description else "Не указано"

            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

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
    markdown += ', '.join(skills) if skills else "Не указаны"

    return markdown

# Получение информации о вакансии
def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)

# Получение информации о кандидате
def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)
