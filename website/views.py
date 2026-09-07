from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    SiteSettings, HeroSlide, ServiceCard, ServiceSection, AboutSection,
    SpecialDish, MenuItem, Testimonial, Feature, Event, GalleryItem, SocialLink,
    Reservation, NewsletterSubscriber,
)


def index(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "reservation":
            try:
                Reservation.objects.create(
                    name=request.POST.get("name", "").strip(),
                    phone=request.POST.get("phone", "").strip(),
                    persons=request.POST.get("person", "").strip(),
                    reservation_date=request.POST.get("reservation-date") or None,
                    reservation_time=request.POST.get("time", "").strip(),
                    message=request.POST.get("message", "").strip(),
                )
                messages.success(request, "Thanks! Your table reservation request has been received.")
            except Exception:
                messages.error(request, "Sorry, something went wrong with your reservation. Please check the form and try again.")
            return redirect(request.path + "#reservation")

        if form_type == "newsletter":
            email = request.POST.get("email_address", "").strip()
            if email:
                NewsletterSubscriber.objects.get_or_create(email=email)
                messages.success(request, "You're subscribed! Thanks for joining our newsletter.")
            return redirect(request.path + "#top")

    context = {
        "site": SiteSettings.load(),
        "hero_slides": HeroSlide.objects.filter(is_active=True),
        "service_section": ServiceSection.load(),
        "service_cards": ServiceCard.objects.filter(is_active=True),
        "about": AboutSection.load(),
        "special_dish": SpecialDish.load(),
        "menu_items": MenuItem.objects.filter(is_active=True),
        "testimonial": Testimonial.objects.filter(is_active=True).first(),
        "features": Feature.objects.filter(is_active=True),
        "events": Event.objects.filter(is_active=True),
        "social_links": SocialLink.objects.filter(is_active=True),
    }
    return render(request, "website/index.html", context)


def gallery(request):
    sections = {}
    for item in GalleryItem.objects.filter(is_active=True):
        section_name = item.category.strip() or "Café Moments"
        sections.setdefault(section_name, []).append(item)

    context = {
        "site": SiteSettings.load(),
        "gallery_sections": [
            {"title": title, "items": items}
            for title, items in sections.items()
        ],
        "social_links": SocialLink.objects.filter(is_active=True),
    }
    return render(request, "website/gallery.html", context)
