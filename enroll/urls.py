from django.urls import path
from .views import *
from accounts.views import login

app_name = "enroll"

urlpatterns = [
    path('',login),
    path('create/', patient_create, name='create'),
    path('patient_list/',patient_list,),
    path('form_list/<p_id>', form_list, name = 'forms'),
    path('patient/<p_id>/',update_patient,name ='update'),
    path('submitted/', successful,),
    path('pdetails/<pk>/', display_patient_detail),
    path('delete/<pk>/',delete_patient),
    path('dates/', date_form),
    path('patient_demo/', patient_demographics),
    path('diahis/', diabetes_history),
    path('previous/', previous),
    path('labtest/', lab_test),
    path('lipidprof/', lipid_profile),
    path('cardiac/', cardiac_enzymes),
    path('lead1/', lead1),
    path('preprocedure/', preprocedure),
    path('indprocedure/', indpreocedure),
    path('staged/', staged),
    path('ffr/', ffr),
    path('lesion1/', lesion1),
    path('stent1/', stent1),
    path('lesion2/', lesion2),
    path('stent2/', stent2),
    path('lesion3/', lesion3),
    path('stent3/', stent3),
    path('cardiac1/', cardiac_enzymes1),
    path('conco1/', concomitant1),
    path('adverse1/', adverse1),
    path('echo/', echo),
    path('vital/', vital_sign),
    path('lead2/', lead2),
    path('cardiac2/', cardiac_enzymes2),
    path('platelet/', platelet_therapy),
    path('conco2/', concomitant2),
    path('adverse2/', adverse2),
    path('onemonth/', onemonth),
    path('assessment/', assessment),
    path('lead3/', lead3),
    path('platelet2/', platelet_therapy2),
    path('conco3/', concomitant3),
    path('adverse3/', adverse3),
    path('6month/', sixmonth_followup),
    path('assessment2/', assessment2),
    path('lead4/', lead4),
    path('labtest2/', lab_test2),
    path('platelet3/', platelet_therapy3),
    path('conco4/', concomitant4),
    path('adverse4/', adverse4),
    path('12month/', twelvemonth_followup),
    path('assessment3/', assessment3),
    path('lvef_details/', lvef_details),
    path('lead5/', lead5),
    path('labtest3/', lab_test3),
    path('platelet4/', platelet_therapy4),
    path('conco5/', concomitant5),
    path('adverse5/',adverse5),
    path('24month/', twentyfourmonth_followup),
    path('assessment4/', assessment4),
    path('lead6/', lead6),
    path('platelet5/', platelet_therapy5),
    path('conco6/', concomitant6),
    path('adverse6/', adverse6),
    path('36month/', thirtysixmonth_followup),
    path('assessment5/', assessment5),
    path('adverse7/', adverse7),
    path('48month/', fourtyeight_followup),
    path('assessment6/', assessment6),
    path('adverse8/', adverse8),
    path('60month/', sixty_followup),
    path('assessment7/', assessment7),
    path('adverse9/', adverse9),
    path('endstudy/',endofstudy),
]