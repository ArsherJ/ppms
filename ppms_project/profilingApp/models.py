from email.policy import default
from wsgiref.validate import validator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from pygrowup import Calculator, helpers

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Barangay(Model):
    brgy_name = models.CharField(max_length=500)
    brgy_phone = models.CharField(max_length=100, null=True, blank=True)
    brgy_address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.brgy_name}'

    def enrolled_preschooler_count(self):
        parent = Parent.objects.filter(barangay=self.id)
        preschoolers_count = Preschooler.lt_60_objects.filter(parent__in=(parent)).count()

        return preschoolers_count
    
    def parent_count(self):
        parent_count = Parent.objects.filter(barangay=self.id).count()

        return parent_count

    def bhw_count(self):
        bhw_count = BarangayHealthWorker.objects.filter(bhw_barangay=self.id).count()

        return bhw_count

class CustomUser(AbstractUser):
    USER_TYPE = [('Choose User Type', 'Choose User Type'),
                 ('Admin', 'Administrator'),
                 ('BHW', 'Barangay Health Worker'),
                 ('P/G', 'Parent/Guardian')]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE)
    middle_name = models.CharField(max_length=100, null=True)
    suffix_name = models.CharField(max_length=100, null=True, blank=True)
    phone_num = models.CharField(max_length=100, null=True)
    history= HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class BarangayHealthWorker(Model):
    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    is_validated = models.BooleanField(default=False)
    bhw_barangay = models.ForeignKey(Barangay, on_delete=CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Parent(Model):
    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    barangay = models.ForeignKey(Barangay, on_delete=CASCADE)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class PreschoolerManagerLess(models.Manager):
    def get_queryset(self):
        greater_than_60_mon = datetime.today() - relativedelta(months=60)

        return super().get_queryset().filter(birthday__gt=greater_than_60_mon)

class PreschoolerManagerGreater(models.Manager):
    def get_queryset(self):
        less_than_60_mon = datetime.today() - relativedelta(months=60)

        return super().get_queryset().filter(birthday__lte=less_than_60_mon)

class Preschooler(Model):
    GENDER = [('Male', 'Male'),
              ('Female', 'Female'),]

    parent = models.ForeignKey(Parent, on_delete=CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    suffix_name = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True,validators=[MinValueValidator(0)])
    weight = models.FloatField(null=True, validators=[MinValueValidator(0)])
    gender = models.CharField(max_length=100, choices=GENDER, null=True)
    date_measured = models.DateField(null=True, blank=True)
    health_problem = models.CharField(max_length=500, null=True, blank=True)
    ps_image = models.ImageField(null=True, blank=True, upload_to='ps_images')

    # === Managers ===
    history= HistoricalRecords()
    objects = models.Manager()

    # less than 60 months old preschooler
    lt_60_objects = PreschoolerManagerLess()

    # greater than or equal to 60 months old preschooler
    gte_60_objects = PreschoolerManagerGreater()


    def age_measured(self):
        today = date.today()
        try:
            date_diff = self.date_measured - self.birthday
            in_days = date_diff.days
            return int((in_days) / (365 / 12)) 
        except: 
             return 'Undefined'
        

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def age_years(self):
        today = date.today()
        one_or_zero = ((today.month, today.day) < (self.birthday.month, self.birthday.day))

        year_difference = today.year - self.birthday.year

        return int(year_difference - one_or_zero)
    
    def age_months(self):
        today = date.today()
        try:
            date_diff = today - self.birthday

            in_days = date_diff.days

            return int((in_days) / (365 / 12)) 
        
        except: 
             return 'Undefined'
    
    def age_weeks(self):
        today = date.today()
        try:
            date_diff = today - self.birthday

            in_days = date_diff.days

            return int((in_days) / (365 / 52))
        
        except: 
             return 'Undefined'
    
    def age_days(self):
        today = date.today()
        try:
            date_diff = today - self.birthday

            in_days = date_diff.days

            return in_days
        
        except: 
             return 'Undefined'

    def age_hours(self):
        today = date.today()
        try:
            date_diff = today - self.birthday

            in_days = date_diff.days

            return int(in_days * 24)
        
        except: 
             return 'Undefined'

    def wfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        try:

            date_diff = self.date_measured - self.birthday
            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))

            return float(calculator.wfa(self.weight, age_months, helpers.get_good_sex(str(self.gender))))
        except:
            pass

    def hfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:

            date_diff = self.date_measured - self.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))

            return float(calculator.lhfa(self.height, age_months, helpers.get_good_sex(str(self.gender))))
        except:
            pass

    def bmifa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:

            date_diff = self.date_measured - self.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))

            bmi = float(self.weight / ((self.height / 100) ** 2))

            return float(calculator.bmifa(bmi, age_months, helpers.get_good_sex(str(self.gender)), self.height))
        except:
            pass

    def whfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:

            date_diff = self.date_measured - self.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))


            return float(calculator.wfl(self.weight, age_months, helpers.get_good_sex(str(self.gender)), self.height))
        except:
            pass
    
    @property
    def bmi_tag(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:
            today = date.today()

            date_diff = self.date_measured - self.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))
            
            bmi = float(self.weight / ((self.height / 100) ** 2))

            bmifa_value = float(calculator.bmifa(bmi, age_months, helpers.get_good_sex(str(self.gender)), self.height))

            if bmifa_value > 2.0:
                return 'ABOVE NORMAL'
            elif bmifa_value >= -2.0 and bmifa_value <= 2.0:
                return 'NORMAL'
            elif bmifa_value >= -3.0 and bmifa_value < -2.0:
                return 'BELOW NORMAL'
            else:
                return 'SEVERE'
        except:
            pass
    
    
    @property
    def whfa_tag(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:

            date_diff = self.date_measured - self.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))
            
            whfa_value = float(calculator.wfl(self.weight, age_months, helpers.get_good_sex(str(self.gender)), self.height))

            if whfa_value > 3.0:
                return 'OBESE'
            elif whfa_value > 2.0 and whfa_value <= 3.0:
                return 'OVERWEIGHT'
            elif whfa_value >= -2.0 and whfa_value <= 2.0:
                return 'NORMAL'
            elif whfa_value >= -3.0 and whfa_value < -2.0:
                return 'UNDERWEIGHT'
            else:
                return 'SEVERE'
        except:
            pass
    
    def vaccine_count(self):
        return Vaccine.objects.filter(vax_preschooler=self).count()
    
    

