from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'textfield'})
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese su contraseña'

