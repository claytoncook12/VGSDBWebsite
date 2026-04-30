from session.models import Tune
qs = Tune.objects.filter(name1__icontains="rollin")
for x in qs:
    print(x.tune_id, repr(x.name1), x.playedtune_set.count())
