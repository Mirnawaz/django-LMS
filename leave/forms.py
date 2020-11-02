from django import forms
from django.contrib import admin
import leave.models

def log(f):
    def logged(*args, **kwargs):
        print(f, "called")
        ans = f(*args, **kwargs)
        print(f, "successfully returned")
        return ans
    return logged

class ApplicationCreationForm(forms.ModelForm):
    class Meta:
        model = leave.models.Application
        fields = ['applicant',
                  'typeOfLeave',
                  'startDate',
                  'endDate',
                  'availLTC',
                  'submitted',
                  'approved',
                  'approved_by',
                  'approver_comments']

    def clean(self):
        start_date = self.cleaned_data.get("startDate")
        end_date = self.cleaned_data.get("endDate")

        if end_date and start_date and end_date < start_date:
            msg = "End date should be greater than start date."
            self._errors["endDate"] = self.error_class([msg])
            raise forms.ValidationError(msg, code='invalid')

class ApplicationChangeForm(forms.ModelForm):
    class Meta:
        model = leave.models.Application
        fields = ['applicant',
                  'typeOfLeave',
                  'startDate',
                  'endDate',
                  'availLTC',
                  'submitted',
                  'approved',
                  'approved_by',
                  'approver_comments']

    def clean(self):
        start_date = self.cleaned_data.get("startDate")
        end_date = self.cleaned_data.get("endDate")

        if end_date and start_date and end_date < start_date:
            msg = "End date should be greater than start date."
            self._errors["endDate"] = self.error_class([msg])
            raise forms.ValidationError(msg, code='invalid')

class ApplicationAdmin(admin.ModelAdmin):

    applicant_cant_modify = ['applicant',
                             'approved',
                             'approved_by',
                             'approver_comments']
    approver_cant_modify =  [   'applicant',
                                'typeOfLeave',
                                'startDate',
                                'endDate',
                                'availLTC',
                                ]

    form = ApplicationCreationForm
    add_form = ApplicationChangeForm

    @log
    def get_readonly_fields(self, request, obj=None, **kwargs):
        if request.user.is_admin:
            self.readonly_fields = []
        elif obj and obj.applicant == request.user:
            self.readonly_fields = self.applicant_cant_modify
        elif request.user.is_approver:
            self.readonly_fields = self.approver_cant_modify

        return self.readonly_fields

    @log
    def get_queryset(self, request):
        res = super(ApplicationAdmin, self).get_queryset(request)
        temp = res.filter(id=-1) # Empty result
        if request.user.is_admin or request.user.is_supervisor:
            temp = res
        if request.user.is_approver:
            temp = res
        if request.user.is_applicant:
            personal = res.filter(applicant=request.user)
            temp = (temp | personal).distinct()
        return temp

    @log
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            if request.user.is_approver:
                kwargs['exclude'] = ['applicant',
                                     'typeOfLeave',
                                     'startDate',
                                     'endDate',
                                     'availLTC',
                                     'submitted',
                                     'approved_by'
                                     ]
            elif not request.user.is_admin:
                kwargs['exclude'] = ['applicant',
                                     'approved',
                                     'approver_comments',
                                     'typeOfLeave',
                                     'approved_by'
                                     ]
        request.user.is_admin
        return super(ApplicationAdmin, self).get_form(request, obj, **kwargs)

    @log
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'applicant':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    @log
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'applicant', None) is None:
            obj.applicant = request.user
        if request.user.is_approver:
            obj.approved_by = request.user
        obj.save()

    list_display = ('applicant',
                    'startDate',
                    'endDate',
                    'typeOfLeave',
                    'submitted',
                    'approved')

    fieldsets = ((None, {'fields': ('applicant',
                                    'typeOfLeave',
                                    'startDate',
                                    'endDate',
                                    'availLTC'
                                    '')}),
                ('Status', {'fields': ('approved',
                                    'approved_by',
                                    )}),
                                    )

    add_fieldsets = ((None,{'fields': ('applicant',
                                        'typeOfLeave',
                                        'startDate',
                                        'endDate',
                                        'availLTC',
                                        'submitted')}))

    list_filter = ('approved',
                   'submitted')

    search_fields = ('startDate',
                     'endDate',
                     'submitted',
                     'approved')
    readonly_fields = ['approved','approved_by']

    ordering = ('startDate', 'endDate')

    filter_horizontal = ()
