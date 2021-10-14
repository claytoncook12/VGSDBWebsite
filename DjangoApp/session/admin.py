from django.contrib import admin
from .models import Tune, Session, PlayedTuneGroup
from .models import PlayedTune, NameYerTune, TuneOfTheMonth
from .models import Key, TuneType


class played_tune_group_inline(admin.TabularInline):
    model = PlayedTuneGroup
    show_change_link = True

@admin.register(Session)
class session_admin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ("date","name")
    inlines = [played_tune_group_inline]
    date_hierarchy = "date"

@admin.register(Tune)
class tune_admin(admin.ModelAdmin):
    ordering = ("name1",)
    search_fields = ("name1","name2","name3","name4")
    list_filter = ("TuneType",)
    list_display = ("name1","name2","TuneType")

class played_tune_inline(admin.TabularInline):
    model = PlayedTune

@admin.register(PlayedTuneGroup)
class played_tune_group_admin(admin.ModelAdmin):
    ordering = ('-session__date','-session_order_num')
    inlines = [played_tune_inline]

@admin.register(PlayedTune)
class played_tune_admin(admin.ModelAdmin):
    date_hierarchy = "played_tune_group__session__date"
    ordering = ('-played_tune_group__session__date','-played_tune_group__session_order_num','-group_order_num')
    list_display = ("Tune","PlayedTuneGroup")

@admin.register(NameYerTune)
class name_yer_tune_admin(admin.ModelAdmin):
    pass

@admin.register(TuneOfTheMonth)
class tune_of_the_month_admin(admin.ModelAdmin):
    ordering = ('-published_date',)

@admin.register(Key)
class key_admin(admin.ModelAdmin):
    ordering = ('key_type_char',)

@admin.register(TuneType)
class tune_type_admin(admin.ModelAdmin):
    ordering = ('tune_type_char',)