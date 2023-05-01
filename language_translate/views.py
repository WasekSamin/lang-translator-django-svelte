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

    def post(self, request, format=None):
        resp_msg = {
            "error": True,
            "status": 400
        }

        text = request.data.get("text")
        src_lang = request.data.get("srcLang")
        dest_lang = request.data.get("destLang")

        if text is not None and src_lang is not None and dest_lang is not None:
            try:
                translator = Translator()
                translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
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
        return Response(resp_msg)