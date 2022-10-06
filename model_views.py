from flask_admin.model import BaseModelView
from peewee import ForeignKeyField, PrimaryKeyField


class MyView(BaseModelView):


    def get_pk_value(self, model):
        return self.model.id

    def scaffold_list_columns(self):
        columns = []

        for n, f in self._get_model_fields():
            # Verify type
            field_class = type(f)

            if field_class == ForeignKeyField:
                columns.append(n)
            elif self.column_display_pk or field_class != PrimaryKeyField:
                columns.append(n)

        return columns