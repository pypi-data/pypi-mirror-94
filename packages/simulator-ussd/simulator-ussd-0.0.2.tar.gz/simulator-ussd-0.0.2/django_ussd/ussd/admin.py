# Prevent local core module from shadowing the core app, from which we
# need to import our CSV export action


from django.contrib import admin
from .models import *
from django.forms import forms, ModelForm
from functools import partial
# class MenuOptionAdmin(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super(MenuOptionAdmin, self).get_queryset(request)
#         return qs.order_by('ussd_handler')


class RouterOptionsInline(admin.TabularInline):
    model = UssdRouterHandler
    fk_name = 'ussd_handler'
    extra = 0

class TextInlineAdmin(admin.TabularInline):
    model = UssdHandler.text.through
    extra = 1

class MenuTextInlineAdmin(admin.TabularInline):
    model = MenuOptions.text.through
    extra = 1
    filter_horizontal = ('text',)

class MenuOptionInline(admin.TabularInline):
    model = MenuOptions
    fk_name = 'ussd_handler'
    show_change_link = True
    extra = 0
    inlines = [MenuTextInlineAdmin]
    filter_horizontal = ('text', )
    #exclude = ('text',)


@admin.register(UssdHandler)
class UssdHandlerAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [TextInlineAdmin, MenuOptionInline, RouterOptionsInline]
    exclude = ('text', )

admin.site.register(Widget)
admin.site.register(ListItems)
admin.site.register(MenuOptions)
admin.site.register(UssdRouterHandler)
admin.site.register(HttpRequest)
admin.site.register(PluginHandler)
admin.site.register(Translation)