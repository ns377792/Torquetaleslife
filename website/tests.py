import tempfile

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import FieldDoesNotExist
from django.test import RequestFactory, TestCase, override_settings

from .admin import HeroSlideAdmin
from .models import Event, GalleryItem, HeroSlide, MenuItem, ServiceCard, SpecialDish


def sample_video(name="sample.mp4"):
    return SimpleUploadedFile(name, b"small-video-for-tests", content_type="video/mp4")


class TemporaryMediaTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_media = tempfile.TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.temp_media.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.temp_media.cleanup()


class MediaValidationTests(TemporaryMediaTestCase):
    def hero(self, **overrides):
        values = {
            "subtitle": "Fresh food",
            "title_line_1": "Welcome",
            "title_line_2": "Today",
            "media_type": "image",
            "image": "hero/sample.jpg",
        }
        values.update(overrides)
        return HeroSlide(**values)

    def test_selected_video_is_valid_without_image(self):
        slide = self.hero(media_type="video", image=None, video=sample_video())
        slide.full_clean()

    def test_selected_media_is_required(self):
        slide = self.hero(media_type="video", image=None, video=None)
        with self.assertRaises(ValidationError):
            slide.full_clean()

    def test_image_and_video_cannot_both_be_stored(self):
        slide = self.hero(media_type="video", video=sample_video())
        with self.assertRaises(ValidationError):
            slide.full_clean()

    def test_unsupported_video_extension_is_rejected(self):
        slide = self.hero(
            media_type="video",
            image=None,
            video=sample_video("sample.txt"),
        )
        with self.assertRaises(ValidationError):
            slide.full_clean()


class HomepageMediaRenderingTests(TemporaryMediaTestCase):
    def test_torque_tales_branding_and_fixed_logo_are_rendered(self):
        response = self.client.get("/")

        self.assertContains(response, "Torque Tales")
        self.assertContains(response, "site-logo-img")
        self.assertContains(response, 'class="brand-name">Torque Tales</span>', count=2)
        self.assertContains(response, "brand-lockup")
        self.assertNotContains(response, "Grilli")

    def test_homepage_renders_selected_video(self):
        HeroSlide.objects.create(
            subtitle="Fresh food",
            title_line_1="Video hero",
            media_type="video",
            image=None,
            video=sample_video(),
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<video")
        self.assertContains(response, "/media/hero/videos/sample.mp4")

    def test_homepage_only_shows_menu_item_price(self):
        SpecialDish.load()
        MenuItem.objects.create(
            title="Test Dish",
            image="menu/test.jpg",
            price="199.00",
            description="Test menu item",
        )

        response = self.client.get("/")

        self.assertContains(response, "₹199.00")
        self.assertContains(response, "View All Menu", count=2)

    def test_removed_section_content_is_not_rendered(self):
        response = self.client.get("/")

        self.assertNotContains(response, "During winter daily")
        self.assertNotContains(response, "7:00 pm")
        self.assertNotContains(response, "9:00 pm")
        self.assertNotContains(response, "View Our Blog")
        self.assertNotContains(response, "publish-date")
        self.assertNotContains(response, "Read More")
        self.assertNotContains(response, "badge-2.png")

    def test_removed_backend_fields_do_not_exist(self):
        for model, field_name in (
            (ServiceCard, "link_text"),
            (SpecialDish, "old_price"),
            (SpecialDish, "new_price"),
            (Event, "date"),
        ):
            with self.assertRaises(FieldDoesNotExist):
                model._meta.get_field(field_name)


class GalleryPageTests(TemporaryMediaTestCase):
    def test_gallery_page_is_linked_from_homepage(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/gallery/"')
        self.assertContains(response, "Gallery")

    def test_gallery_page_renders_active_image_and_video(self):
        GalleryItem.objects.create(
            title="Café Interior",
            category="Ambience",
            image="gallery/interior.jpg",
            order=1,
        )
        GalleryItem.objects.create(
            title="Coffee Pour",
            category="Food",
            media_type="video",
            video=sample_video("coffee.mp4"),
            order=2,
        )
        GalleryItem.objects.create(
            title="Hidden Item",
            image="gallery/hidden.jpg",
            is_active=False,
        )

        response = self.client.get("/gallery/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our Gallery")
        self.assertContains(response, "Café Interior")
        self.assertContains(response, "Coffee Pour")
        self.assertContains(response, "<video")
        self.assertNotContains(response, "Hidden Item")
        self.assertContains(response, '<section class="gallery-category"', count=2)
        self.assertEqual(len(response.context["gallery_sections"]), 2)


class AdminMediaFormTests(TemporaryMediaTestCase):
    def test_switching_to_video_clears_existing_image(self):
        slide = HeroSlide.objects.create(
            subtitle="Fresh food",
            title_line_1="Admin media",
            media_type="image",
            image="hero/existing.jpg",
        )
        model_admin = HeroSlideAdmin(HeroSlide, admin.site)
        request = RequestFactory().post("/admin/website/heroslide/")
        form_class = model_admin.get_form(request, obj=slide)
        form = form_class(
            data={
                "subtitle": slide.subtitle,
                "title_line_1": slide.title_line_1,
                "title_line_2": "",
                "text": slide.text,
                "button_text": slide.button_text,
                "media_type": "video",
                "order": slide.order,
                "is_active": "on",
            },
            files={"video": sample_video()},
            instance=slide,
        )

        self.assertTrue(form.is_valid(), form.errors)
        updated_slide = form.save(commit=False)
        self.assertFalse(updated_slide.image)
        self.assertTrue(updated_slide.video)
