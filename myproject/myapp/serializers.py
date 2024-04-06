from rest_framework import serializers

class SpreadsheetSerializer(serializers.Serializer):
    file = serializers.FileField()
    table_name = serializers.CharField()