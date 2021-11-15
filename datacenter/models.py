import datetime
from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= 'leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )

    @property
    def loc_entered_at(self):
       return timezone.localtime(self.entered_at)
    
    def get_duration(self) -> datetime.timedelta:
        
      if self.leaved_at:
        return self.leaved_at - self.entered_at
      else:
          return timezone.localtime(timezone.now()) - timezone.localtime(self.entered_at)
      
    def is_strange(self):
      return self.get_duration().total_seconds() > 3600
