import asyncio
from collections import namedtuple

from job_match_application.database import SessionLocal
from job_match_application.models import Requirement

session = SessionLocal()

ScoreInfo = namedtuple('ScoreInfo', ['location', 'visa', 'exp', 'category'])


def have_location_preference(preferred: str):
    no_preference = ['No preference (Open to relocate across the US)',
                     'I am open to relocating but I prefer the following locations',
                     ]

    has_preference = ['I strictly need a job in the following location(s)']
    if preferred in has_preference:
        return True

    return False


score_map = {
    "location": 1000,
    "visa": 100,
    "exp": 10,
    "category": {
        "Data Analytics/ Data Scientist": 8_000,
        "Product Management": 6000,
        "Software Engineering": 10_000,
        "Program/Project": 4000,
        "Salesforc": 0
    }

}


def get_score(location: bool, visa: bool, exp: int, category: str):
    exp_score = score_map.get('exp', 0)
    location_score = score_map.get('location', 0)
    visa_score = score_map.get('visa', 0)
    category_score = score_map.get('category')

    score = 0
    exp_ = 0 if not exp else float(exp)
    if location and not have_location_preference(location):
        score += location_score
    if not visa:
        score += visa_score
    if exp_:
        score += int(exp_ * exp_score)

    if category and category in category_score:
        score += category_score.get(category)
    return score


q = session.query(Requirement).filter(Requirement.candidate_id is not None)


# number_of_rows_per_page = 10
# page_number = 1
# req_page = q.limit(number_of_rows_per_page).offset(page_number*number_of_rows_per_page)

# while req_page.page <= req_page.pages:
#     for item in req_page.items:
#         item: Requirement
#         score_info = ScoreInfo(item.preferred_location, item.visa_status , item.total_work_experience,)
#         get_score(*score_info)
#
#     req_page = req_page.next()
async def start():
    bunch_of_items = []
    tasks = []
    # for item in q.filter(Requirement.candidate_id == 303).all():
    for item in q.all():
        item: Requirement
        user_ = item.user
        user_category = user_.category if user_ else None
        score_info = ScoreInfo(item.preferred_location, item.visa_status, item.total_work_experience, user_category)
        score_ = get_score(*score_info)
        item.weight = score_
        bunch_of_items.append(item)

    session.add_all(bunch_of_items)
    session.commit()


asyncio.run(start())
