from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from pymongo import MongoClient, errors, DESCENDING, ASCENDING
from pymongo.auth import authenticate
from django.contrib.auth.decorators import login_required

client = MongoClient("mongodb+srv://Cassie:Cassie@cassie-kdpcc.mongodb.net/test?retryWrites=true&w=majority")
database = client["ticketbooking"]
db = database["booking"]


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(username)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('ticket:index')
    else:
        form = UserCreationForm()
    return render(request, 'ticketbooking/register.html', {'form': form})


@login_required
def index(request):
    return render(request, 'ticketbooking/home.html')


@login_required
def book(request):
    if request.POST:
        if request.POST['source'] == request.POST["dest"]:
            return render(request, 'ticketbooking/book.html', {
                'msg': 'Source and destination cannot be same'
            })
        pass_data = dict()
        pass_data['username'] = request.user.username
        pass_data['amount'] = 20
        for i in request.POST:
            if i not in ['csrfmiddlewaretoken', 'login_submit']:
                pass_data[i] = request.POST[i]
        print(pass_data)
        db.insert_one(pass_data)
        return render(request, 'ticketbooking/book_action.html', {
            'value': '20Rs'
        })
    return render(request, 'ticketbooking/book.html')


@login_required
def tran(request):
    pass_value = list()
    for i in db.find({'username': request.user.username}).sort( [['_id', -1]] ):
        pass_value.append(i)
    return render(request, 'ticketbooking/transac.html', {'datas': pass_value})


@login_required
def receipt(request):
    return render(request, 'ticketbooking/Receipt.html', {
        'data': db.find_one({'username': request.user.username}, sort=[('_id', DESCENDING)])
    })
