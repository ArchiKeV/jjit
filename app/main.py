from sqlalchemy import create_engine, Column, String, Boolean, Integer, not_, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

import requests
import brotli

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from pathlib import Path
from typing import List
import uvicorn

# DB configuration
db_path = "jjit.db.sqlite"
base = declarative_base()
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# FastAPI configuration
templates = Jinja2Templates(directory=Path(__file__).parent.parent.absolute() / "templates")
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)


class Vacancy(base):
    __tablename__ = 'vacancy'
    id = Column(String, primary_key=True)
    title = Column(String)
    title_old = Column(String)
    description = Column(String)
    description_old = Column(String)
    street = Column(String)
    street_old = Column(String)
    city = Column(String)
    city_old = Column(String)
    country_code = Column(String)
    country_code_old = Column(String)
    address_text = Column(String)
    address_text_old = Column(String)
    specialization = Column(String)
    specialization_old = Column(String)
    workplace_type = Column(String)
    workplace_type_old = Column(String)
    company_name = Column(String)
    company_name_old = Column(String)
    company_url = Column(String)
    company_url_old = Column(String)
    company_size = Column(String)
    company_size_old = Column(String)
    experience_level = Column(String)
    experience_level_old = Column(String)
    published_at = Column(String)
    published_at_old = Column(String)
    remote_interview = Column(Boolean)
    remote_interview_old = Column(Boolean)
    salary_permanent = Column(String)
    salary_permanent_old = Column(String)
    salary_mandate = Column(String)
    salary_mandate_old = Column(String)
    salary_b2b = Column(String)
    salary_b2b_old = Column(String)
    skill_01 = Column(String)
    skill_01_old = Column(String)
    skill_01_level = Column(Integer)
    skill_01_level_old = Column(Integer)
    skill_02 = Column(String)
    skill_02_old = Column(String)
    skill_02_level = Column(Integer)
    skill_02_level_old = Column(Integer)
    skill_03 = Column(String)
    skill_03_old = Column(String)
    skill_03_level = Column(Integer)
    skill_03_level_old = Column(Integer)
    skill_04 = Column(String)
    skill_04_old = Column(String)
    skill_04_level = Column(Integer)
    skill_04_level_old = Column(Integer)
    skill_05 = Column(String)
    skill_05_old = Column(String)
    skill_05_level = Column(Integer)
    skill_05_level_old = Column(Integer)
    skill_06 = Column(String)
    skill_06_old = Column(String)
    skill_06_level = Column(Integer)
    skill_06_level_old = Column(Integer)
    skill_07 = Column(String)
    skill_07_old = Column(String)
    skill_07_level = Column(Integer)
    skill_07_level_old = Column(Integer)
    skill_08 = Column(String)
    skill_08_old = Column(String)
    skill_08_level = Column(Integer)
    skill_08_level_old = Column(Integer)
    skill_09 = Column(String)
    skill_09_old = Column(String)
    skill_09_level = Column(Integer)
    skill_09_level_old = Column(Integer)
    skill_10 = Column(String)
    skill_10_old = Column(String)
    skill_10_level = Column(Integer)
    skill_10_level_old = Column(Integer)
    remote_work = Column(Boolean)
    remote_work_old = Column(Boolean)
    comment = Column(String)
    rate = Column(Integer)
    status = Column(String)
    open_to_hire_ukrainians = Column(Boolean)


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def load_vacancy_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://justjoin.it',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0'
    }
    url = 'https://justjoin.it/api/offers'
    response = requests.get(url=url, headers=headers)
    return response.json()


