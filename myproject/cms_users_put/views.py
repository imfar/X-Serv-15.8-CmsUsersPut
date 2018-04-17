from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Resource
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError


HEAD_COMUN = """<html><head><title>SARO-15.8 - CMS USERS PUT\
        </title></head><body><h2>SARO - 15.8 - CSM USERS PUT</h2>
        """  # cerrar etiquetas al utilizar


@csrf_exempt
def root_page(request):
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username + "<a href\
        ='/logout'>  Logout</a>"
    else:
        logged = "Not logged in. <a href='/login'>  Login</a>"

    recursos_DB = Resource.objects.all()
    lista = "<ul>"
    for my_rec in recursos_DB:
        lista += '<li><a href="/' + my_rec.name + '\
        ">' + my_rec.name + '</a></li>'
    lista += "</ul>"

    htmlAnswer = (HEAD_COMUN + "<b><i>" + logged + "</b></i>" +
    "<p>Los recursos hasta el momento son: </p>" + lista + "</body></html>")
    return HttpResponse(htmlAnswer)


@csrf_exempt
def a_page(request, resource):
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username + "<a href\
        ='/logout'>  Logout</a>"
        if request.method == "PUT":
            try:
                resource_DB = Resource.objects.get(name=resource)
                htmlAnswer = HEAD_COMUN + "<b><i>" + logged + "</b></i><br>\
                <br>" + resource_DB.cont + "</body></html>"
                # si el recurso YA existe, SE MUESTRA el contenido(body)
                return HttpResponse(htmlAnswer)
            except Resource.DoesNotExist:
                try:
                    new_resource = Resource(name=resource, cont=request.body)
                    new_resource.save()  # add recurso -- force_insert=True
                    htmlAnswer = (HEAD_COMUN + "<b><i>" + logged + "</b></i>\
                    <p><b>Nuevo Recurso: </b>\
                    <a href='/" + resource + "'>"
                    + resource + "</a> AÑADIDO.</p></body></html>")
                except IntegrityError:
                    htmlAnswer = HEAD_COMUN + "<p>ERROR al GUARDAR el RECURSO\
                    en la Base de Datos.</p></body></html>"
                return HttpResponse(htmlAnswer)

    else:
        logged = "Not logged in. <a href='/login'>  Login</a>"

    if request.method == "GET":
        try:
            resource_DB = Resource.objects.get(name=resource)
            htmlAnswer = HEAD_COMUN + "<b><i>" + logged + "</b></i><br><br>\
            " + resource_DB.cont + "</body></html>"
        except Resource.DoesNotExist:
            htmlAnswer = (HEAD_COMUN + "<b><i>" + logged + "</b></i>\
            <p>ERROR!! El recurso: <b>"
            + resource + "</b> NO existe.</p></body></html>")
        return HttpResponse(htmlAnswer)
    elif request.method == "PUT":
        htmlAnswer = HEAD_COMUN + "<b><i>" + logged + "</b></i>\
        <br><br>Error de AUTENTICACIÓN.</body></html>"
        return HttpResponse(htmlAnswer)
    else:
        htmlAnswer = HEAD_COMUN + "<b><i>" + logged + "</b></i><p><b>OH NO!\
        </b> Para este ejercicio, usa PUT o GET...\
        </p></body></html>"
        return HttpResponse(htmlAnswer)
