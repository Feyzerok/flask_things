import datetime
from exts import db
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy_utils import ChoiceType

class Grade(db.Model):

    __tablename__ = "grade"

    id = db.Column(Integer(), primary_key=True)
    name = db.Column(String(20), nullable=False)

    def __str__(self):
        return self.name

class Subject(db.Model):

    __tablename__ = 'subject'

    id = db.Column(Integer(), primary_key=True)
    name = db.Column(String(20), nullable=False)

    def __str__(self):
        return self.name

class_resources_meta = Table(
    'grade_resources',
    db.metadata,
    db.Column('grade_id', Integer(), ForeignKey('grade.id')),
    db.Column('resource_id', Integer(), ForeignKey('resources.id')),
    extend_existing=True
)

subject_resources_meta = Table(
    'subject_resources',
    db.metadata,
    db.Column('subject_id', Integer(), ForeignKey('subject.id')),
    db.Column('resource_id', Integer(), ForeignKey('resources.id')),
    extend_existing=True
)

resources_themes_meta = Table(
    'resources_themes',
    db.metadata,
    db.Column('resource_id', Integer(), ForeignKey('resources.id')),
    db.Column('theme_id', Integer(), ForeignKey('themes.id')),
    extend_existing = True

)

resource_builds_meta = Table(
    'resource_builds',
    db.metadata,
    db.Column('resource_id', Integer(), ForeignKey('resources.id')),
    db.Column('build_id', Integer(), ForeignKey('builds.id')),
    extend_existing = True
)

subject_builds_meta = Table(
    'subject_builds',
    db.metadata,
    db.Column('subject_id', Integer(), ForeignKey('subject.id')),
    db.Column('build_id', Integer(), ForeignKey('builds.id')),
    extend_existing = True
)

grade_builds_meta = Table(
    'grade_builds',
    db.metadata,
    db.Column('grade_id', Integer(), ForeignKey('grade.id')),
    db.Column('build_id', Integer(), ForeignKey('builds.id')),
    extend_existing=True
)
resource_products_meta = Table(
    'resource_products',
    db.metadata,
    db.Column('resource_id', Integer(), ForeignKey('resources.id')),
    db.Column('product_id', Integer(), ForeignKey('products.id')),
    extend_existing = True
)

subject_products_meta = Table(
    'subject_products',
    db.metadata,
    db.Column('subject_id', Integer(), ForeignKey('subject.id')),
    db.Column('products_id', Integer(), ForeignKey('products.id')),
    extend_existing = True
)

grade_products_meta = Table(
    'grade_products',
    db.metadata,
    db.Column('grade_id', Integer(), ForeignKey('grade.id')),
    db.Column('products_id', Integer(), ForeignKey('products.id')),
    extend_existing=True
)
series_products_meta = Table(
    'series_products',
    db.metadata,
    db.Column('series_id', Integer(), ForeignKey('series.id')),
    db.Column('products_id', Integer(), ForeignKey('products.id')),
    extend_existing=True
)

class Resources(db.Model):

    __tablename__ = 'resources'

    TYPES = [
        ('шаблон', 'шаблон'),
        ('модель', 'модель')
    ]

    id = db.Column('id', Integer(), primary_key=True)
    uin = db.Column('Уникальное имя', String(20), nullable=False)
    type = db.Column(ChoiceType(TYPES))
    title = db.Column(String(60), nullable=False)
    git_url = db.Column('Адрес Git', String(30), nullable=False)
    description = db.Column(String(60))
    grade_name = db.relationship(Grade, secondary=class_resources_meta)
    subject_name = db.relationship(Subject, secondary=subject_resources_meta)

    def __repr__(self):
        return f'{self.uin}, {self.type}, {self.title}, {self.git_url}, {self.description},' \
               f' {self.class_name}, {self.subject_name}'

    def __str__(self):
        return self.title

class Rubricator(db.Model):

    __tablename__ = 'rubricator'

    id = db.Column(Integer(), primary_key=True)
    level = db.Column('Уровень', Integer(), nullable=False)
    parent = db.Column(Integer(), nullable=False)
    title = db.Column(String(20), nullable=False)

    def __repr__(self):
        return f'{self.level}, {self.parent}, {self.title}'

class Themes(db.Model):

    __tablename__ = 'themes'

    id = db.Column(Integer(), primary_key=True)
    title = db.Column(String(20), nullable=False)
    description = db.Column(String(60))
    uid = db.Column(Integer(), nullable=False)
    resource_name = db.relationship(Resources, secondary=resources_themes_meta)

    def __repr__(self):
        return f'{self.title}, {self.description}, {self.uid}, {self.resource_name}'

class Series(db.Model):

    __tablename__ = 'series'

    id = db.Column(Integer(), primary_key=True)
    name = db.Column(String(20), nullable=False)
    build = db.relationship('Builds', back_populates='serie')

    def __repr__(self):
        return f'{self.name}'

class Builds(db.Model):

    __tablename__ = 'builds'

    id = db.Column(db.Integer(), primary_key=True)
    uin = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    short_name = db.Column(db.String(15))
    short_name_tr = db.Column(db.String(20))
    series_id = db.Column(db.Integer(), ForeignKey('series.id'))
    serie = db.relationship('Series', back_populates='build')
    version = db.Column(db.String(10), nullable=False)
    date = db.Column(DateTime, default=datetime.datetime.now)
    organization_name = db.Column(db.String(20), nullable=False)
    grade_name = db.relationship(Grade, secondary=grade_builds_meta)
    subject_name = db.relationship(Subject, secondary=subject_builds_meta)
    resource_name = db.relationship(Resources, secondary=resource_builds_meta)
    is_built = db.Column(db.Boolean(), nullable=False, default=False)
    product_id = db.Column(db.Integer(), ForeignKey('products.id'))
    product = db.relationship('Products', back_populates='build')
    def __repr__(self):
        return f'Сборка {self.name}'

class Products(db.Model):

    __tablename__ = 'products'

    build = db.relationship('Builds', back_populates='product')

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Integer())
    ean = db.Column(db.Integer())
    price = db.Column(db.String(20))
    version = db.Column(db.String())
    name = db.Column(db.String())
    subject = db.relationship(Subject, secondary=subject_products_meta)
    serie = db.relationship(Series, secondary=series_products_meta)
    grade = db.relationship(Grade, secondary=grade_products_meta)
    resource = db.relationship(Resources, secondary=resource_products_meta)
    contents = db.Column(db.String())
    description = db.Column(db.String())
    requirements = db.Column(db.String())
    relise_date = db.Column(db.String())
    help_pdf_link = db.Column(db.String())
    win_link = db.Column(db.String())
    mac_link = db.Column(db.String())
    linux_link = db.Column(db.String())
    reg_num_id = db.Column(db.String())
    type_posob = db.Column(db.String())
    cover = db.Column(db.String())
    images = db.Column(db.String())
    video = db.Column(db.String())
    demo_info = db.Column(db.String())
    update_info = db.Column(db.String())
    distr_info = db.Column(db.String())
    pdf_info = db.Column(db.String())
    nix_update = db.Column(db.String())
    mac_update = db.Column(db.String())
    win_update = db.Column(db.String())
    nix_demo = db.Column(db.String())
    mac_demo = db.Column(db.String())
    win_demo = db.Column(db.String())
    android_link = db.Column(db.String())
    android_update = db.Column(db.String())
    android_demo = db.Column(db.String())
    ios_link = db.Column(db.String())
    ios_update = db.Column(db.String())
    ios_demo = db.Column(db.String())

    def __repr__(self):
        return f'{self.name}'


#Base.metadata.create_all(engine)
