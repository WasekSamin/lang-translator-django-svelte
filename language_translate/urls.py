from django.urls import path

from .views import (
    LanguageTranslateView, 
)

app_name = "language_translator"
urlpatterns = [
    path("translate/text=<str:text>/lang=<str:to_lang>/", LanguageTranslateView.as_view(), name="lang-translate"),
]