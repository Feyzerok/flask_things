from peewee import *
from playhouse.migrate import *

db = SqliteDatabase('data/em_resources.db')
migrator = SqliteMigrator(db)

class BaseModel(Model):
    class Meta:

        database = db

class Rubricator(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    level = IntegerField(null=True, verbose_name="Уровень")
    parrent = IntegerField(null=True, verbose_name="Родитель")
    title = TextField(null=True, verbose_name="Заголовок")  # STRING

    class Meta:
        db_table = 'rubricator'

class Resources(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    uin = CharField(unique=True, verbose_name="уникальное имя")  # STRING
    type = TextField(null=True, verbose_name="Тип", choices=(['1', "тип 1"], ['2', 'тип 2']))  # STRING
    title = TextField(null=True, verbose_name="Заголовок")  # STRING
    git_url = CharField(null=True, verbose_name="Адрес Git")  # STRING
    description = TextField(null=True, verbose_name="Описание")

    class Meta:
        db_table = 'resources'

class RubricatorLink(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    classificator = ForeignKeyField(column_name='rubricator_id', field='id', model=Rubricator, null=True)
    resources = ForeignKeyField(column_name='resources_id', field='id', model=Resources, null=True)

    class Meta:
        db_table = 'rubricator_link'

class Class(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    name = CharField(null=True, verbose_name="Класс")

    class Meta:
        db_table = 'Класс'

class Subject(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    name = CharField(null=True, verbose_name="Класс")

    class Meta:
        db_table = "Предмет"

class SubjectClass(BaseModel):
    id = PrimaryKeyField(unique=True, null=False)
    subject = ForeignKeyField(column_name='subject_id', field='id', model=Subject, null=True)
    Class = ForeignKeyField(column_name='class_id', field='id', model=Class, null=True)
    class Meta:
        db_table = 'Связка предмет-класс'

if __name__ == "__main__":
    with db:
        db.create_tables([Class, Subject, Resources, Rubricator, RubricatorLink, SubjectClass])

        #migrate(
        #    migrator.add_column('resources', 'class', ForeignKeyField(column_name='class_id', field='id', model=Class, null=True))
        #)



