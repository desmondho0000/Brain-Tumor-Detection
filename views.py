from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render,redirect  
from tensorflow import keras
from keras.preprocessing import image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
import numpy as np
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Prediction
from django.utils import timezone


model = keras.models.load_model('./models/Prediction_2.h5')

def index(request):
    context = {'a': 1}

    return render(request, 'main.html', context)

def logOut(request):
    logout(request)
    request.session.pop('username', None)  
    return redirect('homepage')  


def predictImage(request):
    if request.method == 'POST':
        if 'filePath' in request.FILES:     
            fileObj = request.FILES['filePath']
            fs = FileSystemStorage()
            filePathName = fs.save(fileObj.name, fileObj)
            testimage = fs.url(filePathName)
            img_path = os.path.join(fs.location, fileObj.name)  

            img = image.load_img(img_path, target_size=(150, 150))
            x = image.img_to_array(img)
            x /= 127.5
            x = np.expand_dims(x, axis=0)

            images = np.vstack([x])
            predictions = model.predict(images, batch_size=10)

            #-------------------------------------------------
            # this my logic, i put this only come out the result
            # because we need to check the accuracy is more than 0.5 
            if predictions[0] > 0.5:
                predictedLabel = 'Detect'
            else:
                predictedLabel = 'Non-Detect'
            
            
            confidence = 100 * np.max(predictions)
            #---------------------------------------
            

            #predictedLabel = labelInfo[np.argmax(predictions[0])]
            context = {'filePathName': testimage, 'predictedLabel': predictedLabel,'confidentLabel':confidence}

            Prediction.objects.create(
                username=request.user.username,
                patient_name=request.POST.get('patient_name'),
                image=fileObj,
                prediction_result=predictedLabel,
                confidence=confidence,
     
            )

            return render(request, 'predictImage.html', context)
        else:
            context = {'filePathName': None}
            return render(request, 'predictImage.html', context)
    else:
        return render(request, 'predictImage.html', {'filePathName': None})


def login(request):
    if request.method == 'POST':
        loginUser = request.POST.get('Login_username')
        Loginpwd = request.POST.get('Login_password') 
        user = authenticate(request, username=loginUser, password=Loginpwd)

        if user is not None:
            auth_login(request, user)
            request.session['username'] = user.username
            return redirect('homepage')
        else:
            return HttpResponse("Username and Password are not correct. Please try again." )


    return render(request, 'login.html')

def signUp(request):
    if request.method == 'POST':
        signUp_uname = request.POST.get('signUp_username')
        signUp_email = request.POST.get('signUp_email')
        signUp_pwd = request.POST.get('signUp_password')
        signUp_pwd2 = request.POST.get('signUp_password2')

        if User.objects.filter(username=signUp_uname).exists():
            return HttpResponse("This username is already taken. Please choose a different one.")

        if User.objects.filter(email=signUp_email).exists():
            return HttpResponse("This email is already taken. Please choose a different one.")

        
        if signUp_pwd == signUp_pwd2:
            my_user = User.objects.create_user(signUp_uname, signUp_email, signUp_pwd)
            my_user.save()
            return redirect('login')

    

    return render(request, 'signUp.html')


def userAcc(request):
    if 'username' in request.session:
        username = request.session['username']
        data = Prediction.objects.filter(username=username)
        if request.method == 'POST':
            prediction_id = request.POST.get('prediction_id')
            # Retrieve the prediction to be deleted
            try:
                prediction = Prediction.objects.get(pk=prediction_id, username=username)
                prediction.delete()
                return redirect('userAcc')  # Redirect back to the same page after deletion
            except Prediction.DoesNotExist:
                # Handle the case where the prediction does not exist
                return redirect('userAcc')  # Redirect to an error page or display an error message
        return render(request, 'userAcc.html', {'data': data})
    else:
        return HttpResponse("You are not logged in.")


