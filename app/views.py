from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    return render(
        request,
        'property_detail.html',
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

    return render(
        request,
        'contact.html'
    )