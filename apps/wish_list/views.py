from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Item, Wisher
from ..login_registration.models import User
import types

def index(request):
    return render(request, 'login_registration/index.html')

def dashboard(request):
    try:
        items = Item.objects.filter(added_by=request.session['user_id']) | \
            Item.objects.filter(users=request.session['user_id'])
        other_items = Item.objects.all().exclude(added_by=request.session['user_id'])
    except Item.DoesNotExist:
        items = None
        other_items = None
    context = {
        'items': items,
        'other_items': other_items
    }
    return render(request, 'wish_list/dashboard.html', context)

def create(request):
    return render(request, 'wish_list/create.html')

def add_item(request):
    if request.method != 'POST':
        return redirect(reverse('wish_list:create'))
    else:
        item = Item.objects.add_item(request.POST, request.session['user_id'])
        if isinstance(item, types.ListType):
            for error in item:
                messages.error(request, error)
            return redirect(reverse('wish_list:create'))
        else:
            messages.success(request, "Successfully added an item to your wish list!")
            return redirect(reverse('wish_list:dashboard'))

def display_item(request, id):
    item = Item.objects.get(id=id)
    added_by = User.objects.get(user=item.added_by.id)
    context = {
        'item': item,
        'wishers': Wisher.objects.filter(item=item).exclude(user=added_by)
    }
    return render(request, 'wish_list/display.html', context)

def add_to_list(request, id):
    Item.objects.add_to_list(id, request.session['user_id'], request.session['first_name'], request.session['last_name'])
    messages.success(request, "Successfully added item to Wish List!")
    return redirect(reverse('wish_list:dashboard'))

def remove(request, id):
    Wisher.objects.filter(user=request.session['user_id']).get(item=id).delete()
    messages.success(request, "Successfully removed item from your Wish List!")
    return redirect(reverse('wish_list:dashboard'))

def delete(request, id):
    Item.objects.get(id=id).delete()
    messages.success(request, "Successfully deleted item!")
    return redirect(reverse('wish_list:dashboard'))
