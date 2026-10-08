from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Property, SavedProperty
from .forms import RegisterForm, PropertyForm


def home(request):

    featured_properties = Property.objects.filter(
        is_featured=True
    )[:6]

    latest_properties = Property.objects.all()[:6]

    return render(
        request,
        'home.html',
        {
            'featured_properties': featured_properties,
            'latest_properties': latest_properties
        }
    )


def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            send_mail(
            'Registration',
            'Hi {},\n\nRegistration done successfully. Thank you for registering.'.format(user.username),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
             )

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'login.html'
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect('home')


def properties(request):

    property_list = Property.objects.all()

    query = request.GET.get('q', '')
    purpose = request.GET.get('purpose', '')
    property_type = request.GET.get('type', '')

    if query:

        property_list = property_list.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(city__icontains=query)
        )

    if purpose:

        property_list = property_list.filter(
            purpose=purpose
        )

    if property_type:

        property_list = property_list.filter(
            property_type=property_type
        )

    return render(
        request,
        'properties.html',
        {
            'properties': property_list,
            'query': query,
            'purpose': purpose,
            'property_type': property_type
        }
    )


def property_detail(request, pk):

    property_obj = get_object_or_404(
        Property,
        pk=pk
    )

    is_saved = False

    if request.user.is_authenticated:

        is_saved = SavedProperty.objects.filter(
            user=request.user,
            property=property_obj
        ).exists()

    return render(request,'properties_detail.html',
        {
            'property': property_obj,
            'is_saved': is_saved
        }
    )


@login_required
def post_property(request):

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property_obj = form.save(
                commit=False
            )

            property_obj.owner = request.user

            property_obj.save()

            messages.success(
                request,
                'Property posted successfully!'
            )

            return redirect(
                'property_detail',
                pk=property_obj.pk
            )

    else:

        form = PropertyForm()

    return render(
        request,
        'post_property.html',
        {
            'form': form
        }
    )


@login_required
def save_property(request, pk):

    property_obj = get_object_or_404(
        Property,
        pk=pk
    )

    saved, created = SavedProperty.objects.get_or_create(
        user=request.user,
        property=property_obj
    )

    if not created:

        saved.delete()

        messages.info(
            request,
            'Property removed from saved properties.'
        )

    else:

        messages.success(
            request,
            'Property saved successfully.'
        )

    return redirect(
        'property_detail',
        pk=pk
    )


@login_required
def dashboard(request):

    my_properties = Property.objects.filter(
        owner=request.user
    )

    saved_properties = Property.objects.filter(
        savedproperty__user=request.user
    ).distinct()

    return render(
        request,
        'dashboard.html',
        {
            'my_properties': my_properties,
            'saved_properties': saved_properties
        }
    )


@login_required
def delete_property(request, pk):

    property_obj = get_object_or_404(
        Property,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        property_obj.delete()

        messages.success(
            request,
            'Property deleted successfully.'
        )

    return redirect('dashboard')


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name","")
        email = request.POST.get("email","")
        user_message = request.POST.get("message","")

        email_message = (
            "New message from your website\n\n"
            "Name: " + name + "\n"
            "Email: " + email + "\n"
            "Message:\n" + user_message
        )   
        send_mail(
            "New Contact Message",
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.CONTACT_EMAILS,
            fail_silently=False,
        )
        messages.success(
            request,
            "Your message has been sent successfully!"
        )

        return redirect("contact")

    return render(request, "contact.html")
