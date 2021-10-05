"""Admin pages."""
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """Choice show in admin page."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question show in admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently')
    list_filter = ['pub_date', 'end_date']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
