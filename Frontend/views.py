import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
from django.shortcuts import render,redirect
import matplotlib.pyplot as plt
import numpy as np
from django.contrib import messages
from Frontend.models import Registration

def confidence_level(request):
    model = load_model(r"keras_model.h5", compile=False)
    class_names = open(r"labels.txt", "r").readlines()

    camera = cv2.VideoCapture(0)
    cv2.namedWindow("Webcam Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Webcam Image", 800, 600)
    camera.set(3, 640)
    camera.set(4, 480)

    start_time = time.time()  # Get the current time
    time_limit = 30  # Set the time limit to 1 minute

    predicted_classes = []

    while True:
        ret, image = camera.read()
        image=cv2.flip(image,1)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.uint8)

        prediction = model.predict(np.expand_dims(image, axis=0) / 255.0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        predicted_classes.append(class_name)

        class_text = "Class: " + class_name[2:]
        confidence_text = class_text + ":" + str(np.round(confidence_score * 100))[:-2] + "%"
        cv2.putText(image, confidence_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        confidence_bar_length = int(confidence_score * 150)
        cv2.rectangle(image, (10, 80), (10 + confidence_bar_length, 90), (0, 255, 0), -1)


        cv2.imshow("Webcam Image", image)

        keyboard_input = cv2.waitKey(1)

        elapsed_time = time.time() - start_time  # Calculate the elapsed time

        if elapsed_time >= time_limit:  # Check if the time limit has been reached
            break

        if keyboard_input == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

    percentage_confidence =  round(predicted_classes.count('0 Confident\n') / len(predicted_classes) * 100, 2)

    if percentage_confidence < 50:
        confidence_level = 'Low'
    elif 50 <= percentage_confidence < 75:
        confidence_level = 'Medium'
    else:
        confidence_level = 'High'

    non_confident_percentage = 100 - percentage_confidence

    context = {
        'percentage_confidence': percentage_confidence,
        'non_confident_percentage': non_confident_percentage,
        'confidence_level': confidence_level,
    }
    return render(request, 'emotion_analysis.html', context)

def Emotion_analysis(req):
    return render(req,"emotion_analysis.html")

def Home(req):
    return render(req,"Home.html")

def Login_Pg(req):
    return render(req,"Login_Pg.html")



def Registration_Pg(req):
    return render(req,"Registration_pg.html")

def Registration_save(request):
    if request.method == "POST":
        nm = request.POST.get('uname')
        em = request.POST.get('email')
        passw = request.POST.get('password')
        registration = Registration(username=nm, Email=em, Password=passw)
        registration.save()
        return redirect(Login_Pg)

def Login_fun(request):
    if request.method=="POST":
        nm=request.POST.get('txt')
        pwd=request.POST.get('password')
        if Registration.objects.filter(username=nm,Password=pwd).exists():
            request.session['username']=nm
            request.session['Password']=pwd
            messages.success(request, "Logged in Successfully")
            return redirect(Home)
        else:
            messages.warning(request, "Check Your Credentials")
            return redirect(Login_Pg)
    else:
        messages.warning(request, "Check Your Credentials Or Sign Up ")
        return redirect(Login_Pg)

def Logout_fn(request):
    del request.session['username']
    del request.session['Password']
    messages.success(request, "Logged Out Successfully")
    return redirect(Login_Pg)