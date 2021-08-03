from re import T
from typing import Text
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import Patient, Question, Result
from .forms import *
from datetime import date, time
import csv, io

# Create your views here.

def display_patient_detail(request,pk):
    patients = Patient.objects.filter(p_id=pk)
    results = Result.objects.filter(p_id=pk).order_by('q_id')

    if "exit" in request.POST:
        return redirect('/patient_list/')
    context = {
            "patients": patients,
            'results': results,
        }
    return render(request, "enroll/patient_result.html", context)

def details_csv(request,pk):
    i = pk
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename=patient-{i}.csv"
    
    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    results = Result.objects.filter(p_id=pk).order_by('q_id')

    # Add column headings to the csv file
    writer.writerow(['ID','Question', 'Answer'])

    # Loop Thu and output
    for result in results:
        writer.writerow([result.q_id.q_id ,result.q_id.q_text, result.ans_text])

    return response

def successful(request):
    global i
    patients = Patient.objects.get(p_id=i)
    if request.method == "POST":
        return redirect('/create/')
    context = {
        "patients": patients
    }
    return render(request, "enroll/filled_successfully.html", context)

def patient_create(request):
    global i
    form = PatientForm()
    if request.method == "POST":
        print('Receiving a post request')
        if "create" in request.POST:
            print("create clicked")
            form = PatientForm(request.POST)
            if form.is_valid():
                patientform = PatientForm({
                    #'p_id': give_pid(),
                    'f_name': form.cleaned_data['f_name'],
                    'l_name': form.cleaned_data['l_name'],
                    'age': form.cleaned_data['age']
                })
                patientform.save()
                print('Patient Created')
            i=Patient.objects.latest('p_id').p_id
            print(i)
            return redirect('/dates/')

        
    context = {
        "form": form
    }
    return render(request, "enroll/patient_create.html", context)

def patient_list(request):
    patients = Patient.objects.all().order_by('p_id')
    if 'searched' in request.POST:
        try:
            search = request.POST['search']
            search = search[0].upper()
        except:
            pass
        searched_patient = Patient.objects.filter(f_name__contains=search)
        context = {
            'searched_patient':searched_patient,
        }
        return render(request,'enroll/patient_list.html',context)

    if 'exit' in request.POST:
        return redirect('/create/')
    
    context ={
        'patients':patients,
    }
    return render(request,'enroll/patient_list.html',context)

def upload(request, pk):
    global i
    x=Result.objects.filter(p_id = pk)[0]
    print(x)
    i=x.p_id.p_id
    if request.method == "POST":
        #form = imp_exp(request.POST, request.FILES)
        #i = request.POST['p_id']
        f = request.FILES['file']

        if not f.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return redirect('/patient_list/')
        Result.objects.filter(p_id = pk).delete()
        data_set = f.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            _, created = Result.objects.update_or_create(
                p_id = Patient.objects.get(p_id = i),
                q_id = Question.objects.get(q_id = column[0]),
                ans_text = column[2]
            )
        return redirect('/create/') 
    
    return render(request, "enroll/upload_csv.html")

def form_list(request,p_id):
    global i
    i = p_id
    patient = Patient.objects.get(p_id = i)
    lst=[]
    for j in Result.objects.filter(p_id = i):
        lst.append(j.q_id)
    print(lst)
    return render(request, 'enroll/form_list.html', {"patient": patient, "result": lst})

def update_patient(request,p_id):
    global i
    i = p_id
    patient = Patient.objects.get(p_id = i)
    form = PatientForm(request.POST or None,instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST or None, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/patient_list/')
    
    return render(request,'enroll/update_patient.html',{'patient':form})

def delete_patient(request,pk):
    patient = Patient.objects.get(p_id = pk)
    patient.delete()

    return redirect('/patient_list/')
            
# First Page of Form

def date_form(request):
    global ques_id, i
    ques_id = 0

    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    numberform = NumberInput(initial={'ans_text': 0})
    textform = TextInput(initial={'ans_text': "Dr. "})
    patient = Patient.objects.get(p_id=i)
    date_ques1 = Question.objects.filter(q_id__gte=1, q_id__lte=2)
    date_ques2 = Question.objects.filter(q_id=3)
    number_ques = Question.objects.filter(q_id=4)
    text_ques = Question.objects.filter(q_id=5)


    if request.method == 'POST':
        # If answers already exists
        Exists(1, 5)
        # Adding Latest Answers

        ans_text = request.POST.getlist('ans_text')
       
        dateform = DateTime(request.POST)
        numberform = NumberInput(request.POST)
        textform = TextInput(request.POST)

        for date in ans_text[0:3]:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': date})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[3]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/patient_demo/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "patient": patient,
        "dateques1": date_ques1,
        "dateques2": date_ques2,
        "numberques": number_ques,
        "textques": text_ques,
        "dateform": dateform,
        "numberform": numberform,
        "textform": textform,
    }
    return render(request, "enroll/dates.html", context)

# Demographics + vital signs

def patient_demographics(request):
    global ques_id, i
    ques_id = 5

    # demographic
    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    ageform = NumberInput(initial={'ans_text': 0})
    sexform = SexInput(initial={'ans_text': 'Male'})
    addressform = TextInput(initial={'ans_text': "-"})
    phoneform = NumberInput(initial={'ans_text': 0})

    dob_ques = Question.objects.filter(q_id=6)
    age_ques = Question.objects.filter(q_id=7)
    sex_ques = Question.objects.filter(q_id=8)
    address_ques = Question.objects.filter(q_id__gte=9, q_id__lte=11)
    phone_ques = Question.objects.filter(q_id=12)

    # vital
    heartrateform = NumberInput(initial={'ans_text': 0})
    bpform = TextInput()
    whbform = FloatInput(initial={'ans_text': 0.0})

    hr_ques = Question.objects.filter(q_id=13)
    bp_ques = Question.objects.filter(q_id=14)
    weight_hight_bmi_ques = Question.objects.filter(q_id__gte=15, q_id__lte=17)

    if request.method == 'POST':
        # If answers already exists
        Exists(6, 17)
        # Adding Latest Answers

        ans_text = request.POST.getlist('ans_text')

        dateform = DateTime(request.POST)
        ageform = NumberInput(request.POST)
        sexform = SexInput(request.POST)
        addressform = TextInput(request.POST)
        phoneform = NumberInput(request.POST)
        heartrateform = NumberInput(request.POST)
        bpform = TextInput(request.POST)
        whbform = FloatInput(request.POST)

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        quesform = SexInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[2]})
        quesform.save()

        for add in ans_text[3:6]:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': add})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[6]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[7]})
        quesform.save()

        bp = request.POST.getlist("bp[]")
        print(bp)
        blps = '/'.join(bp)
        print(blps)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': blps})
        quesform.save()

        for ans in ans_text[8:11]:
            quesform = FloatInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        if "next" in request.POST:
            return redirect('/diahis/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "dob_ques": dob_ques,
        "age_ques": age_ques,
        "sex_ques": sex_ques,
        "address_ques": address_ques,
        "phone_ques": phone_ques,
        "dateform": dateform,
        "ageform": ageform,
        "sexform": sexform,
        "addressform": addressform,
        'phoneform': phoneform,

        'hrques': hr_ques,
        'bpques': bp_ques,
        'whbques': weight_hight_bmi_ques,
        'hrform': heartrateform,
        'bpform': bpform,
        'whbform': whbform,
    }
    return render(request, "enroll/patient_demo.html", context)

