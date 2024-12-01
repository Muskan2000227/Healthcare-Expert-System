"""
URL configuration for healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from healthcareapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path("admin/", admin.site.urls),
    path("Forgotpass",views.fpass,name="forgotpass"),


    path("Login",views.login,name="login"),
    path("error",views.error,name="error"),
     path("logingoogle",views.logingoogle,name="logingoogle"),
    path("google-login/", views.google_login, name="google_login"),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("logout",views.logout,name="logout"),

    path("Signup",views.signup,name="signup"),
    path("Checkotp",views.check_otp,name="check_otp"),
    path("",views.index,name="index"),
    path("contact",views.contactus,name="contact"),
    path("base",views.base),
    path("thanku",views.thanku),
    path("thankureg",views.thankureg),
    path("sidebar",views.sidebar),
    path("uprofile",views.Userprofile,name="uprofile"),
    path("changepassw",views.chngepass,name="change"),
    path("sidebar1",views.sidebar1,name="sidebar1"),
    path("editprf",views.edprf,name="editprf"),
  
    path("calculator",views.calculators,name="calculator"),
    path("bmi",views.bmi,name="bmi"),
    path("bmr",views.bmr,name="bmr"),
    path('bmr_chart/', views.bmr_chart, name='bmr_chart'),
    path('calorie', views.calorie_intake, name='calorie'),
    path('ideal', views.ideal_body_weight, name='ideal'),
    path('hydration', views.hydration, name='hydration'),
    path('bloodpressure', views.blood_pressure, name='bloodpress'),
    path('diabetes', views.diabetes, name='diabetes'),
    path('anxiety', views.anxiety, name='anxiety'),
    path('depression', views.depression, name='depression'),
    path('drug', views.drugs, name='drug'),
    path('supplement', views.supplements, name='supplement'),
    path('drugshow/<int:id>/', views.drugshow, name='drugshow'),
    path('supplementshow/<int:id>/', views.supplementshow, name='supplementshow'),
    path('body',views.body,name="body"),
    path('symptoms/<int:id>/',views.symptom,name="symptoms"),
    path('disease',views.disease_view,name="disease"),
    path('diseaseanalysis',views.diseaseanalysis,name="diseaseanalysis"),
    path('diabkidanalysis',views.diabkidanalysis,name="diabkidanalysis"),
    path('neurologanalysis',views.neurologanalysis,name="neurologanalysis"),
    path('digestiveanalysis',views.digestiveanalysis,name="digestiveanalysis"),
    path('respiratoryanalysis',views.respiratoryanalysis,name="respiratoryanalysis"),
    path('cardio1',views.cardio1,name="cardio1"),
    path('cardio2',views.cardio2,name="cardio2"),
    path('cardio3',views.cardio3,name="cardio3"),
    path('cardio4',views.cardio4,name="cardio4"),
    path('cardio5',views.cardio5,name="cardio5"),
    path('cardio6',views.cardio6,name="cardio6"),
    path('cardio7',views.cardio7,name="cardio7"),
    path('diab1',views.diab1,name="diab1"),
    path('diab2',views.diab2,name="diab2"),
    path('diab3',views.diab3,name="diab3"),
    path('diab4',views.diab4,name="diab4"),
    path('diab5',views.diab5,name="diab5"),
    path('diab6',views.diab6,name="diab6"),
    path('diab7',views.diab7,name="diab7"),
    path('neuro1',views.neuro1,name="neuro1"),
    path('neuro2',views.neuro2,name="neuro2"),
    path('neuro3',views.neuro3,name="neuro3"),
    path('neuro4',views.neuro4,name="neuro4"),
    path('neuro5',views.neuro5,name="neuro5"),
    path('neuro6',views.neuro6,name="neuro6"),
    path('neuro7',views.neuro7,name="neuro7"),
    path('dig1',views.dig1,name="dig1"),
    path('dig2',views.dig2,name="dig2"),
    path('dig3',views.dig3,name="dig3"),
    path('dig4',views.dig4,name="dig4"),
    path('dig5',views.dig5,name="dig5"),
    path('dig6',views.dig6,name="dig6"),
    path('dig7',views.dig7,name="dig7"),
    path('resp1',views.resp1,name="resp1"),
    path('resp2',views.resp2,name="resp2"),
    path('resp3',views.resp3,name="resp3"),
    path('resp4',views.resp4,name="resp4"),
    path('resp5',views.resp5,name="resp5"),
    path('resp6',views.resp6,name="resp6"),
    path('resp7',views.resp7,name="resp7"),
    path('disdisorder',views.disdisorder,name="disdisorder"),
    path('disorder1',views.disorder1,name="disorder1"),
    path('mentaldis',views.mentaldis,name="mentaldis"),
    path('healthexpense',views.healthexpense,name="healthexpense"),
    path('diseasecards',views.diseasecards,name="diseasecards"),
    path('disordercards',views.disordercards,name="disordercards"),
    path('anxanalysis',views.anxanalysis,name="anxanalysis"),
    path('depanalysis',views.depanalysis,name="depsnalysis"),
    path('mentaldis1',views.mentaldis1,name="mentaldis1"),
    path('mentaldis2',views.mentaldis2,name="mentaldis2"),
    path('mentaldis3',views.mentaldis3,name="mentaldis3"),
    path('mentaldis4',views.mentaldis4,name="mentaldis4"),
    path('mentaldis5',views.mentaldis5,name="mentaldis5"),
    path('mentaldis6',views.mentaldis6,name="mentaldis6"),
    path('anx1',views.anx1,name="anx1"),
    path('anx2',views.anx2,name="anx2"),
    path('anx3',views.anx3,name="anx3"),
    path('anx4',views.anx4,name="anx4"),
    path('anx5',views.anx5,name="anx5"),
    path('anx6',views.anx6,name="anx6"),
    path('anx7',views.anx7,name="anx7"),
    path('dep1',views.dep1,name="dep1"),
    path('dep2',views.dep2,name="dep2"),
    path('dep3',views.dep3,name="dep3"),
    path('dep4',views.dep4,name="dep4"),
    path('dep5',views.dep5,name="dep5"),
    path('dep6',views.dep6,name="dep6"),
    path('dep7',views.dep7,name="dep7"),
    path('health1',views.health1,name="health1"),
    path('health2',views.health2,name="health2"),
    path('health3',views.health3,name="health3"),
    path('health4',views.health4,name="health4"),
    path('health5',views.health5,name="health5"),
    path('health6',views.health6,name="health6"),
    path('health7',views.health7,name="health7"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('dash',views.dash,name="dash"),
    path('cdisease_prediction',views.cdisease_prediction,name="cdisease_prediction"),
    path('nprediction',views.nprediction,name="nprediction"),
    path('digprediction',views.digprediction,name="digprediction"),
    path('dkprediction',views.dkprediction,name="dkprediction"),
    path('rprediction',views.rprediction,name="rprediction"),
    path('arima_result',views.arima_result,name="arima_result"),
    path('predictionmain',views.predictionmain,name="predictionmain"),
    path('preddiscards',views.preddiscards,name="preddiscards"),
    path('predictiondiscards',views.predictiondiscards,name="predictiondiscards"),
    path('mentalprediction',views.mentalprediction,name="mentalprediction"),
    path('anxietyprediction',views.anxietyprediction,name="anxietyprediction"),
    path('depressprediction',views.depressprediction,name="depressprediction"),
    path('healthprediction',views.healthprediction,name="healthprediction"),
    path('heartupload',views.heartupload,name="heartupload"),
    path('heartresult',views.heartresult,name="heartresult"),
    path('predictheart',views.predictheart,name="predictheart"),
    path('about',views.about,name="about"),
    path('eda',views.eda,name="eda"),
    path('eda1',views.eda1,name="eda1"),
    path('edagraph',views.edagraph,name="edagraph"),
    path('edagraph1',views.edagraph1,name="edagraph1"),
    path('edagraph2',views.edagraph2,name="edagraph2"),
    path('edagraph3',views.edagraph3,name="edagraph3"),
    path('edagraph4',views.edagraph4,name="edagraph4"),
    path('edagraph5',views.edagraph5,name="edagraph5"),
    path('progheartcards',views.progheartcards,name="progheartcards"),
    path('chatbot',views.chatbot,name="chatbot"),
    path('chatbotnav',views.chatbotnav,name="chabottnav"),
    path('navbar',views.navbar,name="navbar"),
    path('blogs',views.blogs,name="blogs"),
    path('blog/<int:blog_id>/',views.blog_detail,name="blog_detail"),
    path('news',views.news,name="news"),
    path('identify_pill', views.identify_pill, name='identify_pill'),
    path('pill-search', views.pill_search, name='pill_search'),



    
  


    
   
]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)




