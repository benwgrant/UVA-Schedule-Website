from difflib import SequenceMatcher
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import SubjectClasses, Cart, Schedule, AdvisorProfile, UserProfile
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, FloatField
import pandas as pd
from django.db.models import F, Case, Value, When
from django.contrib.postgres.search import TrigramSimilarity
# for generating the advisors
import random
# timezone stuff, py timezone
import pytz

# len(AdvisorProfile.objects.filter(username=request.user.username)) == 0 or


def index(request):
    if (not request.user.is_authenticated):  # not logged in
        # return redirect('/accounts/google/login/?process=login')
        return redirect('/accounts/login')
    # and len(AdvisorProfile.objects.filter(advisor_email=request.user.email)) == 0:
    elif len(AdvisorProfile.objects.filter(username=request.user.username)) == 0:
        return redirect("/user")
    else:
        return redirect("/superuser")


def superuser(request):
    context = {}

    # find all of the users that correspond to this advisor
    advisor_profile = AdvisorProfile.objects.get(
        username=request.user.username)
    advisee_profiles = UserProfile.objects.filter(
        advisor=advisor_profile)

    # check if there are 0 users, then display "no advisees"
    noUsersBool = 0
    if len(advisee_profiles) == 0:
        noUsersBool = 1
        context['noUsersBool'] = noUsersBool
    else:
        context['noUsersBool'] = noUsersBool

    context["advisee_profiles"] = advisee_profiles
    context["Subject"] = advisor_profile.advisor_subject

    return render(request, "main/superuser.html", context)


