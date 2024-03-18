from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    current_passcard_visits = Visit.objects.filter(passcard__passcode=passcode)

    this_passcard_visits = [
        {
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(),
            'is_strange': visit.is_long()
        } for visit in current_passcard_visits
    ]
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
