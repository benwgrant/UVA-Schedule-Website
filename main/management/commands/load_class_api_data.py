from django.core.management.base import BaseCommand, CommandError
from main.models import SubjectClasses, AllSubjects
from datetime import datetime
import pandas as pd
import json
import requests
import time  # This function allows us to sleep between api calls to avoid overwhelming the sis api


class Command(BaseCommand):

    help = "loads class data for all subjects and a provided page into the database."

    def add_arguments(self, parser):
        parser.add_argument('page', type=int, help='page to load')

    def handle(self, *args, **options):

        base_api_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
        response = requests.get(base_api_url)

        # to avoid any issue at the start loading the initial data
        time.sleep(1)

        json_data = response.json()
        df = pd.DataFrame(json_data['subjects'])
        subject_list = df['subject'].unique()

        page = options['page']  # The argument for the page from above

        # deletes the currently existing model for page, page
        SubjectClasses.objects.filter(page=page).delete()

        # spring and fall 2023 terms, could add other terms if we wanted to
        term_list = ['1232']

        print("Beginning loop:")

        total = 202
        sofar = 0

        for subject in subject_list:
            base_api_url = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term_list[0]}&subject={subject}&page={page}"
            response = requests.get(base_api_url)
            json_data2 = response.json()

            # here is where we create a table entry for the first 100 classes of each subject

            for item in json_data2:
                # These initialize the start and end time fields if they exist
                # there are some edge cases where classes don't have meeting times, this if block solves those.
                if len(item['meetings']) != 0:
                    start_time = item['meetings'][0]['start_time']
                    end_time = item['meetings'][0]['end_time']
                    days = item['meetings'][0]['days']
                    facility_id = item['meetings'][0]['facility_id']
                else:
                    start_time = "N/A"
                    end_time = "N/A"
                    days = "N/A"
                    facility_id = "N/A"

                # code to extract the email of the instructor for the advisor model.
                if len(item['instructors']) != 0:
                    instructor = item['instructors'][0]['name']
                    instructor_email = item['instructors'][0]['email']
                else:
                    instructor = "N/A"
                    instructor_email = "N/A"

                # necessary for html logic, don't want to display buttons for labs
                if item['component'] == "LEC":
                    isLecture = 1
                else:
                    isLecture = 0

                subject_n = SubjectClasses(
                    index=item['index'],
                    crse_id=item['crse_id'],
                    strm=item['strm'],
                    session_code=item['session_code'],
                    class_section=item['class_section'],
                    class_nbr=item['class_nbr'],
                    component=item['component'],
                    isLecture=isLecture,
                    subject=item['subject'],
                    catalog_nbr=item['catalog_nbr'],
                    acad_group=item['acad_group'],
                    class_capacity=item['class_capacity'],
                    enrollment_total=item['enrollment_total'],
                    enrollment_available=item['enrollment_available'],
                    descr=item['descr'],
                    # here is where the above start and end times are assigned
                    start_time=start_time,
                    end_time=end_time,
                    days=days,
                    facility_id=facility_id,
                    instructor=instructor,
                    instructor_email=instructor_email,
                    # The page of where the class was loaded
                    page=page
                )
                subject_n.save()
            sofar += 1
            print(
                f"Loaded {subject} page: {page}, waiting 0.1s to avoid overloading sis api. Completed {sofar} / {total}")
            time.sleep(0.1)  # sleeping to rate limit the api
        self.stdout.write(self.style.SUCCESS(
            f'Successfully populated SubjectClasses for all subjects, page:{page}.'))
