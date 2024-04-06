import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SpreadsheetSerializer
from .models import create_dynamic_model
from rest_framework import status

from django.core.management import call_command
from django.db import connection
    
class SpreadsheetUploadView(APIView):    
    def post(self, request, *args, **kwargs):
        serializer = SpreadsheetSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            table_name = serializer.validated_data['table_name']

            # Check for missing data in request
            if 'table_name' not in request.data or 'file' not in request.data:
                return Response(
                    {
                        'code': 400,
                        'reason': 'Missing payload error: missing required fields. Please provide both table_name and file.',
                        'pointer': '/spreadsheet'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )            
                            
            # Validate file type
            if not file.name.endswith(('.xls', '.xlsx')): 
                return Response(
                    {
                        'code': 400,
                        'reason': 'Invalid payload error: Unsupported file format. Only xls and xlsx files are allowed.',
                        'pointer': '/spreadsheet' 
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Read the spreadsheet and extract column names
            df = pd.read_excel(file, sheet_name=0, header=0) 
            columns = df.columns.tolist()     

            # Check for missing values in the dataset
            if df.isnull().values.any():
                return Response(
                    {
                        'code': 400,
                        'reason': 'Spreadsheet blank row error: The uploaded spreadsheet contains blank rows. Please ensure all rows have data.',
                        'pointer': '/spreadsheet' 
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )     
            
            # Checking table existence
            if not self.table_exists(table_name):
                # Create the dynamic model
                DynamicModel = create_dynamic_model(table_name, columns)
                
                # Create the table in the database
                call_command('makemigrations', 'myapp')
                call_command('migrate', 'myapp')
                
                # Insert the data into the database
                for index, row in df.iterrows():
                    instance = DynamicModel(**{col: str(val) for col, val in row.items()})
                    instance.save()
                
                return Response({"message": f"Data uploaded successfully to {table_name}"}, status=status.HTTP_201_CREATED)

            else:
                # Compare table columns with request columns
                existing_columns = self.get_table_columns(table_name)
                if existing_columns != columns:
                    return Response(
                        {
                            'code': 409,
                            'reason': 'Mismatch error: Spreadsheet does not have the same format as the table.',
                            'pointer': '/columns'
                        },
                        status=status.HTTP_409_CONFLICT
                    )
                else: 
                    # Read existing data from the table
                    existing_data = pd.read_sql(f"SELECT * FROM {table_name}", connection)

                    # Append the new data from df to the existing data
                    combined_data = existing_data.append(df, ignore_index=True)

                    # Insert the combined data back into the database
                    combined_data.to_sql(table_name, connection, if_exists='append', index=False)

                    return Response({"message": f"Data uploaded successfully to {table_name}"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def table_exists(self, table_name):
        """
        Check if the table exists in the database.
        """         
        return table_name in connection.introspection.table_names()
    
    def get_table_columns(self, table_name):
        """
        Retrieve column names of the specified table.
        """
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
        columns = [col.name for col in cursor.description]
        return columns   