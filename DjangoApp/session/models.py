from django.db import models

# Create your models here.
class tune_type(models.Model):
    tune_type_id = models.AutoField(primary_key=True)
    tune_type_char = models.CharField('Tune Type', max_length=50, unique=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.tune_type_char = self.tune_type_char.lower()
        super(tune_type, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.tune_type_char

class key(models.Model):
    key_id = models.AutoField(primary_key=True)
    key_type_char = models.CharField('Key', max_length=15, unique=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.key_type_char = self.key_type_char.lower()
        super(key, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.key_type_char

class tune(models.Model):
    tune_id = models.AutoField(primary_key=True)
    name1 = models.CharField('Tune Name', max_length=300)
    name2 = models.CharField('Alternate Name', max_length=300, blank=True)
    name3 = models.CharField('Alternate Name', max_length=300, blank=True)
    name4 = models.CharField('Alternate Name', max_length=300, blank=True)
    tune_type = models.ForeignKey(tune_type, on_delete=models.CASCADE, verbose_name="Tune Type")
    the_session_url = models.URLField(blank=True)
    tune_info = models.CharField('Information about the tune', max_length=300, blank=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.name1 = self.name1.lower()
        self.name2 = self.name2.lower()
        self.name3 = self.name3.lower()
        self.name4 = self.name4.lower()
        super(tune, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return  self.name1 + " (" + self.tune_type.tune_type_char + ")"

class session(models.Model):
    session_id = models.AutoField(primary_key=True)
    name = models.CharField('Session Name', max_length=300, unique=True)
    date = models.DateField('Session Date')
    youtube_url = models.URLField('Session Youtube URL', blank=True)

    # Force lowercase values only
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.name = self.name.lower()
        super(session, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.date.strftime("%m/%d/%Y") + ": " + self.name

class played_tune_group(models.Model):
    played_tune_group_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(session, on_delete=models.CASCADE, verbose_name="Session")
    session_order_num = models.IntegerField('Order of Tune Group')
    start_time = models.DurationField('Start Time of Group\nin Youtube Recording')
    end_time = models.DurationField('End Time of Group\nin Youtube Recording')
    offertory = models.BooleanField('Is tune group an offertory?')

    def __str__(self):
        return self.session.date.strftime("%m/%d/%Y") + ": Song Group " + str(self.session_order_num) + " [" + \
        str(self.start_time) + " to " + str(self.end_time) + "]"

class played_tune(models.Model):
    played_tune_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    played_tune_group = models.ForeignKey(played_tune_group, on_delete=models.CASCADE, verbose_name="Played Tune Group")
    key = models.ForeignKey(key, on_delete=models.CASCADE, verbose_name="Key of Tune", related_name='Key')
    group_order_num = models.IntegerField('Order tune was played in tune group.')
    add_info = models.CharField('Additional information about the tune for this perticular time\
                                it was played', max_length=300, blank=True)

    def __str__(self):
        return self.played_tune_group.session.date.strftime("%m/%d/%Y") + " - " +\
            "Group " + str(self.played_tune_group.session_order_num) + ' - ' + \
            str(self.group_order_num) + " - " + \
            self.tune.name1 + " (" + self.key.key_type_char + ") " + "(" + \
            self.tune.tune_type.tune_type_char + ")"

class name_yer_tune(models.Model):
    name_yer_tune_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    session = models.ForeignKey(session, on_delete=models.CASCADE, verbose_name="Session")
    youtube_teaching_url = models.URLField('#nameyertune Youtube Teaching Embeded URL')

    def __str__(self):
        return self.session.date.strftime("%m/%d/%Y") + " " + self.tune.name1

class tune_of_the_month(models.Model):
    tune_of_the_month_id = models.AutoField(primary_key=True)
    tune = models.ForeignKey(tune, on_delete=models.CASCADE, verbose_name="Tune Name")
    published_date = models.DateField('Published Date')
    youtube_teaching_url = models.URLField('Tune of the Month Embeded URL')

    def __str__(self):
        return self.published_date.strftime("%m/%d/%Y") + " " + self.tune.name1