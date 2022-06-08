import sqlite3
import click
# g: 각 요청에 대해 고유한 특수 개체, 요청하는 동안 여러 기능에서 액세스 할 수 있는 데이터를 저장하는데 사용
from flask import current_app, g
from flask.cli import with_appcontext

# get_db: 동일한 요청에서 두 번째로 호출되는 경우 새 연결을 만드는 대신 연결이 저장되고 재사용
def get_db():
  if 'db' not in g:
    # current_app: 요청을 처리하는 Flask 응용 프로그램을 가리키는 또 다른 특수 객체
    # sqlite3.connect(): DATABASE 구성 키가 가리키는 파일에 대한 연결을 설정
    g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
    # sqlite3.Row: dicts처럼 작동하는 행을 반환하도록 연결에 지시
    g.db.row_factory = sqlite3.Row

  return g.db
# close_db(): 설정 되었는지 확인하여 g.db 연결이 생성되었는지 확인
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
def init_db():
  db = get_db()

  # open_resource(): flaskr 패키지와 관련된 파일을 염
  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))

# click.command(): init_db 함수를 호출하고 사용자에게 성공 메시지를 표시하는 명령줄 명령의 정의
@click.command('init-db')
@with_appcontext
def init_db_command():
  init_db()
  click.echo('Initialized the database.')

def init_app(app):
  # app.teardown_appcontext(): 응답을 반환한 후 정리할 때 해당 함수를 호출하도록 Flask에 지시
  app.teardown_appcontext(close_db)
  # app.cli.add_command(): 호출할 수 있는 새 명령을 추가
  app.cli.add_command(init_db_command)