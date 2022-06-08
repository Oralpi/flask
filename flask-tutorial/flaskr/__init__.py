import os
from flask import Flask
from . import db, auth, blog

def create_app(test_config=None):
  # Flask 인스턴스 생성
  # __name__: 현재 Python 모듈의 이름
  # instance_relative_config=True: 구성 파일이 인스턴스 폴더에 상대적임을 앱에 알림
  app = Flask(__name__, instance_relative_config=True)

  # 앱이 사용할 몇 가지 기본 구성을 설정
  # SECRET_KEY: Flask 및 확장 프로그램에서 데이터를 안전하게 유지하는데 사용
  # DATABASE: SQLite 데이터베이스 파일이 저장될 경로
  # app.instance_path: Flask가 인스턴스 폴더에 대해 선택한 경로
  app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))

  if test_config is None:
    # config.py가 존재하는 경우 인스턴스 폴더의 파일에서 가져온 값으로 기본 구성을 재정의
    app.config.from_pyfile('config.py', silent=True)
  else:
    # test_config: 팩토리로 전달할 수도 있으며, 인스턴스 구성 대신 사용
    app.config.from_mapping(test_config)

  try:
    # app.instance_path가 존재하는지 확인
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # 작동하는 애플리케이션을 볼 수 있도록 간단한 경로를 생성
  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  db.init_app(app)
  app.register_blueprint(auth.bp)
  app.register_blueprint(blog.bp)
  app.add_url_rule('/', endpoint='index')

  return app