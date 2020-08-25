from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        #user.save(commit=False)  # load the profile instance created by the signal
        person = user.person
        person.birth_date = form.cleaned_data.get('birth_date')
        person.tel = form.cleaned_data.get('tel').as_e164
        person.sexe = form.cleaned_data.get('sexe')
        person.adresse = form.cleaned_data.get('adresse')
        
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
            person.save()
        return user