from django.contrib import admin
from .models import Tune, Session, PlayedTuneGroup
from .models import PlayedTune, NameYerTune, TuneOfTheMonth
from .models import Key, TuneType, ShannonTeachingBookRef


class PlayedTuneGroupInline(admin.TabularInline):
    model = PlayedTuneGroup
    extra = 0
    show_change_link = True

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ("date","name")
    inlines = [PlayedTuneGroupInline]
    #date_hierarchy = "date" note: error with  ENGINE:"mysql.connector.django"

@admin.register(Tune)
class TuneAdmin(admin.ModelAdmin):
    ordering = ("name1",)
    search_fields = ("name1","name2","name3","name4")
    list_filter = ("tune_type","common_core")
    list_display = ("name1","name2","tune_type","common_core")

class PlayedTuneInline(admin.TabularInline):
    model = PlayedTune
    extra = 0
    raw_id_fields = ("tune",)

@admin.register(PlayedTuneGroup)
class PlayedTuneGroupAdmin(admin.ModelAdmin):
    ordering = ('-session__date','-session_order_num')
    inlines = [PlayedTuneInline]
    #date_hierarchy = "session__date" note: error with  ENGINE:"mysql.connector.django"

@admin.register(PlayedTune)
class PlayedTuneAdmin(admin.ModelAdmin):
    ordering = ('-played_tune_group__session__date','-played_tune_group__session_order_num','-group_order_num')
    list_display = ("tune_id","tune","played_tune_group")
    raw_id_fields = ("tune","played_tune_group")
    search_fields = ("tune__name1","tune__name2","tune__name3","tune__name4")
    #date_hierarchy = "played_tune_group__session__date" note: error with  ENGINE:"mysql.connector.django"

@admin.register(NameYerTune)
class NameYerTuneAdmin(admin.ModelAdmin):
    pass

@admin.register(TuneOfTheMonth)
class TuneOfTheMonthAdmin(admin.ModelAdmin):
    ordering = ('-published_date',)

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    ordering = ('key_type_char',)

@admin.register(TuneType)
class TuneTypeAdmin(admin.ModelAdmin):
    ordering = ('tune_type_char',)

@admin.register(ShannonTeachingBookRef)
class ShannonTeachingBookRefAdmin(admin.ModelAdmin):
    ordering = ('title',)