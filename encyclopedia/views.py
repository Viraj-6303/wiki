from django.shortcuts import render
import markdown2
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse


from . import util

from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def name(request, var):
    var.capitalize()
    try:
        entry = markdown(util.get_entry(var))
        return render(request, "encyclopedia/search.html", {
            "name" : var,
            "entry": entry,
            "exist" : True,})
    except:
        return render(request, "encyclopedia/search.html", {
            "entry": var,
            "exist": False,
        }) 
    
def search(request):
    var = str(request.POST.get("q"))
    return HttpResponseRedirect(reverse("name", kwargs={'var':var}))
    