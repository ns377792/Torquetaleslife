from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import (
    SiteSettings, HeroSlide, ServiceCard, ServiceSection, AboutSection,
    SpecialDish, MenuItem, Testimonial, Feature, Event, GalleryItem, SocialLink,
    Reservation, NewsletterSubscriber,
)


class SingleMediaAdminForm(forms.ModelForm):
    """Clear the inactive upload so each media slot stores only one file."""

    media_pairs = (
        ("media_type", "image", "video"),
        ("media_type", "banner_image", "video"),
        ("banner_media_type", "banner_image", "banner_video"),
        ("background_media_type", "background_image", "background_video"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, image_field, video_field in self.media_pairs:
            if image_field in self.fields:
                self.fields[image_field].required = False
            if video_field in self.fields:
                self.fields[video_field].required = False

    def clean(self):
        cleaned_data = super().clean()
        available_fields = set(self.fields)

        for type_field, image_field, video_field in self.media_pairs:
            if not {type_field, image_field, video_field}.issubset(available_fields):
                continue

            if cleaned_data.get(type_field) == "video":
                cleaned_data[image_field] = False
            else:
                cleaned_data[video_field] = False

        return cleaned_data


class MediaToggleAdminMixin:
    form = SingleMediaAdminForm

    class Media:
        js = ("website/admin/media-toggle.js",)


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
class HeroSlideAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    list_display = ("order", "title_line_1", "subtitle", "media_type", "media_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title_line_1",)
    ordering = ("order",)
    radio_fields = {"media_type": admin.HORIZONTAL}

    def media_preview(self, obj):
        return "Video" if obj.media_type == "video" and obj.video else thumb(obj, "image")
    media_preview.short_description = "Selected media"


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ServiceSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceCard)
class ServiceCardAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    list_display = ("order", "title", "media_type", "media_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)
    radio_fields = {"media_type": admin.HORIZONTAL}

    def media_preview(self, obj):
        return "Video" if obj.media_type == "video" and obj.video else thumb(obj, "image")
    media_preview.short_description = "Selected media"


@admin.register(AboutSection)
class AboutSectionAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    radio_fields = {"banner_media_type": admin.HORIZONTAL}

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SpecialDish)
class SpecialDishAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    radio_fields = {"media_type": admin.HORIZONTAL}

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
class TestimonialAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    list_display = ("order", "customer_name", "background_media_type", "avatar_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("customer_name",)
    ordering = ("order",)
    radio_fields = {"background_media_type": admin.HORIZONTAL}

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
class EventAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    list_display = ("order", "title", "media_type", "media_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    ordering = ("order",)
    radio_fields = {"media_type": admin.HORIZONTAL}

    def media_preview(self, obj):
        return "Video" if obj.media_type == "video" and obj.video else thumb(obj, "image")
    media_preview.short_description = "Selected media"


@admin.register(GalleryItem)
class GalleryItemAdmin(MediaToggleAdminMixin, admin.ModelAdmin):
    list_display = ("order", "title", "category", "media_type", "media_preview", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    list_filter = ("category", "media_type", "is_active")
    search_fields = ("title", "category")
    ordering = ("order",)
    radio_fields = {"media_type": admin.HORIZONTAL}

    def media_preview(self, obj):
        return "Video" if obj.media_type == "video" and obj.video else thumb(obj, "image")
    media_preview.short_description = "Selected media"


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


admin.site.site_header = "Torque Tales Website Administration"
admin.site.site_title = "Torque Tales Admin"
admin.site.index_title = "Manage Torque Tales website content"
