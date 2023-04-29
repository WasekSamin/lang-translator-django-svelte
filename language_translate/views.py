from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from googletrans import Translator


class LanguageTranslateView(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = ()

    def post(self, request, text, to_lang, format=None):
        resp_msg = {
            "error": True,
            "status": 400
        }

        try:
            translator = Translator()
            translated_text = translator.translate(text, dest=to_lang)
        except:
            return Response(resp_msg)
        else:
            print(translated_text)
            resp_msg = {
                "error": False,
                "status": 200,
                "text": translated_text.text
            }
        return Response(resp_msg)