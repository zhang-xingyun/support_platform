# -*- coding: utf-8 -*-

"""
@author: robot
@Remark: 发布版本
"""
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from dvadmin.utils.json_response import (
    DetailResponse,
    SuccessResponse,
    ErrorResponse,
)
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from dvadmin.system.models import Users
from dvadmin.system.models import Product
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from .models import PublishedVersion, ReleaseType, DownloadRecord
import urllib.parse
import re
import json
import base64
from django.conf import settings
import requests
import datetime

MAX_DEPTH = 5
MIN_SUB_MINUTES = 30


class PublishedVersionSerializer(CustomModelSerializer):
    """
    Published Version Serializer
    """

    def create(self, validated_data):
        if (
            PublishedVersion.objects.filter(name=validated_data["name"],
                                            product_name=validated_data["product_name"])
            .exists()
        ):
            raise serializers.ValidationError(detail={"msg": "注册的版本已存在"})

        validated_data["creator"] = self.context["request"].user

        return PublishedVersion.objects.create(**validated_data)

    class Meta:
        model = PublishedVersion
        fields = "__all__"
        read_only_fields = ["id"]


class PublishedVersionViewSet(CustomModelViewSet):
    """
    Published Version view set
    """

    queryset = PublishedVersion.objects.all()
    serializer_class = PublishedVersionSerializer
    filter_fields = ["name", "id", "product_name", "product_number", "release_time", "type", "delisting_time", "release_note"]
    search_fields = ["name", "product_name", "product_number", "type__name", "release_note"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 设置除了管理员可以全部访问，普通用户只能访问没有过期的发版版本
        # date_now = datetime.datetime.today()
        # admin_key = 'admin'
        # role_admin_ids = request.user.role.filter(key=admin_key).values_list('id',
        #                                                          flat=True)
        # if request.user.is_superuser == 1 or 1 in role_admin_ids:
        #     queryset = queryset
        # else:
        #     queryset = queryset.filter(delisting_time__gte=date_now)
        serializer = self.get_serializer(
            queryset, many=True, request=request
        )
        return SuccessResponse(data=serializer.data, msg="获取成功")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        if request.data['delisting_time'] == '':
            request.data['delisting_time'] = None
        if request.data['release_time'] == '':
            request.data['release_time'] = None
        serializer = self.get_serializer(
            instance, data=request.data, request=request, partial=partial
        )
        print(request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return DetailResponse(data=serializer.data, msg="更新成功")


class DownloadRecordSerializer(CustomModelSerializer):
    """
    Download Record Serializer
    """

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        print(validated_data)
        return DownloadRecord.objects.create(**validated_data)

    class Meta:
        model = DownloadRecord
        fields = "__all__"
        read_only_fields = ["id"]


class DownloadRecordViewSet(CustomModelViewSet):
    """
    Download Record view set
    """

    queryset = DownloadRecord.objects.all()
    serializer_class = DownloadRecordSerializer
    filter_fields = ["version", "id", "apply_time", "apply_user"]
    search_fields = ["version__name", "apply_user"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True, request=request
        )
        return SuccessResponse(data=serializer.data, msg="获取成功")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")


class ReleaseTypeSerializer(CustomModelSerializer):
    """
    Release Type Serializer
    """

    class Meta:
        model = ReleaseType
        fields = "__all__"
        read_only_fields = ["id"]


class ReleaseTypeViewSet(CustomModelViewSet):
    """
    Release Type view set
    """

    queryset = ReleaseType.objects.all()
    serializer_class = ReleaseTypeSerializer
    filter_fields = ["name", "id"]
    search_fields = ["name"]
