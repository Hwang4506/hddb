from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Info, Answer

class InfoResource(resources.ModelResource):
    # widget=ForeignKeyWidget(Info, 'info')
    # name = fields.Field(column_name='name', attribute='Info',
    #                           widget=ForeignKeyWidget(Info, 'name'))
    # name = fields.Field(column_name='name', attribute='Info', widget=widgets.ForeignKeyWidget(Info, 'name'))

    class Meta:
        model = Info

        fields = ('id', 'name', 'ph', 'message', 'create_date')
        # export_order = ('id', 'name', 'ph', 'message', 'create_date', 'memo')
        # fields = ('info', 'name', 'author', 'memo', 'create_date')
        # export_order = ('info', 'name', 'memo', 'author', 'create_date')