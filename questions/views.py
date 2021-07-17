from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choices, Vote
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from scipy import spatial

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
        return redirect('questions:show')
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

@login_required(login_url = "/accounts/login")
def showResult(request):
    user = request.user
    votes = Vote.objects.filter(user = user)
    last15 = votes.order_by('-id')[:16]
    reversed(last15)
    print(last15)
    df = pd.read_csv('./fully_processed_college_db.csv')
    for u in votes:
        print(u.choice)
    userList = []
    for vote in last15:
        userList.append(int(vote.choice))
    userList.pop()
    #userList.reverse()
    print(userList)
    df['Score'] = ''
    w1,w2,w3 = 3,2,1
    def score(u,c):
        sc = w1*(1 - spatial.distance.cosine(u[0:4],c[0:4])) +  w2*(1 - spatial.distance.cosine(u[4:13],c[4:13])) + w3*(1 - spatial.distance.cosine(u[13:],c[13:]))
        p = (sc / 6) * 100
        return p
    for ind in df.index:
        college = [df['r_research'][ind], df['r_sports_gym'][ind], df['r_diversity'][ind], df['r_hostels'][ind], 
                df['r_transportation_facilities'][ind], df['r_alumni_network'][ind], df['r_safety'][ind], df['r_on_campus_life'][ind],  
                df['r_food'][ind], df['r_clubs'][ind], df['r_infrastructure'][ind], df['r_fests'][ind], 
                df['r_scholarships'][ind], df['r_study_abroad'][ind], df['r_placements'][ind]]
        df['Score'][ind] = score(userList,college)
    df = df.sort_values(by="Score",ascending=False)
    resultDict = {}
    flag = 0
    for i in df.index:
        resultDict[df['college_name'][i]] = df['campus_size'][i]
        print(df['college_name'][i])
        flag += 1
        if flag == 10:
            break
    df = None
    return render(request, 'questions/show.html', {'resultDict': resultDict})