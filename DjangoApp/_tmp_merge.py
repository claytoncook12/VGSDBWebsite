from session.models import Tune, PlayedTune
keep = Tune.objects.get(tune_id=256)
dup = Tune.objects.get(tune_id=1041)
moved = PlayedTune.objects.filter(tune=dup).update(tune=keep)
print("moved swingin'->swinging:", moved)
dup.delete()
print("deleted pk 1041")
