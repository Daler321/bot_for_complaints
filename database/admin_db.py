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


class Admin(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="admins")

    id: int = ormar.Integer(primary_key=True)
    banned: bool = ormar.Boolean(default=False)
    approved: bool = ormar.Boolean(default=False)
    trys: int = ormar.Integer(default=0)

engine = sqlalchemy.create_engine(DATABASE_URL)

async def create_admin(id):
  await Admin.objects.create(id=id)

async def is_admin_exists(id):
   try:
    await Admin.objects.get(id=id)
    return True
   except:
    return False
  
async def is_admin_approved(id):
  admin =  await Admin.objects.get(id=id)
  return admin.approved
  
async def is_admin_banned(id):
  admin =  await Admin.objects.get(id=id)
  return admin.banned
   
async def try_approve(id, password):
  admin = await Admin.objects.get(id=id)
  
  if password == '123':
    await aprove_admin(id)
    return 'Approved'
  elif admin.trys + 1 > 3:
    await ban_admin(id)
    return 'Banned'
  else:
    admin.trys += 1
    await admin.update()
    return f'You have {3 - admin.trys} trys'

async def ban_admin(admin_id):
  admin = await Admin.objects.get(id=admin_id)
  admin.banned = True
  await admin.update()

async def aprove_admin(admin_id):
  admin = await Admin.objects.get(id=admin_id)
  admin.approved = True
  await admin.update()

async def take_aproved_admins():
  admins = await Admin.objects.all()
  return [x for x in admins if x.approved]

if __name__ == '__main__':
  base_ormar_config.metadata.create_all(base_ormar_config.engine)
