from django.db import models

# Create your models here.

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    heading= models.CharField(max_length=750,default="")
    subheading= models.CharField(max_length=750,default="")
    description= models.CharField(max_length=750,default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="blog/images",default="")

    def __str__(self):
        return self.title
