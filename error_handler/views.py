from django.http.response import Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.core.exceptions import ViewDoesNotExist

# Create your views here.
def handle_400_error(request, exception):
  context = {
    'error_code': 400,
    'message': 'Bad Request',
    'hint': "Server can't/won't process the request due to client error. \
Don't repeat this request without modification."
  }
  return render(
    request = request,
    template_name = 'error_handler/error.html',
    context = context,
    status = 400)

def handle_403_error(request, exception):
  context = {
    'error_code': 403,
    'message': 'Forbidden',
    'hint': "You are unauthorized to access this."
  }
  return render(
    request = request,
    template_name = 'error_handler/error.html',
    context = context,
    status = 403)

def handle_404_error(request, exception):
  context = {
    'error_code': 404,
    'message': 'Not Found',
    'hint': "Requested content can't be found in the server."
  }
  return render(
    request = request,
    template_name = 'error_handler/error.html',
    context = context,
    status = 404)

def handle_500_error(request):
  context = {
    'error_code': 500,
    'message': 'Internal Server Error',
    'hint': "This is an edge case contact the developer."
  }
  return render(
    request = request,
    template_name = 'error_handler/error.html',
    context = context,
    status = 500)
