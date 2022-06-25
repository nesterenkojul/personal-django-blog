from django.db import models
from django.urls import reverse
from tinymce import HTMLField


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    overview = models.TextField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={
            'title': self.title
        })


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    overview = models.TextField()
    body = HTMLField()
    thumbnail = models.ImageField()
    featured = models.BooleanField(default=False)
    posted = models.DateField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details', kwargs={
            'id': self.id
        })

    def get_edit_url(self):
        return reverse('post_edit', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post_delete', kwargs={
            'id': self.id
        })

    @property
    def get_view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def get_comments(self):
        return self.comments.all().order_by('-posted')


class Comment(models.Model):
    author = models.CharField(max_length=30, unique=True)
    body = models.TextField()
    posted = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.author


class PostView(models.Model):
    user_ip = models.GenericIPAddressField()
    post = models.ForeignKey(Post, related_name='views', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_ip