def diabetes_history(request):
    global ques_id, i
    ques_id = 22
    diabetesform = YesNoUNK()
    durationform = NumberInput(initial={'ans_text': 0})
    textform = TextInput(initial={'ans_text': "-"})
    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    NYHAform = NYHAClass()

    diabetes_ques = Question.objects.filter(q_id=23)
    type_ques = Question.objects.filter(q_id=25)
    yesnounk_ques1 = Question.objects.filter(q_id__gte=26, q_id__lte=29)  # CAD
    yesnounk_ques2 = Question.objects.filter(
        q_id__gte=30, q_id__lte=40)  # Medical Histort
    yesnounk_ques3 = Question.objects.filter(
        q_id=41)                     # If yes question
    yesnounk_ques4 = Question.objects.filter(
        q_id__gte=43, q_id__lte=44)  # LVEF and new added question
    number_ques = Question.objects.filter(
        q_id=45)                        # -do-
    date_ques = Question.objects.filter(
        q_id=46)                          # -do-
    if_ques = Question.objects.filter(q_id=47)  # Angina
    nyha_ques = Question.objects.filter(q_id=55)  # NYHA Class

    if request.method == 'POST':
        # If answers already exists
        Exists(23, 56)
        # Adding Latest Answers

        diabetesform = YesNoUNK(request.POST)
        textform = TextInput(request.POST)
        durationform = NumberInput(request.POST)
        dateform = DateTime(request.POST)
        NYHAform = NYHAClass(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ans[]')

        quesform = YesNoUNK({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No' or ans[0] == 'UNK'):
            get_ques()
        else:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

        diab = request.POST.getlist('diab[]')
        if(diab[0] == 'None'):
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': diab[0]})
            quesform.save()
        else:
            dia = '/'.join(diab)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dia})
            quesform.save()

        # CAD and Medical history
        for val in ans_text[0:15]:
            quesform = YesNoUNK({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        dis = request.POST.getlist('dis[]')
        quesform = YesNoUNK({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dis[0]})
        quesform.save()
        if dis[0] == 'No' or dis[0] == 'UNK':
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dis[1]})
            quesform.save()

        for val in ans_text[15:17]:
            quesform = YesNoUNK({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[17]})
        quesform.save()

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[18]})
        quesform.save()

        # Angina Status
        dia = request.POST.getlist('Dia1[]')
        print(dia)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dia[0]})
        quesform.save()
        if dia[0] == 'None' or dia[0] == 'Non-ST Elevation MI (NSTEMI)':
            ques_id = 54
        elif dia[0] == 'ST Elevation MI (STEMI)':
            ques_id = 49
            for val in dia[1:4]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()
            ques_id = 54
        elif dia[0] == 'Unstable Angina':
            ques_id = 47
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dia[4]})
            quesform.save()
            ques_id = 54
        elif dia[0] == 'Stable Angina':
            ques_id = 48
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dia[5]})
            quesform.save()
            ques_id = 54

        elif dia[0] == 'Silent Ischemia':
            ques_id = 52
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dia[6]})
            quesform.save()
            ques_id = 54
        elif dia[0] == 'Angina Equivalent':
            ques_id = 53
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dia[7]})
            quesform.save()

        quesform = NYHAClass({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[19]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/previous/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'diabetesform': diabetesform,
        'durationform': durationform,
        'dateform': dateform,
        'textform': textform,
        'NYHAform': NYHAform,
        'diabetes_ques': diabetes_ques,
        'type_ques': type_ques,
        'yesnounkques1': yesnounk_ques1,
        'yesnounkques2': yesnounk_ques2,
        'yesnounk_ques3': yesnounk_ques3,
        'yesnounk_ques4': yesnounk_ques4,
        'number_ques': number_ques,
        'date_ques': date_ques,
        'if_ques': if_ques,
        'nyha_ques': nyha_ques,
    }

    return render(request, "enroll/diahis.html", context)

# PCI from Q=61

def previous(request):
    global ques_id, i
    ques_id = 60
    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    numberform = NumberInput(initial={'ans_text': 0})
    textform = TextInput(initial={'ans_text': 'None'})

    yesno_ques = Question.objects.filter(q_id=61)  # Yes/No
    date_ques = Question.objects.filter(q_id=62)  # Date
    number_ques = Question.objects.filter(q_id__gte=63, q_id__lte=65)  # CASS
    text_ques = Question.objects.filter(q_id=66)

    if request.method == 'POST':

        Exists(61, 66)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        numberform = NumberInput(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        for val in ans_text[2:5]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        proc = request.POST.getlist('procedure[]')
        proc_new = [string for string in proc if string != ""]
        if(proc_new == []):
            get_ques()
        else:
            proc = ','.join(proc_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': proc})
            quesform.save()

        if "next" in request.POST:
            return redirect('/labtest/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "dateform": dateform,
        'numberform': numberform,
        'textform': textform,
        'yesnoform': yesnoform,
        "yesno_ques": yesno_ques,
        'date_ques': date_ques,
        'number_ques': number_ques,
        "text_ques": text_ques,
    }
    return render(request, "enroll/previous.html", context)

# Lab from question 70

def lab_test(request):
    global ques_id, i
    ques_id = 69
    date_form = DateTime(initial={'ans_text': date.today()})
    lab_codeform = LabCodes()
    lab_resultform = FloatInput(initial={'ans_text': 0})
    lab_unitform = LabUnit()

    date_ques = Question.objects.filter(q_id=70)
    labpara_ques = Question.objects.filter(q_id__gte=71, q_id__lte=84)

    if request.method == 'POST':

        Exists(70, 84)

        date_form = DateTime(request.POST)
        lab_codeform = LabCodes(request.POST)
        lab_resultform = FloatInput(request.POST)
        lab_unitform = LabUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        skip = 0
        while (skip != (len(ans_text)-1)):
            get_ques()
            skip = skip+1
            quesform = LabCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = FloatInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = LabUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lipidprof/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "date_ques": date_ques,
        'labpara_ques': labpara_ques,
        "date_form": date_form,
        'lab_codeform': lab_codeform,
        'lab_resultform': lab_resultform,
        'lab_unitform': lab_unitform,
    }
    return render(request, 'enroll/lab.html', context)

# Questions for LIPID start from 90

def lipid_profile(request):
    global ques_id, i
    ques_id = 89
    date_form = DateTime(initial={'ans_text': date.today()})
    lab_codeform = LabCodes()
    lab_resultform = NumberInput(initial={'ans_text': 0})
    lab_unitform = LabUnit()

    date_ques = Question.objects.filter(q_id=90)
    labpara_ques = Question.objects.filter(q_id__gte=91, q_id__lte=94)

    if request.method == 'POST':

        Exists(90, 94)

        date_form = DateTime(request.POST)
        lab_codeform = LabCodes(request.POST)
        lab_resultform = NumberInput(request.POST)
        lab_unitform = LabUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        skip = 0
        while (skip != len(ans_text)-1):
            get_ques()
            skip = skip+1
            quesform = LabCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/cardiac/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "date_ques": date_ques,
        'labpara_ques': labpara_ques,
        "date_form": date_form,
        'lab_codeform': lab_codeform,
        'lab_resultform': lab_resultform,
        'lab_unitform': lab_unitform,
    }
    return render(request, 'enroll/lipid.html', context)

# Questions start from 100

def cardiac_enzymes(request):

    global ques_id, i
    ques_id = 99

    date_form = DateTime(initial={'ans_text': date.today()})
    cardiac_codeform = CardiacCodes()
    done_form = CardiacDone()
    cardiac_resultform = NumberInput(initial={'ans_text': 0})
    cardiac_unitform = CardiacUnit(initial={'ans_text': 0})

    date_ques = Question.objects.filter(q_id=100)
    cardiac_ques = Question.objects.filter(q_id__gte=101, q_id__lte=104)

    if request.method == 'POST':

        Exists(100, 104)

        date_form = DateTime(request.POST)
        cardiac_codeform = CardiacCodes(request.POST)
        done_form = CardiacDone(request.POST)
        cardiac_resultform = NumberInput(request.POST)
        cardiac_unitform = CardiacUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        skip = 0
        while skip != len(ans_text)-1:
            get_ques()
            skip = skip+1
            quesform = CardiacDone({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = CardiacUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip + 1
            quesform = CardiacCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lead1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "date_ques": date_ques,
        'cardiac_ques': cardiac_ques,
        "date_form": date_form,
        'cardiac_codeform': cardiac_codeform,
        'done_form': done_form,
        'cardiac_resultform': cardiac_resultform,
        'cardiac_unitform': cardiac_unitform,
    }
    return render(request, 'enroll/cardiac1.html', context)

# Question from 110

def lead1(request):
    global ques_id, i
    ques_id = 109

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    no_abform = NormalAbnormal()
    textform = TextInput(initial={'ans_text': 'None'})
    numberform = NumberInput(initial={'ans_text': 0})

    yesno_ques = Question.objects.filter(q_id=110)
    no_ab_ques = Question.objects.filter(q_id=112)
    ifabnoraml = Question.objects.filter(q_id=113)
    st_ques = Question.objects.filter(q_id=114)
    cond_ques = Question.objects.filter(q_id=115)
    qrs_ques = Question.objects.filter(q_id=116)

    if request.method == 'POST':

        Exists(110, 116)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        no_abform = NormalAbnormal(request.POST)
        textform = TextInput(request.POST)
        numberform = NumberInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')
        cond = request.POST.getlist('Conduction[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = NormalAbnormal({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if(ans_text[0] == 'Normal'):
            if "next" in request.POST:
                return redirect('/preprocedure/')
            elif "home" in request.POST:
                return redirect('/submitted/')
        else:
            get_ques()

            # ST Deviation
            if(st[0] == 'No'):
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': st[0]})
                quesform.save()
            else:
                st_new = ','.join(st[1:])
                print(st_new)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': st_new})
                quesform.save()

            # Conduction abnormality
            if(cond[0] == 'No'):
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': cond[0]})
                quesform.save()
            else:
                cond_new = ','.join(cond[1:])
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': cond_new})
                quesform.save()

            # QRS
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/preprocedure/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques': yesno_ques,
        'no_ab_ques': no_ab_ques,
        'ifabnoraml': ifabnoraml,
        'st_ques': st_ques,
        'cond_ques': cond_ques,
        'qrs_ques': qrs_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'no_abform': no_abform,
        'numberform': numberform,
    }
    return render(request, "enroll/lead.html", context)

# Question from 120

def preprocedure(request):
    global ques_id, i
    ques_id = 119

    textform = TextInput(initial={'ans_text': 'None'})
    yesnoform = YesNo()
    numberform = NumberInput(initial={'ans_text': '0'})

    asprin_ques = Question.objects.filter(q_id=120)
    tick_ques1 = Question.objects.filter(q_id=121)
    dia_ques = Question.objects.filter(q_id=122)
    tick_ques2 = Question.objects.filter(q_id=123)

    if request.method == 'POST':

        Exists(120, 123)

        yesnoform = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        asprin = request.POST.getlist('asprin[]')
        pre = request.POST.getlist('pre2[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
        else:
            asp_new = ','.join(asprin)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': asp_new})
            quesform.save()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()
        if ans_text[1] == 'No':
            get_ques()
        else:
            pre_new = ','.join(pre)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': pre_new})
            quesform.save()

        if "next" in request.POST:
            return redirect('/indprocedure/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'asprin_ques': asprin_ques,
        'tick_ques1': tick_ques1,
        'dia_ques': dia_ques,
        'tick_ques2': tick_ques2,
        'yesnoform': yesnoform,
    }
    return render(request, "enroll/preprocedure.html", context)

# Question = 130

def indpreocedure(request):
    global ques_id, i
    ques_id = 129

    fundform = FundChoice()
    dateform = DateTime(initial={'ans_text': date.today()})
    timeform = Time()
    numberform = NumberInput(initial={'ans_text': 0})
    vesselform = Vessel()
    yesnoform = YesNo()
    vascularform = Vascular()
    textform = TextInput()

    fund_ques = Question.objects.filter(q_id=130)
    date_ques = Question.objects.filter(q_id=131)
    time_ques = Question.objects.filter(q_id__gte=132, q_id__lte=133)
    guide_ques = Question.objects.filter(q_id=134)
    score_ques = Question.objects.filter(q_id=135)
    LMCA_ques = Question.objects.filter(q_id=136)
    vessel_ques = Question.objects.filter(q_id__gte=137, q_id__lte=138)
    stage_ques = Question.objects.filter(q_id=139)
    vascular_ques = Question.objects.filter(q_id=140)
    yesno_ques = Question.objects.filter(q_id__gte=141, q_id__lte=142)

    if request.method == 'POST':

        Exists(130, 143)

        fundform = FundChoice(request.POST)
        dateform = DateTime(request.POST)
        timeform = Time(request.POST)
        textform = TextInput(request.POST)
        numberform = NumberInput(request.POST)
        yesnoform = YesNo(request.POST)
        vesselform = Vessel(request.POST)
        vascularform = Vascular(request.POST)

        ans_text = request.POST.getlist('ans_text')
        guide = request.POST.getlist('guide[]')
        lmca = request.POST.getlist('lmca[]')
        therapy = request.POST.getlist('therapy[]')

        quesform = FundChoice({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        for time in ans_text[2:4]:
            quesform = Time({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': time})
            quesform.save()

        if(guide == []):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': guide[0]})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        if(lmca[0] == 'No'):
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': lmca[0]})
            quesform.save()
        else:
            lmca_new = ','.join(lmca)+'% Stenosis'
            print(lmca_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': lmca_new})
            quesform.save()

        for val in ans_text[5:7]:
            quesform = Vessel({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[7]})
        quesform.save()

        quesform = Vascular({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[8]})
        quesform.save()

        for val in ans_text[9:11]:
            quesform = Vessel({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        therapy_new = [string for string in therapy if string != ""]
        if therapy_new == []:
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': therapy_new})
            quesform.save()

        if "next" in request.POST:
            return redirect('/staged/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'fund_ques': fund_ques,
        'date_ques': date_ques,
        'time_ques': time_ques,
        'guide_ques': guide_ques,
        'score_ques': score_ques,
        'LMCA_ques': LMCA_ques,
        'vessel_ques': vessel_ques,
        'stage_ques': stage_ques,
        'vascular_ques': vascular_ques,
        'yesno_ques': yesno_ques,

        'fundform': fundform,
        'dateform': dateform,
        'timeform': timeform,
        'numberform': numberform,
        'yesnoform': yesnoform,
        'vesselform': vesselform,
        "vascularform": vascularform,
    }
    return render(request, "enroll/indprocedure.html", context)

def staged(request):
    global ques_id, i
    ques_id = 150
    yesno_form = YesNo()
    date_form = DateTime(initial={'ans_text': date.today()})
    multiple_choiceform = ReasonForStaging()
    other_form = TextInput(initial={'ans_text': 'None'})

    yesno_ques = Question.objects.filter(q_id=151)
    date_ques = Question.objects.filter(q_id=152)
    reason_ques = Question.objects.filter(q_id=153)
    other_ques = Question.objects.filter(q_id=154)

    if request.method == 'POST':

        Exists(151, 154)

        yesno_form = YesNo(request.POST)
        date_form = DateTime(request.POST)
        multiple_choiceform = ReasonForStaging(request.POST)

        ans = request.POST.getlist('ans_text')
        text = request.POST.getlist('text[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[1]})
        quesform.save()

        if ans[2:] == []:
            get_ques()
        else:
            quesform = ReasonForStaging({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[2:]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': text[0]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/ffr/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "yesno_ques": yesno_ques,
        'date_ques': date_ques,
        'reason_ques': reason_ques,
        'other_ques': other_ques,


        "yesno_form": yesno_form,
        'date_form': date_form,
        'multiple_choiceform': multiple_choiceform,
        'other_form': other_form,
    }
    return render(request, "enroll/staged.html", context)

def ffr(request):
    global ques_id, i
    ques_id = 160
    yesno_form = YesNo()
    date_form = DateTime(initial={'ans_text': date.today()})
    ffr_choiceform2 = FFRChoice2()
    ffr_valueform = FloatInput(initial={'ans_text': 0.0})
    select_form = TextInput(initial={'ans_text': '-'})

    yesno_ques = Question.objects.filter(q_id=161)
    ifyes_ques = Question.objects.filter(q_id=162)
    date_ques = Question.objects.filter(q_id=163)
    site_ques = Question.objects.filter(q_id=164)
    value_ques = Question.objects.filter(q_id=165)
    prepci_ques = Question.objects.filter(q_id=166)
    yesno2_ques = Question.objects.filter(q_id=167)
    select_ques = Question.objects.filter(q_id=168)

    if request.method == 'POST':

        Exists(161, 168)

        yesno_form = YesNo(request.POST)
        date_form = DateTime(request.POST)
        ffr_choiceform2 = FFRChoice2(request.POST)
        ffr_valueform = FloatInput(request.POST)

        ans = request.POST.getlist('ans_text')
        yn = request.POST.getlist('y/n[]')
        yn1 = request.POST.getlist('yn1[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn[0]})
        quesform.save()
        if (yn[0] == 'No'):
            get_ques()
        else:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn[1]})
            quesform.save()

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        quesform = FFRChoice2({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[1]})
        quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[2]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()
        if (yn1[0] == 'No'):
            get_ques()
        else:
            if(yn1[1] == 'Calcium'):
                yn_new = yn1[1]+': Arc=' + yn1[2] + \
                    ', Length=' + yn1[3] + ', Depth=' + yn1[4]
            else:
                yn_new = yn1[1]

            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn_new})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[3]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/lesion1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "yesno_ques": yesno_ques,
        'ifyes_ques': ifyes_ques,
        'date_ques': date_ques,
        "site_ques": site_ques,
        'value_ques': value_ques,
        'prepci_ques': prepci_ques,
        'yesno2_ques': yesno2_ques,
        'select_ques': select_ques,

        "yesno_form": yesno_form,
        "date_form": date_form,
        'ffr_choiceform2': ffr_choiceform2,
        "ffr_valueform": ffr_valueform,
        "select_form": select_form,
    }
    return render(request, "enroll/ffr.html", context)

def lesion1(request):
    global ques_id, i
    ques_id = 174
    date_form = DateTime(initial={'ans_text': date.today()})
    cass_form = NumberInput(initial={'ans_text': 0})
    prepci_form = PrePciForm()
    length_form = FloatInput(initial={'ans_text': 0})
    choice_form = LessionChoice1()
    stent_usedform = NumberInput(initial={'ans_text': 0})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=175)
    questions2a = Question.objects.filter(q_id=176)
    questions2b = Question.objects.filter(q_id__gte=177, q_id__lte=178)
    questions3 = Question.objects.filter(q_id=179)
    questions4 = Question.objects.filter(q_id=180)
    questions5 = Question.objects.filter(q_id=181)
    questions6 = Question.objects.filter(q_id=182)
    questions7 = Question.objects.filter(q_id=183)
    questions8 = Question.objects.filter(q_id=184)
    questions9 = Question.objects.filter(q_id=185)
    questions11 = Question.objects.filter(q_id=187)
    questions12 = Question.objects.filter(q_id__gte=188, q_id__lte=193)
    questions13 = Question.objects.filter(q_id=194)
    questions14 = Question.objects.filter(q_id=195)
    question15 = Question.objects.filter(q_id=196)

    if request.method == 'POST':

        Exists(175, 197)

        date_form = DateTime(request.POST)
        cass_form = NumberInput(request.POST)
        prepci_form = PrePciForm(request.POST)
        length_form = FloatInput(request.POST)
        choice_form = LessionChoice1(request.POST)
        stent_usedform = NumberInput(request.POST)
        yesno_form = YesNo(request.POST)

        ans_text = request.POST.getlist('ans_text')

        print(ans_text, len(ans_text))

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        for ans in ans_text[1:4]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = PrePciForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        # Thrombus Question and if yes then dropdown 0-5
        thrombus = request.POST.getlist('thrombus[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': thrombus[0]})
        quesform.save()
        if (thrombus[0] == 'No'):
            get_ques()
        else:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': thrombus[1]})
        quesform.save()

        for ans in ans_text[5:8]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        med = request.POST.getlist('med[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': med[0]})
        quesform.save()

        if (med[0] == 'No'):
            get_ques()
        else:
            quesform = LessionChoice1({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': med[1]})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[8]})
        quesform.save()

        for ans in ans_text[9:15]:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        yesno1 = request.POST.getlist('yesno1[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yesno1[0]})
        quesform.save()

        if (yesno1[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno1[1]})
            quesform.save()

        yesno2 = request.POST.getlist('yesno2[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yesno2[0]})
        quesform.save()

        if (yesno2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/stent1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "questions1": questions1,
        'questions2a': questions2a,
        'questions2b': questions2b,
        'questions3': questions3,
        "questions4": questions4,
        'questions5': questions5,
        'questions6': questions6,
        'questions7': questions7,
        "questions8": questions8,
        'questions9': questions9,
        'questions11': questions11,
        'questions12': questions12,
        'questions13': questions13,
        'questions14': questions14,
        'question15': question15,
        "date_form": date_form,
        'cass_form': cass_form,
        "prepci_form": prepci_form,
        'length_form': length_form,
        "choice_form": choice_form,
        'stent_usedform': stent_usedform,
        "yesno_form": yesno_form,

    }
    return render(request, "enroll/lesion1.html", context)

def stent1(request):
    global i, ques_id
    ques_id = 209

    number_form = PrePciForm(initial={'ans_text': 0})
    yesno_form = YesNo()

    question1 = Question.objects.filter(q_id=210)
    question2 = Question.objects.filter(q_id=214)
    question4 = Question.objects.filter(q_id__gte=216, q_id__lte=219)
    question5 = Question.objects.filter(q_id=220)
    question6 = Question.objects.filter(q_id=223)    # Post Dialation YesNo
    question7 = Question.objects.filter(q_id=224)
    question8 = Question.objects.filter(q_id=226)

    if request.method == 'POST':

        Exists(210, 227)

        number_form = PrePciForm(request.POST)
        yesno_form = YesNo(request.POST)

        ans_text = request.POST.getlist('ans_text')  # 4 items in list
        stent = request.POST.getlist('stent[]')  # 4/8/12 items in list
        timi = request.POST.getlist('timi[]')
        complication = request.POST.getlist('complication[]')
        finding = request.POST.getlist('findings[]')
        values = request.POST.getlist('value[]')

        print('ans', ans_text)
        print('stent', stent)
        print('timi', timi)
        print('complication', complication)
        print('finding', finding)
        print('value', values)

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': stent[0]})
        quesform.save()

        if (stent[0] == '0'):
            ques_id = 213
        else:
            if (stent[0] == '1'):
                new_stent = "First Stent :- Name -" + \
                    stent[1] + " , Diameter - " + stent[2] + ", Length - " + \
                    stent[3] + ", Max Deployment Pressure - " + stent[4]
            elif (stent[0] == '2'):
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    "\nSecond Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + \
                    ", Length - " + stent[7] + \
                    ", Max Deployment Pressure - " + stent[8]
            else:
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    "\nSecond Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + ", Length - " + stent[7] + ", Max Deployment Pressure - " + stent[8] + \
                    "\nThird Stent :- Name -" + stent[9] + " , Diameter - " + stent[10] + \
                    ", Length - " + stent[11] + \
                    ", Max Deployment Pressure - " + stent[12]

            print(new_stent)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': new_stent})
            quesform.save()
            ques_id = 213

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': timi[0]})
        quesform.save()

        if (timi[0] == 'Unknown' or timi[0] == 3):
            get_ques()
        else:
            drugs = ','.join(timi[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': drugs})
            quesform.save()

        for ans in ans_text[0:4]:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': complication[0]})
        quesform.save()

        if (complication[0] == 'No'):
            ques_id = 222
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': complication[1:]})
            quesform.save()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': finding[0]})
        quesform.save()

        if (finding[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': finding[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': values[0]})
        quesform.save()

        if (values[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': values[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lesion2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "number_form": number_form,
        'yesno_form': yesno_form,

        'question1': question1,
        'question2': question2,
        'question4': question4,
        'question5': question5,
        'question6': question6,
        'question7': question7,
        'question8': question8,

    }
    return render(request, 'enroll/stent.html', context)

def lesion2(request):
    global ques_id, i
    ques_id = 240
    date_form = DateTime(initial={'ans_text': date.today()})
    cass_form = NumberInput(initial={'ans_text': 0})
    prepci_form = PrePciForm()
    length_form = FloatInput(initial={'ans_text': 0})
    choice_form = LessionChoice1()
    stent_usedform = NumberInput(initial={'ans_text': 0})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=241)
    questions2a = Question.objects.filter(q_id=242)
    questions2b = Question.objects.filter(q_id__gte=243, q_id__lte=244)
    questions3 = Question.objects.filter(q_id=245)
    questions4 = Question.objects.filter(q_id=246)
    questions5 = Question.objects.filter(q_id=247)
    questions6 = Question.objects.filter(q_id=248)
    questions7 = Question.objects.filter(q_id=249)
    questions8 = Question.objects.filter(q_id=250)
    questions9 = Question.objects.filter(q_id=251)
    questions11 = Question.objects.filter(q_id=253)
    questions12 = Question.objects.filter(q_id__gte=254, q_id__lte=259)
    questions13 = Question.objects.filter(q_id=260)
    questions14 = Question.objects.filter(q_id=261)
    question15 = Question.objects.filter(q_id=262)

    if request.method == 'POST':

        Exists(240, 263)

        date_form = DateTime(request.POST)
        cass_form = NumberInput(request.POST)
        prepci_form = PrePciForm(request.POST)
        length_form = FloatInput(request.POST)
        choice_form = LessionChoice1(request.POST)
        stent_usedform = NumberInput(request.POST)
        yesno_form = YesNo(request.POST)

        ans_text = request.POST.getlist('ans_text')

        print(ans_text, len(ans_text))

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        for ans in ans_text[1:4]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = PrePciForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        # Thrombus Question and if yes then dropdown 0-5
        thrombus = request.POST.getlist('thrombus[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': thrombus[0]})
        quesform.save()
        if (thrombus[0] == 'No'):
            get_ques()
        else:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': thrombus[1]})
        quesform.save()

        for ans in ans_text[5:8]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        med = request.POST.getlist('med[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': med[0]})
        quesform.save()

        if (med[0] == 'No'):
            get_ques()
        else:
            quesform = LessionChoice1({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': med[1]})
            quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[8]})
        quesform.save()

        for ans in ans_text[9:15]:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        yesno1 = request.POST.getlist('yesno1[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yesno1[0]})
        quesform.save()

        if (yesno1[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno1[1]})
            quesform.save()

        yesno2 = request.POST.getlist('yesno2[]')
        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yesno2[0]})
        quesform.save()

        if (yesno2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/stent2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "questions1": questions1,
        'questions2a': questions2a,
        'questions2b': questions2b,
        'questions3': questions3,
        "questions4": questions4,
        'questions5': questions5,
        'questions6': questions6,
        'questions7': questions7,
        "questions8": questions8,
        'questions9': questions9,
        'questions11': questions11,
        'questions12': questions12,
        'questions13': questions13,
        'questions14': questions14,
        'question15': question15,
        "date_form": date_form,
        'cass_form': cass_form,
        "prepci_form": prepci_form,
        'length_form': length_form,
        "choice_form": choice_form,
        'stent_usedform': stent_usedform,
        "yesno_form": yesno_form,

    }
    return render(request, "enroll/lesion2.html", context)

def stent2(request):
    global i, ques_id
    ques_id = 269

    number_form = PrePciForm(initial={'ans_text': 0})
    yesno_form = YesNo()

    question1 = Question.objects.filter(q_id=270)
    question2 = Question.objects.filter(q_id=272)
    question4 = Question.objects.filter(q_id__gte=274, q_id__lte=277)
    question5 = Question.objects.filter(q_id=278)
    question6 = Question.objects.filter(q_id=280)    # Post Dialation YesNo
    question7 = Question.objects.filter(q_id=281)
    question8 = Question.objects.filter(q_id=283)

    if request.method == 'POST':

        Exists(270, 284)

        number_form = PrePciForm(request.POST)
        yesno_form = YesNo(request.POST)

        ans_text = request.POST.getlist('ans_text')  # 4 items in list
        stent = request.POST.getlist('stent[]')  # 4/8/12 items in list
        timi = request.POST.getlist('timi[]')
        complication = request.POST.getlist('complication[]')
        finding = request.POST.getlist('findings[]')
        values = request.POST.getlist('value[]')

        print('ans', ans_text)
        print('stent', stent)
        print('timi', timi)
        print('complication', complication)
        print('finding', finding)
        print('value', values)

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': stent[0]})
        quesform.save()

        if (stent[0] == '0'):
            get_ques()
        else:
            if (stent[0] == '1'):
                new_stent = "First Stent :- Name -" + \
                    stent[1] + " , Diameter - " + stent[2] + ", Length - " + \
                    stent[3] + ", Max Deployment Pressure - " + stent[4]
            elif (stent[0] == '2'):
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    ".Second Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + \
                    ", Length - " + stent[7] + \
                    ", Max Deployment Pressure - " + stent[8]
            else:
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    ". Second Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + ", Length - " + stent[7] + ", Max Deployment Pressure - " + stent[8] + \
                    ". Third Stent :- Name -" + stent[9] + " , Diameter - " + stent[10] + \
                    ", Length - " + stent[11] + \
                    ", Max Deployment Pressure - " + stent[12]

            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': new_stent})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': timi[0]})
        quesform.save()

        if (timi[0] == 'Unknown' or timi[0] == 3):
            get_ques()
        else:
            drugs = ','.join(timi[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': drugs})
            quesform.save()

        for ans in ans_text[0:4]:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': complication[0]})
        quesform.save()

        if (complication[0] == 'No'):
            get_ques()
        else:
            comp = ','.join(complication[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': comp})
            quesform.save()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': finding[0]})
        quesform.save()

        if (finding[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': finding[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': values[0]})
        quesform.save()

        if (values[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': values[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lesion3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "number_form": number_form,
        'yesno_form': yesno_form,

        'question1': question1,
        'question2': question2,
        'question4': question4,
        'question5': question5,
        'question6': question6,
        'question7': question7,
        'question8': question8,

    }
    return render(request, 'enroll/stent.html', context)

def lesion3(request):
    global ques_id, i
    ques_id = 289
    date_form = DateTime(initial={'ans_text': date.today()})
    cass_form = NumberInput(initial={'ans_text': 0})
    prepci_form = PrePciForm()
    length_form = FloatInput(initial={'ans_text': 0})
    choice_form = LessionChoice1()
    stent_usedform = NumberInput(initial={'ans_text': 0})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=290)
    questions2a = Question.objects.filter(q_id=291)
    questions2b = Question.objects.filter(q_id__gte=292, q_id__lte=293)
    questions3 = Question.objects.filter(q_id=294)
    questions4 = Question.objects.filter(q_id=295)
    questions5 = Question.objects.filter(q_id=296)
    questions6 = Question.objects.filter(q_id=297)
    questions7 = Question.objects.filter(q_id=298)
    questions8 = Question.objects.filter(q_id=299)
    questions9 = Question.objects.filter(q_id=300)
    questions11 = Question.objects.filter(q_id=302)
    questions12 = Question.objects.filter(q_id__gte=303, q_id__lte=308)
    questions13 = Question.objects.filter(q_id=309)
    questions14 = Question.objects.filter(q_id=310)
    question15 = Question.objects.filter(q_id=311)

    if request.method == 'POST':

        Exists(290, 312)

        date_form = DateTime(request.POST)
        cass_form = NumberInput(request.POST)
        prepci_form = PrePciForm(request.POST)
        length_form = FloatInput(request.POST)
        choice_form = LessionChoice1(request.POST)
        stent_usedform = NumberInput(request.POST)
        yesno_form = YesNo(request.POST)

        NA = request.POST.getlist('NA[]')
        NA.append('A')
        print(NA)
        if(NA[0] == 'NA'):
            if "next" in request.POST:
                return redirect('/stent3/')
            elif "home" in request.POST:
                return redirect('/')
        else:
            ans_text = request.POST.getlist('ans_text')

            print(ans_text, len(ans_text))

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[0]})
            quesform.save()

            for ans in ans_text[1:4]:
                quesform = NumberInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': ans})
                quesform.save()

            quesform = PrePciForm({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[4]})
            quesform.save()

            # Thrombus Question and if yes then dropdown 0-5
            thrombus = request.POST.getlist('thrombus[]')
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': thrombus[0]})
            quesform.save()
            if (thrombus[0] == 'No'):
                get_ques()
            else:
                quesform = NumberInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': thrombus[1]})
            quesform.save()

            for ans in ans_text[5:8]:
                quesform = NumberInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': ans})
                quesform.save()

            med = request.POST.getlist('med[]')
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': med[0]})
            quesform.save()

            if (med[0] == 'No'):
                get_ques()
            else:
                quesform = LessionChoice1({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': med[1]})
                quesform.save()

            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[8]})
            quesform.save()

            for ans in ans_text[9:15]:
                quesform = YesNo({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': ans})
                quesform.save()

            yesno1 = request.POST.getlist('yesno1[]')
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno1[0]})
            quesform.save()

            if (yesno1[0] == 'No'):
                get_ques()
            else:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': yesno1[1]})
                quesform.save()

            yesno2 = request.POST.getlist('yesno2[]')
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yesno2[0]})
            quesform.save()

            if (yesno2[0] == 'No'):
                get_ques()
            else:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': yesno2[1]})
                quesform.save()

            if "next" in request.POST:
                return redirect('/stent3/')
            elif "home" in request.POST:
                return redirect('/submitted/')


    context = {
        "questions1": questions1,
        'questions2a': questions2a,
        'questions2b': questions2b,
        'questions3': questions3,
        "questions4": questions4,
        'questions5': questions5,
        'questions6': questions6,
        'questions7': questions7,
        "questions8": questions8,
        'questions9': questions9,
        'questions11': questions11,
        'questions12': questions12,
        'questions13': questions13,
        'questions14': questions14,
        'question15': question15,
        "date_form": date_form,
        'cass_form': cass_form,
        "prepci_form": prepci_form,
        'length_form': length_form,
        "choice_form": choice_form,
        'stent_usedform': stent_usedform,
        "yesno_form": yesno_form,

    }
    return render(request, "enroll/lesion3.html", context)

def stent3(request):
    global i, ques_id
    ques_id = 269

    number_form = PrePciForm(initial={'ans_text': 0})
    yesno_form = YesNo()

    question1 = Question.objects.filter(q_id=320)
    question2 = Question.objects.filter(q_id=322)
    question4 = Question.objects.filter(q_id__gte=324, q_id__lte=327)
    question5 = Question.objects.filter(q_id=328)
    question6 = Question.objects.filter(q_id=330)    # Post Dialation YesNo
    question7 = Question.objects.filter(q_id=331)
    question8 = Question.objects.filter(q_id=333)

    if request.method == 'POST':

        Exists(320, 334)

        number_form = PrePciForm(request.POST)
        yesno_form = YesNo(request.POST)

        ans_text = request.POST.getlist('ans_text')  # 4 items in list
        stent = request.POST.getlist('stent[]')  # 4/8/12 items in list
        timi = request.POST.getlist('timi[]')
        complication = request.POST.getlist('complication[]')
        finding = request.POST.getlist('findings[]')
        values = request.POST.getlist('value[]')

        print('ans', ans_text)
        print('stent', stent)
        print('timi', timi)
        print('complication', complication)
        print('finding', finding)
        print('value', values)

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': stent[0]})
        quesform.save()

        if (stent[0] == '0'):
            get_ques()
        else:
            if (stent[0] == '1'):
                new_stent = "First Stent :- Name -" + \
                    stent[1] + " , Diameter - " + stent[2] + ", Length - " + \
                    stent[3] + ", Max Deployment Pressure - " + stent[4]
            elif (stent[0] == '2'):
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    ".Second Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + \
                    ", Length - " + stent[7] + \
                    ", Max Deployment Pressure - " + stent[8]
            else:
                new_stent = "First Stent :- Name - " + stent[1] + " , Diameter - " + stent[2] + ", Length - " + stent[3] + ", Max Deployment Pressure - " + stent[4] + \
                    ". Second Stent :- Name " + stent[5] + " , Diameter - " + stent[6] + ", Length - " + stent[7] + ", Max Deployment Pressure - " + stent[8] + \
                    ". Third Stent :- Name -" + stent[9] + " , Diameter - " + stent[10] + \
                    ", Length - " + stent[11] + \
                    ", Max Deployment Pressure - " + stent[12]

            print(new_stent)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': new_stent})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': timi[0]})
        quesform.save()

        if (timi[0] == 'Unknown' or timi[0] == 3):
            get_ques()
        else:
            drugs = ','.join(timi[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': drugs})
            quesform.save()

        for ans in ans_text[0:4]:
            quesform = YesNo({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': complication[0]})
        quesform.save()

        if (complication[0] == 'No'):
            get_ques()
        else:
            comp = ','.join(complication[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': comp})
            quesform.save()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': finding[0]})
        quesform.save()

        if (finding[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': finding[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': values[0]})
        quesform.save()

        if (values[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': values[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/cardiac1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "number_form": number_form,
        'yesno_form': yesno_form,

        'question1': question1,
        'question2': question2,
        'question4': question4,
        'question5': question5,
        'question6': question6,
        'question7': question7,
        'question8': question8,

    }
    return render(request, 'enroll/stent.html', context)

def cardiac_enzymes1(request):
    global ques_id, i
    ques_id = 339

    date_form = DateTime(initial={'ans_text': date.today()})
    cardiac_codeform = CardiacCodes()
    done_form = CardiacDone()
    cardiac_resultform = NumberInput(initial={'ans_text': 0})
    cardiac_unitform = CardiacUnit(initial={'ans_text': 0})

    date_ques = Question.objects.filter(q_id=340)
    cardiac_ques = Question.objects.filter(q_id__gte=341, q_id__lte=344)

    if request.method == 'POST':

        Exists(340, 344)

        date_form = DateTime(request.POST)
        cardiac_codeform = CardiacCodes(request.POST)
        done_form = CardiacDone(request.POST)
        cardiac_resultform = NumberInput(request.POST)
        cardiac_unitform = CardiacUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        skip = 0
        while skip != len(ans_text)-1:
            get_ques()
            skip = skip+1
            quesform = CardiacDone({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = CardiacUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip + 1
            quesform = CardiacCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "date_ques": date_ques,
        'cardiac_ques': cardiac_ques,
        "date_form": date_form,
        'cardiac_codeform': cardiac_codeform,
        'done_form': done_form,
        'cardiac_resultform': cardiac_resultform,
        'cardiac_unitform': cardiac_unitform,
    }
    return render(request, 'enroll/cardiac2.html', context)

def concomitant1(request):
    global ques_id, i
    ques_id = 349
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=350)
    questions2 = Question.objects.filter(q_id=351)

    if request.method == 'POST':

        Exists(350, 351)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse1/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse1(request):
    global ques_id, i
    ques_id = 359
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=360)
    questions2 = Question.objects.filter(q_id=361)
    questions3 = Question.objects.filter(q_id=362)

    if request.method == 'POST':

        Exists(360, 362)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/echo/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

def echo(request):
    global i, ques_id
    ques_id = 370
    number_form = NumberInput(initial={'ans_text': 0})
    decimal_form = FloatInput()
    yesno_form = YesNo()
    mr_form = MR_Grade()
    pah_form = PresentAbsent()
    nmab_form = NormalAbnormal()

    question1 = Question.objects.filter(q_id__gte=373, q_id__lte=375)

    if request.method == 'POST':

        Exists(370, 382)

        number_form = NumberInput(request.POST)
        decimal_form = FloatInput(request.POST)
        yesno_form = YesNo(request.POST)
        mr_form = MR_Grade(request.POST)
        pah_form = PresentAbsent(request.POST)
        nmab_form = NormalAbnormal(request.POST)

        ans_text = request.POST.getlist('ans_text')
        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')
        print('ans_text', ans_text)
        print('yn1', yn1)
        print('yn2', yn2)

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if yn1[0] == 'Yes':
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1[1]})
            quesform.save()
        else:
            get_ques()

        for ans in ans_text[:3]:
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans})
            quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[3]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if yn2[0] == 'Yes':
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()
        else:
            get_ques()

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[4]})
        quesform.save()

        quesform = MR_Grade({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[5]})
        quesform.save()

        quesform = PresentAbsent({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[6]})
        quesform.save()

        quesform = NormalAbnormal({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[7]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/vital/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'number_form': number_form,
        'decimal_form': decimal_form,
        'yesno_form': yesno_form,
        'mr_form': mr_form,
        'pah_form': pah_form,
        'nmab_form': nmab_form,

        'question1': question1

    }
    return render(request, 'enroll/echo.html', context)

def vital_sign(request):
    global i, ques_id
    ques_id = 389

    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    heartrateform = NumberInput(initial={'ans_text': 0})
    bpform = TextInput()
    weightform = FloatInput(initial={'ans_text': 0.0})

    date_ques = Question.objects.filter(q_id=390)
    hr_ques = Question.objects.filter(q_id=391)
    bp_ques = Question.objects.filter(q_id=392)
    weight_ques = Question.objects.filter(q_id=393)

    if request.method == 'POST':

        Exists(390, 393)

        dateform = DateTime(request.POST)
        heartrateform = NumberInput(request.POST)
        bpform = TextInput(request.POST)
        weightform = FloatInput(request.POST)

        ans = request.POST.getlist('ans_text')
        bp = request.POST.getlist("bp[]")

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[1]})
        quesform.save()

        blps = '/'.join(bp)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': blps})
        quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[2]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/lead2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'dateques': date_ques,
        'hrques': hr_ques,
        'bpques': bp_ques,
        'wtques': weight_ques,
        'dateform': dateform,
        'hrform': heartrateform,
        'bpform': bpform,
        'wtform': weightform,
    }
    return render(request, 'enroll/vital.html', context)

def lead2(request):
    global ques_id, i
    ques_id = 399

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    arrhythmiaform = ArrhythmiaForm()
    atrioventricularblockform = AtrioventricularBlockForm()

    yesno_ques1 = Question.objects.filter(q_id=400)
    yesno_ques2 = Question.objects.filter(q_id=402)
    arrhythmia_ques = Question.objects.filter(q_id=404)
    atrioventricular_ques = Question.objects.filter(q_id=405)

    if request.method == 'POST':

        Exists(400, 405)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        arrhythmiaform = ArrhythmiaForm(request.POST)
        atrioventricularblockform = AtrioventricularBlockForm(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': st[0]})
        quesform.save()

        if(st[0] == 'No'):
            get_ques()
        else:
            st_new = ','.join(st[1:])
            print(st_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': st_new})
            quesform.save()

        quesform = ArrhythmiaForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        # QRS
        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/cardiac2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques1': yesno_ques1,
        'yesno_ques2': yesno_ques2,
        'arrhythmia_ques': arrhythmia_ques,
        'atrioventricular_ques': atrioventricular_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'arrhythmiaform': arrhythmiaform,
        'atrioventricularblockform': atrioventricularblockform,
    }
    return render(request, "enroll/lead_discharge.html", context)

def cardiac_enzymes2(request):
    global ques_id, i
    ques_id = 420

    date_form = DateTime(initial={'ans_text': date.today()})
    cardiac_codeform = CardiacCodes()
    done_form = CardiacDone()
    cardiac_resultform = NumberInput(initial={'ans_text': 0})
    cardiac_unitform = CardiacUnit(initial={'ans_text': 0})

    date_ques = Question.objects.filter(q_id=421)
    cardiac_ques = Question.objects.filter(q_id__gte=422, q_id__lte=425)

    if request.method == 'POST':

        Exists(421, 425)

        date_form = DateTime(request.POST)
        cardiac_codeform = CardiacCodes(request.POST)
        done_form = CardiacDone(request.POST)
        cardiac_resultform = NumberInput(request.POST)
        cardiac_unitform = CardiacUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')

        quesform = DateTime({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        skip = 0
        while skip != len(ans_text)-1:
            get_ques()
            skip = skip+1
            quesform = CardiacDone({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = NumberInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = CardiacUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip + 1
            quesform = CardiacCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/platelet/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        "date_ques": date_ques,
        'cardiac_ques': cardiac_ques,
        "date_form": date_form,
        'cardiac_codeform': cardiac_codeform,
        'done_form': done_form,
        'cardiac_resultform': cardiac_resultform,
        'cardiac_unitform': cardiac_unitform,
    }
    return render(request, 'enroll/cardiac2.html', context)

def platelet_therapy(request):
    global ques_id, i
    ques_id = 439

    question1 = Question.objects.filter(q_id=440)

    if request.method == 'POST':

        Exists(440, 443)

        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if (yn1[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1[1:]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if (yn2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'question1': question1,
    }

    return render(request, 'enroll/anti_platelet.html', context)

def concomitant2(request):
    global ques_id, i
    ques_id = 450
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=451)
    questions2 = Question.objects.filter(q_id=452)

    if request.method == 'POST':

        Exists(451, 452)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse2(request):
    global ques_id, i
    ques_id = 460
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=360)
    questions2 = Question.objects.filter(q_id=361)
    questions3 = Question.objects.filter(q_id=362)

    if request.method == 'POST':

        Exists(461, 463)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/onemonth/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)


###################################### ONE MONTH #############################################


def onemonth(request):
    global ques_id, i
    ques_id = 469

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    heartrateform = NumberInput(initial={'ans_text': 0})
    weightform = FloatInput(initial={'ans_text': 0.0})

    hr_ques = Question.objects.filter(q_id=473)
    bp_ques = Question.objects.filter(q_id=474)
    weight_ques = Question.objects.filter(q_id=475)

    if request.method == 'POST':

        Exists(470, 475)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)
        dateform = DateTime(request.POST)
        heartrateform = NumberInput(request.POST)
        weightform = FloatInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        bp = request.POST.getlist("bp[]")
        ans = request.POST.getlist('yn1[]')
        print(ans)

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            ques_id = 472
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[2]})
            quesform.save()

        # vital
        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        blps = '/'.join(bp)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': blps})
        quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/assessment/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'hrques': hr_ques,
        'bpques': bp_ques,
        'wtques': weight_ques,
        'hrform': heartrateform,
        'textform': textform,
        'wtform': weightform,
    }
    return render(request, "enroll/01Month.html", context)

def assessment(request):
    global ques_id, i
    ques_id = 479

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=480)
    question2 = Question.objects.filter(q_id=481)
    question3 = Question.objects.filter(q_id=482)

    if request.method == 'POST':

        Exists(480, 482)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')
        print(ans_text)
        print(ang)

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lead3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def lead3(request):
    global ques_id, i
    ques_id = 482

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    arrhythmiaform = ArrhythmiaForm()
    atrioventricularblockform = AtrioventricularBlockForm()

    yesno_ques1 = Question.objects.filter(q_id=483)
    yesno_ques2 = Question.objects.filter(q_id=485)
    arrhythmia_ques = Question.objects.filter(q_id=487)
    atrioventricular_ques = Question.objects.filter(q_id=488)

    if request.method == 'POST':

        Exists(483, 488)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        arrhythmiaform = ArrhythmiaForm(request.POST)
        atrioventricularblockform = AtrioventricularBlockForm(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': st[0]})
        quesform.save()

        if(st[0] == 'No'):
            get_ques()
        else:
            st_new = ','.join(st[1:])
            print(st_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': st_new})
            quesform.save()

        quesform = ArrhythmiaForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        # QRS
        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/platelet2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques1': yesno_ques1,
        'yesno_ques2': yesno_ques2,
        'arrhythmia_ques': arrhythmia_ques,
        'atrioventricular_ques': atrioventricular_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'arrhythmiaform': arrhythmiaform,
        'atrioventricularblockform': atrioventricularblockform,
    }
    return render(request, "enroll/lead1.html", context)

def platelet_therapy2(request):
    global ques_id, i
    ques_id = 490

    question1 = Question.objects.filter(q_id=491)

    if request.method == 'POST':

        Exists(491, 494)

        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if (yn1[0] == 'No'):
            get_ques()
        else:
            yn1_new = ','.join(yn1[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1_new})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if (yn2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'question1': question1,
    }

    return render(request, 'enroll/anti_platelet1.html', context)

def concomitant3(request):
    global ques_id, i
    ques_id = 499
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=500)
    questions2 = Question.objects.filter(q_id=501)

    if request.method == 'POST':

        Exists(500, 501)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse3(request):
    global ques_id, i
    ques_id = 504
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=505)
    questions2 = Question.objects.filter(q_id=506)
    questions3 = Question.objects.filter(q_id=507)

    if request.method == 'POST':

        Exists(505, 507)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/adverse3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## SIX MONTHS ######################################################

