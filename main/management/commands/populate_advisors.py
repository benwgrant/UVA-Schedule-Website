from django.core.management.base import BaseCommand, CommandError
from main.models import AdvisorProfile, SubjectClasses, UserProfile
from django.contrib.auth.models import User
import pandas as pd

# this command populates the advisor models with advisors from every subject that can be randomly assigned to students who fill out the form on the home page.


class Command(BaseCommand):

    def handle(self, *args, **options):

        # wipe all current advisors
        AdvisorProfile.objects.all().delete()
        UserProfile.objects.all().delete()

        User.objects.all().delete()  # temporary for testing purposes

        # Get all of the classes
        classList = SubjectClasses.objects.all()
        df_classes = pd.DataFrame(classList.values())

        # get a list of the different subjects
        subjectList = df_classes['subject'].unique()

        # maintain a list of advisors to avoid duplicates
        advisors = []

        current = 0
        total = 2323

        # Loop through every subject and every instructor creating a potential advisor for each one. This simultaneously creates an actual account for the given user whom we will later prompt to change their password.
        for subject in subjectList:
            subjectQuery = SubjectClasses.objects.filter(subject=subject)
            instructorNum = 0
            for course in subjectQuery:
                # and instructorNum <= 10:
                if course.instructor not in advisors and course.instructor_email and instructorNum <= 10:
                    advisor_computingid = course.instructor_email.split('@')[0]
                    # The two models created below are an advisor and a user to match that advisor, when advisors log in using their computing id as both username and password they will be prompted to change their password.
                    advisor = AdvisorProfile(instructor_name=course.instructor, username=advisor_computingid,
                                             advisor_email=course.instructor_email, advisor_subject=subject)
                    user = User.objects.create_user(
                        username=advisor_computingid, email=course.instructor_email, password=advisor_computingid)

                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully created a django account for {course.instructor} this is {instructorNum}/10 for {subject}'))
                    user.save()
                    advisor.save()
                    advisors.append(course.instructor)

                    instructorNum += 1
                    current += 1
