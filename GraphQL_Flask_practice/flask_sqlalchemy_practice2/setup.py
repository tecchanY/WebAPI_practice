from ast import literal_eval
from database.model_people import ModelPeople
from database.model_planet import ModelPlanet
from database import base
import logging
import sys

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# ファイルがimportされた際にプログラムが動かないようにするためにif文を記述
if __name__ == "__main__":
    # def init_db():
    log.info("Drop and Create database {}".format(base.db_name))
    base.Base.metadata.drop_all(base.engine)
    base.Base.metadata.create_all(base.engine)

    log.info("Insert Planet data in database")
    with open("database/data/planet.json", "r") as file:
        data = literal_eval(file.read())
        for record in data:
            planet = ModelPlanet(**record)
            base.db_session.add(planet)
        base.db_session.commit()

    log.info("Insert People data in database")
    with open("database/data/people.json", "r") as file:
        data = literal_eval(file.read())
        for record in data:
            planet = ModelPeople(**record)
            base.db_session.add(planet)
        base.db_session.commit()


# 最初にこのファイルを実行して初期データベースを作成
# init_db()としてapi.pyと同時に実行する必要はなし

# The next file setup.py will create the database database.db and load data into it.
# Data is available in the project repository in the shape of JSON files:

# people.json
# planet.json

# In the database folder create another data sub folder and place the JSON files in it.
# Your path should be something like:

# example/database/data/people.json
# example/database/data/planet.json

# Remark: It is important to import ModelPeople before ModelPlanet because the
# relationship between the two classes has been defined in the ModelPlanet class.
# This means SQLAlchemy requires ModelPeople to be created first in order to be
# able to create ModelPlanet.