def approveSchedule(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user_schedule = Schedule.objects.get(id=id)
        user_schedule.is_approved = True
        user_schedule.save()

        return redirect("/superuser")


def rejectSchedule(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user_schedule = Schedule.objects.get(id=id)
        user_schedule.is_approved = False
        user_schedule.save()

        return redirect('/superuser')


def user(request):

    context = {}

    # find the userprofile if it exists, otherwise make one on the spot
    if UserProfile.objects.filter(username=request.user.username).exists():
        userQuery = UserProfile.objects.get(username=request.user.username)
    else:
        userQuery = UserProfile(username=request.user.username,
                                user_email=request.user.email)
        userQuery.save()

    # meaning they have not chosen their major yet
    chosenBool = 1  # defaults to one, switched to 0 if N/C "Not Chosen"
    if userQuery.user_major == "N/C":
        chosenBool = 0
        df = pd.DataFrame(SubjectClasses.objects.all().values())
        subjectList = df.sort_values(by='subject')['subject'].unique()
        # for use in the html to display a drop down menu of choices for majors if the user has never chosen one.
        context['subjectList'] = subjectList
        context['chosenBool'] = chosenBool
    else:
        # this will be 1 telling us not to display the drop down menu but instead the advisor.
        context['chosenBool'] = chosenBool
        context['advisor'] = userQuery.advisor

        df = pd.DataFrame(SubjectClasses.objects.all().values())
        subjectList = df.sort_values(by='subject')['subject'].unique()
        context['subjectList'] = subjectList

    return render(request, "main/user.html", context)


def generateAdvisor(request):
    if request.method == "GET":
        subject = request.GET.get("subject")
        advisors = AdvisorProfile.objects.filter(advisor_subject=subject)

        # randomness begins here
        random_index = random.randint(0, len(advisors)-1)
        random_advisor = advisors[random_index]

        user = UserProfile.objects.get(username=request.user.username)

        user.user_major = subject
        user.advisor = random_advisor

        user.save()
    # they want to choose a different major:
    elif request.method == "POST":
        schedules = Schedule.objects.filter(username=request.user.username)

        # set all schedules to default value of false for new advisor.
        for schedule in schedules:
            schedule.is_approved = False
            schedule.save()

        user = UserProfile.objects.get(username=request.user.username)
        user.user_major = "N/C"
        user.advisor = None
        user.save()

    return redirect("/user")


def chooseAdvisor(request):
    if request.method == "POST":

        advisor_username = request.POST.get("advisor_username")

        user = UserProfile.objects.get(username=request.user.username)

        if len(AdvisorProfile.objects.filter(username=advisor_username)) != 0:
            user.advisor = AdvisorProfile.objects.get(
                username=advisor_username)
            user.user_major = "Undecided"
            user.save()

        return redirect("/user")

# Converts the given user account to an advisor account, all schedule data will be lost


def convertToAdvisor(request):
    if request.method == "POST":
        if (request.POST.get('advPass') == "cs3240"):
            # desiredUsername = request.POST.get("desiredUsername")
            user_profile = UserProfile.objects.get(
                username=request.user.username)
            AdvisorProfile.objects.filter(
                username=request.user.username).delete()
            advisor_account = AdvisorProfile(instructor_name=request.user.username, username=request.user.username,
                                             advisor_email=request.user.email, advisor_subject=request.POST.get('subjectFooter'))

            # clear the existing schedules for this user
            Schedule.objects.filter(username=request.user.username).delete()

            user_profile.delete()
            advisor_account.save()

            return redirect("/superuser")
        else:
            return redirect('index')

# Converts the given account to a user account, schedule data wiped and no assigned advisor


def convertToUser(request):
    if request.method == "POST":
        advisor_profile = AdvisorProfile.objects.get(
            instructor_name=request.user.username)
        UserProfile.objects.filter(username=request.user.username).delete()
        user_account = UserProfile(username=advisor_profile.username,
                                   user_email=advisor_profile.advisor_email, user_major="N/C", advisor=None)

        advisor_profile.delete()
        user_account.save()

        return redirect('index')


def searchPage(request):
    df = pd.DataFrame(SubjectClasses.objects.all().values())
    subjectList = df.sort_values(by='subject')['subject'].unique()
    context = {"subjectList": subjectList}
    return render(request, "main/searchPage.html", context)


def displayClasses(request):

    # This view queries the database and displays the subject and the page requested.

    if request.method == "GET":
        numGiven = True

        if ("subject" in request.GET):
            subject = request.GET.get('subject')

            try:
                number = int(request.GET.get('num'))
            except:
                numGiven = False

            try:
                page = int(request.GET.get('page'))
            except:
                page = 1

            # prepares the data to be sent to the html
            if (subject == ''):
                return redirect('/searchPage')

            if (numGiven):
                queryset = SubjectClasses.objects.filter(
                    subject=subject.upper(), catalog_nbr=number, component="LEC")
            else:
                queryset = SubjectClasses.objects.filter(
                    subject=subject.upper(), component="LEC")

        else:  # elif(request.GET.get("search_name")):
            name = request.GET.get('name')
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
            if (name == ''):
                return redirect('/searchPage')
            queryset = SubjectClasses.objects.annotate(sim=TrigramSimilarity(
                "descr", str(name))).filter(sim__gt=.3, component="LEC").order_by('-sim')

        data = queryset.values()
        df = pd.DataFrame(data)

        if len(queryset) != 0:
            desired_cols = ['crse_id', 'component',
                            'subject', 'catalog_nbr', 'descr', 'instructor']

            # slice the dataframe by the desired columns, don't have to drop them
            df = df[desired_cols]

        numPages = int(df.shape[0]/10+1)

        if (numPages > 1):
            df = df.truncate(before=10*(page-1), after=10*page)

        paginator = Paginator(df, 10)

        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            classes = paginator.page(paginator.num_pages)

        context = {'df': df,
                   'classes': classes,
                   'page': page,
                   'numPages': numPages}

        return render(request, 'main/displayClasses.html', context)
    else:
        return redirect('/searchPage')

# Display sections is loaded upon clicking the button at the end of each row displayed in displayClasses.


def displaySections(request):
    if request.method == "POST":

        filter1 = request.POST.get('catalog_nbr')
        filter2 = request.POST.get('subject')

        queryset = SubjectClasses.objects.filter(
            catalog_nbr=filter1, subject=filter2, component="LEC")
        data = queryset.values()
        df = pd.DataFrame(data)

        # dropping these columns for readability
        cols_to_drop = ['id', 'index', 'strm', 'session_code',
                        'acad_group', 'page']

        df.drop(columns=cols_to_drop, inplace=True)

        context = {'df': df}

        # Sends all of the sections pertaining to a single class to displaySections.html where they can be added to a cart

        return render(request, 'main/displaySections.html', context)

    else:
        return redirect("/searchPage")


def displayCart(request):

    # if the request is a GET we just display the cart
    if request.method == "GET":

        username = request.user.username

        # if there isn't a cart we have to make one first
        try:
            cart = Cart.objects.get(username=username)
        except Cart.DoesNotExist:
            cart = Cart(username=username, num_credits=0, num_classes=0)
            cart.save()

        context = {"cart": cart}

        if len(cart.classes.all()) == 0:
            context['emptyCartBool'] = 1

        return render(request, "main/displayCart.html", context)

    # A post always comes from adding a class, a get just wants to display the cart
    if request.method == "POST":
        # grabs filters from html
        catalog_nbr = request.POST.get('catalog_nbr')
        class_nbr = request.POST.get('class_nbr')

        # filters from local database and gets the class
        users_class = SubjectClasses.objects.get(
            catalog_nbr=catalog_nbr, class_nbr=class_nbr)

        # get currently logged in users username
        username = request.user.username

        try:
            cart = Cart.objects.get(username=username)
        except Cart.DoesNotExist:
            cart = Cart(username=username, num_credits=0, num_classes=0)
            cart.save()

        context = {"cart": cart}

        if len(cart.classes.all()) == 0:
            context['emptyCartBool'] = 1

        # here is the primary logic, I realize it could use some refactoring, I intend to do so eventually

        classConflict = 0  # bool to keep track of whether there was a conflict
        duplicateClass = 0

        # grabs start and end of users class:
        users_class_start = users_class.start_time
        users_class_end = users_class.end_time

        if cart.classes.all():  # Checks the cart to make sure there is at least 1 before beginning logic, adds the class otherwise
            for u_class in cart.classes.all():
                # seeing if days of the week are the same, "TuTh"=="MoWeFr", hardcoded an exception for MoTuWeTh to always check.
                if u_class.days in users_class.days or users_class.days in u_class.days or u_class.days == "MoTuWeTh" or users_class.days == "MoTuWeTh":

                    # verify these aren't the same classes
                    if u_class.catalog_nbr == users_class.catalog_nbr and users_class.component == "LEC":
                        duplicateClass = 1
                        break

                    # grabbing start and end time for the cart classes
                    u_class_start = u_class.start_time
                    u_class_end = u_class.end_time

                    # Helper function that checks if the classes overlap
                    if overlapChecker(u_class_start, u_class_end, users_class_start, users_class_end) and users_class.component == "LEC":
                        # there was an overlap with an existing class, do not add the class to the cart
                        classConflict = 1
                        break
                    # this means that we are adding a dis/lab and there was a conflict
                    elif overlapChecker(u_class_start, u_class_end, users_class_start, users_class_end) and users_class.component != "LEC":
                        classConflict = 1
                        for user_class in cart.classes.all():
                            if user_class.catalog_nbr == users_class.catalog_nbr and user_class.subject == users_class.subject:
                                class_to_remove = cart.classes.get(
                                    id=user_class.id)
                                cart.classes.remove(class_to_remove)
                        break

        # this code is pretty brutal at this point, but it handles all lab/discussion stuff and any class conflict, be it the same class or a timing thing.
        if not classConflict:
            if not duplicateClass:
                addClass(cart, users_class)
                context['emptyCartBool'] = 0
            else:
                context['duplicateClass'] = duplicateClass
                return render(request, 'main/displayCart.html', context)
            # Redirect to a page asking the user to add the LAB/DIS corresponding to this course.
            if has_lab_or_discussion(users_class) and users_class.component == "LEC":
                df = pd.DataFrame(SubjectClasses.objects.filter(
                    subject=users_class.subject, catalog_nbr=users_class.catalog_nbr).exclude(component="LEC").values())
                cols_to_drop = ['id', 'index', 'strm',
                                'session_code', 'acad_group', 'page']
                df.drop(columns=cols_to_drop, inplace=True)
                context['df'] = df
                context['addingNonLecComp'] = 1
                return render(request, "main/displaySections.html", context)
            else:
                return render(request, "main/displayCart.html", context)
        elif classConflict:
            context['conflictBool'] = classConflict
            return render(request, "main/displayCart.html", context)


# helper functiont that determines if a class has a discussion or lab component.
def has_lab_or_discussion(users_class):

    for subject_class in SubjectClasses.objects.filter(subject=users_class.subject, catalog_nbr=users_class.catalog_nbr):
        if subject_class.component != "LEC":
            return 1

    return 0


def deleteClass(request):

    cart = Cart.objects.get(username=request.user.username)
    context = {"cart": cart}

    if request.method == "POST":
        # grab class_nbr and catalog_nbr
        catalog_nbr = request.POST.get('catalog_nbr')
        class_nbr = request.POST.get('class_nbr')

        # get the class that is being deleted
        the_class = SubjectClasses.objects.get(
            catalog_nbr=catalog_nbr, class_nbr=class_nbr)

        # calls helper function that removed the class. This will also remove any labs/discussions attached to the cart
        removeClass(cart, the_class)

        if len(cart.classes.all()) == 0:
            context['emptyCartBool'] = 1

        # reload the cart
        return render(request, "main/displayCart.html", context)
    else:
        render(request, "main/displayCart.html", context)

# This method basically creates and saves the user schedule from the cart, a little bit redundant but it works


def displaySchedules(request):
    # User is adding a schedule.

    context = {}

    if request.method == "POST":
        cart = Cart.objects.get(username=request.user.username)

        user_schedule = Schedule(username=request.user.username)
        user_schedule.save()

        for u_class in cart.classes.all():
            user_schedule.classes.add(u_class)

        user = UserProfile.objects.get(username=request.user.username)

        # Saves both the schedule as existing and the adds the schedule to the users schedule list
        user_schedule.save()
        user.save()

        all_schedules = Schedule.objects.filter(username=request.user.username)

        if schedule_already_exists_checker(user.schedules.all(), user_schedule):
            user_schedule.delete()
            context['duplicateBool'] = 1
            context['all_schedules'] = all_schedules
            return render(request, "main/displaySchedules.html", context)

        user.schedules.add(user_schedule)
        context['emptySchedulesBool'] = 0
        context['all_schedules'] = all_schedules

        return render(request, "main/displaySchedules.html", context)
    else:
        all_schedules = Schedule.objects.filter(username=request.user.username)
        if not all_schedules.exists():
            context['emptySchedulesBool'] = 1
        context['all_schedules'] = all_schedules
        return render(request, "main/displaySchedules.html", context)


def sendSchedule(request):
    context = {}

    # if the method is post, we are sending the schedule
    if request.method == "POST":
        id = request.POST.get('id')
        schedule = Schedule.objects.get(username=request.user.username, id=id)
        schedule.is_sent = True
        schedule.save()
    # If the request is a get we are unmarking the schedule as sent
    elif request.method == "GET":
        id = request.GET.get('id')
        schedule = Schedule.objects.get(username=request.user.username, id=id)
        schedule.is_sent = False
        schedule.is_approved = False
        schedule.save()

    context['all_schedules'] = Schedule.objects.filter(
        username=request.user.username)
    return render(request, "main/displaySchedules.html", context)


def deleteSchedule(request):

    # gets the id of the schedule and deletes it, reloads the page.
    id = request.POST.get('id')
    Schedule.objects.get(username=request.user.username, id=id).delete()

    return redirect("/displaySchedules")

# adds the class to the cart, another helper function


def addClass(user_cart, user_class):
    user_cart.classes.add(user_class)
    user_cart.num_classes += 1
    # hardcoding 3 for now, hope to add this as a field to the model
    user_cart.num_credits += 3
    user_cart.save()

# helper function that removes classes from carts.


def removeClass(user_cart, user_class):

    # Scans through and also removes any labs/discussions the user has that have the same sub/catalog
    for u_class in user_cart.classes.all():
        if u_class.component != "LEC" and u_class.subject == user_class.subject and u_class.catalog_nbr == user_class.catalog_nbr:
            user_cart.classes.remove(u_class)

    user_cart.classes.remove(user_class)
    user_cart.save()

# external function for checking if class times overlap


def overlapChecker(c1Start, c1End, c2Start, c2End):

    # first convert to datetime and remove timezone offset

    format_string = "%H.%M.%S.%f"
    c1Start_dt = datetime.strptime(c1Start[:-6], format_string)
    c1End_dt = datetime.strptime(c1End[:-6], format_string)
    c2Start_dt = datetime.strptime(c2Start[:-6], format_string)
    c2End_dt = datetime.strptime(c2End[:-6], format_string)

    # check for overlap of the times
    overlap = min(c1End_dt, c2End_dt) - max(c1Start_dt, c2Start_dt)

    # if there was an overlap, return True, otherwise False
    if overlap.total_seconds() > 0:
        return True
    else:
        return False

# Helper function to determine if a schedule being added already exists. Currently just iterates over every class and checks.


def schedule_already_exists_checker(listOfSchedules, schedule_to_add):

    duplicateBool = 0
    for schedule in listOfSchedules:
        if set(schedule.classes.all()) == set(schedule_to_add.classes.all()):
            duplicateBool = 1

    return duplicateBool
