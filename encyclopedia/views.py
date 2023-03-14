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
    all = util.list_entries()
    var = str(request.POST.get("q")) # the input we got from the form 
    exist = False
    # if the input is in the list of titles/entries, redirect to the wiki/<title> page
    if var in all:
        return HttpResponseRedirect(reverse("name", kwargs={'var':var}))
    
    # to return all pages which has a sub string of given input
    search = []
    for one in all:
        if var in one:
            search += [one]
            exist = True
    if exist:
        return render(request, "encyclopedia/index.html", {
        "entries": search
    })
    return HttpResponseRedirect(reverse("name", kwargs={'var':var}))