from django.core.management.base import BaseCommand, CommandError
from main.models import SubjectClasses, AllSubjects
from datetime import datetime
import pandas as pd
import json
import requests


class Command(BaseCommand):
    #populates the models in the postgres database
    
    help = "Populates the AllSubjects table in the database"
    
    def handle(self, *args, **options): #populates the local data
        #Get data
        base_api_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
        response = requests.get(base_api_url)
        
        if(response.status_code != 200):
            print("Error getting API data for AllSubjects")
        
        json_data = response.json()
    
        for item in json_data['subjects']:
            subject = AllSubjects(subject = item['subject'], descr = item['descr'], acad_groups = item['acad_groups'], careers = item['careers'], campuses = item['campuses'])
            subject.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated AllSubjects.'))