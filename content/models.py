import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import format_html
from moviepy.editor import VideoFileClip
from shared.helper import Helper

helper = Helper()


class Content(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    name = models.CharField(max_length=255)
    hidden = models.BooleanField(default=False)
    cover = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Content, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/content/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Content, dispatch_uid="s3_upload")
def update_content(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Content, dispatch_uid="s3_delete")
def delete_content(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)


class Genre(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    name = models.CharField(
        max_length=255
    )
    cover_credit = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    cover = models.FileField(
        upload_to=helper.get_file_path,
        blank=True,
        null=True
    )
    hidden = models.BooleanField(
        default=False
    )
    featured = models.BooleanField(
        default=False
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    order = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Genre, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/genre/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


@receiver(post_save, sender=Genre, dispatch_uid="s3_upload")
def update_genre(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Genre, dispatch_uid="s3_delete")
def delete_genre(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)


class Media(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    hash = models.CharField(max_length=36, unique=True)
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    cover = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    description = models.TextField(null=True, blank=True)
    hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Media, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/media/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Media, dispatch_uid="s3_upload")
def update_media(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Media, dispatch_uid="s3_delete")
def delete_media(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)


class Season(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    hash = models.CharField(max_length=36, unique=True)
    number = models.IntegerField()
    date = models.DateField(blank=True, null=True)
    hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Season, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/season/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def __str__(self):
        return "{} (S{})".format(
            self.media,
            "0{}".format(self.number) if self.number < 10 else self.number
        )

    class Meta:
        ordering = ['-created_date']


class Tag(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    name = models.CharField(
        max_length=255
    )
    cover = models.FileField(
        upload_to=helper.get_file_path,
        blank=True,
        null=True
    )
    hidden = models.BooleanField(
        default=False
    )
    order = models.IntegerField(
        default=0, blank=True, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Tag, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/tag/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


@receiver(post_save, sender=Tag, dispatch_uid="s3_upload")
def update_tag(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Tag, dispatch_uid="s3_delete")
def delete_tag(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)


class Subtitle(models.Model):
    language = models.CharField(max_length=2)
    label = models.CharField(max_length=255)
    vtt = models.FileField(upload_to=helper.get_file_path)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Subtitle, dispatch_uid="s3_upload")
def update_subtitle(sender, instance, **kwargs):
    if instance.vtt and 'tmp' in instance.vtt.url:
        path = "/app/{}".format(instance.vtt.url)
        instance.vtt = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Subtitle, dispatch_uid="s3_delete")
def delete_subtitle(sender, instance, **kwargs):
    if instance.vtt and instance.vtt.url:
        helper.delete_file(instance.vtt.url)


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    hash = models.CharField(max_length=36, unique=True)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag, blank=True)
    subtitle = models.ForeignKey(
        Subtitle, on_delete=models.CASCADE, null=True, blank=True)
    cover = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    media = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    duration = models.FloatField(default=0)
    frames = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    date = models.DateField(blank=True, null=True)
    hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        found = model.objects.filter(user=user, episode=self).count()
        return found > 0

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Episode, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/episode/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Episode, dispatch_uid="s3_upload")
def update_episode(sender, instance, **kwargs):
    if instance.media and 'tmp' in instance.media.url:
        path = "/app/{}".format(instance.media.url)

        clip = VideoFileClip(path)

        instance.duration = clip.duration
        instance.frames = clip.fps
        width, height = clip.size

        instance.width = width
        instance.height = height

        frame = int(clip.duration - (clip.duration/4))
        cover = helper.extract_frame(path, frame)

        instance.cover = helper.upload_file("/app/tmp/{}".format(cover))
        instance.media = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Episode, dispatch_uid="s3_delete")
def delete_episode(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)
    if instance.media and instance.media.url:
        helper.delete_file(instance.media.url)


