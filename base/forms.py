from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from base.models import Review, Item

class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

        def clean_password(self):
            password = self.clean_data.get('password')
            return password

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user

class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 6, })
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる
        self.fields['product'].widget = forms.HiddenInput(attrs={'readonly': 'readonly'})
        self.fields['reviewer'].widget = forms.HiddenInput(attrs={'readonly': 'readonly'})
    
    class Meta:
        model = Review
        fields = ['rate', 'title', 'comment', 'product', 'reviewer']