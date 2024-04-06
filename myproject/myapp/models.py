from django.db import models

def create_dynamic_model(table_name, columns):
    fields = {
        'id': models.AutoField(primary_key=True),
    }
    for column in columns:
        fields[column] = models.CharField(max_length=255)  # Assuming all data are strings
    return type(table_name, (models.Model,), {
        '__module__': __name__,
        **fields,
    })