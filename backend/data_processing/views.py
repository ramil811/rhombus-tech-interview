from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import File
from . import process_file
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(View):
    def post(self, request):
        file = request.FILES['file']
        # check if file uploaded is a csv or excel file type and return error if not
        if not file.name.endswith('.csv') and not file.name.endswith('.xlsx'):
            return JsonResponse({'status': '400', 'message': 'File must be a csv or excel file type'}, status=400)
        
        # save file to database
        file_obj = File.objects.create(name=file.name, file=file)

        file_path = file_obj.file.path

        # process the file and infer data types
        processed_data, data_types = process_file.infer_and_convert_data_types(file_path)

        # return the processed data and data types
        return JsonResponse({
            'status': '200',
            'processed_data': processed_data,
            'data_types': data_types,
        }, status=200)
