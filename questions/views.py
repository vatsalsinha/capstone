from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choices, Vote
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.views import generic

# Create your views here.
def index(request):
    questions = Question.objects.all()
    return render(request, 'questions/allquestions.html', {'questions' : questions})
    
@login_required(login_url = "/accounts/login")
def questionDetail(request, question_id):
    # question = get_object_or_404(Question, pk = question_id)
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        return redirect('questions:index')
    return render(request, 'questions/questiondetail.html', {'question': question})



@login_required(login_url = "/accounts/login")
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    user = request.user
    try:
        option_selected = question.choices_set.get(pk= request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        return render(request, 'questions/questiondetail.html', {'error_message': "you didnt select a choice"})
    else:
        vote = Vote(user=request.user, question=question, choice=option_selected)
        vote.save()
    return HttpResponseRedirect(reverse('questions:detail', args=(question_id+1,))) # does '/polls/id/results/'

    