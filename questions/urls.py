from django.urls import path
from . import views 
app_name = 'questions'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:question_id>/', views.questionDetail, name = 'detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    
]