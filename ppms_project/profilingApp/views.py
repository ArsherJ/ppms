from itertools import count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from datetime import datetime, timedelta
from json import dumps
from PIL import Image
from django.db.models import Q
# Create your views here.

@unauthenticated_user
def login_registration(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'register_btn' in request.POST:
            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                messages.success(
                    request, 'Your account is successfully created.')
                form.save()
            else:
                CRITICAL = 50
                error_string = ''.join([''.join(x for x in l)
                                       for l in list(form.errors.values())])
                messages.add_message(request, CRITICAL, str(error_string))

        else:
            current_date =  datetime.now()
            format_date =  current_date.strftime("%Y/%m/%d, %H:%M:%S")
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=user_email, password=password)
            if user is not None and user.user_type == 'P/G':
                login(request, user)
                Log.objects.create(log_action = 'Logged IN', logged_userid  = user.id,  log_email = user.email, datetime_log = format_date
                )
                return redirect('parent_home')
                
            elif user is not None and user.user_type == 'BHW':
                bhw_validation_status = BarangayHealthWorker.objects.get(
                    user=user)
                if bhw_validation_status.is_validated:
                    login(request, user)
                    Log.objects.create(log_action = 'logged in', logged_userid  = user.id, log_email = user.email, datetime_log = format_date
                )
                    return redirect('bhw_home')
                else:
                    # Error message pop-up
                    messages.warning(
                        request, 'Please wait for the validation.')
            elif user is not None and user.user_type == 'Admin':
                login(request, user)
                Log.objects.create(log_action = 'logged in', logged_userid  = user.id, log_email = user.email, datetime_log = format_date
                )
                return redirect('admin_home')
            else:
                messages.error(request, 'Login Failed')

    context = {'form': form}
    return render(request, 'activities/login_registration.html', context)


def logout_user(request):
    user= request.user
    current_date =  datetime.now()
    format_date =  current_date.strftime("%Y/%m/%d, %H:%M:%S")
    Log.objects.create(log_action = 'Logged Out', logged_userid  = user.id, log_email = user.email, datetime_log = format_date
                )
    logout(request)
    return redirect('login_registration')

def privacyPolicy(request):

     return render(request, 'activities/Privacy_Policy.html')

# ================================== PARENTS/GUARDIANS ==================================

@login_required(login_url='login_registration')
def parent_home(request):
    if request.user.is_authenticated and request.user.user_type == 'P/G':
        parent_user = Parent.objects.get(user_id=request.user.id)
        preschooler = Preschooler.objects.filter(parent=parent_user)

        if request.method == 'POST':
            parent = parent_user
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            
            if request.POST.get('suffix_name') is None:
                suffix_name = None
            else:
                suffix_name = request.POST.get('suffix_name')
                birthday = request.POST.get('birthday')
                gender = request.POST.get('gender')

            if Preschooler.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name, suffix_name=suffix_name).exists():

                messages.warning(request, f'{first_name} {middle_name} {last_name} {suffix_name} already exists.')

                return redirect('parent_home')

            else:

                psa = Preschooler.objects.create(parent=parent,
                                                first_name=first_name,
                                                middle_name=middle_name,
                                                last_name=last_name,
                                                suffix_name=suffix_name,
                                                birthday=birthday,
                                                gender=gender
                                                
                                                )
                return redirect('parent_home')

        if len(preschooler) <= 2:
            numberOfColumns = 6
            bootstrapColWidth = int(12 / numberOfColumns)
            chunks = [preschooler[i:i+bootstrapColWidth] for i in range(0,len(preschooler),bootstrapColWidth)]
            context = {
                'chunks': chunks,
                'numberOfColumns': numberOfColumns,
                'bootstrapColWidth' : bootstrapColWidth,
                'parent' : parent_user
            }
            return render(request, 'activities/Parent Home.html', context)
        else:
            numberOfColumns = 4
            bootstrapColWidth = int(12 / numberOfColumns)
            chunks = [preschooler[i:i+bootstrapColWidth] for i in range(0,len(preschooler),bootstrapColWidth)]
            context = {
                'parent' : parent_user,
                'chunks': chunks,
                'numberOfColumns': numberOfColumns,
                'bootstrapColWidth' : bootstrapColWidth
            }
            return render(request, 'activities/Parent Home.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')