def sixmonth_followup(request):
    global ques_id, i
    ques_id = 510

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    heartrateform = NumberInput(initial={'ans_text': 0})
    weightform = FloatInput(initial={'ans_text': 0.0})

    hr_ques = Question.objects.filter(q_id=514)
    bp_ques = Question.objects.filter(q_id=515)
    weight_ques = Question.objects.filter(q_id=516)

    if request.method == 'POST':

        Exists(511, 516)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)
        dateform = DateTime(request.POST)
        heartrateform = NumberInput(request.POST)
        weightform = FloatInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        bp = request.POST.getlist("bp[]")
        ans = request.POST.getlist('yn1[]')
        print(ans)

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            ques_id = 513
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[2]})
            quesform.save()

        # vital
        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        blps = '/'.join(bp)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': blps})
        quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/6month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'hrques': hr_ques,
        'bpques': bp_ques,
        'wtques': weight_ques,
        'hrform': heartrateform,
        'textform': textform,
        'wtform': weightform,
    }
    return render(request, "enroll/06month.html", context)

def assessment2(request):
    global ques_id, i
    ques_id = 519

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=520)
    question2 = Question.objects.filter(q_id=521)
    question3 = Question.objects.filter(q_id=522)

    if request.method == 'POST':

        Exists(520, 522)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')
        print(ans_text)
        print(ang)

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lead4/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def lead4(request):
    global ques_id, i
    ques_id = 525

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    arrhythmiaform = ArrhythmiaForm()
    atrioventricularblockform = AtrioventricularBlockForm()

    yesno_ques1 = Question.objects.filter(q_id=526)
    yesno_ques2 = Question.objects.filter(q_id=528)
    arrhythmia_ques = Question.objects.filter(q_id=530)
    atrioventricular_ques = Question.objects.filter(q_id=531)

    if request.method == 'POST':

        Exists(526, 531)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        arrhythmiaform = ArrhythmiaForm(request.POST)
        atrioventricularblockform = AtrioventricularBlockForm(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': st[0]})
        quesform.save()

        if(st[0] == 'No'):
            get_ques()
        else:
            st_new = ','.join(st[1:])
            print(st_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': st_new})
            quesform.save()

        quesform = ArrhythmiaForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/labtest2/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques1': yesno_ques1,
        'yesno_ques2': yesno_ques2,
        'arrhythmia_ques': arrhythmia_ques,
        'atrioventricular_ques': atrioventricular_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'arrhythmiaform': arrhythmiaform,
        'atrioventricularblockform': atrioventricularblockform,
    }
    return render(request, "enroll/lead1.html", context)

def lab_test2(request):
    global ques_id, i
    ques_id = 539
    lab_codeform = LabCodes()
    lab_resultform = FloatInput(initial={'ans_text': 0})
    lab_unitform = LabUnit()

    labpara_ques = Question.objects.filter(q_id__gte=540, q_id__lte=552)

    if request.method == 'POST':

        Exists(540, 552)

        lab_codeform = LabCodes(request.POST)
        lab_resultform = FloatInput(request.POST)
        lab_unitform = LabUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')
        print(ans_text)

        skip = -1
        while (skip != (len(ans_text))-1):
            get_ques()
            skip = skip+1
            quesform = LabCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = FloatInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = LabUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/platelet3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'labpara_ques': labpara_ques,
        'lab_codeform': lab_codeform,
        'lab_resultform': lab_resultform,
        'lab_unitform': lab_unitform,
    }
    return render(request, 'enroll/lab1.html', context)

