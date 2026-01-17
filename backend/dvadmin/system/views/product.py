# -*- coding: utf-8 -*-

"""
@author: zhihui.hao
@Remark: 平台管理
"""
from rest_framework import serializers

from dvadmin.system.models import Product
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProductSerializer(CustomModelSerializer):
    """
    Product Serializer
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]


class ProductViewSet(CustomModelViewSet):
    """
    Platform view set
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ["name", "id"]
    search_fields = ["name"]
