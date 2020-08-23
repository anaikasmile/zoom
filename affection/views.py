from django.shortcuts import render,get_object_or_404, redirect

from .models import AgenceUser
from utilisateurs.models import User
from .forms import AgenceUserForm
from django.contrib import messages

# Create your views here.

def affectation_create(request, user_id=None):
    user = get_object_or_404(User, id=user_id)  
    try:
        affectation = AgenceUser.objects.get(agent = user)
        form = AgenceUserForm(instance=affectation, agent=None,agence=None)
    except AgenceUser.DoesNotExist:
        form = AgenceUserForm(agent=user, agence=None)

    if request.method == "POST":
        form = AgenceUserForm(request.POST, agent=user, agence=None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent affecté')
            return redirect(request.path)
        else:
            pass
    
        
    context = {
        'form': form
    }
    return render(request, 'affectation/create.html', context)