def platelet_therapy3(request):
    global ques_id, i
    ques_id = 559

    question1 = Question.objects.filter(q_id=560)

    if request.method == 'POST':

        Exists(560, 563)

        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if (yn1[0] == 'No'):
            get_ques()
        else:
            yn1_new = ','.join(yn1[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1_new})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if (yn2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco4/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'question1': question1,
    }

    return render(request, 'enroll/anti_platelet1.html', context)

def concomitant4(request):
    global ques_id, i
    ques_id = 565
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=566)
    questions2 = Question.objects.filter(q_id=567)

    if request.method == 'POST':

        Exists(566, 567)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse4/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse4(request):
    global ques_id, i
    ques_id = 570
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=571)
    questions2 = Question.objects.filter(q_id=572)
    questions3 = Question.objects.filter(q_id=573)

    if request.method == 'POST':

        Exists(571, 573)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/12month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## 12 MONTHS ######################################################

def twelvemonth_followup(request):
    global ques_id, i
    ques_id = 580

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    dateform = DateTime(initial={'ans_text': datetime.date.today()})
    heartrateform = NumberInput(initial={'ans_text': 0})
    weightform = FloatInput(initial={'ans_text': 0.0})

    hr_ques = Question.objects.filter(q_id=584)
    bp_ques = Question.objects.filter(q_id=585)
    weight_ques = Question.objects.filter(q_id=586)

    if request.method == 'POST':

        Exists(581, 586)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)
        dateform = DateTime(request.POST)
        heartrateform = NumberInput(request.POST)
        weightform = FloatInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        bp = request.POST.getlist("bp[]")
        ans = request.POST.getlist('yn1[]')
        print(ans)

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            ques_id = 583
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[2]})
            quesform.save()

        # vital
        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        blps = '/'.join(bp)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': blps})
        quesform.save()

        quesform = FloatInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/assessment3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'hrques': hr_ques,
        'bpques': bp_ques,
        'wtques': weight_ques,
        'hrform': heartrateform,
        'textform': textform,
        'wtform': weightform,
    }
    return render(request, "enroll/12month.html", context)

