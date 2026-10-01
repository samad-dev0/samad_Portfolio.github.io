from django.contrib import admin

from .models import ContactMessage, Metric, PortfolioProfile, Service, Skill


@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not PortfolioProfile.objects.exists()


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("value", "title", "position")
    ordering = ("position",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "position")
    ordering = ("position",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "position")
    ordering = ("position",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
