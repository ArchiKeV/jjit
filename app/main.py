from sqlalchemy import create_engine, and_, or_, desc
from sqlalchemy.orm.session import sessionmaker
from dateutil import parser
from pathlib import Path

import requests
import brotli

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from typing import List
import uvicorn

from pbh_companies import pbh_companies
from classes import base, Vacancy, SortName


# Main configuration
base_path = Path(__file__).parent.parent.absolute()

# DB configuration
db_path = "jjit.db.sqlite"
engine = create_engine(f'sqlite:///{base_path / db_path}', echo=True)

# FastAPI configuration
templates = Jinja2Templates(directory=base_path / "templates")
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=base_path / "static"),
    name="static",
)

base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def load_vacancy_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
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
            vac["published_at"] = parser.isoparse(vac["published_at"])
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
        for sk_attr in vacancy_skills_attr:
            for skill in ses.query(getattr(Vacancy, sk_attr)).filter(getattr(Vacancy, sk_attr).is_not(None)).all():
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
    remote_interview_list = []
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
        request: Request, spec: List[str] = Query(None),
        company_on: List[str] = Query(None), company_off: List[str] = Query(None),
        skill_on: List[str] = Query(None), skill_off: List[str] = Query(None),
        country: List[str] = Query(None), salary_type: List[str] = Query(None),
        workplace_type: List[str] = Query(None), remote_interview: List[bool] = Query(None),
        sort_asc: SortName = Query(None), sort_desc: SortName = Query(None)
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
        if company_on or company_off:
            from urllib.parse import unquote
            if company_on:
                sub_conditions = or_(
                    Vacancy.company_name.is_(unquote(comp)) for comp in company_on
                )
                conditions.append(sub_conditions)
            if company_off:
                conditions.append(and_(or_(
                    Vacancy.company_name.is_not(unquote(comp)) for comp in company_off
                )))
        if skill_on or skill_off:
            from urllib.parse import unquote
            vacancy_skills_attr = [
                x for x in dir(Vacancy) if x.startswith('skill') and not x.endswith('old') and not x.endswith('level')
            ]
            if skill_on:
                for skill in skill_on:
                    conditions.append(or_(
                        getattr(Vacancy, skill_attr).is_(unquote(skill)) for skill_attr in vacancy_skills_attr
                    ))
            if skill_off:
                for skill in skill_off:
                    conditions.append(and_(
                        or_(
                            getattr(Vacancy, skill_attr).is_not(unquote(skill)),
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
        if len(conditions) > 0:
            if sort_asc:
                list_of_vacancy.extend(ses.query(Vacancy).filter(and_(*conditions)).order_by(
                    getattr(Vacancy, sort_asc)
                ).all())
            elif sort_desc:
                list_of_vacancy.extend(ses.query(Vacancy).filter(and_(*conditions)).order_by(
                    desc(getattr(Vacancy, sort_desc))
                ).all())
            else:
                list_of_vacancy.extend(ses.query(Vacancy).filter(and_(*conditions)).all())
        else:
            list_of_vacancy = ses.query(Vacancy).all()
        path_with_query = str(request.url.include_query_params()).split('/')[-1]
        if "sort_asc" in request.url.query:
            query_without_sort = request.url.remove_query_params("sort_asc").query
        elif "sort_desc" in request.url.query:
            query_without_sort = request.url.remove_query_params("sort_desc").query
        else:
            query_without_sort = request.url.query
        return templates.TemplateResponse(
            "vacancy_list.html",
            {
                "request": request,
                "list_of_vacancy": list_of_vacancy,
                "vac_len": len(list_of_vacancy),
                "query_without_sort": query_without_sort
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


@app.get("/api/pbh_companies")
async def api_pbh_companies():
    return pbh_companies


if __name__ == '__main__':
    uvicorn.run(app)
