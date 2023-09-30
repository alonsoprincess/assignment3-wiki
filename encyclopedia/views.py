import random
from markdown2 import Markdown
from django.shortcuts import render
from django import forms

from . import util

def mdConverter(entryTitle):
    content = util.get_entry(entryTitle)
    md = Markdown()
    if content == None:
        return None
    else:
        return md.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entryTitle):
    entryPage = mdConverter(entryTitle)
    if entryPage == None:
        return render(request, "encyclopedia/error.html", {
            "message" : "This does not exist. Yet..."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle" : entryTitle,
            "entry" : entryPage
        })

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        value = mdConverter(search_entry)
        if (value is not None):
            return render(request, "encyclopedia/entry.html", {
                "entryTitle" : search_entry,
                "entry": value
            })
        else:
            closeMatch = []
            for entry in util.list_entries():
                if search_entry.lower() in entry.lower():
                    closeMatch.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entryTitle" : search_entry,
                "closeMatch" : closeMatch
            })
        
def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newPage.html")
    else:
        entryTitle = request.POST['title']
        entry = request.POST['content']
        if (util.get_entry(entryTitle) is not None):
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(entryTitle, entry)
            entry = mdConverter(entryTitle)
            return render(request, "encyclopedia/entry.html", {
                "entryTitle": entryTitle,
                "entry": entry
            })
        
def edit(request):
    if request.method == "POST":
        entryTitle = request.POST['entryTitle']
        entry = util.get_entry(entryTitle)
        return render(request, "encyclopedia/edit.html", {
            "entryTitle": entryTitle,
            "entry": entry
        })
    
def savePage(request):
    if request.method == "POST":
        entryTitle = request.POST['entryTitle']
        entry = request.POST['entry']
        util.save_entry(entryTitle, entry)
        entry = mdConverter(entryTitle)
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": entryTitle,
            "entry": entry
        })
    
def randomize(request):
    randomEntryTitle = random.choice(util.list_entries())
    randomEntry = mdConverter(randomEntryTitle)
    return render(request, "encyclopedia/entry.html", {
        "entryTitle": randomEntryTitle,
        "entry": randomEntry
    })