def assessment3(request):
    global ques_id, i
    ques_id = 590

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=591)
    question2 = Question.objects.filter(q_id=592)
    question3 = Question.objects.filter(q_id=593)

    if request.method == 'POST':

        Exists(591, 593)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')
        print(ans_text)
        print(ang)

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lvef_details/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def lvef_details(request):
    global ques_id, i
    ques_id = 600

    if request.method == 'POST':

        Exists(601, 603)

        yn1 = request.POST.getlist('yn1[]')
        print(yn1)
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if yn1[0] == 'No':
            ques_id = 603
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1[1]})
            quesform.save()

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1[2]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lead5/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    return render(request, "enroll/lvef_details.html",)

def lead5(request):
    global ques_id, i
    ques_id = 610

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    arrhythmiaform = ArrhythmiaForm()
    atrioventricularblockform = AtrioventricularBlockForm()

    yesno_ques1 = Question.objects.filter(q_id=611)
    yesno_ques2 = Question.objects.filter(q_id=613)
    arrhythmia_ques = Question.objects.filter(q_id=615)
    atrioventricular_ques = Question.objects.filter(q_id=616)

    if request.method == 'POST':

        Exists(611, 616)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        arrhythmiaform = ArrhythmiaForm(request.POST)
        atrioventricularblockform = AtrioventricularBlockForm(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': st[0]})
        quesform.save()

        if(st[0] == 'No'):
            get_ques()
        else:
            st_new = ','.join(st[1:])
            print(st_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': st_new})
            quesform.save()

        quesform = ArrhythmiaForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/labtest3/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques1': yesno_ques1,
        'yesno_ques2': yesno_ques2,
        'arrhythmia_ques': arrhythmia_ques,
        'atrioventricular_ques': atrioventricular_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'arrhythmiaform': arrhythmiaform,
        'atrioventricularblockform': atrioventricularblockform,
    }
    return render(request, "enroll/lead1.html", context)

def lab_test3(request):
    global ques_id, i
    ques_id = 620
    lab_codeform = LabCodes()
    lab_resultform = FloatInput(initial={'ans_text': 0})
    lab_unitform = LabUnit()

    labpara_ques = Question.objects.filter(q_id__gte=621, q_id__lte=633)

    if request.method == 'POST':

        Exists(621, 633)

        lab_codeform = LabCodes(request.POST)
        lab_resultform = FloatInput(request.POST)
        lab_unitform = LabUnit(request.POST)

        ans_text = request.POST.getlist('ans_text')
        print(ans_text)

        skip = -1
        while (skip != (len(ans_text))-1):
            get_ques()
            skip = skip+1
            quesform = LabCodes({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = FloatInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

            skip = skip+1
            quesform = LabUnit({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=ques_id),
                'ans_text': ans_text[skip]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/platelet4/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'labpara_ques': labpara_ques,
        'lab_codeform': lab_codeform,
        'lab_resultform': lab_resultform,
        'lab_unitform': lab_unitform,
    }
    return render(request, 'enroll/lab1.html', context)

def platelet_therapy4(request):
    global ques_id, i
    ques_id = 670

    question1 = Question.objects.filter(q_id=560)

    if request.method == 'POST':

        Exists(671, 674)

        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if (yn1[0] == 'No'):
            get_ques()
        else:
            yn1_new = ','.join(yn1[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1_new})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if (yn2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco5/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'question1': question1,
    }

    return render(request, 'enroll/anti_platelet1.html', context)

def concomitant5(request):
    global ques_id, i
    ques_id = 680
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=681)
    questions2 = Question.objects.filter(q_id=682)

    if request.method == 'POST':

        Exists(681, 682)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse5/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse5(request):
    global ques_id, i
    ques_id = 690
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=691)
    questions2 = Question.objects.filter(q_id=692)
    questions3 = Question.objects.filter(q_id=693)

    if request.method == 'POST':

        Exists(691, 693)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/24month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## 24 MONTHS ######################################################

def twentyfourmonth_followup(request):
    global ques_id, i
    ques_id = 699

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()
    dateform = DateTime(initial={'ans_text': datetime.date.today()})

    question1 = Question.objects.filter(q_id=700)

    if request.method == 'POST':

        Exists(700, 702)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans = request.POST.getlist('yn1[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            return redirect('/assessment4/')
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[2]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/assessment4/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'textform': textform,
        'question1': question1,
    }
    return render(request, "enroll/24month.html", context)

def assessment4(request):
    global ques_id, i
    ques_id = 704

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=705)
    question2 = Question.objects.filter(q_id=706)
    question3 = Question.objects.filter(q_id=707)

    if request.method == 'POST':

        Exists(705, 707)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/lead6/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def lead6(request):
    global ques_id, i
    ques_id = 710

    yesnoform = YesNo()
    dateform = DateTime(initial={'ans_text': date.today()})
    arrhythmiaform = ArrhythmiaForm()
    atrioventricularblockform = AtrioventricularBlockForm()

    yesno_ques1 = Question.objects.filter(q_id=711)
    yesno_ques2 = Question.objects.filter(q_id=713)
    arrhythmia_ques = Question.objects.filter(q_id=715)
    atrioventricular_ques = Question.objects.filter(q_id=716)

    if request.method == 'POST':

        Exists(711, 716)

        yesnoform = YesNo(request.POST)
        dateform = DateTime(request.POST)
        arrhythmiaform = ArrhythmiaForm(request.POST)
        atrioventricularblockform = AtrioventricularBlockForm(request.POST)

        ans_text = request.POST.getlist('ans_text')
        dt = request.POST.getlist('dt[]')
        st = request.POST.getlist('ST[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': dt[0]})
        quesform.save()
        if(dt[0] == 'No'):
            get_ques()
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': dt[1]})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': st[0]})
        quesform.save()

        if(st[0] == 'No'):
            get_ques()
        else:
            st_new = ','.join(st[1:])
            print(st_new)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': st_new})
            quesform.save()

        quesform = ArrhythmiaForm({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        quesform = NumberInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[1]})
        quesform.save()

        if "next" in request.POST:
            return redirect('/platelet5/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesno_ques1': yesno_ques1,
        'yesno_ques2': yesno_ques2,
        'arrhythmia_ques': arrhythmia_ques,
        'atrioventricular_ques': atrioventricular_ques,
        'yesnoform': yesnoform,
        'dateform': dateform,
        'arrhythmiaform': arrhythmiaform,
        'atrioventricularblockform': atrioventricularblockform,
    }
    return render(request, "enroll/lead1.html", context)

