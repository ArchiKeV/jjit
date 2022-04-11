from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

base = declarative_base()


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
    published_at = Column(DateTime)
    published_at_old = Column(DateTime)
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


class SortName(str, Enum):
    title = "title"
    company_name = "company_name"
    city = "city"
    country_code = "country_code"
    specialization = "specialization"
    remote_interview = "remote_interview"
    workplace_type = "workplace_type"
    rate = "rate"
    published_at = "published_at"
    status = "status"