def write_vac_list_to_db(vac_list):
    with session() as ses:
        for vac in vac_list:
            vac['specialization'] = vac['marker_icon']
            vac.pop("marker_icon")
            vac.pop('latitude')
            vac.pop('longitude')
            employment_types = vac["employment_types"]
            for salary in employment_types:
                if salary["type"] == 'permanent':
                    if salary.get("salary", None):
                        s_from = salary["salary"]["from"]
                        s_to = salary["salary"]["to"]
                        s_curr = salary["salary"]["currency"]
                        vac["salary_permanent"] = f'{s_from} - {s_to} {s_curr}'
                    else:
                        vac["salary_permanent"] = 'Undisclosed Salary'
                if salary["type"] == 'b2b':
                    if salary.get("salary", None):
                        s_from = salary["salary"]["from"]
                        s_to = salary["salary"]["to"]
                        s_curr = salary["salary"]["currency"]
                        vac["salary_b2b"] = f'{s_from} - {s_to} {s_curr}'
                    else:
                        vac["salary_b2b"] = 'Undisclosed Salary'
                if salary["type"] == 'mandate_contract':
                    if salary.get("salary", None):
                        s_from = salary["salary"]["from"]
                        s_to = salary["salary"]["to"]
                        s_curr = salary["salary"]["currency"]
                        vac["salary_mandate"] = f'{s_from} - {s_to} {s_curr}'
                    else:
                        vac["salary_mandate"] = 'Undisclosed Salary'
            vac.pop('employment_types')
            vac.pop('company_logo_url')
            for enum, skill in enumerate(vac['skills']):
                vac[f'skill_0{enum + 1}'] = skill['name']
                vac[f'skill_0{enum + 1}_level'] = skill['level']
            vac.pop('skills')
            vac['remote_work'] = vac['remote']
            vac.pop('remote')
            vac['status'] = 'Loaded'
            old_vacancy: Vacancy = ses.query(Vacancy).filter(Vacancy.id == vac["id"]).first()
            if old_vacancy:
                vacancy_attr_list = [x for x in dir(old_vacancy) if not x.startswith('_') and not x.endswith('_old')]
                for k in vacancy_attr_list:
                    old_v_attr_value = getattr(old_vacancy, k, False)
                    v_attr_value = vac.get(k, False)
                    if old_v_attr_value and v_attr_value and old_v_attr_value != v_attr_value:
                        setattr(old_vacancy, f"{k}_old", old_v_attr_value)
                        setattr(old_vacancy, k, v_attr_value)
                    elif old_v_attr_value and not v_attr_value:
                        setattr(old_vacancy, f"{k}_old", old_v_attr_value)
                        setattr(old_vacancy, k, None)
                    elif not old_v_attr_value and v_attr_value:
                        setattr(old_vacancy, f"{k}_old", None)
                        setattr(old_vacancy, k, v_attr_value)
            else:
                ses.add(Vacancy(**vac))
        ses.commit()
        ses.query(Vacancy).filter(Vacancy.status.is_(None), Vacancy.comment.is_(None)).delete(synchronize_session=False)
        ses.commit()
        loaded_vacancy_list = ses.query(Vacancy).filter(Vacancy.status == 'Loaded').all()
        for vac in loaded_vacancy_list:
            setattr(vac, 'status', None)
        ses.commit()


def load_vacancy(vac_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'https://justjoin.it/offers/{vac_id}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0'
    }
    url = f'https://justjoin.it/api/offers/{vac_id}'
    response = requests.get(url=url, headers=headers)
    return response.json()


def write_vac_to_db(vac_dict, vac: Vacancy):
    vac.description = vac_dict['body']
    if len(vac_dict['skills']) > 3:
        for enum, skill in enumerate(vac_dict['skills']):
            if enum > 2:
                setattr(vac, f'skill_{enum + 1:02}', skill['name'])
                setattr(vac, f'skill_{enum + 1:02}_level', skill['level'])


unique_skills = []


def get_skills_list_with_repeat_num():
    global unique_skills
    unique_skills = []
    raw_unique_skills = {}
    with session.begin() as ses:
        vacancy_skills_attr = [
            x for x in dir(Vacancy) if x.startswith('skill') and not x.endswith('old') and not x.endswith('level')
        ]
        for skill_attr in vacancy_skills_attr:
            for skill in ses.query(getattr(Vacancy, skill_attr)).filter(getattr(Vacancy, skill_attr).is_not(None)).all():
                if not raw_unique_skills.get(skill[0], False):
                    raw_unique_skills.update({skill[0]: 1})
                else:
                    raw_unique_skills[skill[0]] += 1
        for num, (skill_name, skill_num) in enumerate(raw_unique_skills.items()):
            unique_skills.append({"name": skill_name, "num": skill_num, "id": f's{num}'})


company_list = []


def get_company_list_with_repeat_num():
    global company_list
    company_list = []
    raw_company_list = {}
    with session.begin() as ses:
        for company in ses.query(Vacancy.company_name).filter(Vacancy.company_name.is_not(None)).all():
            if not raw_company_list.get(company[0], False):
                raw_company_list.update({company[0]: 1})
            else:
                raw_company_list[company[0]] += 1
        for num, (company_name, company_num) in enumerate(raw_company_list.items()):
            company_list.append({"name": company_name, "num": company_num, "id": f'c{num}'})


