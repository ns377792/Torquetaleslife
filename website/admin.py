from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SiteSettings, HeroSlide, ServiceCard, ServiceSection, AboutSection,
    SpecialDish, MenuItem, Testimonial, Feature, Event, SocialLink,
    Reservation, NewsletterSubscriber,
)


def thumb(obj, field_name):
    field = getattr(obj, field_name, None)
    if field:
        return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', field.url)
    return "-"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo", "favicon")}),
        ("Top Bar / Contact", {"fields": ("address", "open_hours", "phone", "phone_link", "email")}),
        ("Navbar / Booking", {"fields": ("navbar_open_hours", "booking_phone", "booking_phone_link")}),
        ("Reservation Section", {"fields": ("reservation_lunch_time", "reservation_dinner_time")}),
        ("Footer", {"fields": (
            "footer_background", "footer_open_hours",
            "newsletter_offer_text", "copyright_text",
        )}),
    )

    def has_add_permission(self, request):
        # singleton: only one row allowed
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("order", "title_line_1", "subtitle", "image_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title_line_1",)
    ordering = ("order",)

    def image_preview(self, obj):
        return thumb(obj, "image")
    image_preview.short_description = "Image"


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ServiceSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "link_text", "image_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)

    def image_preview(self, obj):
        return thumb(obj, "image")
    image_preview.short_description = "Image"


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SpecialDish)
class SpecialDishAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SpecialDish.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "price", "badge", "image_preview", "is_active")
    list_editable = ("order", "price", "badge", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)
    search_fields = ("title",)

    def image_preview(self, obj):
        return thumb(obj, "image")
    image_preview.short_description = "Image"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("order", "customer_name", "avatar_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("customer_name",)
    ordering = ("order",)

    def avatar_preview(self, obj):
        return thumb(obj, "avatar")
    avatar_preview.short_description = "Avatar"


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "icon_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)

    def icon_preview(self, obj):
        return thumb(obj, "icon")
    icon_preview.short_description = "Icon"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "date", "image_preview", "is_active")
    list_editable = ("order", "date", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)

    def image_preview(self, obj):
        return thumb(obj, "image")
    image_preview.short_description = "Image"


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "url", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("name",)
    ordering = ("order",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "persons", "reservation_date", "reservation_time", "is_confirmed", "created_at")
    list_editable = ("is_confirmed",)
    list_filter = ("is_confirmed", "reservation_date")
    search_fields = ("name", "phone")
    ordering = ("-created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    ordering = ("-subscribed_at",)


admin.site.site_header = "Grilli Website Administration"
admin.site.site_title = "Grilli Admin"
admin.site.index_title = "Manage your website content"
