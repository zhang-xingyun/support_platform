from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from dvadmin.utils.models import CoreModel, table_prefix
from dvadmin.system.models import Product


class ReleaseType(CoreModel):
    """
    发布类型
    """

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        verbose_name="发布类型",
        help_text="发布类型",
    )
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", help_text="显示排序"
    )
    description = models.TextField(
        blank=True, default="", verbose_name="描述", help_text="描述"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + "release_type"
        verbose_name = "发布类型"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)


class PublishedVersion(CoreModel):
    """
    发布版本
    """
    name = models.CharField(
        max_length=128,
        verbose_name="版本名称",
        help_text="版本名称",
    )
    product_number = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="版本名称",
        help_text="版本名称",
    )
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", help_text="显示排序"
    )
    type = models.ForeignKey(
        to=ReleaseType,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=True,
        verbose_name="发布类型",
        help_text="发布类型",
    )
    product_name = models.CharField(
        max_length=50,
        verbose_name="项目",
        help_text="项目",
    )
    release_time = models.DateTimeField(
        verbose_name="发布时间",
        help_text="发布时间",
    )
    delisting_time = models.DateTimeField(
        verbose_name="失效时间",
        help_text="失效时间",
        null=True,
        blank=True,
    )
    project_id = models.CharField(
        max_length=128,
        verbose_name="项目号",
        help_text="项目号",
        default=None,
        null=True,
        blank=True,
    )
    config_link = models.CharField(
        max_length=512,
        verbose_name="软件文档链接",
        help_text="软件文档链接",
        null=True,
        blank=True,
    )
    release_note = models.TextField(
        blank=True, default="", verbose_name="发布说明", help_text="发布说明"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + "published_version"
        verbose_name = "发布版本"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)


class DownloadRecord(CoreModel):
    """
    下载版本记录
    """
    version = models.ForeignKey(
        to=PublishedVersion,
        on_delete=models.PROTECT,
        verbose_name="已发布版本",
        help_text="已发布版本",
    )
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", help_text="显示排序"
    )
    apply_user = models.CharField(
        max_length=128,
        verbose_name="申请下载用户",
        help_text="申请下载用户",
    )
    apply_time = models.DateTimeField(
        verbose_name="申请时间",
        help_text="申请时间",
    )
    description = models.TextField(
        blank=True, default="", verbose_name="描述", help_text="描述"
    )

    def __str__(self):
        return self.version_name

    class Meta:
        db_table = table_prefix + "download_record"
        verbose_name = "下载版本记录"
        verbose_name_plural = verbose_name
        ordering = ("apply_time",)
