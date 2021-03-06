from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, DATETIME, CHAR, INTEGER
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime, timezone, timedelta
from pathlib import Path
from decouple import AutoConfig


BASE_DIR = PurePath(__file__).parent.parent
config = AutoConfig(search_path=BASE_DIR.joinpath('config'))

DATABASE_USER = config('POSTGRES_USER')
DATABASE_NAME = config('POSTGRES_DB')
DATABASE_PASSWORD = config('POSTGRES_PASSWORD')
DATABASE_HOST = config('DATABASE_HOST')
DATABASE_PORT = config('DATABASE_PORT')


engine = create_engine(
        f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@'
        f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

session_factory = sessionmaker(engine)
session = session_factory()


meta = MetaData(engine)


def get_now(offset):
    _offset = timezone(timedelta(hours=offset))
    now = datetime.now(_offset)
    return now


announce = Table('accounts_announce', meta,
                 Column('id', INTEGER, primary_key=True),
                 Column('announce', String, nullable=True, default=''),
                 Column('created', DATETIME),
                 Column('author', CHAR, nullable=False),
                 )


bot_users_table = Table('accounts_botusers', meta,
                    Column('id', INTEGER, primary_key=True),
                    Column('chat_id', CHAR, nullable=False),
                    Column('nickname', CHAR, nullable=True, ),
                    Column('name', CHAR, nullable=True, ),
                    Column('telephone', CHAR, nullable=True),
                    Column('location', CHAR, nullable=True, default=''),
                    Column('user_created', DATETIME)
                    )


users_messages = Table('accounts_usersmessages', meta,
                       Column('id', INTEGER, primary_key=True),
                       Column('chat_id_id', INTEGER, nullable=True),
                       Column('nickname', CHAR, nullable=True),
                       Column('name', CHAR, nullable=True),
                       Column('message', String, nullable=False),
                       Column('location', CHAR, nullable=True),
                       Column('message_time', DATETIME),
                       Column('status', CHAR, nullable=True, default='')
                       )

reply_messages = Table('accounts_messagesreplys', meta,
                       Column('id', INTEGER, primary_key=True),
                       Column('chat_id_id', INTEGER, nullable=True),
                       Column('nickname', CHAR, nullable=True),
                       Column('name', CHAR, nullable=True),
                       Column('message', String, nullable=False),
                       Column('message_time', DATETIME),
                       Column('status', CHAR, nullable=True, default='')
                       )


def db_insert_or_update(chat_id, nickname=None, name=None,
                        telephone=None, location=None,
                        ):

    with engine.connect() as conn:
        try:
            insert_statement = bot_users_table.insert().values(chat_id=chat_id,
                                                           nickname=nickname,
                                                           name=name,
                                                           telephone=telephone,
                                                           location=location,
                                                           user_created=get_now(3)
                                                           )
            conn.execute(insert_statement)
        except:
            insert_statement = bot_users_table.update().values(nickname=nickname,
                                                           name=name,
                                                           telephone=telephone
                                                           ).\
                where(bot_users_table.c.chat_id == chat_id)
            conn.execute(insert_statement)


def db_get_contact_number(chat_id):
    try:
        user = session.query(bot_users_table)\
            .filter(bot_users_table.c.chat_id == chat_id).one()
        return user.telephone
    except:
        pass


def db_get_location(chat_id):

    try:
        user = session.query(bot_users_table)\
            .filter(bot_users_table.c.chat_id == chat_id).one()
        return user.location
    except:
        pass


def db_get_id(chat_id):

    try:
        user = session.query(bot_users_table) \
            .filter(bot_users_table.c.chat_id == chat_id).one()
        return user.id
    except(Exception) as e:
        print('ERORO chat ID', e)
        pass


def db_update_location(chat_id, location):
    with engine.connect() as conn:
        try:
            insert_statement = bot_users_table.update().values(location=location). \
                where(bot_users_table.c.chat_id == chat_id)
            conn.execute(insert_statement)
        except Exception as e:
            print('ERROR!!!!!!!!!!!!!!!!', e)
            pass


def db_insert_reply_message(chat_id_id, nickname=None, name=None, reply_message=None):

    with engine.connect() as conn:

        insert_statement = reply_messages.insert().values(chat_id_id=chat_id_id,
                                                       nickname=nickname,
                                                       name=name,
                                                       message=reply_message,
                                                       message_time=get_now(3)
                                                       )
        conn.execute(insert_statement)


def db_insert_user_message(chat_id_id, nickname=None, location=None,
                           name=None, message=None):

    with engine.connect() as conn:

        insert_statement = users_messages.insert().values(chat_id_id=chat_id_id,
                                                          nickname=nickname,
                                                          name=name,
                                                          message=message,
                                                          location=location,
                                                          message_time=get_now(3)
                                                          )
        conn.execute(insert_statement)


def db_insert_announce(author, bot_announce):

    with engine.connect() as conn:

        insert_statement = announce.insert().values(announce=bot_announce,
                                                    author=author,
                                                    created=get_now(3)
                                                    )
        conn.execute(insert_statement)


# usage:

# db_insert_or_update(chat_id='417070387', nickname='Balsh', name='Dmitry', telephone='23432432')
# print(db_get_contact_number('417070387'))
# db_insert_reply_message(chat_id='1660356916', reply_message='asdasd')
# db_update_location(chat_id='1660356916', location='lsdkjfldskj')
# print(db_get_id('417070387'))
