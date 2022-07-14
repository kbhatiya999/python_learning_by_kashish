"""
References:
    1. https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html#generating-mappings-from-an-existing-metadata
"""

# crawler_db = "mysql://kashish_match:Kashish$1234@65.108.144.228:3306/job_scraper/job_board_list"
import contextvars
import itertools
import sys
import traceback

from sqlalchemy import MetaData, create_engine, func, inspect
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Query, Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm.strategy_options import load_only
from tenacity import Retrying, stop_after_attempt, RetryError, wait_fixed

crawler_db = "mysql://kashish_match:Kashish$1234@localhost:3307/job_scraper"
# crawler_db = "mysql://kashish_match:Kashish$1234@65.108.144.228:3306/job_scraper"

mysql_db = {

    # 'host': "136.243.32.134",
    'host': "localhost",
    'db': 'aditya_buildtab',
    'user': 'aditya_sendmaildb',
    'pass': 'sendmaildb@123',
    'port': '3306',
}

table_ = "job_board_list"

SessionLocal = sessionmaker(autocommit=True,
                            autoflush=True
                            )

SQLALCHEMY_DATABASE_URL = URL.create(drivername='mysql', username=mysql_db['user'], password=mysql_db['pass'],
                                     database=mysql_db['db'], host=mysql_db['host'], port=mysql_db['port'])

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
metadata = MetaData()
metadata.reflect(engine, only=['job_board_list', 'job_matching_score'])
Base = automap_base(metadata=metadata)
Base.prepare()
# Base.prepare(engine, reflect=True)


crawler_engine = create_engine(crawler_db, echo=True)
crawler_metadata = MetaData()
crawler_metadata.reflect(crawler_engine, only=['job_board_list'])

CrawlerBase = automap_base(metadata=crawler_metadata)
CrawlerBase.prepare()
# CrawlerBase.prepare(crawler_engine, reflect=True)

JobBoardList = Base.classes.job_board_list
JobBoardListCrawler = CrawlerBase.classes.job_board_list
JobMatchingScore = Base.classes.job_matching_score
cols = [c.name for c in inspect(JobBoardList).c]

SessionLocal.configure(binds={Base: engine, CrawlerBase: crawler_engine})

# _session = contextvars.ContextVar('session', default=None)

# ----------------------------------------------------------------------------------------------------------------------

def model2dict(model):
    columns_ = model.__table__.c

    d = {}
    for column in columns_:
        d[column.name] = getattr(model, column.name)

    return d


def batch_ranks(start_rank, end_rank, batch_size):
    """
    :param start_rank:
    :param end_rank:
    :param batch_size:
    :return:

    >>> batch_ranks(1, 10, 4)
    """

    left_ranks = range(start_rank, end_rank + 1, batch_size)
    right_ranks = []

    """If rank = 1 and size =4
     (rank + size -1) = (1 + 4 - 1) = 4
    (1, 4)"""

    def create_right_ranks(left_ranks, end_rank):
        _right_ranks = []
        for rank in left_ranks:
            _rank = rank + batch_size - 1
            if _rank < end_rank:
                _right_ranks.append(_rank)
            else:
                _right_ranks.append(end_rank)
        return _right_ranks

    right_ranks = create_right_ranks(left_ranks, end_rank)

    for x, y in zip(left_ranks, right_ranks):
        yield x, y


class ExistingDomains(object):
    def fetch(self, session):
        query = Query(JobBoardList).join(JobMatchingScore, JobBoardList.id == JobMatchingScore.job_id)
        # query = session.query(JobBoardList).select_from(JobMatchingScore)\
        #     .filter(JobBoardList.id == JobMatchingScore.job_id)\

        query = query.with_entities(JobBoardList.domains).distinct()
        # temp_data = query.with_session(session).all()
        # domains = list(zip(*temp_data))[0]

        domains = query.with_session(session).all()
        return domains


# def get_query(between_left, between_right, ignore_domains, session):
#     subquery1 = session.query(JobBoardListCrawler.id, JobBoardListCrawler.domains,
#                               func.rank().over(
#                                   order_by=JobBoardListCrawler.id.asc(),
#                                   partition_by=JobBoardListCrawler.domains)
#                               .label('rnk')
#                               ).subquery()
#
#     subquery2 = (session.query(subquery1.c.id)
#                  .filter(subquery1.c.rnk.between(between_left, between_right))
#                  .subquery())
#     query = session.query(JobBoardListCrawler)
#     query = query.filter(subquery.c.rnk.between(between_left, between_right))
#     if ignore_domains:
#         query = query.filter(subquery.c.domains.not_in(ignore_domains))
#     return query


