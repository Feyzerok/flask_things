import os
from flask_admin.helpers import get_form_data
from flask_admin.contrib.sqla import ModelView
from flask_admin import form, expose
from flask import redirect, flash, url_for
from markupsafe import Markup
from flask_admin.babel import gettext


"""Класс, позволяющий отображать relationship поля у таблицы resources в админке"""
class ResView(ModelView):
    column_hide_backrefs = False
    column_list = ('uin', 'type', 'title', 'git_url', 'description', 'class_name', 'subject_name')

class ThemeView(ModelView):
    column_hide_backrefs = False
    column_list = ('id', 'title', 'uid', 'resource_name', 'description')

class BuildsView(ModelView):
    STORAGE_PATH = os.path.abspath('data/temp')
    column_hide_backrefs = False
    column_list = ('product', 'uin', 'name', 'short_name', #'short_name_tr', "series_id",
                   'serie', 'version',
                   'organization_name', 'date', 'grade_name', 'subject_name', 'resource_name', 'make_build')

    # override the column labels
    column_labels = {

        'name': 'Название',
        'short_name': 'Короткое название',
        'version': 'Версия',
        'serie': 'Серия',
        'organization_name': 'Название организации',
        'date': 'Дата создания',
        'make_build': 'Запустить сборку'

    }

    form_extra_fields = {
        'file_png': form.FileUploadField('png file', base_path=STORAGE_PATH),
        'file_ico': form.FileUploadField('ico file', base_path=STORAGE_PATH)
    }

    def _format_make_build(view, context, model, name):

        if model.is_built:
            return 'Собрано'

        checkout_url = url_for('.checkout_view')

        _html = '''
                    <form action="{checkout_url}" method="POST">
                        <input id="build_id" name="build_id"  type="hidden" value="{build_id}">
                        <button type='submit'>Собрать</button>
                    </form
                '''.format(checkout_url=checkout_url, build_id=model.id)

        return Markup(_html)

    column_formatters = {
        'make_build': _format_make_build
    }

    @expose('checkout', methods=['POST'])
    def checkout_view(self):

        return_url = self.get_url('.index_view')

        form_data = get_form_data()

        if not form_data:
            print('ошибка 1')
            flash(gettext('Could not get form from request.'), 'error')
            return redirect(return_url)
        build_id = form_data['build_id']

        model = self.get_one(build_id)

        if model is None:
            print('ошибка 2')
            flash(gettext('Build not not found.'), 'error')
            return redirect(return_url)

        model.is_built = True

        try:
            self.session.commit()
            flash(gettext('Build, ID: {build_id}, set as built'.format(build_id=build_id)))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to set build, ID: {build_id}, as built'.format(build_id=build_id),
                          error=str(ex)), 'error')

        return redirect(return_url)

    def _change_path_data(self, _form):
        global STORAGE_PATH
        try:
            storage_file_png = _form.file_png.data

            if storage_file_png is not None:

                ext = storage_file_png.filename.split('.')[-1]
                filename = 'bg' + f'.{ext}'
                uin_in_model = str(_form.uin.data)

                if not os.path.exists(os.path.join(STORAGE_PATH, uin_in_model)):
                    os.mkdir(os.path.join(STORAGE_PATH, uin_in_model))

                storage_file_png.save(
                    os.path.join(STORAGE_PATH, uin_in_model, filename)
                )

                #_form.name.data = _form.name.data or storage_file.filename
                del _form.file_png

        except Exception as ex:
            print(ex)

        try:
            storage_file_ico = _form.file_ico.data

            if storage_file_ico is not None:

                ext = storage_file_ico.filename.split('.')[-1]
                filename = 'ico' + f'.{ext}'
                uin_in_model = str(_form.uin.data)

                if not os.path.exists(os.path.join(STORAGE_PATH, uin_in_model)):
                    os.mkdir(os.path.join(STORAGE_PATH, uin_in_model))

                storage_file_ico.save(
                    os.path.join(STORAGE_PATH, uin_in_model, filename)
                )

                #_form.name.data = _form.name.data or storage_file.filename
                del _form.file_ico

        except Exception as ex:
            print(ex)

        return _form

    #def _get_path(self, filename):
    #    if not self.base_path:
    #        raise ValueError('FileUploadField field requires base_path to be set.')
#
    #    if callable(self.base_path):
    #        return os.path.join(self.base_path(), 'build_folder', filename)
    #    return os.path.join(self.base_path, 'build_folder', filename)

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(BuildsView, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(BuildsView, self).create_form(obj)
        )

class ProductView(ModelView):
    column_hide_backrefs = False
    column_list = ('id', 'active', 'ean', 'price', 'grade', 'subject', 'serie')