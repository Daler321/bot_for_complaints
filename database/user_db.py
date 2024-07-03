from typing import Optional

import databases
import pydantic

import ormar
import sqlalchemy

DATABASE_URL = "sqlite:///db.sqlite"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

base_ormar_config = ormar.OrmarConfig(
    database=databases.Database(DATABASE_URL),
    metadata=sqlalchemy.MetaData(),
    engine=sqlalchemy.create_engine(DATABASE_URL),
)


class User(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="users")

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    number: str = ormar.String(max_length=15)

engine = sqlalchemy.create_engine(DATABASE_URL)

async def create_user(id, name, number):
  await User.objects.create(id=id, name=name, number=number)

async def is_user_exists(id):
   try:
    await User.objects.get(id=id)
    return True
   except:
    return False

async def update_user_name(user_id, new_name):
  user = await User.objects.get(id=user_id)
  user.name = new_name
  await user.update()

async def update_user_number(user_id, new_number):
  user = await User.objects.get(id=user_id)
  user.number = new_number
  await user.update()

async def take_user(user_id):
  user = await User.objects.get(id=user_id)
  return user

if __name__ == '__main__':
  base_ormar_config.metadata.create_all(base_ormar_config.engine)