def platelet_therapy5(request):
    global ques_id, i
    ques_id = 719

    question1 = Question.objects.filter(q_id=720)

    if request.method == 'POST':

        Exists(720, 723)

        yn1 = request.POST.getlist('yn1[]')
        yn2 = request.POST.getlist('yn2[]')

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn1[0]})
        quesform.save()

        if (yn1[0] == 'No'):
            get_ques()
        else:
            yn1_new = ','.join(yn1[1:])
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn1_new})
            quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn2[0]})
        quesform.save()

        if (yn2[0] == 'No'):
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': yn2[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/conco6/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'question1': question1,
    }

    return render(request, 'enroll/anti_platelet1.html', context)

def concomitant6(request):
    global ques_id, i
    ques_id = 725
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=726)
    questions2 = Question.objects.filter(q_id=727)

    if request.method == 'POST':

        Exists(726, 727)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('pre[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()

        if ans_text[0] == 'No':
            get_ques()
        else:
            val = ','.join(ans)
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': val})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse6/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        "textform": textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/conco.html", context)

def adverse6(request):
    global ques_id, i
    ques_id = 730
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=731)
    questions2 = Question.objects.filter(q_id=732)
    questions3 = Question.objects.filter(q_id=733)

    if request.method == 'POST':

        Exists(731, 733)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/36month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## 36 MONTHS ######################################################

