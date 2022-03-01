from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

import requests
import brotli

from starlette.datastructures import URL, QueryParams
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from asgiref.typing import WWWScope
from pathlib import Path
from typing import List
from uvicorn.protocols.utils import get_path_with_query_string
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


@app.on_event("startup")
def startup_event():
    ...


@app.get("/refresh")
async def vacancy_refresh():
    list_of_vacancy = load_vacancy_list()
    write_vac_list_to_db(list_of_vacancy)
    return RedirectResponse(url=app.url_path_for("home_page"))


spec_list = []
path_with_query = ''


@app.get("/vacancy_list")
async def vacancy_list(request: Request, spec: List[str] = Query(None), company: List[str] = Query(None)):
    global path_with_query
    with session.begin() as ses:
        if spec and not company:
            global spec_list
            spec_list = spec
            list_of_vacancy = []
            if spec_list:
                vac_with_specs = [
                    ses.query(Vacancy).filter(Vacancy.specialization.contains(spec)).all() for spec in spec_list
                ]
                for vac_spec in vac_with_specs:
                    list_of_vacancy.extend(vac_spec)
        elif company and not spec:
            list_of_vacancy = []
            vac_with_company = [
                ses.query(Vacancy).filter(Vacancy.company_name.contains(comp)).all() for comp in company
            ]
            for vac_company in vac_with_company:
                list_of_vacancy.extend(vac_company)
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
        print('ololo')
        print(path_with_query)
        print('ololo')
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
    with session.begin() as ses:
        vacancy_count = ses.query(Vacancy).count()
        specs_list = [x[0] for x in ses.query(Vacancy.specialization.distinct()).all()]
    return templates.TemplateResponse(
        "index.html", {"request": request, "vac_num": vacancy_count, "specs_list": specs_list}
    )


if __name__ == '__main__':
    uvicorn.run(app)
