from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
# Comment.objects.all().delete()

def index(request):
    return render(request, 'wall_feed/index.html')

def user_create(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')

    else:
        if request.POST['create'] == 'register':
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])

            request.session['first_name'] = new_user.first_name
            request.session['user_id'] = new_user.id

        return redirect(f'/wall')



def login(request):

    matching_users = User.objects.filter(email = request.POST['login_email'])

    if matching_users:
        user = matching_users[0]
        if user.password == request.POST["login_password"]:
            request.session['first_name'] = user.first_name
            request.session['user_id'] = user.id
        else:
            messages.error(request, "Incorrect password.")
    else:
        messages.error(request, "User does not exist.")


    return redirect(f'/wall')

def logout(request):
    request.session.clear()
    return redirect("/")


def wall_feed(request):


    context = {
        "messages": Message.objects.all(),
        "user": User.objects.get(id=request.session['user_id']),

    }
    return render(request, 'wall_feed/main.html', context)


def post_message(request):
    user_id = request.session['user_id']
    this_user = User.objects.get(id = user_id)
    Message.objects.create(message=request.POST['message_content'], user=this_user)

    return redirect('/wall')


def post_comment(request, message_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_message = Message.objects.get(id = message_id)
    new_comment = Comment.objects.create(comment=request.POST['comment_content'], message=this_message, user=this_user)
    this_message.comments.add(new_comment)

    print(new_comment)
    return redirect('/wall')