def thirtysixmonth_followup(request):
    global ques_id, i
    ques_id = 739

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()
    dateform = DateTime(initial={'ans_text': datetime.date.today()})

    question1 = Question.objects.filter(q_id=740)

    if request.method == 'POST':

        Exists(740, 741)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans = request.POST.getlist('yn1[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            return redirect('/assessment5/')
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/assessment5/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'textform': textform,
        'question1': question1,
    }
    return render(request, "enroll/36month.html", context)

def assessment5(request):
    global ques_id, i
    ques_id = 744

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=745)
    question2 = Question.objects.filter(q_id=746)
    question3 = Question.objects.filter(q_id=747)

    if request.method == 'POST':

        Exists(745, 747)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse7/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def adverse7(request):
    global ques_id, i
    ques_id = 750
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=751)
    questions2 = Question.objects.filter(q_id=752)
    questions3 = Question.objects.filter(q_id=753)

    if request.method == 'POST':

        Exists(751, 753)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/48month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## 48 MONTHS ######################################################

def fourtyeight_followup(request):
    global ques_id, i
    ques_id = 759

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()
    dateform = DateTime(initial={'ans_text': datetime.date.today()})

    question1 = Question.objects.filter(q_id=760)

    if request.method == 'POST':

        Exists(760, 741)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans = request.POST.getlist('yn1[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            return redirect('/assessment6/')
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/assesment6/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'textform': textform,
        'question1': question1,
    }
    return render(request, "enroll/48month.html", context)

