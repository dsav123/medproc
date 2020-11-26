from django import forms
from .models import Document, Appointment


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)

symptlist = []
for i in Appointment.objects.all():
    symptlist.append((i.symptom, i.symptom))
newsymptlist = list(dict.fromkeys(symptlist))


class Symptom(forms.Form):
    symptom = forms.ChoiceField(choices=newsymptlist, label="Enter Symptom")


diaglist = []
for i in Appointment.objects.all():
    diaglist.append((i.diagnosis, i.diagnosis))
newdiaglist = list(dict.fromkeys(diaglist))


class Diagnosis(forms.Form):
    diag = forms.ChoiceField(choices=newdiaglist, label="Enter Diagnosis")


Reportchoice = [('General Date', 'General Date'), ('General Symptoms', 'General Symptoms'),
                ('General Diagnosis', 'General Diagnosis'), ('Specific Symptom', 'Specific Symptom'),
                ('Specific Diagnosis', 'Specific Diagnosis')]

dlist = []
for i in Appointment.objects.all():
    dlist.append((i.date[:10], i.date[:10]))
newdatelist = list(dict.fromkeys(dlist))


class Report(forms.Form):
    report = forms.ChoiceField(choices=Reportchoice, label="Report Type")
    startdate = forms.CharField( label="Start Date", max_length=10)
    enddate = forms.CharField(label="End Date", max_length=10)