class Log(Model):
    log_action = models.CharField(max_length=500, null=True)
    logged_userid = models.IntegerField(null=True)
    log_email = models.CharField(max_length=500,null=True)
    datetime_log = models.CharField(max_length=500, null=True)

class Vaccine(Model):
    VACCINES = [('BCG', 'BCG'),
                ('Hepatitis B', 'Hepatitis B'),
                ('Oral Poliovirus Vaccine', 'Oral Poliovirus Vaccine'),
                ('Pentavalent Vaccine', 'Pentavalent Vaccine'),
                ('Measles Containing Vaccines', 'Measles Containing Vaccines'),
                ('Tetanus Toxoid', 'Tetanus Toxoid'),
                ('Inactivated Polio Vaccine', 'Inactivated Polio Vaccine'),
                ('Measles Mumps - Rubella', 'Measles Mumps - Rubella'),]

    vax_preschooler = models.ForeignKey(Preschooler, on_delete=CASCADE)
    vax_name = models.CharField(max_length=500, choices=VACCINES)
    vax_dose = models.IntegerField()
    vax_date = models.DateField(null=True, blank=True)
    vax_remarks = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.vax_preschooler} : {self.vax_name}'

class PreschoolerHistory(Model):
    id_preschooler = models.ForeignKey(Preschooler, on_delete=CASCADE)
    height = models.FloatField(null=True, validators=[MinValueValidator(45.0), MaxValueValidator(120.0)])
    weight = models.FloatField(null=True, validators=[MinValueValidator(1.0), MaxValueValidator(28.0)])
    date_measured = models.DateField(null=True, blank=True)

    def wfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        try:
            today = date.today()
            
            date_diff = self.date_measured - self.id_preschooler.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))

            return float(calculator.wfa(self.weight, age_months, helpers.get_good_sex(str(self.id_preschooler.gender))))
        except:
            pass
    
    def hfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:
            today = date.today()

            date_diff = self.date_measured - self.id_preschooler.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))

            return float(calculator.lhfa(self.height, age_months, helpers.get_good_sex(str(self.id_preschooler.gender))))
        except:
            pass
    
    def whfa(self):
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
        
        try:
            today = date.today()

            date_diff = self.date_measured - self.id_preschooler.birthday

            in_days = date_diff.days
            age_months = int((in_days) / (365 / 12))


            return float(calculator.wfl(self.weight, age_months, helpers.get_good_sex(str(self.id_preschooler.gender)), self.height))
        except:
            pass