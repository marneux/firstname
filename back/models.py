from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User

class Firstname(models.Model):
    firstname = models.CharField(max_length = 200)
    metaphone = models.CharField(max_length=50, null=True)
    sex = models.CharField(max_length=1)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['firstname', 'sex'], name = 'uk_firstname_sex')
        ]

    def __str__(self):
        return self.firstname

class Vote(models.Model):
    firstname = models.ForeignKey(Firstname, on_delete=models.CASCADE, null=False, blank=False)
    who = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    choice = models.BooleanField()
    modify_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-modify_at']
    @property
    def soundex(self, value):
        self.soundex = value
        return self.soundex

    class Meta:
        constraints = [
            UniqueConstraint(fields=['firstname', 'who'], name = 'uk_firstname_who')
        ]

    def __str__(self):
        if self.choice:
            return f"oui pour {self.firstname.firstname}"
        else:
            return f"non pour {self.firstname.firstname}"