class Movie(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    title = models.CharField(
        max_length=255
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
    )
    tag = models.ManyToManyField(
        Tag,
        blank=True,
    )
    subtitle = models.ForeignKey(Subtitle, on_delete=models.CASCADE,
                                 null=True, blank=True)
    cover = models.FileField(
        upload_to=helper.get_file_path,
        blank=True,
        null=True
    )
    media = models.FileField(
        upload_to=helper.get_file_path,
        blank=True,
        null=True
    )
    embed = models.TextField(
        default="", null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True
    )
    views = models.IntegerField(
        default=0
    )
    duration = models.FloatField(
        default=0
    )
    frames = models.FloatField(
        default=0
    )
    width = models.FloatField(
        default=0
    )
    height = models.FloatField(
        default=0
    )
    date = models.DateField(
        blank=True, null=True
    )
    hidden = models.BooleanField(
        default=False
    )
    metadata = models.BooleanField(
        default=False
    )
    bypass_metadata = models.BooleanField(
        default=False
    )
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        if user.email == "anon@fehra.co":
            return False
        found = model.objects.filter(user=user, movie=self).count()
        return found > 0

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Movie, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/movie/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


@receiver(post_save, sender=Movie, dispatch_uid="s3_upload")
def update_movie(sender, instance, **kwargs):
    if instance.media and 'tmp' in instance.media.url:
        path = "/app/{}".format(instance.media.url)

        clip = VideoFileClip(path)

        instance.duration = clip.duration
        instance.frames = clip.fps
        width, height = clip.size

        instance.width = width
        instance.height = height

        frame = int(clip.duration - (clip.duration/4))
        cover = helper.extract_frame(path, frame)

        instance.cover = helper.upload_file("/app/tmp/{}".format(cover))
        instance.media = helper.upload_file(path)
        instance.save()

    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Movie, dispatch_uid="s3_delete")
def delete_movie(sender, instance, **kwargs):
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)
    if instance.media and instance.media.url:
        helper.delete_file(instance.media.url)


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    time = models.FloatField(blank=True,
                             null=True,
                             default=0)
    volume = models.FloatField(blank=True,
                               null=True,
                               default=1)
    speed = models.FloatField(blank=True,
                              null=True,
                              default=1)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def __str__(self):
        return "{}, {}".format(self.time, self.modified_date)

    class Meta:
        ordering = ['-created_date']


class Photo(models.Model):
    photo = models.FileField(upload_to=helper.get_file_path)
    hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Photo, dispatch_uid="s3_upload")
def update_photo(sender, instance, **kwargs):
    if instance.photo and 'tmp' in instance.photo.url:
        path = "/app/{}".format(instance.photo.url)
        instance.photo = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Photo, dispatch_uid="s3_delete")
def delete_photo(sender, instance, **kwargs):
    if instance.photo and instance.photo.url:
        helper.delete_file(instance.photo.url)


class PhotoCollection(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    cover = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    photos = models.ManyToManyField(Photo, blank=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def is_watchlist(self, user, model):
        return False

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(PhotoCollection, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/photo/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=PhotoCollection, dispatch_uid="s3_upload")
def update_photocollection(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=PhotoCollection, dispatch_uid="s3_delete")
def delete_photocollection(sender, instance, **kwargs):
    instance.photos.all().delete()
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def __str__(self):
        return "{}, {}".format(self.user.first_name, self.modified_date)

    class Meta:
        ordering = ['-created_date']


class WatchParty(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    playing = models.BooleanField(default=False)
    current_time = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(WatchParty, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/watchparty/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        ordering = ['-created_date']


class MessageWatchParty(models.Model):
    watch_party = models.ForeignKey(WatchParty, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def __str__(self):
        return "{}".format(self.text)

    class Meta:
        ordering = ['created_date']


class Playlist(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    name = models.CharField(max_length=255)
    hidden = models.BooleanField(default=False)
    movies = models.ManyToManyField(Movie)
    cover = models.FileField(upload_to=helper.get_file_path,
                             blank=True,
                             null=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                         blank=True,
                                         null=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = str(uuid.uuid1())
        super(Playlist, self).save(*args, **kwargs)

    def link(self):
        return format_html(
            "<a target='_blank' href='{}/playlist/{}'>View</a>".format(
                settings.FRONTEND_URL,
                self.hash
            )
        )

    def get_cover(self):
        if self.cover:
            return format_html(
                "<img src='{}' width='100' />".format(
                    helper.create_presigned_url(self.cover.url)
                )
            )
        return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=Playlist, dispatch_uid="s3_upload")
def update_playlist(sender, instance, **kwargs):
    if instance.cover and 'tmp' in instance.cover.url:
        path = "/app/{}".format(instance.cover.url)
        path = helper.resize_image(path, 1280, crop=720)
        instance.cover = helper.upload_file(path)
        instance.save()


@receiver(pre_delete, sender=Playlist, dispatch_uid="s3_delete")
def delete_playlist(sender, instance, **kwargs):
    instance.photos.all().delete()
    if instance.cover and instance.cover.url:
        helper.delete_file(instance.cover.url)