class ThingTwo(object):
    def go(self, session, priority=0, job_ids=None):
        """
        Copy data from one db source to another for the passed job_ids.

        :param session:
        :param priority:
        :param job_ids:
        :return:
        """
        if not job_ids:
            raise ValueError('Job_ids parameter can not be none or empty')

        data_for_insert = []
        query = session.query(JobBoardListCrawler).filter(JobBoardListCrawler.id.in_(job_ids))

        #  Paginated data
        def query_batch_generator(query, batch_size=1000):
            """
            Iterator implementation for paginating a Query.
            :param query:
            :param batch_size:
            :return:
            """
            query = query.limit(batch_size)
            _offset = 0
            while True:
                # with SessionLocal() as session:
                #   with session.begin():
                data = query.offset(_offset).with_session(session)
                insert_data = list(data)
                if not insert_data:
                    break
                yield insert_data
                _offset += batch_size

        batched_generator = query_batch_generator(query)

        for queried_data in batched_generator:
            # queried_data = query.all()
            queried_apply_links = [d.apply_links for d in queried_data]
            potential_integrity_errors = list(map(lambda x: x[0], session.query(JobBoardList.apply_links)
                                                  .filter(JobBoardList.apply_links.in_(queried_apply_links))))

            data_for_insert.extend(
                [
                    JobBoardList(**{k: v for k, v in model2dict(d).items() if k in cols}, priority=priority)
                    for d in queried_data if d.apply_links not in potential_integrity_errors]
            )
        return data_for_insert
        # session.commit()
        # session.bulk_save_objects(data_for_insert)
        # if len(data_for_insert) == 0:
        #     return False


class RankedJobs:
    def fetch(self, session, between_left, between_right, ignore_domains, ):
        search_keyword = '%salesforce%'

        subquery1 = session.query(JobBoardListCrawler.id,
                                  JobBoardListCrawler.domains,
                                  JobBoardListCrawler.job_category,
                                  func.rank()
                                  .over(
                                      order_by=JobBoardListCrawler.upd_ts.desc(),
                                      partition_by=JobBoardListCrawler.domains
                                  )
                                  .label('rnk')
                                  ).subquery()

        query = (session.query(subquery1.c.id)
                 .filter(subquery1.c.rnk.between(between_left, between_right), subquery1.c.job_category.like(search_keyword))
                 )
        data = query.all()
        job_ids = list(zip(*data))
        return job_ids[0]


def get_split_iterator(iterable, size=10_000):
    it = iter(iterable)
    while data := list(itertools.islice(it, 10_000)):
        yield data


def insert_in_batch_with_retry(session, data_to_be_inserted, retry_count=3):
    global attempt
    for batch in get_split_iterator(data_to_be_inserted, size=1000):
        batch_data = list(batch)
        if not batch_data:
            break
        try:
            for attempt in Retrying(stop=stop_after_attempt(5), wait=wait_fixed(1)):
                with attempt:
                    with session.begin():
                        session.bulk_save_objects(batch_data)
                        print(f'inserting BATCH of {len(batch_data)}')
        except RetryError:
            traceback.print_exc()


def start(session: Session, priority, start_rank, end_rank, size, exclude):
    # global attempt, data_to_be_inserted
    for l, r in batch_ranks(start_rank, end_rank, size):
        try:
            job_ids_to_fetch = get_ranked_jobs_between(session, l, r, exclude)
            data_to_be_inserted = fetch_data(session, job_ids_to_fetch, priority)
            if not data_to_be_inserted: break
            insert_in_batch_with_retry(session, data_to_be_inserted)
            print(f'Completed working with rank ({l}, {r})')
        except (IntegrityError, Exception) as e:
            ei = sys.exc_info()
            print(f'Skipping with rank ({l}, {r})')
            traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])

        finally:
            priority += 1


def get_ranked_jobs_between(session, l, r, exclude):
    with session.begin():
        job_ids_to_fetch = RankedJobs().fetch(session, between_left=l, between_right=r, ignore_domains=exclude)
    return job_ids_to_fetch


def fetch_data(session, job_ids, priority_for_insert):
    try:
        for attempt in Retrying(stop=stop_after_attempt(5), wait=wait_fixed(1)):
            with attempt:
                with session.begin():
                    data_to_be_inserted = ThingTwo().go(session, priority=priority_for_insert, job_ids=job_ids)
    except RetryError:
        traceback.print_exc()
    return data_to_be_inserted


def get_next_priority(session: Session):
    max_priority = session.query(func.max(JobBoardList.priority)).one()[0]
    priority_for_insert = 0 if not max_priority else max_priority + 1

    return priority_for_insert


if __name__ == '__main__':
    # session.set(SessionLocal())
    session = SessionLocal()
    from_ = 1
    to_ = 20
    batch_ = 1

    # global ignore_domains, priority_for_insert
    with session.begin():
        existing_domains = ExistingDomains().fetch(session)

    priority_ = get_next_priority(session)
    start(session=session, priority=priority_, start_rank=from_, end_rank=to_, size=batch_, exclude=existing_domains)
