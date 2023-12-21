from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question,Topic,Answer,User
from .forms import QuestionForm,UserForm,MyUserCreationForm,AnswerForm

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email=request.POST.get("email").lower()
        password=request.POST.get("password")
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist")
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Incorrect Information")
    context={'page':page}
    return render(request,'base/auth.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    form=MyUserCreationForm()

    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error occured during registration')

    context={'page':page,'form':form}
    return render(request,'base/auth.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    questions=Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(query__icontains=q)
        )
    topics=Topic.objects.all()[0:5]
    question_count=questions.count()
    answers=Answer.objects.filter(
        Q(question__topic__name__icontains=q)
    )

    context={'questions':questions,'topics':topics,'question_count':question_count,'answers':answers}
    return render(request,'base/home.html',context)

def question(request,pk):
    question=Question.objects.get(id=pk)
    answers=question.answer_set.all().order_by('-created')
    participants=question.participants.all()

    if request.method == 'POST':
        answer=Answer.objects.create(
            user=request.user,
            question=question,
            body=request.POST.get('body')
        )
        question.participants.add(request.user)
        return redirect('question',pk=question.id)

    context={'question':question,'answers':answers,'participants':participants}
    return render(request,'base/question.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    questions=user.question_set.all()
    answers=user.answer_set.all()
    topics=Topic.objects.all()
    context={'user':user,'questions':questions,'answers':answers,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url="/login")
def createQuestion(request):
    form=QuestionForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        Question.objects.create(
            host=request.user,
            topic=topic,
            query=request.POST.get('query')
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/question_form.html',context)

@login_required(login_url="/login")
def updateQuestion(request,pk):
    question=Question.objects.get(id=pk)
    form=QuestionForm(instance=question)
    topics=Topic.objects.all()

    if request.user != question.host:
        return HttpResponse("You are not allowed")

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        question.query=request.POST.get('query')
        question.topic=topic
        question.save()
        return redirect('home')
    context={'question':question,'form':form,'topics':topics}
    return render(request,'base/question_form.html',context)

@login_required(login_url="/login")
def deleteQuestion(request,pk):
    question=Question.objects.get(id=pk)

    if request.user != question.host:
        return HttpResponse("You are not allowed")

    if request.method=='POST':
        question.delete()
        return redirect('home')
    context={'obj':question}
    return render(request,'base/delete.html',context)

@login_required(login_url="/login")
def deleteAnswer(request,pk):
    answer=Answer.objects.get(id=pk)

    if request.user != answer.user:
        return HttpResponse("You are not allowed")

    if request.method=='POST':
        answer.delete()
        return redirect('home')
    context={'obj':answer}
    return render(request,'base/delete.html',context)

@login_required(login_url='/login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    context={'form':form}
    return render(request,'base/update-user.html',context)

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'base/topics.html',context)

def activityPage(request):
    answers=Answer.objects.all()
    context={'answers':answers}
    return render(request,'base/activity.html',context)

@login_required(login_url='/login')
def answer(request,pk):
    question=Question.objects.get(id=pk)
    form=AnswerForm()
    if request.method == 'POST':
        answer=Answer.objects.create(
            user=request.user,
            question=question,
            body=request.POST.get('body')
        )
        question.participants.add(request.user)
        return redirect('question',pk=question.id)
    context={'form':form,'question':question}
    return render(request,'base/answer_form.html',context)
