from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORIES = (
	('CM','Crypto Mining'),
	('S','Stock'),
	('M','Market'),
	('O','Other'),
)

# Create your models here.
class Author(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	profile_picture = models.ImageField(upload_to = 'static/core/profile_pictures',null = True)
	
	def __str__(self):
		return str(self.user)


class Post(models.Model):
	title = models.CharField(max_length = 100)
	overview = models.TextField()
	text = models.TextField()
	featured = models.BooleanField(default = False)
	author = models.ForeignKey(Author, on_delete = models.CASCADE)
	category = models.CharField(choices = CATEGORIES,max_length = 2, default='O')
	thumbnail = models.ImageField(upload_to = 'static/core/thumbnails',null = True)
	views = models.IntegerField(default = 0)
	comments = models.IntegerField(default = 0)
	timestamp = models.DateTimeField()
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
	text = models.TextField()
	replies = models.ManyToManyField("Reply")
	
	def __str__(self):
		return self.text[:25] + '...'
		

class Reply(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	comment_on = models.ForeignKey(Comment, on_delete = models.CASCADE)
	post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
	text = models.TextField()
	
	def __str__(self):
		return self.text[:25] + '...'

class FAQ(models.Model):
	title = models.CharField(max_length = 200)
	text = models.TextField()
	
	def __str__(self):
		return self.title
