from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentListView,
    DocumentDetailView,
    QADetailView,
    IntegratedQAView,
)

app_name = 'documents'
urlpatterns = [
    path("documents/create", DocumentCreateView.as_view(), name="documents-list"),
    path('documents/', DocumentListView.as_view(), name="documents-list"),
    path("documents/<int:pk>/", DocumentDetailView.as_view(), name="documents-detail"),

    path("qu_ans/<int:pk>/", QADetailView.as_view(), name="qa-detail"),
    path("search/", IntegratedQAView.as_view(), name="fts-search"),
]
