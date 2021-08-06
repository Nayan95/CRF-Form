from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, models
from .models import Result, Patient
import datetime


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('f_name', 'l_name', 'age')
        labels = {
            #'p_id': 'Patient ID ',
            'f_name': 'First Name ',
            'l_name': 'Last Name ',
            'age': 'Age '
        }
        widgets = {
            # 'p_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'f_name': forms.TextInput(attrs={'class': 'form-control'}),
            'l_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'})
            # 'visit_date': forms.DateInput(format='%d/%m/%Y'),
        }

class imp_exp(forms.Form):
    p_id = forms.IntegerField(label='Patient ID', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    file = forms.FileField()

class GetDetails(forms.Form):
    p_id = forms.IntegerField(label='Patient ID', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))


class FloatInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control w-35'})
        }


class YesNo(forms.ModelForm):
    class Meta:
        truefalse = [
            ('No', 'No'),
            ('Yes', 'Yes')
        ]
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=truefalse, attrs={'class': 'form-control w-35'})
        }


class SexInput(forms.ModelForm):
    class Meta:
        truefalse = [
            ('Male', 'Male'),
            ('Female', 'Female')
        ]
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=truefalse, attrs={'class': 'form-control w-35' })
        }


class YesNoUNK(forms.ModelForm):
    class Meta:
        truefalse = (
            ('No', 'No'),
            ('Yes', 'Yes'),
            ('UNK', 'UNK')
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=truefalse, attrs={'class': 'form-control w-35' })
        }


class NumberInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.NumberInput(attrs={'class': 'form-control w-35'})
        }


class NYHAClass(forms.ModelForm):
    class Meta:
        types = (
                ('None', 'None'),
                ('Class I', 'Class I'),
                ('Class II', 'Class II'),
                ('Class III', 'Class III'),
                ('Class IV', 'Class IV')
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control'})
        }


class TextInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.TextInput(attrs={'class': 'form-control w-35'})
        }


class DateTime(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.DateInput(attrs={'type': 'date', 'class': 'form-control w-35'})
        }


class LabCodes(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('Normal', 'Normal'),
                ('Out of Range', 'Out of Range'),
                ('Not Done', 'Not Done')
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes, attrs={'class': 'form-control w-35'})
        }


class LabUnit(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('g/dl', 'g/dl'),
                ('Per/mm3', 'Per/mm3'),
                ('Lac/mm3', 'Lac/mm3'),
                ('Mg/dl', 'Mg/dl'),
                ('Ml/min/m2', 'Ml/min/m2'),
                ('%', '%'),
                ('Mg/dl', 'Mg/dl'),
                ('Mg/L', 'Mg/L'),
                ('Micromole/L', 'Micromole/L'),
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes, attrs={'class': 'form-control'})
        }


class CardiacCodes(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('Normal', 'Normal'),
                ('Out of Range', 'Out of Range'),
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes, attrs={'class': 'form-control'})
        }


class CardiacUnit(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('U/ L', 'U/ L'),
                ('Ng/ml', 'Ng/ml'),
                ('mcg/ l', 'mcg/ l')
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes, attrs={'class': 'form-control'})
        }


class CardiacDone(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('Done', 'Done'),
                ('Not Done', 'Not Done')
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes, attrs={'class': 'form-control'})
        }


class NormalAbnormal(forms.ModelForm):
    class Meta:
        types = (
                ('Normal', 'Normal'),
                ('Abnormal', 'Abnormal'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class FundChoice(forms.ModelForm):
    class Meta:
        types = (
            ('Self Financed', 'Self Financed'),
            ('Ayushman', 'Ayushman'),
            ('Himcare', 'Himcare'),
            ('Reimbursement', 'Reimbursement'),
            ('Others', 'Others'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class Time(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control w-35'})
        }


class Vessel(forms.ModelForm):
    class Meta:
        types = (
            ('1', '1'),
            ('2', '2'),
            ('3', ' 3'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class Vascular(forms.ModelForm):
    class Meta:
        types = (
                ('Femoral', 'Femoral'),
                ('Distal Radial', 'Distal Radial'),
                ('Radial', 'Radial'),
                ('Ulnar', 'Ulnar'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


reasons = (
    ('Due to Reimbursement (financial reason)',
     'Due to Reimbursement (financial reason)'),
    ('Staging was planned prior to index procedure due to obvious case complexity*',
     'Staging was planned prior to index procedure due to obvious case complexity*'),
    ('Due to unanticipated case complexity*',
     'Due to unanticipated case complexity*'),
    ('Due to reached limits of contrast use*',
     'Due to reached limits of contrast use*'),
    ('Due to reached limits of radiation*',
     'Due to reached limits of radiation*'),
    ('Due to patient fatigue*', 'Due to patient fatigue*'),
    ('Due to operator discretion*', 'Due to operator discretion*'),
    ('Due to procedural complication or patient instability*',
     'Due to procedural complication or patient instability*')

)


class ReasonForStaging(forms.ModelForm):
    ans_text = forms.MultipleChoiceField(
        choices=reasons, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')


class FFRChoice2(forms.ModelForm):
    class Meta:
        types = (
                ('LMCA ', 'LMCA '),
                ('LAD/D1 ', ' LAD/D1 '),
                ('LCx/OM1 ', 'LCx/OM1'),
                ('RCA/PDA or PLV', 'RCA/PDA or PLV'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class PresentAbsent(forms.ModelForm):
    class Meta:
        types = (
                ('Present', 'Present'),
                ('Absent', 'Absent'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class select_form(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Textarea(attrs={'class': 'form-control'})
        }


class PrePciForm(forms.ModelForm):
    class Meta:
        types = (
                ('0', '0 '),
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class LessionChoice1(forms.ModelForm):
    class Meta:
        types = (
                ('0.0.1 ', ' 0.0.1 '),
                ('0.1.0', '0.1.0'),
                ('1.0.0 ', '1.0.0 '),
                ('0.1.1 ', ' 0.1.1'),
                (' 1.0.1 ', ' 1.0.1 '),
                ('1.1.0 ', '1.1.0 '),
                ('1.1.1', '1.1.1'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class MR_Grade(forms.ModelForm):
    class Meta:
        types = (
                ('Absent', ' Absent '),
                ('Mild ', 'Mild'),
                ('Moderate', 'Moderate'),
                ('Severe', 'Severe'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }


class ArrhythmiaForm(forms.ModelForm):
    class Meta:
        opt = (
            ('No', 'No'),
            ('Atrial Fibrillation', 'Atrial Fibrillation'),
            ('Ventricular Tachycardia', 'Ventricular Tachycardia'),
            ('Ventricular Fibrillation', 'Ventricular Fibrillation'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices = opt, attrs={'class': 'form-control w-35'})
        }

class AtrioventricularBlockForm(forms.ModelForm):
    class Meta:
        types = (
                ('2', '2'),
                ('3', '3'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types, attrs={'class': 'form-control w-35'})
        }
