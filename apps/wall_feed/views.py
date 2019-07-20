from django.shortcuts import render, redirect
from apps.wall_feed.models import *
from django.contrib import messages

# Create your views here.

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


def wall_feed(request):


    context = {
        "messages": Message.objects.all(),
        "user": User.objects.get(id=request.session['user_id']),

    }
    return render(request, 'wall_feed/main.html', context)


def post_message(request):
    user_id = request.session['user_id']
    this_user = User.objects.get(id = user_id)


    new_message = Message.objects.create(message=request.POST['message_content'], user=this_user)
    request.session['message_id'] = new_message.id

    return redirect('/wall')


def post_comment(request):
    this_user = User.objects.get(id = request.session['user_id'])
    message_id = request.session['message_id']
    this_message = Message.objects.get(id = message_id)
    new_comment = Comment.objects.create(comment=request.POST['comment_content'], message=this_message, user=this_user)

    request.session['comment_id'] = new_comment.id

    print(new_comment)
    return redirect('/wall')


def logout(request):
    request.session.clear()
    return redirect('/')