from django.shortcuts import render
import json

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *

def index(request):
  students = Student.objects.all().values()
  template = loader.get_template('index.html')
  return HttpResponse(template.render({'students':students}, request))

def get_students(request):
      if request.method == 'GET':
          try:
            students = Student.objects.all().values('name', 'city')
    
            return JsonResponse({'students': list(students)})
          except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
      return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
def add_student(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      student = Student(name=data['New'], city=data['NewYork'])
      student.save()
      return JsonResponse({'success': True, 'student': {'name': student.name, 'city': student.city}})
    except Exception as e:
      return JsonResponse({'error': str(e)}, status=500)
  return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def update_student(request, student_id):
  if request.method == 'PUT':
    try:
      data = json.loads(request.body)
      student = Student.objects.get(id=student_id)
      student.name = data['name']
      student.city = data['city']
      student.save()
      return JsonResponse({'success': True, 'student': {'name': student.name, 'city': student.city}})
    except Student.DoesNotExist:
      return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
      return JsonResponse({'error': str(e)}, status=500)
  return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def delete_student(request, student_id):
  if request.method == 'DELETE':
    try:
      student = Student.objects.get(id=student_id)
      student.delete()
      return JsonResponse({'success': True})
    except Student.DoesNotExist:
      return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
      return JsonResponse({'error': str(e)}, status=500)
  return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
