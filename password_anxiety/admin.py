from django.contrib import admin
from .models import PasswordBehavior, AnxietySurvey

@admin.register(PasswordBehavior)
class PasswordBehaviorAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'password_reuse', 'password_modification', 'memory_anxiety', 'password_behavior_score', 'created_at')
    
    list_filter = ('password_reuse', 'password_modification', 'memory_anxiety')
    
    # Fields that should be editable in the list display
    list_editable = ('password_reuse', 'password_modification', 'memory_anxiety')

    readonly_fields = ('created_at',)
    # Adding ordering
    ordering = ('-created_at',)  # Order by the creation date in descending order

    # Customizing form fields display in the edit view
    fieldsets = (
        (None, {
            'fields': ('user', 'password_reuse', 'password_modification', 'memory_anxiety', 'password_behavior_score')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False



@admin.register(AnxietySurvey)
class AnxietySurveyAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'confidence_score', 'anxiety_level', 'date_taken')
    # Filters for better navigation
    list_filter = ('user',)

    # Customizing form fields display in the edit view
    readonly_fields = ('date_taken',)
    fieldsets = (
        (None, {
            'fields': ('user', 'confidence_score', 'anxiety_level')
        }),
        ('Timestamps', {
            'fields': ('date_taken',),
            'classes': ('collapse',)
        }),
    )


    # def has_add_permission(self, request):
    #     return False
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False