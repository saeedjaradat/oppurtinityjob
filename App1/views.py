from django.shortcuts import render,redirect
from.import models
from.models import labour,company
from django.contrib import messages

def index(request):
    return render(request,'index.html')

def cregister(request):
    return render(request,'companies.html')

def login(request):
    return render(request,'login.html')

def clogin(request):
    return render(request,'comlogin.html')

def lsignup(request):
    if request.method=='POST':
        errors = labour.objects.labour_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            models.Register(request)
            return redirect('/')


def csignup(request):
    if request.method=='POST':
        errors = labour.objects.companies_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/cregister')
        else:
            models.company_Register(request)
            return redirect('/cregister')

def lsignin(request):
    
    if models.lab_Login(request):
       return redirect('/labourpage')
    else:
        return redirect('/login')

def csignin(request):
    if models.comp_Login(request):
       return redirect('/companypage')
    else:
        return redirect('/clogin')

def jobboard(request):
    context={
        'labours':models.get_labour_info(request),
        'positions':models.get_position_info(request),
    }
    return render (request,'jobboard.html',context)

def position(request):
    return render(request,'position.html')

def addposition(request):
    if request.method=='POST':
        models.add_position(request)
    return redirect ('/position')

def apply(request,position_id):
    models.apply_to_position(request,position_id)
    return redirect('/jobboard')

def view(request,position_id):
    context={
    'position':models.get_position(request,position_id)
    }
    return render(request,'view.html',context)

def companypage(request):
    context={
    'company':models.get_companie(request),
    }
    return render (request,'companypage.html',context)

def labourpage(request):
    context={
        'labours':models.get_labour_info(request),
        'positions':models.get_position_info(request),
    }
    return render (request,'labourpage.html',context)