def assessment6(request):
    global ques_id, i
    ques_id = 764

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=765)
    question2 = Question.objects.filter(q_id=766)
    question3 = Question.objects.filter(q_id=767)

    if request.method == 'POST':

        Exists(765, 767)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse8/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def adverse8(request):
    global ques_id, i
    ques_id = 770
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=771)
    questions2 = Question.objects.filter(q_id=772)
    questions3 = Question.objects.filter(q_id=773)

    if request.method == 'POST':

        Exists(771, 773)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/60month/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

######################################## 60 MONTHS ######################################################

def sixty_followup(request):
    global ques_id, i
    ques_id = 779

    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()
    dateform = DateTime(initial={'ans_text': datetime.date.today()})

    question1 = Question.objects.filter(q_id=780)

    if request.method == 'POST':

        Exists(780, 781)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans = request.POST.getlist('yn1[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
        quesform.save()

        if(ans[0] == 'No'):
            return redirect('/assessment7/')
        else:
            quesform = DateTime({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/assessment7/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'yesnoform': yesno_form,
        'textform': textform,
        'question1': question1,
    }
    return render(request, "enroll/60month.html", context)

def assessment7(request):
    global ques_id, i
    ques_id = 784

    textform = TextInput(initial={'ans_text': "-"})

    question1 = Question.objects.filter(q_id=785)
    question2 = Question.objects.filter(q_id=786)
    question3 = Question.objects.filter(q_id=787)

    if request.method == 'POST':

        Exists(785, 787)

        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ang = request.POST.getlist('ang[]')

        if ang[0] != 'NA':
            get_ques()
            for val in ang[:]:
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ang[0]})
            quesform.save()

        if "next" in request.POST:
            return redirect('/adverse9/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'textform': textform,
        'question1': question1,
        'question2': question2,
        'question3': question3,
    }

    return render(request, "enroll/assessment.html", context)

def adverse9(request):
    global ques_id, i
    ques_id = 790
    textform = TextInput(initial={'ans_text': 'None'})
    yesno_form = YesNo()

    questions1 = Question.objects.filter(q_id=791)
    questions2 = Question.objects.filter(q_id=792)
    questions3 = Question.objects.filter(q_id=793)

    if request.method == 'POST':

        Exists(791, 793)

        yesno_form = YesNo(request.POST)
        textform = TextInput(request.POST)

        ans_text = request.POST.getlist('ans_text')
        ans = request.POST.getlist('ser[]')

        quesform = YesNo({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans_text[0]})
        quesform.save()
        if(ans_text[0] == 'No'):
            get_ques()
            get_ques()
        else:
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans_text[1]})
            quesform.save()
            if(ans_text[1] == 'No'):
                get_ques()
            else:
                val = ', '.join(ans)
                quesform = TextInput({
                    'p_id': Patient.objects.get(p_id=i),
                    'q_id': Question.objects.get(q_id=get_ques()),
                    'ans_text': val})
                quesform.save()

        if "next" in request.POST:
            return redirect('/endstudy/')
        elif "home" in request.POST:
            return redirect('/submitted/')

    context = {
        'questions1': questions1,
        'questions2': questions2,
        'questions3': questions3,
        'textform': textform,
        'yesnoform': yesno_form,
    }
    return render(request, "enroll/adverse.html", context)

def endofstudy(request):
    global ques_id, i
    ques_id = 800

    textform = TextInput(initial={'ans_text': 'None'})
    date_form = DateTime(initial={'ans_text': datetime.date.today()})

    protocol_question = Question.objects.filter(q_id=801)
    date_question1 = Question.objects.filter(q_id=802)
    date_question2 = Question.objects.filter(q_id=803)
    premature_question = Question.objects.filter(q_id=804)
    concent_question = Question.objects.filter(q_id=805)

    if request.method == 'POST':

        Exists(801, 805)

        date_form = DateTime(request.POST)
        textform = TextInput(request.POST)

        ans = request.POST.getlist('ans_text') # concent
        yn = request.POST.getlist('yn1[]') #dates
        premature = request.POST.getlist('opt2[]') # multiple choice

        print(ans)
        print(yn)
        print(premature)

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': yn[0]})
        quesform.save()

        if(yn[0] == 'Yes'):
            quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[0]})
            quesform.save()
        else:
            get_ques()
            quesform = TextInput({
                'p_id': Patient.objects.get(p_id=i),
                'q_id': Question.objects.get(q_id=get_ques()),
                'ans_text': ans[1]})
            quesform.save()
        
        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': premature[0]})
        quesform.save()

        quesform = TextInput({
            'p_id': Patient.objects.get(p_id=i),
            'q_id': Question.objects.get(q_id=get_ques()),
            'ans_text': ans[2]})
        quesform.save()

        return redirect('/submitted/')

    context = {
        'protocol_question': protocol_question,
        'date_question1': date_question1,
        'date_question2': date_question2,
        'premature_question': premature_question,
        'concent_question': concent_question,
        'date_form':date_form,
    }
    return render(request, "enroll/endofstudy.html", context)


i = 0


def give_pid():
    global i
    try:
        patients = Patient.objects.latest('p_id')
        i = patients.p_id + 1
    except:
        i=1
    print(i)
    return(i)

ques_id = 0

def get_ques():
    global ques_id
    ques_id = ques_id+1
    return(ques_id)

def Exists(a, b):
    global i
    exists = Result.objects.filter(p_id=i, q_id__gte=a, q_id__lte=b)
    exists.delete()