from django.shortcuts import render, get_object_or_404
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
    
    sessions = session.objects.all()
    tunes = tune.objects.all()
    name_yer_tunes = name_yer_tune.objects.all()
    played_tunes = played_tune.objects.all()
    tune_sets = played_tune_group.objects.all()

    
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

    sessions = session.objects.order_by('-date')

    return render(request, 'session/full_yt_session_list.html', {'sessions': sessions})

def session_detail(request, year, month, day):
    """
    Display of Youtube Session Details
    """

    # Get Session If Avaliable
    url_date = str(year) + '-' + str(month) + "-" + str(day)
    session_id_detail = get_object_or_404(session, date=url_date)

    # Get embed values
    videoId = session_id_detail.youtube_url.split('embed/')[1]

    # Get Tunes Played
    tune_groups = []
    r = played_tune_group.objects.filter(session=session_id_detail).order_by('session_order_num')
    for group in r:
        tune_groups.append({'group': group, 'played_tunes': played_tune.objects.filter(played_tune_group=group).order_by('group_order_num')})

    return render(request, 'session/session_detail.html', {'session_id_detail': session_id_detail,
                                                           'videoId': videoId,
                                                           'tune_groups_buttons': r,
                                                           'tune_groups': tune_groups})

def tunes_all(request):
    """
    Display all Tunes in Database
    """

    played_tunes = played_tune.objects.values('tune__tune_id'
                ).annotate(Count('tune__tune_id')
                ).annotate(keys=Concat('key__key_type_char', distinct=True)
                ).order_by('tune__name1'
                ).values('tune__tune_id','tune__name1', 'tune__tune_id__count', 'keys','tune__tune_type__tune_type_char')

    return render(request, 'session/tunes_all.html', {'played_tunes': played_tunes})


def tune_detail(request, tune_id):
    """
    Detail Page for Tune
    """

    # Get Tune
    tune_id_detail = get_object_or_404(tune, pk=tune_id) 

    # Previous Times It Has Been Played
    played_tune_all =  played_tune.objects.filter(tune=tune_id_detail).order_by('-played_tune_group__session__date')
    played_tune_all_count = played_tune_all.count()

    # NameYerTune Video if Present
    try:
        name_yer_tune_detail = name_yer_tune.objects.get(tune=tune_id_detail)
    except name_yer_tune.DoesNotExist:
        name_yer_tune_detail = None
    
    # tune_of_the_month Video if Present
    try:
        tune_of_the_month_detail = tune_of_the_month.objects.get(tune=tune_id_detail)
    except tune_of_the_month.DoesNotExist:
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

    name_yer_tunes_all = name_yer_tune.objects.all().order_by('-session__date')

    return render(request, 'session/name_yer_tune_all.html', {'name_yer_tunes_all': name_yer_tunes_all})

def youtube_loop_test1(request):

    youtube_video = session.objects.get(date='2020-11-21')
    videoId = youtube_video.youtube_url.split('embed/')[1]

    r = played_tune_group.objects.filter(session=youtube_video)

    return render(request, 'session/youtube_loop_test2.html', {'youtube_video': youtube_video,
                                                               'videoId': videoId,
                                                               'tune_groups': r})
