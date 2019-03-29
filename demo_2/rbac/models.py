from django.db import models

from api.models import UserInfo
# Create your models here.


class User(models.Model):
    id = models.IntegerField(max_length=32)
    name = models.OneToOneField("UserInfo", to_field="username", on_delete=models.CASCADE)


class Role(models.Model):
    id = models.IntegerField(max_length=32)
    name = models.CharField(max_length=32, help_text="角色名称")
    role_id = models.IntegerField(unique=True)
    role_type = models.CharField(max_length=32, help_text="角色类型")


class Premissions(models.Model):
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=64, verbose_name='权限', null=True, blank=True)
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    name = models.CharField(
        max_length=32,
        verbose_name='url别名',
        default="",
        null=True,
        blank=True)

    # is_menu = models.BooleanField(default=False)
    # icon = models.CharField(max_length=32, default="")

    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(max_length=32, verbose_name='菜单')
    icon = models.CharField(
        max_length=32,
        verbose_name='图标',
        null=True,
        blank=True)
    fid = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)