from django.contrib import admin
from .models import tune, session, played_tune_group
from .models import played_tune, name_yer_tune, tune_of_the_month
from .models import key, tune_type


class played_tune_group_inline(admin.TabularInline):
    model = played_tune_group
    show_change_link = True

@admin.register(session)
class session_admin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ("date","name")
    inlines = [played_tune_group_inline]
    date_hierarchy = "date"

@admin.register(tune)
class tune_admin(admin.ModelAdmin):
    ordering = ("name1",)
    search_fields = ("name1","name2","name3","name4")
    list_filter = ("tune_type",)
    list_display = ("name1","name2","tune_type")

class played_tune_inline(admin.TabularInline):
    model = played_tune

@admin.register(played_tune_group)
class played_tune_group_admin(admin.ModelAdmin):
    ordering = ('-session__date','-session_order_num')
    inlines = [played_tune_inline]

@admin.register(played_tune)
class played_tune_admin(admin.ModelAdmin):
    date_hierarchy = "played_tune_group__session__date"
    ordering = ('-played_tune_group__session__date','-played_tune_group__session_order_num','-group_order_num')
    list_display = ("tune","played_tune_group")

@admin.register(name_yer_tune)
class name_yer_tune_admin(admin.ModelAdmin):
    pass

@admin.register(tune_of_the_month)
class tune_of_the_month_admin(admin.ModelAdmin):
    ordering = ('-published_date',)

@admin.register(key)
class key_admin(admin.ModelAdmin):
    ordering = ('key_type_char',)

@admin.register(tune_type)
class tune_type_admin(admin.ModelAdmin):
    ordering = ('tune_type_char',)