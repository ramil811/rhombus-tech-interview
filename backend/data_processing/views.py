from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import File
from . import process_file

# Create your views here.
class FileUploadView(View):
    def post(self, request):
        file = request.FILES['file']
        file_obj = File.objects.create(name=file.name, file=file)

        file_path = file_obj.file.path

        processed_data = process_file.process(file_path)

        return JsonResponse({'status': '200', 'processed_data': processed_data})
