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

class GetDetails(forms.Form):
    p_id = forms.IntegerField(label='Patient ID', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))


class FloatInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.NumberInput(attrs={'step': 0.1})
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
            'ans_text': forms.Select(choices=truefalse)
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
            'ans_text': forms.Select(choices=truefalse)
        }


"""class GetDetails(forms.Form):
    truefalse = (
        ('q1', '≤14 Days to ≤24 Days To PCI'),
        ('q2', 'PCI-Index Procedure'),
        ('q3', 'DISCHARGE'),
        ('q4', '01Month (± 7 days)'),
        ('6 Months (± 30 days)', '6 Months (± 30 days)'),
        ('12 Months (± 30 days)', '12 Months (± 30 days)'),
        ('24 Months (± 30 days)', '24 Months (± 30 days)'),
        ('36 Months (± 30 days)', '36 Months (± 30 days)'),
        ('48 Months (± 30 days)', '48 Months (± 30 days)'),
        ('60 Months (± 30 days)', '60 Months (± 30 days)'),
    )
    p_id = forms.IntegerField(label='Patient ID')
    query = forms.TypedChoiceField(choices=truefalse)"""


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
            'ans_text': forms.Select(choices=truefalse)
        }


class NumberInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.NumberInput(attrs={'class': 'form-control'})
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
            'ans_text': forms.Select(choices=types)
        }


class TextInput(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.TextInput(attrs={'class': 'form-control'})
        }


class DateTime(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.DateInput(attrs={'type': 'date'})
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
            'ans_text': forms.Select(choices=codes,)
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
            'ans_text': forms.Select(choices=codes,)
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
            'ans_text': forms.Select(choices=codes,)
        }


class CardiacUnit(forms.ModelForm):
    class Meta:
        model = Result
        codes = (
                ('-', 'Select'),
                ('U/ L', 'U/ L'),
                ('Ng/ml', 'Ng/ml'),
                ('mcg/ l', 'mcg/ l')
        )
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=codes,)
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
            'ans_text': forms.Select(choices=codes,)
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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
        }


"""class RandChoice2(forms.ModelForm):
    class Meta:
        types = (
                ('TVD ', 'TVD '),
                ('DVD', ' DVD'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }"""


class Time(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.TimeInput(attrs={'type': 'time'})
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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
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


class FFRChoice1(forms.ModelForm):
    class Meta:
        types = (
                ('FFR', 'FFR'),
                ('IFR', ' IFR'),
                ('RFR', 'RFR'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
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
            'ans_text': forms.Select(choices=types)
        }


class SupraflexDiameter(forms.ModelForm):
    class Meta:
        types = (
                ('2.00mm ', ' 2.00mm'),
                ('2.25mm', '2.25mm'),
                ('2.50mm', '2.50mm'),
                ('2.75mm', ' 2.75mm'),
                ('3.00mm', '3.00mm'),
                ('3.50mm', '3.50mm'),
                ('4.00mm', '4.00mm'),
                ('4.50mm', '4.50mm'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


class SupraflexLength(forms.ModelForm):
    class Meta:
        types = (
                ('8 mm', ' 8 mm'),
                ('12 mm', '12 mm'),
                ('16 mm ', '16 mm'),
                ('20 mm', ' 20 mm'),
                ('24 mm', '24 mm'),
                ('28 mm', '28 mm'),
                ('32 mm', '32 mm'),
                ('36 mm', '36 mm'),
                ('40 mm', '40 mm'),
                ('44 mm', '44 mm'),
                ('48 mm', '48 mm'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


class XienceDiameter(forms.ModelForm):
    class Meta:
        types = (
                ('2.25mm', '2.25mm'),
                ('2.50mm', '2.50mm'),
                ('2.75mm', ' 2.75mm'),
                ('3.00mm', '3.00mm'),
                ('3.25mm', '3.25mm'),
                ('3.50mm', '3.50mm'),
                ('4.00mm', '4.00mm'),


        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


class XienceLength(forms.ModelForm):
    class Meta:
        types = (
                ('8 mm', ' 8 mm'),
                ('12 mm', '12 mm'),
                ('15 mm ', '15 mm'),
                ('18 mm', ' 18 mm'),
                ('23 mm', '23 mm'),
                ('28 mm', '28 mm'),
                ('33 mm', '33 mm'),
                ('38 mm', '38 mm'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


class StentType(forms.ModelForm):
    class Meta:
        types = (
                ('SUPRAFLEX', 'SUPRAFLEX'),
                ('XIENCE', 'XIENCE'),
                (' Other,Specify', ' Other,Specify'),

        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=types)
        }


class TimiFlow(forms.ModelForm):
    class Meta:
        truefalse = (
            ('Unknown', 'Unknown'),
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=truefalse)
        }


class Complication(forms.ModelForm):
    class Meta:
        truefalse = (
            ('Dissection > Type B', 'Dissection > Type B'),
            ('No re-flow1', 'No re-flow1'),
            ('Distal embolization', 'Distal embolization2'),
            ('Perforation', 'Perforation'),
            ('Abrupt closure', 'Abrupt closure')
        )
        model = Result
        fields = ('p_id', 'q_id', 'ans_text')
        widgets = {
            'ans_text': forms.Select(choices=truefalse)
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
            'ans_text': forms.Select(choices = opt)
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
            'ans_text': forms.Select(choices=types)
        }