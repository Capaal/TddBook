from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    aList = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': aList})

def new_list(request):
    aList = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=aList)
    return redirect(f'/lists/{aList.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
