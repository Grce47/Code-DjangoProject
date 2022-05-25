import traceback
from django.shortcuts import render
import sys
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
    output = ""
    if request.method == "POST":
        codeareadata = request.POST['codearea']
        try:
            #save original standart output reference

            original_stdout = sys.stdout
            sys.stdout = output #change the standard output to the file we created

            #execute code

            exec(codeareadata)
            sys.stdout.close()

            sys.stdout = original_stdout  #reset the standard output to its original value

            # finally read output from file and save in output variable

            
        except Exception as e:
            # to return error in the code
            e_type,e_val,e_tb = sys.exc_info()
            sys.stdout = original_stdout
            output = traceback.format_exc()
            
            x1 = output.find("File")
            x2 = output.find("File",x1+1,len(output)-1)

            tmp = ""
            for idx,ele in enumerate(output):
                if idx >= x2 or idx < x1:
                    tmp += ele
            
            output = tmp

    context = {
        'main_video' : Video.objects.all()[index-1],
        'videos' : Video.objects.all(),
        'index' : index,
        'title' : 'Course ' + str(index),
        'code' : codeareadata,
        'output' : output
    }
    if(not codeareadata.isspace() and len(codeareadata)):
        my_code = pythonCode.create(request.user,codeareadata,output,request.session.session_key)
        my_code.save()
    
    output = ""
    return render(request,'Course/home.html',context=context)
