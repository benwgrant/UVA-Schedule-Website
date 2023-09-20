from django.test import RequestFactory, TestCase, Client
import requests
from django.contrib import admin
from django.urls import include, path
from .views import index, superuser, user
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
import requests
import json
import pandas as pd

# Create your tests here.


class Sprint4(TestCase):
    # def setUp(self):
    #     self.factory = RequestFactory()
    #     self.user = User.objects.create_user(
    #         username="hanewton35@gmail.com", email="hanewton35@gmail.com", password="test")

    # def test_SISAvail(self):
    #     """Can't access SIS"""
    #     try:
    #         base_api_url = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01"
    #         response = requests.get(base_api_url)
    #     except:
    #         self.fail()

    def test_indexAvail(self):
        """Can't access index"""
        try:
            redirect('/')
        except:
            self.fail()

    def test_superuserAvail(self):
        """Can't access superuser"""
        try:
            redirect('/superuser')
        except:
            self.fail()

    def test_userAvail(self):
        """Can't access user"""
        try:
            redirect('/user')
        except:
            self.fail()

    def test_searchPageAvail(self):
        """Can't access searchPage"""
        try:
            redirect('/searchPage')
        except:
            self.fail()

    def test_displayClassesAvail(self):
        """Can't access displayClasses"""
        try:
            redirect('/displayClasses')
        except:
            self.fail()

    # def test_SubjectSearch(self):
    #     """Subject Search Not Working"""
    #     c = Client()
    #     response = c.get("/displayClasses", {"subject": "CS"})
    #     self.assertNotContains(response, "No Results")

    # def test_NameSearch(self):
    #     """Name Search Not Working"""
    #     c = Client()
    #     response = c.get("/displayClasses", {"name": "Introduction"})
    #     self.assertNotContains(response, "No Results")
