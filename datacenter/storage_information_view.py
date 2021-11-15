from datetime import timedelta
from django.utils import timezone
from datacenter.models import Visit
from django.shortcuts import render


def format_duration(duration: timedelta) -> str:
  seconds = duration.total_seconds()
  
  days, seconds = divmod(seconds, 86400)
  formatted_duration = f'{int(days)} д ' if days > 0 else ''

  hours, seconds = divmod(seconds, 3600)
  formatted_duration += f'{int(hours)} ч ' if hours > 0 else ''

  minutes, seconds = divmod(seconds, 60)
  formatted_duration += f'{int(minutes)} м ' if minutes > 0 else ''

  formatted_duration += f'{round(seconds)} с'

  return formatted_duration


def storage_information_view(request):
    
    ongoing_visits = Visit.objects.filter(entered_at__lte=timezone.now(), leaved_at__isnull=True)

    non_closed_visits = []
    for visit in ongoing_visits:
      person_in_storage = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.loc_entered_at,
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_strange(),
      }

      non_closed_visits.append(person_in_storage)

    context = {
        'non_closed_visits': non_closed_visits, 
    }
    return render(request, 'storage_information.html', context)
