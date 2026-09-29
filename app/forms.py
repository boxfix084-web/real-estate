from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Property


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    first_name = forms.CharField(
        max_length=100,
        required=True
    )

    last_name = forms.CharField(
        max_length=100,
        required=True
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = [
            'title',
            'property_type',
            'purpose',
            'location',
            'city',
            'price',
            'bedrooms',
            'bathrooms',
            'area',
            'description',
            'image',
            'is_featured'
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter property title'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Locality / Area'
                }
            ),

            'city': forms.TextInput(
                attrs={
                    'placeholder': 'City'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'placeholder': 'Property price'
                }
            ),

            'bedrooms': forms.NumberInput(
                attrs={
                    'placeholder': 'Bedrooms'
                }
            ),

            'bathrooms': forms.NumberInput(
                attrs={
                    'placeholder': 'Bathrooms'
                }
            ),

            'area': forms.NumberInput(
                attrs={
                    'placeholder': 'Area in sq.ft'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your property...',
                    'rows': 5
                }
            ),
        }