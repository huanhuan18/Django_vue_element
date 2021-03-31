from django.db import models

# Create your models here.
class Siteinfo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=50)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True) # upload_to就是上传到设置的MEDIA_ROOT路径
    def __int__(self):
        """展现的一个形式"""
        return self.id