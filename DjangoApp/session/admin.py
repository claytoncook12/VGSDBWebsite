from django.contrib import admin
from .models import Tune, Session, PlayedTuneGroup
from .models import PlayedTune, NameYerTune, TuneOfTheMonth
from .models import Key, TuneType


class PlayedTuneGroupInline(admin.TabularInline):
    model = PlayedTuneGroup
    show_change_link = True

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ("date","name")
    inlines = [PlayedTuneGroupInline]
    date_hierarchy = "date"

@admin.register(Tune)
class TuneAdmin(admin.ModelAdmin):
    ordering = ("name1",)
    search_fields = ("name1","name2","name3","name4")
    list_filter = ("tune_type",)
    list_display = ("name1","name2","tune_type")

class PlayedTuneInline(admin.TabularInline):
    model = PlayedTune

@admin.register(PlayedTuneGroup)
class PlayedTuneGroupAdmin(admin.ModelAdmin):
    ordering = ('-session__date','-session_order_num')
    inlines = [PlayedTuneInline]

@admin.register(PlayedTune)
class PlayedTuneAdmin(admin.ModelAdmin):
    date_hierarchy = "played_tune_group__session__date"
    ordering = ('-played_tune_group__session__date','-played_tune_group__session_order_num','-group_order_num')
    list_display = ("tune","played_tune_group")

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