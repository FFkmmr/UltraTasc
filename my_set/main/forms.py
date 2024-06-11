from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    placeholders = {
        'username': 'Username..',
        'email': 'Email..',
        'password1': 'Enter password...',
        'password2': 'Re-enter Password...'
    }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field_name, placeholder in self.placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})