salary_dict = {}


def get_salary_list_with_repeat_num():
    global salary_dict
    with session.begin() as ses:
        mandate_count = ses.query(Vacancy.salary_mandate).filter(Vacancy.salary_mandate.is_not(None)).count()
        salary_dict.update({"mandate": mandate_count})
        b2b_count = ses.query(Vacancy.salary_b2b).filter(Vacancy.salary_b2b.is_not(None)).count()
        salary_dict.update({"b2b": b2b_count})
        permanent_count = ses.query(Vacancy.salary_permanent).filter(Vacancy.salary_permanent.is_not(None)).count()
        salary_dict.update({"permanent": permanent_count})


country_list = []


def get_country_dict_with_repeat_num():
    global country_list
    country_list = []
    with session.begin() as ses:
        county_none = []
        for country in ses.query(Vacancy.country_code.distinct()).all():
            if country[0] is None:
                county_none.append('Country not specified')
            else:
                country_list.append(country[0])
        country_list.extend(county_none)


workplace_type_list = []


def get_workplace_type_list_with_repeat_num():
    global workplace_type_list
    workplace_type_list = []
    with session.begin() as ses:
        for w_type in ses.query(Vacancy.workplace_type.distinct()).all():
            workplace_type_list.append(w_type[0])


remote_interview_list = []


def get_interview_type_list_with_repeat_num():
    global remote_interview_list
    with session.begin() as ses:
        for r_i_tf in ses.query(Vacancy.remote_interview.distinct()).all():
            remote_interview_list.append(r_i_tf[0])


get_skills_list_with_repeat_num()
get_company_list_with_repeat_num()
get_salary_list_with_repeat_num()
get_country_dict_with_repeat_num()
get_workplace_type_list_with_repeat_num()
get_interview_type_list_with_repeat_num()


@app.get("/refresh")
async def vacancy_refresh():
    list_of_vacancy = load_vacancy_list()
    write_vac_list_to_db(list_of_vacancy)
    get_skills_list_with_repeat_num()
    get_company_list_with_repeat_num()
    get_salary_list_with_repeat_num()
    get_country_dict_with_repeat_num()
    get_workplace_type_list_with_repeat_num()
    get_interview_type_list_with_repeat_num()
    return RedirectResponse(url=app.url_path_for("home_page"))


spec_list = []
path_with_query = ''


