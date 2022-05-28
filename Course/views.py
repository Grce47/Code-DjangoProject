import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from videos.models import Video
from User.models import pythonCode


@login_required
def home(request,index=1):
    context = {
        'main_video' : Video.objects.all()[index-1],
        'videos' : Video.objects.all(),
        'index' : index,
        'title' : 'Course ' + str(index)
    }
    return render(request,'Course/home.html',context=context)

@login_required
def runcode(request,index=1):
    if request.method == "POST":
        codeareadata = request.POST['codearea']

        url = 'https://api.jdoodle.com/v1/execute'
        myobj = {
            'clientId' : '955c02a67dab8632da1bfda6b53d4fd3',
            'clientSecret' : '4f50bf0ab404ca19efaae76d33ce378f90f569cf16e72fe26dc54939087b8f1',
            'script' : codeareadata,
            'stdin' : '',
            'language' : 'python3',
            'versionIndex' : 0
        }

        output_json = requests.post(url,json=myobj).json()
        output = output_json['output']
        output = output.replace('Jdoodle','Main').replace('jdoodle','main')

    
    if(not codeareadata.isspace() and len(codeareadata)):
        my_code = pythonCode.create(request.user,codeareadata,output,request.session.session_key,request.user.username)
        my_code.save()
    context = {
        'main_video' : Video.objects.all()[index-1],
        'videos' : Video.objects.all(),
        'index' : index,
        'title' : 'Course ' + str(index),
        'code' : codeareadata,
        'output' : output,
        'my_code' : my_code
    }
    return render(request,'Course/home.html',context=context)
