from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from .storage_information_view import format_duration
 

def passcard_info_view(request, passcode):

  passcard = get_object_or_404(Passcard, passcode=passcode)

  passcard_visits = Visit.objects.filter(passcard=passcard)

  this_passcard_visits = []
  for visit in passcard_visits:
    this_passcard_visit = {
          'entered_at': visit.loc_entered_at,
          'duration': format_duration(visit.get_duration()),
          'is_strange': 'Да' if visit.is_strange() else 'Нет',
        }
    this_passcard_visits.append(this_passcard_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