@app.get("/vacancy_list")
async def vacancy_list(
        request: Request, spec: List[str] = Query(None), company: List[str] = Query(None),
        company_on_id: List[str] = Query(None), company_off_id: List[str] = Query(None),
        skill_on_id: List[str] = Query(None), skill_off_id: List[str] = Query(None), country: List[str] = Query(None),
        salary_type: List[str] = Query(None), workplace_type: List[str] = Query(None),
        remote_interview: List[bool] = Query(None)
):
    global path_with_query
    list_of_vacancy = []
    conditions = []
    with session.begin() as ses:
        if spec:
            global spec_list
            spec_list = spec
            sub_conditions = or_(Vacancy.specialization.contains(sp) for sp in spec)
            conditions.append(sub_conditions)
        if company:
            conditions.append(or_(Vacancy.company_name.is_(cmp) for cmp in company))
        if company_on_id or company_off_id:
            global company_list
            if company_on_id:
                sub_conditions = or_(
                    Vacancy.company_name.contains(company_list[int(comp[1:])]['name']) for comp in company_on_id
                )
                conditions.append(sub_conditions)
            if company_off_id:
                conditions.append(and_(or_(
                    ~Vacancy.company_name.contains(company_list[int(comp[1:])]['name']) for comp in company_on_id
                )))
        if skill_on_id or skill_off_id:
            global unique_skills
            vacancy_skills_attr = [
                x for x in dir(Vacancy) if x.startswith('skill') and not x.endswith('old') and not x.endswith('level')
            ]
            if skill_on_id:
                for skill_id in skill_on_id:
                    skill = unique_skills[int(skill_id[1:])]["name"]
                    conditions.append(or_(
                        getattr(Vacancy, skill_attr).contains(skill) for skill_attr in vacancy_skills_attr
                    ))
            if skill_off_id:
                for skill_id in skill_off_id:
                    skill = unique_skills[int(skill_id[1:])]["name"]
                    conditions.append(and_(
                        or_(
                            ~getattr(Vacancy, skill_attr).contains(skill),
                            getattr(Vacancy, skill_attr).is_(None)
                        ) for skill_attr in vacancy_skills_attr
                    ))
        if country:
            sub_conditions = []
            for cntr in country:
                if cntr == 'Country not specified':
                    sub_conditions.append(Vacancy.country_code.is_(None))
                else:
                    sub_conditions.append(Vacancy.country_code.contains(cntr))
            sub_conditions = or_(*sub_conditions)
            conditions.append(sub_conditions)
        if salary_type:
            sub_conditions = []
            for s_type in salary_type:
                sub_conditions.append(getattr(Vacancy, f'salary_{s_type}').is_not(None))
            sub_conditions = or_(*sub_conditions)
            conditions.append(sub_conditions)
        if workplace_type:
            sub_conditions = []
            for w_type in workplace_type:
                sub_conditions.append(Vacancy.workplace_type.is_(w_type))
            sub_conditions = or_(*sub_conditions)
            conditions.append(sub_conditions)
        if remote_interview:
            sub_conditions = []
            for r_i_tf in remote_interview:
                sub_conditions.append(Vacancy.remote_interview.is_(bool(r_i_tf)))
            sub_conditions = or_(*sub_conditions)
            conditions.append(sub_conditions)
        if len(conditions) == 1:
            list_of_vacancy.extend(ses.query(Vacancy).filter(*conditions).all())
        elif len(conditions) > 1:
            list_of_vacancy.extend(ses.query(Vacancy).filter(and_(*conditions)).all())
        else:
            list_of_vacancy = ses.query(Vacancy).all()
        path_with_query = str(request.url.include_query_params()).split('/')[-1]
        return templates.TemplateResponse(
            "vacancy_list.html",
            {
                "request": request,
                "list_of_vacancy": list_of_vacancy,
                "vac_len": len(list_of_vacancy)
            }
        )


@app.get("/vacancy")
async def vacancy(request: Request, vac_id: str = None):
    global path_with_query
    with session.begin() as ses:
        selected_vacancy = ses.query(Vacancy).filter(Vacancy.id.is_(vac_id)).first()
        if not selected_vacancy.description:
            write_vac_to_db(load_vacancy(vac_id), selected_vacancy)
            selected_vacancy = ses.query(Vacancy).filter(Vacancy.id.is_(vac_id)).first()
        vacancy_dict = selected_vacancy.__dict__
        delete_attr = []
        for key in vacancy_dict:
            if key.startswith('_'):
                delete_attr.append(key)
            elif not vacancy_dict[key]:
                delete_attr.append(key)
        list_of_skill_keys = []
        for key in vacancy_dict:
            if key.startswith('skill') and not key.endswith('old') and not key.endswith('level'):
                list_of_skill_keys.append(key)
        list_of_skill_keys.sort()
        list_of_skills = [
            {
                'skill': vacancy_dict[key], 'level': vacancy_dict[f'{key}_level'],
                'skill_old': vacancy_dict[f'{key}_old'], 'level_old': vacancy_dict[f'{key}_level_old']
            }
            for key in list_of_skill_keys if vacancy_dict.get(key, False)
        ]
        get_skills_list_with_repeat_num()
        return templates.TemplateResponse(
            "vacancy.html",
            {
                "request": request,
                "vacancy": vacancy_dict,
                "skills": list_of_skills,
                "path_with_query": path_with_query
            }
        )


@app.get("/")
async def home_page(request: Request):
    global salary_dict
    global country_list
    global workplace_type_list
    global remote_interview_list
    with session.begin() as ses:
        vacancy_count = ses.query(Vacancy).count()
        specs_list = [x[0] for x in ses.query(Vacancy.specialization.distinct()).all()]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request, "vac_num": vacancy_count, "specs_list": specs_list, "country_list": country_list,
            "salary_dict": salary_dict, "workplace_type_list": workplace_type_list,
            "remote_interview_list": remote_interview_list
        }
    )


@app.get("/api/skills")
async def api_skills():
    global unique_skills
    return unique_skills


@app.get("/api/companies")
async def api_companies():
    global company_list
    return company_list


if __name__ == '__main__':
    uvicorn.run(app)
