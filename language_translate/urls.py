from django.urls import path

from .views import (
    LanguageTranslateView, 
)

app_name = "language_translator"
urlpatterns = [
    path("translate/", LanguageTranslateView.as_view(), name="lang-translate"),
]