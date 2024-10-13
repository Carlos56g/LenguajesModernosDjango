from django.urls import path

from . import views

app_name="polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("newQuestion", views.QuestionCreateView.as_view(), name="newQuestion"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/",views.vote, name="vote"),
    path("<int:pk>/UpdateQuestion", views.UpdateQuestion.as_view(), name="updateQuestion"),
    path("<int:question_id>/put/", views.putQuestion, name="putQuestion"),
]