# Create your views here.
from django.shortcuts import render, redirect
from .models import Appointment, Dates
from .forms import DocumentForm, Symptom, Report, Diagnosis
import openpyxl
from .algo import *
import statistics


def index(request):
    return render(request, 'medproc/index.html')


def about(request):
    return render(request, 'medproc/about.html')


def datapage(request):
    list1 = []
    list2 = []
    list3 = []
    for i in Appointment.objects.all():
        list1.append(i.date[:10])
        list2.append(i.symptom)
        list3.append(i.diagnosis)

    return render(request, 'medproc/datapage.html', {'list1': list1, 'list2': list2, 'list3' : list3})


def model_form_upload(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        docu = request.FILES['document']
        if form.is_valid():
            Appointment.objects.all().delete()
            wb = openpyxl.load_workbook(docu)
            excel_data = list()
            worksheet = wb["Sheet1"]
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            for i in excel_data:
                Appointment.objects.create(date=i[0], symptom=i[1], diagnosis=i[2])

            return redirect('medproc:reportselect')
    else:
        form = DocumentForm()
    return render(request, 'medproc/upload.html', {'form': form})


def reportselect(request):
    if request.method == 'POST':
        form = Report(request.POST)
        reply = request.POST['report']
        a = request.POST['startdate']
        b = request.POST['enddate']


        list = []
        for i in Appointment.objects.all():
            list.append(i.date)

        if comparedate(a, b, list) == False:
            mess = "Your dates are out of scope"
            return render(request, 'medproc/reportselect.html', {'form': form, 'mess': mess})
        Dates.objects.all().delete()
        Dates.objects.create(startdate=a, enddate=b)

        if reply == 'General Date':
            return redirect('medproc:gendateview')
        if reply == 'General Symptoms':
            return redirect('medproc:gensymptview')
        if reply == 'General Diagnosis':
            return redirect('medproc:gendiagview')
        if reply == 'Specific Symptom':
            return redirect('medproc:choosesympt')
        if reply == 'Specific Diagnosis':
            return redirect('medproc:diagform')
    else:
        form = Report()

    return render(request, 'medproc/reportselect.html', {'form':form})


def gendateview(request):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date[:10], i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = generaldate(newlist)
    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/gendatetemp.html', {'key':key, 'value': value, 'forma': forma, 'med': med})


def generalsymptview(request):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = generalsympt(newlist)
    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/gensympttemp.html', {'key':key, 'value': value, 'forma': forma, 'med': med})


def altgensympt(request):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = generalsympt(newlist)
    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/altgensymp.html', {'key':key, 'value': value, 'forma': forma, 'med': med})


def generaldiagview(request):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = generaldiag(newlist)
    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/gendiagtemp.html', {'key':key, 'value': value, 'forma': forma, 'med': med})


def altgendiag(request):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = generalsympt(newlist)
    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/altgendiag.html', {'key':key, 'value': value, 'forma': forma, 'med': med})


def specform(request):
    if request.method == 'POST':
        form = Symptom(request.POST)
        if form.is_valid():
            sympt = request.POST['symptom']
            lowsymp = sympt.lower()
            return specsymptview(request, sympt)
    sympt = Symptom()
    return render(request, 'medproc/choosesympt.html', {'form' : sympt})


def diagform(request):
    if request.method == 'POST':
        diag = request.POST['diag']
        lowdiag = diag.lower()
        return specdiagview(request, lowdiag)
    else:
        diag = Diagnosis()
    return render(request, 'medproc/choosediag.html', {'form': diag})


def specsymptview(request, sympt):
    print('working')
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom, i.diagnosis))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = specsympt(newlist, sympt)
    key1, value1 = corrsympt(newlist, sympt)

    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/specsympttemp.html', {'key':key, 'value': value, 'key1': key1, 'value1': value1, 'forma': forma, 'med': med, 'sympt': sympt})


def specdiagview(request, diag):
    list = []
    for i in Appointment.objects.all():
        list.append((i.date, i.symptom.lower(), i.diagnosis.lower()))

    startdate = Dates.objects.latest('startdate').startdate
    enddate = Dates.objects.latest('enddate').enddate

    newlist = choosedates(list, startdate, enddate)

    a = specdiag(newlist, diag)

    key1, value1 = corrdiag(newlist, diag)

    key = []
    value = []
    for i in a:
        key.append(i[0])
        value.append(i[1])

    forma = "{:.2f}".format(listsum(a))
    med = statistics.median(value)

    return render(request, 'medproc/specdiagtemp.html', {'key':key, 'value': value, 'key1': key1, 'value1': value1, 'forma': forma, 'med': med, 'diag': diag})
