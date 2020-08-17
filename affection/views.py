from django.shortcuts import render,get_object_or_404, redirect

from .models import AgenceUser
from utilisateurs.models import User
from .forms import AgenceUserForm

# Create your views here.

def affectation_create(request, user_id=None):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = AgenceUserForm(request.POST, agent=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent affecté')
            return redirect('affectation:create')
        else:
            pass
    else:
        form = AgenceUserForm(agent=user)
    context = {
        'form': form
    }
    return render(request, 'affectation/create.html', context)