@login_required(login_url='login_registration')
def parent_preschooler(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'P/G':
        preschooler = Preschooler.objects.get(id=pk)
        preschooler_history = PreschoolerHistory.objects.filter(id_preschooler=preschooler)

        context = {'preschooler' : preschooler,
                   'history' : preschooler_history,}

        return render(request, 'activities/Parent - Preschooler Profile.html', context)
        
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
        

# ================================== ADMIN ==================================

@login_required(login_url='login_registration')
def admin_home(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        all_bhw = BarangayHealthWorker.objects.all()
        validated_status = BarangayHealthWorker.objects.filter(
            is_validated=True).count()
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()
        parent_count = Parent.objects.all().count()
        preschooler_count = Preschooler.objects.all().count()

        count_list = [validated_status, invalidated_status,
                    parent_count, preschooler_count]
        data_json = dumps(count_list)

        context = {'bhws': all_bhw,
                'validated_count': validated_status,
                'invalidated_count': invalidated_status,
                'parent_count': parent_count,
                'preschooler_count': preschooler_count,
                'count_data': data_json}

        return render(request, 'activities/Admin Home.html', context)
        
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def bhw_validation(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        bhw = BarangayHealthWorker.objects.filter(is_validated=False)

        parent = Parent.objects.all()
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        context = {'bhws': bhw, 
                'invalidated_count': invalidated_status,
                'parents' : parent,}

        return render(request, 'activities/Admin - Validation.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def set_pass(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        user = CustomUser.objects.get(id=pk)
        form = SetPasswordForm(user)
        
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed.')
            else:
                messages.error(request, 'New Password did not match. Please fill up the form correctly!')

        context = {'form' : form, 'user' :user}

        return render(request, 'activities/Admin - Set Password.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def admin_preschoolers(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        barangays = Barangay.objects.all()
        current_date =  datetime.now()


        preschooler_normal = []
        preschooler_wasted = []
        preschooler_severly = []
        preschooler_overweight = []
        preschooler_obese = []

        for obj in Preschooler.lt_60_objects.all():
            if obj.whfa_tag == 'OBESE':
                preschooler_obese.append(obj)
            elif obj.whfa_tag == 'OVERWEIGHT':
                preschooler_overweight.append(obj)
            elif obj.whfa_tag == 'NORMAL':
                preschooler_normal.append(obj)
            elif obj.whfa_tag == 'UNDERWEIGHT':
                preschooler_wasted.append(obj)
            elif obj.whfa_tag == 'SEVERE':
                preschooler_severly.append(obj)

        normal_count = len(preschooler_normal)
        wasted_count = len(preschooler_wasted)
        severly_count = len(preschooler_severly)
        overweight_count = len(preschooler_overweight)
        obese_count = len(preschooler_obese)

        count_list = [severly_count, wasted_count, normal_count, overweight_count, obese_count]
        data_json = dumps(count_list)

        # ==== Total Preschoolers ======
        all_preschoolers = Preschooler.objects.all().count()
        all_preschoolersList = Preschooler.lt_60_objects.all()
        all_preschoolersListCount = Preschooler.lt_60_objects.all().count

        # ==== Total Male Preschoolers ======
        total_male = Preschooler.lt_60_objects.filter(Q(gender='Male')).count
        
         # ==== Total Female Preschoolers ======
        total_Female = Preschooler.lt_60_objects.filter(Q(gender='Female')).count

        # ==== Preschooler w/ out Records ====
        preschooler_without_record = Preschooler.lt_60_objects.filter(Q(height__isnull=True) | Q(weight__isnull=True)).count()

        # ==== Preschooler w Records ====
        preschooler_with_record = Preschooler.lt_60_objects.filter(Q(height__isnull=False) | Q(weight__isnull=False) | Q(date_measured__isnull=False))
        preschooler_with_record_count = preschooler_with_record.count()

        # ==== Preschooler above 60 months ====
        preschooler_60_above = Preschooler.gte_60_objects.all()
        preschooler_60_above_count = preschooler_60_above.count()
        
        context = {'invalidated_count': invalidated_status,
                'normal' : normal_count,
                'wasted' : wasted_count,
                'severly' : severly_count,
                'overweight' : overweight_count,
                'obese' : obese_count,
                'barangays' : barangays,
                'total_male': total_male,
                'total_Female': total_Female,
                'all_preschoolersList': all_preschoolersList,
                'all_preschooler_count' : all_preschoolers,
                'all_preschoolersListCount':all_preschoolersListCount,
                'preschooler_without_record_count' : preschooler_without_record,
                'preschooler_with_record_count' : preschooler_with_record_count,
                'preschooler_60_above_count' : preschooler_60_above_count,
                'preschooler_with_record' : preschooler_with_record,
                'preschooler_60_above' : preschooler_60_above,
                'count_data' : data_json,
                'current_date': current_date}

        return render(request, 'activities/Admin - Preschooler.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def admin_preschoolers_barangay(request, brgy):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        parents = Parent.objects.filter(barangay=brgy)
        preschoolers = Preschooler.lt_60_objects.filter(parent__in=(parents))
        current_date =  datetime.now()

        barangay = Barangay.objects.get(id=brgy)
        barangays = Barangay.objects.all()

        preschooler_normal = []
        preschooler_wasted = []
        preschooler_severly = []
        preschooler_overweight = []
        preschooler_obese = []

        for p in preschoolers:
            if p.whfa_tag == 'OBESE':
                preschooler_obese.append(p)
            elif p.whfa_tag == 'OVERWEIGHT':
                preschooler_overweight.append(p)
            elif p.whfa_tag == 'NORMAL':
                preschooler_normal.append(p)
            elif p.whfa_tag == 'UNDERWEIGHT':
                preschooler_wasted.append(p)
            elif p.whfa_tag == 'SEVERE':
                preschooler_severly.append(p)
        
        normal_count = len(preschooler_normal)
        wasted_count = len(preschooler_wasted)
        severly_count = len(preschooler_severly)
        overweight_count = len(preschooler_overweight)
        obese_count = len(preschooler_obese)

        count_list = [severly_count, wasted_count, normal_count, overweight_count, obese_count]
        data_json = dumps(count_list)

         # ==== Total Preschoolers ======
        all_preschoolers = Preschooler.objects.filter(parent__in=(parents)).count
        all_preschoolersListCount = Preschooler.lt_60_objects.filter(parent__in=(parents)).count

         # ==== Total Male Preschoolers ======
        total_male = preschoolers.filter(Q(gender='Male')).count
        
         # ==== Total Female Preschoolers ======
        total_Female = preschoolers.filter(Q(gender='Female')).count


        # ==== Preschooler w/ out Records ====
        preschooler_without_record = preschoolers.filter(Q(height__isnull=True) | Q(weight__isnull=True)).count()

        # ==== Preschooler w Records ====
        preschooler_with_record = preschoolers.filter(Q(height__isnull=False) | Q(weight__isnull=False) | Q(date_measured__isnull=False))
        preschooler_with_record_count = preschooler_with_record.count()

        # ==== Preschooler above 60 months ====
        preschooler_60_above = Preschooler.gte_60_objects.filter(parent__in=(parents))
        preschooler_60_above_count = preschooler_60_above.count()
        
        

        context = {'invalidated_count': invalidated_status,
                'brgy' : barangay,
                'normal' : normal_count,
                'wasted' : wasted_count,
                'severly' : severly_count,
                'overweight' : overweight_count,
                'obese' : obese_count,
                'current_date': current_date,
                'barangays' : barangays,
                'total_male': total_male,
                'total_Female': total_Female,
                'all_preschooler_count' : all_preschoolers,
                'all_preschoolersListCount': all_preschoolersListCount,
                'preschooler_without_record_count' : preschooler_without_record,
                'preschooler_with_record_count' : preschooler_with_record_count,
                'preschooler_60_above_count' : preschooler_60_above_count,
                'preschooler_with_record' : preschooler_with_record,
                'preschooler_60_above' : preschooler_60_above,
                'count_data' : data_json
                }

        return render(request, 'activities/Admin - Preschooler_barangay.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def unvalidated_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        unvalidate_bhw = BarangayHealthWorker.objects.get(user_id=pk)
        form = Validate_BHW(instance=unvalidate_bhw)

        if request.method == 'POST':
            form = Validate_BHW(request.POST, instance=unvalidate_bhw)
            if form.is_valid():
                form.save()
                return redirect('bhw_validation')

        context = {'bhw': unvalidate_bhw,
                'form': form}
        return render(request, 'activities/Unvalidated Profile.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')



@login_required(login_url='login_registration')
def delete_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        delete_bhw = BarangayHealthWorker.objects.get(user_id=pk)
        user_bhw = CustomUser.objects.get(id=pk)

        if request.method == 'POST':

            user_bhw.delete()

            return redirect('bhw_validation')

        context = {'bhw': delete_bhw}
        return render(request, 'activities/Admin Delete Confirmation.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def admin_barangay(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()
        barangays = Barangay.objects.all()
        allbarangays = Barangay.objects.all().count()
        allBHW = BarangayHealthWorker.objects.all().count()
        allParent = Parent.objects.all().count()
        allPreschoolers = Preschooler.lt_60_objects.all().count()
        current_date =  datetime.now()


        form = AddBarangay()
        if request.method == 'POST':
            form = AddBarangay(request.POST)
            
            if form.is_valid():
                brgy_name = form.cleaned_data['brgy_name']

                if Barangay.objects.filter(brgy_name=brgy_name).exists():
                    
                    messages.warning(request, f'{brgy_name} already exists.')
                    return redirect('admin_barangay')

                else:

                    form.save()
                    return redirect('admin_barangay')

        context = {'barangays' : barangays,
                    'allbarangays': allbarangays,
                    'allBHW': allBHW,
                    'allParent': allParent,
                    'allPreschoolers': allPreschoolers,
                    'current_date': current_date,
                   'invalidated_count' : invalidated_status,
                   'form' : form}
    
        return render(request, 'activities/Admin - barangay.html', context)


@login_required(login_url='login_registration')
def admin_userAccounts(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        all_bhw = BarangayHealthWorker.objects.all()
        all_parents = Parent.objects.all()

        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        context = {'bhws': all_bhw,
                    'invalidated_count': invalidated_status,
                   'parents' : all_parents}
    
        return render(request, 'activities/Admin - User accounts.html', context)

@login_required(login_url='login_registration')
def admin_historyLogs(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        
        bhw_history = BarangayHealthWorker.history.all()
        current_date =  datetime.now()


        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        context = {
                   'invalidated_count': invalidated_status,
                   'validate_logs' : bhw_history,
                   'current_date': current_date,
                   }
    
        return render(request, 'activities/Admin - History Logs.html', context)

# ================================== BHW ==================================


@login_required(login_url='login_registration')
def bhw_home(request):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
        bhw_logged = BarangayHealthWorker.objects.get(user_id=request.user.id)
        parents = Parent.objects.filter(barangay=bhw_logged.bhw_barangay)
        preschoolers = Preschooler.lt_60_objects.filter(parent__in=(parents))

        preschooler_normal = []
        preschooler_wasted = []
        preschooler_severly = []
        preschooler_overweight = []
        preschooler_obese = []

        for p in preschoolers:
            if p.whfa_tag == 'OBESE':
                preschooler_obese.append(p)
            elif p.whfa_tag == 'OVERWEIGHT':
                preschooler_overweight.append(p)
            elif p.whfa_tag == 'NORMAL':
                preschooler_normal.append(p)
            elif p.whfa_tag == 'UNDERWEIGHT':
                preschooler_wasted.append(p)
            elif p.whfa_tag == 'SEVERE':
                preschooler_severly.append(p)
        
        normal_count = len(preschooler_normal)
        wasted_count = len(preschooler_wasted)
        severly_count = len(preschooler_severly)
        overweight_count = len(preschooler_overweight)
        obese_count = len(preschooler_obese)

        count_list = [severly_count, wasted_count,normal_count,overweight_count, obese_count]
        data_json = dumps(count_list)

         # ==== Total Preschoolers ======
        all_preschoolers = Preschooler.objects.filter(parent__in=(parents)).count
        all_preschoolersListCount = Preschooler.lt_60_objects.filter(parent__in=(parents)).count


        # ==== Preschooler w/ out Records ====
        preschooler_without_record = preschoolers.filter(Q(height__isnull=True) | Q(weight__isnull=True)).count()

        # ==== Preschooler w Records ====
        preschooler_with_record = preschoolers.filter(Q(height__isnull=False) | Q(weight__isnull=False) | Q(date_measured__isnull=False))
        preschooler_with_record_count = preschooler_with_record.count()

        # ==== Preschooler above 60 months ====
        preschooler_60_above = Preschooler.gte_60_objects.filter(parent__in=(parents))
        preschooler_60_above_count = preschooler_60_above.count()
        
        
        context = {'bhw' : bhw_logged,
                'severly' : severly_count,
                'wasted' : wasted_count,
                'normal' : normal_count,
                'overweight' : overweight_count,
                'obese' : obese_count,
                'all_preschooler_count' : all_preschoolers,
                'all_preschoolersListCount': all_preschoolersListCount,
                'preschooler_without_record_count' : preschooler_without_record,
                'preschooler_with_record_count' : preschooler_with_record_count,
                'preschooler_60_above_count' : preschooler_60_above_count,
                'preschooler_with_record' : preschooler_with_record,
                'preschooler_60_above' : preschooler_60_above,
                'count_data' : data_json}
        return render(request, 'activities/BHW Home.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def preschooler_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
        bhw_logged = BarangayHealthWorker.objects.get(user_id=request.user.id)
        parents = Parent.objects.filter(barangay=bhw_logged.bhw_barangay)
        preschooler = Preschooler.lt_60_objects.filter(parent__in=(parents))

        # ==== Total Preschoolers ======
        all_preschoolersListCount = Preschooler.lt_60_objects.filter(parent__in=(parents)).count

        # ==== Preschooler above 60 months ====
        preschooler_60months = Preschooler.gte_60_objects.filter(parent__in=(parents))
        preschooler_60monthsList = Preschooler.gte_60_objects.filter(parent__in=(parents)).count

         # ==== Preschooler w/ out Records ====
        preschooler_without_record = preschooler.filter(Q(height__isnull=True) | Q(weight__isnull=True)).count()

        # ==== Preschooler w Records ====
        preschooler_with_record = preschooler.filter(Q(height__isnull=False) | Q(weight__isnull=False) | Q(date_measured__isnull=False))
        preschooler_with_record_count = preschooler_with_record.count()

        current_date =  datetime.now()

        context = {'bhw' : bhw_logged,
                   'preschoolers': preschooler,
                   'all_preschoolersListCount': all_preschoolersListCount,
                   'preschooler_without_record': preschooler_without_record,
                   'preschooler_with_record_count': preschooler_with_record_count,
                   'archive_preschoolers' : preschooler_60months,
                   'current_date': current_date,
                   'preschooler_60monthsList': preschooler_60monthsList,}
        
        return render(request, 'activities/BHW Preschooler Dashboard.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def preschooler_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
        preschooler = Preschooler.objects.get(id=pk)
       
        changepic_form = ChangePicture(instance=preschooler)
        form = UpdatePreschooler(instance=preschooler)
        preschooler_history = PreschoolerHistory.objects.filter(id_preschooler=preschooler)

        if request.method == 'POST':
            
            form = UpdatePreschooler(request.POST, instance=preschooler)
            birthday = preschooler.birthday
            
            changepic_form = ChangePicture(request.POST, request.FILES, instance=preschooler)
            if changepic_form.is_valid():

                changepic_form.save()
                try:
                    image_path = preschooler.ps_image.path
                    image = Image.open(image_path)
                    image.save(image_path, quality=40)
                except:
                    pass

                return redirect('preschooler_profile', preschooler.id)

            if form.is_valid():
                dateMeasured = form.cleaned_data['date_measured']

                if dateMeasured >= birthday:
                    p_history = PreschoolerHistory.objects.create(id_preschooler=preschooler,
                                                                height=form.cleaned_data['height'],
                                                                weight=form.cleaned_data['weight'],
                                                                date_measured=form.cleaned_data['date_measured'])
                    form.save()
                    return redirect('preschooler_profile', preschooler.id)

                else:
                    messages.error(request, 'Date Measured must be later than the Date of Birth')
                    return redirect('preschooler_profile', preschooler.id)
                    

        context = {'preschooler' : preschooler,
                   'form' : form,
                   'history' : preschooler_history,
                   'changepic_form' : changepic_form}
                   
        return render(request, 'activities/Preschooler Profile.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


@login_required(login_url='login_registration')
def change_pass(request, pk):
    user = CustomUser.objects.get(id=pk)

    if user.user_type == 'P/G':
        parent = Parent.objects.get(user_id=user)
        form = ChangePasswordForm(user)
    
        if request.method == 'POST':
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed.')
            else:
                messages.error(request, 'New Password did not match. Please fill up the form correctly!')

        context = {'form' : form, 'user' :user, 'parent' : parent}

        return render(request, 'activities/Change Password.html', context)
    else:
        bhw = BarangayHealthWorker.objects.get(user_id=user)
        form = ChangePasswordForm(user)
        
        if request.method == 'POST':
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed.')
            else:
                messages.error(request, 'New Password did not match. Please fill up the form correctly!')

        context = {'form' : form, 'user' :user, 'bhw' : bhw}

        return render(request, 'activities/Change Password.html', context)


# ================================== MODAL UPDATE ==================================

@login_required(login_url='login_registration')
def update_preschooler(request):
    return render(request, 'activities/Preschooler Profile.html')


@login_required(login_url='login_registration')
def immunization_schedule(request, pk):
    loggedin = request.user.user_type
    preschooler = Preschooler.objects.get(id=pk)
    vaccines = Vaccine.objects.filter(vax_preschooler=preschooler)
    vax_list = list(vaccines.values_list('vax_name', flat=True))
    dose_list = vaccines.values_list('vax_dose', flat=True)
    current_date =  datetime.now()

    
    vax_24hrs = vaccines.filter(vax_name__in=['BCG', 'Hepatitis B']).count()
    vax_6weeks = vaccines.filter(vax_name__in=['Oral Poliovirus Vaccine', 'Pentavalent Vaccine', 'Measles Containing Vaccines']).count()
    vax_10weeks = vaccines.filter(vax_name__in=['Oral Poliovirus Vaccine', 'Pentavalent Vaccine', 'Measles Containing Vaccines']).count()
    vax_14weeks = vaccines.filter(vax_name__in=['Oral Poliovirus Vaccine', 'Pentavalent Vaccine', 'Inactivated Polio Vaccine','Measles Containing Vaccines']).count()
    vax_9months = vaccines.filter(vax_name__in=['Measles Mumps - Rubella']).count()

    if len(vaccines) == 0:
        next_vax_date = 'None'
    elif len(vaccines) == 8:
        next_vax_date = 'Complete'
    else:
        next_vax_date = vaccines.order_by('-id')[0].vax_remarks
    
    if request.method == 'POST':
        preschooler_obj = preschooler
        vaxname = request.POST.get('vax_name')
        other = request.POST.get('Others')
        dose = request.POST.get('dose')
        vaxdate = request.POST.get('immune_date')
        vaxremark = request.POST.get('remarks')

        if vaxname == 'Measles Mumps - Rubella':
            if preschooler.age_months() < 9:
                messages.warning(request, f'Too young.')
                return redirect('immunization_schedule', pk=preschooler.id)

        elif vaxname == 'Inactivated Polio Vaccine':
            if preschooler.age_weeks() < 14:
                messages.warning(request, f'Too young.')
                return redirect('immunization_schedule', pk=preschooler.id)
                
        elif vaxname == 'Oral Poliovirus Vaccine' or vaxname == 'Pentavalent Vaccine' or vaxname == 'Measles Containing Vaccines':
            if preschooler.age_weeks() < 6:
                messages.warning(request, f'Too young.')
                return redirect('immunization_schedule', pk=preschooler.id)

        if vaxname in vax_list:
            if vaxname == 'Oral Poliovirus Vaccine' or vaxname == 'Pentavalent Vaccine' or vaxname == 'Measles Containing Vaccines':
                if preschooler.age_weeks() >= 6 and preschooler.age_weeks() < 10:
                    if vax_list.count(vaxname) == 1:
                        messages.warning(request, f'{vaxname} already exists.')
                        return redirect('immunization_schedule', pk=preschooler.id)

                elif preschooler.age_weeks() >= 10 and preschooler.age_weeks() < 14:
                    if vax_list.count(vaxname) == 2:
                        messages.warning(request, f'{vaxname} already exists.')
                        return redirect('immunization_schedule', pk=preschooler.id)

                elif preschooler.age_weeks() >= 14 and preschooler.age_months() < 9:
                    if vax_list.count(vaxname) == 3:
                        messages.warning(request, f'{vaxname} already exists.')
                        return redirect('immunization_schedule', pk=preschooler.id)

                elif vax_list.count(vaxname) == 3:
                    messages.warning(request, f'{vaxname} already exists.')
                    return redirect('immunization_schedule', pk=preschooler.id)
            
            elif vaxname == 'Measles Mumps - Rubella':
                if preschooler.age_months() >= 9 and preschooler.age_months() < 12:
                    if vax_list.count(vaxname) == 1:
                        messages.warning(request, f'{vaxname} already exists.')
                        return redirect('immunization_schedule', pk=preschooler.id)

                elif preschooler.age_months() >= 12 and preschooler.age_months() <= 15:
                    if vax_list.count(vaxname) == 2:
                        messages.warning(request, f'{vaxname} already exists.')
                        return redirect('immunization_schedule', pk=preschooler.id)
            
            else:
                
                messages.warning(request, f'{vaxname} already exists.')
                return redirect('immunization_schedule', pk=preschooler.id)
            
            
        if vaxname == 'Others':
            vax_create = Vaccine.objects.create(vax_preschooler=preschooler_obj,
                                            vax_name=other,
                                            vax_dose=1,
                                            vax_date=vaxdate,
                                            vax_remarks=vaxremark
                                            )
        else:
            vax_create = Vaccine.objects.create(vax_preschooler=preschooler_obj,
                                                vax_name=vaxname,
                                                vax_dose=1,
                                                vax_date=vaxdate,
                                                vax_remarks=vaxremark
                                                )
        
        return redirect('immunization_schedule', pk=preschooler.id)
        
    context = {'vaccines' : vaccines,
               'vax_list' : vax_list,
               'dose_list' : dose_list,
               'preschooler':preschooler,
               'loggedin': loggedin,
               'next_vax' : next_vax_date,
               'vax_24hrs' : vax_24hrs,
               'vax_6weeks' : vax_6weeks,
               'vax_10weeks' : vax_10weeks,
               'vax_14weeks' : vax_14weeks,
               'vax_9months' : vax_9months,
               'current_date': current_date,
               }


    return render(request, 'activities/BHW Immunization Status.html', context)

    
