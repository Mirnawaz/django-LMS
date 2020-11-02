from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password ')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.user_type = 2
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password)
        user.user_type = 0
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_types = ((0, 'Admin'),
                  (1, 'Manager'),
                  (2, 'Employee')
                 )

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    g = ((1, 'Male'),
        (2, 'Female'),
        (3, 'Other'))
    gender = models.IntegerField(choices=g, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=True)
    applicant = models.BooleanField(default=False)
    user_type = models.IntegerField(choices=user_types, default=4)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.


    def get_full_name(self):
        ans  = str(self.firstName)
        if self.lastName is not None:
            ans += " " + str(self.lastName)
        return ans

    def get_short_name(self):
        return self.firstName

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        if perm in ['accounts.change_user', 'leave.change_application']:
            return True
        if self.is_admin:
            return True
        if self.is_applicant and perm in ['leave.add_application']:
            return True
        if self.is_manager and perm in ['leave.change_application', 'leave.delete_application']:
            return True    
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_manager(self):
        "Is the user a manager?"
        return self.user_type == 1

    @property
    def is_employee(self):
        "Is the user a employee?"
        return self.user_type == 2

    @property
    def is_supervisor(self):
        "Is the user a supervisor?"
        return self.user_type == 1

    @property
    def is_approver(self):
        "Is the user an approver?"
        return self.user_type == 1        

    @property
    def is_staff(self):
        "Is the user a staff?"
        return True

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.user_type == 0

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_applicant(self):
        "Is the user an applicant?"
        return self.applicant
