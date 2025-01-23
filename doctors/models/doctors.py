from django.db import models

from Accounts.models import User
from django.urls import reverse
from django.utils.text import slugify

class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="specialities/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    doctors = models.ManyToManyField(User, related_name="specialties")



    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("doctors:list") + f"?speciality={self.slug}"

    @property
    def doctor_count(self):
        return self.doctor_set.filter(is_active=True).count()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/assets/img/specialities/default.png"


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    patient = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="reviews_given"
    )
    doctor = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="reviews_received",
    )
    booking = models.OneToOneField(
        "bookings.Booking", on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["patient", "booking"]

    def __str__(self):
        return f"Review by {self.patient} for Dr. {self.doctor}"

    @property
    def rating_percent(self):
        return (self.rating / 5) * 100

class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="educations"
    )
    college = models.CharField(max_length=300)
    degree = models.CharField(max_length=100)
    year_of_completion = models.IntegerField()

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Doctor Educations"

    def __str__(self) -> str:
        return (
            f"{self.user.get_full_name()} -> {self.college} -> {self.degree}"
        )


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="experiences"
    )
    institution = models.CharField(max_length=300)
    from_year = models.IntegerField()
    to_year = models.IntegerField()
    working_here = models.BooleanField("Currently working here", default=False)
    designation = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Work & Experience"
        verbose_name_plural = "Works & Experiences"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} -> {self.institution}"


class Review(models.Model):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_reviews"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_reviews"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["doctor", "patient"]
        ordering = ["-created_at"]


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    