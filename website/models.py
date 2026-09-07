from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


MEDIA_TYPE_CHOICES = [
    ("image", "Image"),
    ("video", "Video"),
]

VIDEO_EXTENSIONS = ["mp4", "webm", "ogg"]
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_video_upload(value):
    """Allow browser-friendly videos up to 50 MB."""
    FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)(value)

    if value.size > MAX_VIDEO_SIZE:
        raise ValidationError("Video file must be 50 MB or smaller.")

    content_type = getattr(value.file, "content_type", "")
    if content_type and content_type not in {"video/mp4", "video/webm", "video/ogg"}:
        raise ValidationError("Upload an MP4, WebM, or OGG video.")


def validate_single_media(instance, type_field, image_field, video_field, required=False):
    """Ensure the selected media exists and image/video are not both stored."""
    media_type = getattr(instance, type_field)
    image = getattr(instance, image_field)
    video = getattr(instance, video_field)
    errors = {}

    if image and video:
        errors[video_field] = "Keep only one file: either an image or a video."

    selected_file = video if media_type == "video" else image
    selected_field = video_field if media_type == "video" else image_field
    if required and not selected_file:
        errors[selected_field] = f"Upload a {media_type} for the selected media type."

    if errors:
        raise ValidationError(errors)


class SiteSettings(models.Model):
    """Global site info shown in topbar, header, footer, reservation section.
    Only one row is used (singleton) — edit it from the admin panel."""

    site_name = models.CharField(max_length=100, default="Torque Tales")
    tagline = models.CharField(max_length=200, default="Amazing & Delicious Food")

    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    address = models.CharField(max_length=255, default="Restaurant St, Delicious City, London 9578, UK")
    open_hours = models.CharField(max_length=100, default="Daily : 8.00 am to 10.00 pm")
    phone = models.CharField(max_length=30, default="+1 123 456 7890")
    phone_link = models.CharField(max_length=30, default="+11234567890", help_text="Digits only, used for tel: link")
    email = models.EmailField(default="booking@restaurant.com")

    navbar_open_hours = models.CharField(max_length=100, default="Open: 9.30 am - 2.30pm")
    booking_phone = models.CharField(max_length=30, default="+88-123-123456")
    booking_phone_link = models.CharField(max_length=30, default="+88123123456")

    reservation_lunch_time = models.CharField(max_length=100, default="Monday to Sunday, 11.00 am - 2.30pm")
    reservation_dinner_time = models.CharField(max_length=100, default="Monday to Sunday, 05.00 pm - 10.00pm")

    footer_background = models.ImageField(upload_to="site/", blank=True, null=True)
    footer_open_hours = models.CharField(max_length=100, default="Open : 09:00 am - 01:00 pm")
    newsletter_offer_text = models.CharField(max_length=100, default="Subscribe us & Get 25% Off.")
    copyright_text = models.CharField(max_length=255, default="© 2026 Torque Tales. All Rights Reserved")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # keep this a singleton: always overwrite the first row
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    subtitle = models.CharField(max_length=100, help_text="Small text above the title, e.g. 'Traditional & Hygiene'")
    title_line_1 = models.CharField(max_length=100)
    title_line_2 = models.CharField(max_length=100, blank=True)
    text = models.CharField(max_length=255, default="Come with family & feel the joy of mouthwatering food")
    button_text = models.CharField(max_length=50, default="View Our Menu")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    image = models.ImageField(upload_to="hero/", blank=True, null=True)
    video = models.FileField(
        upload_to="hero/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.order}. {self.title_line_1}"

    def clean(self):
        super().clean()
        validate_single_media(self, "media_type", "image", "video", required=True)


class ServiceCard(models.Model):
    """The 3 cards in the 'We Offer Top Notch' section (Breakfast, Appetizers, Drinks)."""
    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    image = models.ImageField(upload_to="service/", blank=True, null=True)
    video = models.FileField(
        upload_to="service/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        validate_single_media(self, "media_type", "image", "video", required=True)


class ServiceSection(models.Model):
    """The heading/intro text above the service cards."""
    subtitle = models.CharField(max_length=100, default="Flavors For Royalty")
    title = models.CharField(max_length=150, default="We Offer Top Notch")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")

    class Meta:
        verbose_name = "Service Section (heading)"
        verbose_name_plural = "Service Section (heading)"

    def __str__(self):
        return "Service section heading"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutSection(models.Model):
    subtitle = models.CharField(max_length=100, default="Our Story")
    title = models.CharField(max_length=150, default="Every Flavor Tells a Story")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")
    call_phone = models.CharField(max_length=30, default="+80 (400) 123 4567")
    call_phone_link = models.CharField(max_length=30, default="+804001234567")
    banner_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    banner_image = models.ImageField(upload_to="about/", blank=True, null=True)
    banner_video = models.FileField(
        upload_to="about/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    small_image = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        validate_single_media(
            self, "banner_media_type", "banner_image", "banner_video", required=False
        )

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SpecialDish(models.Model):
    subtitle = models.CharField(max_length=100, default="Special Dish")
    title = models.CharField(max_length=150, default="Lobster Tortellini")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    banner_image = models.ImageField(upload_to="special-dish/", blank=True, null=True)
    video = models.FileField(
        upload_to="special-dish/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )

    class Meta:
        verbose_name = "Special Dish"
        verbose_name_plural = "Special Dish"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        validate_single_media(self, "media_type", "banner_image", "video", required=False)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MenuItem(models.Model):
    BADGE_CHOICES = [
        ("", "No badge"),
        ("New", "New"),
        ("Seasonal", "Seasonal"),
        ("Hot", "Hot"),
    ]
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="menu/")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, default="")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    text = models.TextField()
    customer_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    background_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    background_image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    background_video = models.FileField(
        upload_to="testimonials/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.customer_name

    def clean(self):
        super().clean()
        validate_single_media(
            self,
            "background_media_type",
            "background_image",
            "background_video",
            required=False,
        )


class Feature(models.Model):
    """'Why Choose Us' cards."""
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="features/")
    text = models.CharField(max_length=255, default="Lorem Ipsum is simply dummy printing and typesetting.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100, help_text="e.g. 'Food, Flavour'")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    video = models.FileField(
        upload_to="events/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        validate_single_media(self, "media_type", "image", "video", required=True)


class GalleryItem(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(
        max_length=80,
        blank=True,
        help_text="Items with the same category appear together under one heading, e.g. Bikes & Rides, Food & Coffee, Café Vibes.",
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    video = models.FileField(
        upload_to="gallery/videos/", blank=True, null=True,
        validators=[validate_video_upload],
        help_text="MP4, WebM, or OGG. Maximum size: 50 MB.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        validate_single_media(self, "media_type", "image", "video", required=True)


class SocialLink(models.Model):
    name = models.CharField(max_length=50, help_text="e.g. Facebook, Instagram")
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """Saved when a visitor submits the 'Online Reservation' form."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    persons = models.CharField(max_length=20)
    reservation_date = models.DateField()
    reservation_time = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.reservation_date}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
