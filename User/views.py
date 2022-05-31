from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserSignUpForm
from django.contrib.auth.decorators import login_required
from .models import pythonCode
from .forms import EditStatusForm
import csv

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            if request.user.is_authenticated:
                return redirect('Course-home')
            return redirect('User-login')
    else:
        form = UserSignUpForm()
    
    return render(request, 'User/signup.html', {'form': form, 'title': 'Sign Up'})

@login_required
def listcodes(request):
    context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)
    }
    return render(request,'User/list_codes.html',context=context)


@login_required
def detailcodes(request,index=1):
    code = pythonCode.objects.filter(user=request.user)[index-1]
    form = EditStatusForm(instance=code)
    if request.method == 'POST':
        form = EditStatusForm(request.POST,instance=code)
        if form.is_valid():
            form.save()
            return redirect('/list_codes/')
    
    
    context = {
        'title' : str(code),
        'code'  : code,
        'form' : form
    }
    return render(request,'User/detail_code.html',context)

@login_required
def download_data(request):
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Username','Session Key', 'Code', 'Output','Date','Time','Done','Feedback'])
        for code in pythonCode.objects.all():
            column = [code.username,code.session_key,code.codearea,code.output,code.added.strftime('%Y-%m-%d') , code.added.strftime('%H:%M'),code.Done,code.Feedback]
            writer.writerow(column)
        
        response['Content-Disposition'] = 'attachment; filename="codes.csv"'
        return response
    else:
        context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)
        }   
        return render(request,'User/list_codes.html',context=context)

