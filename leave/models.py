from django.db import models

class Application(models.Model):
    c = (
        ('EL', 'Earned Leave'),
        ('HPL', 'Half Pay Leave'),
        ('OT', 'Other Leave'),
        )
    typeOfLeave = models.CharField(choices=c ,max_length=3,default='OT')
    startDate = models.DateField()
    endDate = models.DateField()
    applicant = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True)
    
    availLTC = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('accounts.User',on_delete=models.CASCADE, blank=True, null=True, related_name="Approved_by")
    approver_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.applicant.get_full_name()) + " from " + str(self.startDate) + " - " + str(self.endDate)

    @property
    def is_submitted(self):
        return self.submitted

    @property
    def full_name(self):
        return self.applicant.get_full_name()

    @property
    def is_approved(self):
        return self.approved
