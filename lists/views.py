from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    aList = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=aList)
            item.full_clean()
            item.save()            
            return redirect(aList)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': aList, 'error': error})

def new_list(request):
    aList = List.objects.create()
    item = Item(text=request.POST['item_text'], list=aList)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        aList.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(aList)
