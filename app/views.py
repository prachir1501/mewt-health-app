# app/views.py
from datetime import datetime, timedelta
from distutils.log import log

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .models import *


@login_required
def home(request):
    patients = Patient.objects.filter(doctor=request.user)
    context = {
        'patients': patients,
    }
    return render(request, 'app/index.html', context)


@login_required
def detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    context = {
        'patient': patient,
    }
    return render(request, 'app/detail.html', context)


@login_required
def create(request):
    context = {}
    if request.method == 'GET':
        form = PatientForm()
        context['form'] = PatientForm()
        return render(request, 'app/create.html', context)
    elif request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            new = Patient()
            user = request.user
            new.doctor = user
            new.name = form['name'].value()
            new.age = form['age'].value()
            new.city = form['city'].value()
            new.appointment_date = form['appointment_date'].value()
            new.appointment_details = form['appointment_details'].value()
            new.save()
            return redirect('home')
        else:
            form = PatientForm()
            context['form'] = PatientForm()
            return render(request, 'app/create.html', context)
    return render(request, 'app/create.html', context)


@login_required
def update(request, id):
    patient = get_object_or_404(Patient, id=id)
    context = {
        'patient': patient
    }
    if request.method == 'GET':
        form = PatientForm(instance=patient)
        context['form'] = form
        return render(request, 'app/update.html', context)
    elif request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('detail', patient.id)
        else:
            form = PatientForm(instance=patient)
            context['form'] = form
            return render(request, 'app/update.html', context)
    return render(request, 'app/update.html', context)


@login_required
def delete(request, id):
    patient = get_object_or_404(Patient, id=id)
    if not request.user == patient.doctor:
        return redirect('detail', patient.id)
    else:
        name = patient.name
        patient.delete()
        context = {
            'name': name
        }
        return render(request, 'app/delete.html', context)


@login_required
def search(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'app/search.html', context)
    elif request.method == 'POST':
        try:
            id = int(request.POST.get('idInput'))
        except:
            return render(request, 'app/search.html', context)
        patients = Patient.objects.filter(pk=id, doctor=request.user)
        if len(patients) == 0:
            return render(request, 'app/no_search_results.html', context)

        context = {
            'patients': patients,
        }
        return render(request, 'app/search_results.html', context)

    return render(request, 'app/search.html', context)
