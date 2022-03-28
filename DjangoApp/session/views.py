import sys
import os
from datetime import datetime
from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core.management import call_command
from django.conf import settings
from .models import Session, PlayedTuneGroup, Tune, PlayedTune, NameYerTune, TuneOfTheMonth
from django.db.models import Count, Aggregate, CharField

# Code for Custom ORM Method
class Concat(Aggregate):
    """ORM is used to group other fields. This is equivalent to group_concat"""
    function = 'array_agg'
    template = '%(function)s(%(distinct)s%(expressions)s)'
    allow_distinct = True
 
    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)

# Create your views here.
def home(request):
    """
    Landing page of session home page
    """
    
    sessions = Session.objects.all()
    tunes = Tune.objects.all()
    name_yer_tunes = NameYerTune.objects.all()
    played_tunes = PlayedTune.objects.all()
    tune_sets = PlayedTuneGroup.objects.all()

    
    return render(request, 'session/home.html', {'tunes_count': tunes.count(),
                                                'sessions_count': sessions.count(),
                                                'name_yer_tunes_count': name_yer_tunes.count(),
                                                'played_tunes_count': played_tunes.count(),
                                                'tune_sets_count': tune_sets.count()})

def about(request):
    """
    About page
    """

    return render(request, 'session/about.html')

def full_yt_session_list(request):
    """
    Full List of Youtube Sessions
    """

    sessions = Session.objects.order_by('-date')

    return render(request, 'session/full_yt_session_list.html', {'sessions': sessions})

def session_detail(request, session_id):
    """
    Display of Youtube Session Details
    """

    # Get Session If Avaliable
    session_id_detail = get_object_or_404(Session, session_id=session_id)
    session_date = session_id_detail.date

    # Get embed values
    videoId = session_id_detail.youtube_url.split('embed/')[1]

    # Get Tunes Played
    tune_groups = []
    r = PlayedTuneGroup.objects.filter(session=session_id_detail).order_by('session_order_num')
    for group in r:
        tune_groups.append({'group': group, 'played_tunes': PlayedTune.objects.filter(played_tune_group=group).order_by('group_order_num')})

    return render(request, 'session/session_detail.html', {'session_id_detail': session_id_detail,
                                                           'videoId': videoId,
                                                           'tune_groups_buttons': r,
                                                           'tune_groups': tune_groups,
                                                           'session_date': session_date})

def tunes_all(request):
    """
    Display all Tunes in Database
    """

    played_tunes = PlayedTune.objects.values('tune__tune_id'
                ).annotate(Count('tune__tune_id')
                ).annotate(keys=Concat('key__key_type_char', distinct=True)
                ).order_by('tune__name1'
                ).values('tune__tune_id','tune__name1', 'tune__tune_id__count', 'keys','tune__tune_type__tune_type_char','tune__common_core')

    return render(request, 'session/tunes_all.html', {'played_tunes': played_tunes})


def tune_detail(request, tune_id):
    """
    Detail Page for Tune
    """

    # Get Tune
    tune_id_detail = get_object_or_404(Tune, pk=tune_id) 

    # Previous Times It Has Been Played
    played_tune_all =  PlayedTune.objects.filter(tune=tune_id_detail).order_by('-played_tune_group__session__date')
    played_tune_all_count = played_tune_all.count()

    # NameYerTune Video if Present
    try:
        name_yer_tune_detail = NameYerTune.objects.get(tune=tune_id_detail)
    except NameYerTune.DoesNotExist:
        name_yer_tune_detail = None
    
    # tune_of_the_month Video if Present
    try:
        tune_of_the_month_detail = TuneOfTheMonth.objects.get(tune=tune_id_detail)
    except TuneOfTheMonth.DoesNotExist:
        tune_of_the_month_detail = None

    return render(request, 'session/tune_detail.html', {'tune_id_detail': tune_id_detail,
                                                        'played_tune_all': played_tune_all,
                                                        'played_tune_all_count': played_tune_all_count,
                                                        'name_yer_tune_detail': name_yer_tune_detail,
                                                        'tune_of_the_month_detail': tune_of_the_month_detail})

def nameyertune_all(request):
    """
    All the #NameYerTune Tunes
    """

    name_yer_tunes_all = NameYerTune.objects.all().order_by('-session__date')

    return render(request, 'session/name_yer_tune_all.html', {'name_yer_tunes_all': name_yer_tunes_all})

def youtube_loop_test2(request):

    return render(request, 'session/youtube_loop_test2.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_links(request):

    return render(request, 'session/admin_links.html')

@user_passes_test(lambda u: u.is_superuser)
def session_json(request):

    # Make File Name
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H-%M-%S")
    json_file_name = f'{date_time}sessiondb.json'
    path = Path(settings.BASE_DIR) / 'datadump'
    json_file = path / json_file_name

    # Point SystemOutput to file, write to file, and close
    sys.stdout = open(json_file, 'w+') # Point stdout at a file for dumping data too.
    call_command('dumpdata', 'session', indent=3) # Data from session app
    sys.stdout.close()

    # Write File Contents to Temp File
    with open(json_file, 'r') as f:
        file_data = f.read()

    # Delete Out File Location
    os.remove(json_file)

    # Create Reponse to Send
    response = HttpResponse(file_data, content_type="text/plain")
    response['Content-Disposition'] = f'attachment; filename={json_file_name}'

    return response
