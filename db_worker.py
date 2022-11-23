
from models import Grade, Subject, Series, Products
from data.constant_subjects_grades_series import subjects, grades, series
import json
import os
from ast import literal_eval

def prepare_const_data(db,subjects, grades, series):
    subjects_to_add = [Subject(name=i) for i in subjects]
    grades_to_add = [Grade(name=i) for i in grades]
    series_to_add = [Series(name=i) for i in series]

    db.session.add_all(subjects_to_add)
    db.session.add_all(grades_to_add)
    db.session.add_all(series_to_add)

    db.session.commit()


def fill_products_data(db, path_to_json):
    with open(path_to_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        products_to_add = []
        for i in data['rows']:
            grades = literal_eval(i[8])
            grades_to_add = [db.session.query(Grade).filter_by(name=i).first() for i in grades]

            subjects = literal_eval(i[6])
            subjects_to_add = [db.session.query(Subject).filter_by(name=i).first() for i in subjects]

            serie = i[7]
            serie_to_add = [db.session.query(Series).filter_by(name=serie).first()]


            products_to_add.append(Products(id=i[0], active=i[1], ean=i[2], price=i[3], version=i[4], name=i[5],
                                            grade=grades_to_add, subject=subjects_to_add,
                                            serie=serie_to_add, contents=i[9],
                                            description=i[10], requirements=i[11], relise_date=i[12],
                                            help_pdf_link=i[13], win_link=i[14], mac_link=i[15], linux_link=i[16],
                                            reg_num_id=i[17], type_posob=i[18], cover=i[19], images=i[20],
                                            video=i[21], demo_info=i[22], update_info=i[23], distr_info=i[24],
                                            pdf_info=i[25], nix_update=i[26], mac_update=i[27], win_update=i[28],
                                            nix_demo=i[29], mac_demo=i[30], win_demo=i[31], android_link=i[32],
                                            android_update=i[33], android_demo=i[34], ios_link=i[35], ios_update=i[36],
                                            ios_demo=i[37]))
        db.session.add_all(products_to_add)

        db.session.commit()

if __name__ == "__main__":
    path_to_json = os.path.join('data', 'products.json')
    prepare_const_data(subjects, grades, series)

    fill_products_data(path_to_json)