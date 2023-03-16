from django import forms
from django.shortcuts import render
import markdown2
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random

from . import util

from markdown2 import markdown

class CreateNewPage(forms.Form):
    title = forms.CharField(label="Title", max_length=15)
    content = forms.CharField(label="stuff", widget=forms.Textarea(attrs={'style' : 'width: 50%; height:50%'}), max_length=200)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "all_pages" : True,
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
        "entries": search,
        "all_pages" : False,
        "name" : var,
    })
    return HttpResponseRedirect(reverse("name", kwargs={'var':var}))


def new(request):
    titles = util.list_entries()
    if request.method == "POST":
        form = CreateNewPage(request.POST) 
        if form.is_valid():
            new_title = str(form.cleaned_data["title"]).capitalize()
            content = str(form.cleaned_data["content"])
            if new_title.upper() in (title.upper() for title in titles):
                messages.error(request, 'Title already exists')
            else:
                file_path = 'entries/' + str(new_title) + '.md'
                with open(file_path, 'w') as f:
                    f.write(content)
                return HttpResponseRedirect(reverse("name", kwargs={'var':new_title}))

    return render(request, "encyclopedia/new.html", {
        "title" : CreateNewPage(),
        "error" : False
    })

def edit(request, edit_name):
    file_name = 'entries/' + edit_name + '.md'
    with open(file_name, 'r') as f:
        existing_content = f.read()
    if request.method == "POST":
        new_content = str(request.POST.get("input_content"))
        lines = new_content.split('\n')
        lines = [line.rstrip() for line in lines]
        new_content = '\n'.join(lines)
        if new_content.replace("\t",'').replace('\n','') == existing_content.replace("\t",'').replace('\n',''):
            return name(request, edit_name)
        else:
            with open(file_name, 'w') as f:
                f.write(new_content.rstrip())
            return name(request, edit_name)
    return render(request, 'encyclopedia/edit.html', {
        "content" : existing_content,
        "name" : edit_name,
    })

def random_page(request):
    entries = util.list_entries()
    page = random.choice(entries)
    return HttpResponseRedirect(reverse('name', kwargs={'var':page}))