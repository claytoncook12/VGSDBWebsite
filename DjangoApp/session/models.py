from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class TuneType(models.Model):
    tune_type_id = models.AutoField(primary_key=True)
    tune_type_char = models.CharField('Tune Type', max_length=50, unique=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.tune_type_char = self.tune_type_char.lower()
        super(TuneType, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.tune_type_char

class Key(models.Model):
    key_id = models.AutoField(primary_key=True)
    key_type_char = models.CharField('Key', max_length=15, unique=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.key_type_char = self.key_type_char.lower()
        super(Key, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.key_type_char

class ShannonTeachingBookRef(models.Model):
    title = models.CharField("Name of Shannon Teaching Book", max_length=100)
    resource_url = models.URLField("Resource URL for tune")

    def __str__(self):
        return self.title

class Tune(models.Model):
    tune_id = models.AutoField(primary_key=True)
    name1 = models.CharField('Tune Name', max_length=300)
    name2 = models.CharField('Alternate Name', max_length=300, blank=True)
    name3 = models.CharField('Alternate Name', max_length=300, blank=True)
    name4 = models.CharField('Alternate Name', max_length=300, blank=True)
    tune_type = models.ForeignKey(TuneType, on_delete=models.CASCADE, verbose_name="Tune Type")
    the_session_url = models.URLField(blank=True)
    tune_info = models.CharField('Information about the Tune', max_length=300, blank=True)
    common_core = models.BooleanField("Common Core Tune", default=False)
    shannon_teaching_book_ref = models.ForeignKey(ShannonTeachingBookRef,
                                                  on_delete=models.CASCADE,
                                                  verbose_name="Shannon Teaching Reference",
                                                  null=True,
                                                  blank=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.name1 = self.name1.lower()
        self.name2 = self.name2.lower()
        self.name3 = self.name3.lower()
        self.name4 = self.name4.lower()
        super(Tune, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return  self.name1 + " (" + self.tune_type.tune_type_char + ")"

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    name = models.CharField('Session Name', max_length=300)
    date = models.DateField('Session Date')
    youtube_url = models.URLField('Session Youtube URL', blank=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.name = self.name.lower()
        super(Session, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.date.strftime("%m/%d/%Y") + ": " + self.name

class PlayedTuneGroup(models.Model):
    played_tune_group_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Session")
    session_order_num = models.IntegerField('Order of Tune Group')
    start_time = models.DurationField('Start Time of Group\nin Youtube Recording')
    end_time = models.DurationField('End Time of Group\nin Youtube Recording')
    offertory = models.BooleanField('Is Tune group an offertory?')
    teaching = models.BooleanField('Is Tune a Teaching Set?', default=False)

    def __str__(self):
        return self.session.date.strftime("%m/%d/%Y") + ": Song Group " + str(self.session_order_num) + " [" + \
        str(self.start_time) + " to " + str(self.end_time) + "]"

class PlayedTune(models.Model):
    played_tune_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    played_tune_group = models.ForeignKey(PlayedTuneGroup, on_delete=models.CASCADE, verbose_name="Played Tune Group")
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name="Key of Tune", related_name='Key')
    group_order_num = models.IntegerField('Order Tune was played in Tune group.')
    add_info = models.CharField('Additional information about the Tune for this perticular time\
                                it was played', max_length=300, blank=True)

    def __str__(self):
        return self.played_tune_group.session.date.strftime("%m/%d/%Y") + " - " +\
            "Group " + str(self.played_tune_group.session_order_num) + ' - ' + \
            str(self.group_order_num) + " - " + \
            self.tune.name1 + " (" + self.key.key_type_char + ") " + "(" + \
            self.tune.tune_type.tune_type_char + ")"

class NameYerTune(models.Model):
    name_yer_tune_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Session", null=True, blank=True)
    youtube_teaching_url = models.URLField('#nameyertune Youtube Teaching Embeded URL')

    def __str__(self):
        if self.session == None:
            return f'{self.tune.name1} (No Session Assigned)'
        return self.session.date.strftime("%m/%d/%Y") + " " + self.tune.name1
    
    def clean(self, *args, **kwargs):
        super().clean()
        if  "youtube.com/embed/" not in self.youtube_teaching_url:
            raise ValidationError('YouTube url must be the www.youtube.com/embed/# formate')

class TuneOfTheMonth(models.Model):
    tune_of_the_month_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    published_date = models.DateField('Published Date')
    youtube_teaching_url = models.URLField('Tune of the Month Embeded URL')

    def __str__(self):
        return self.published_date.strftime("%m/%d/%Y") + " " + self.tune.name1