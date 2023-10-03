import string

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import Response

import json

from . import models


# Create your views here.

@api_view()
def register_dummy(request):
    # generate random username
    charset = string.ascii_letters


    user = models.CustomUser(username='dummy', password='dummy')
    user.save()
    return Response({'user': user.username})
