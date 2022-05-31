import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from User.forms import EditStatusForm
from videos.models import Video
from User.models import pythonCode

@login_required
def home(request, index=1):
    context = {
        'main_video': Video.objects.all()[index-1],
        'videos': Video.objects.all(),
        'index': index,
        'title': 'Course ' + str(index),
        'form2' : False,
    }
    if request.method == "POST":
        
        print(request.POST)
        if(request.POST.get('codearea',None) != None):
            codeareadata = request.POST['codearea']

            url = 'https://api.jdoodle.com/v1/execute'
            myobj = {
                'clientId': '955c02a67dab8632da1bfda6b53d4fd3',
                'clientSecret': '4f50bf0ab404ca19efaae76d33ce378f90f569cf16e72fe26dc54939087b8f1',
                'script': codeareadata,
                'stdin': '',
                'language': 'python3',
                'versionIndex': 0
            }

            output_json = requests.post(url, json=myobj).json()
            output = output_json['output']
            output = output.replace('Jdoodle', 'Main').replace('jdoodle', 'main')
            
            if(not codeareadata.isspace() and len(codeareadata)):
                my_code = pythonCode.create(
                    request.user, codeareadata, output, request.session.session_key, request.user.username)
                my_code.save()
                context['form2_val'] = EditStatusForm(instance=my_code)
                context['form2'] = True
               

            context['code'] = codeareadata
            context['output'] = output
            context['my_code'] = my_code
            return render(request, 'Course/home.html', context=context)
        else:
            my_code = pythonCode.objects.filter(user=request.user).first()
            form = EditStatusForm(request.POST,instance=my_code)
            if form.is_valid():
                form.save()
            context['code'] = my_code.codearea
            context['form2'] = True
            context['form2_val'] = EditStatusForm(instance=my_code)
            context['output'] = my_code.output
            context['my_code'] = my_code
            return render(request, 'Course/home.html', context=context)

    else:
        return render(request, 'Course/home.html', context=context)
