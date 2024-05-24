from django.urls import path
from Frontend import views

urlpatterns=[
    path('Registration_Pg/',views.Registration_Pg,name="Registration_Pg"),
    path('Registration_save/',views.Registration_save,name="Registration_save"),

    path('Login_Pg/',views.Login_Pg,name="Login_Pg"),
    path('Login_fun/',views.Login_fun,name="Login_fun"),

    path('Home/',views.Home,name="Home"),
    path('Emotion_analysis/',views.Emotion_analysis,name="Emotion_analysis"),

    path('confidence_level/',views.confidence_level,name="confidence_level"),
    path('Logout_fn/',views.Logout_fn,name="Logout_fn"),

]