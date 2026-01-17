import hashlib
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_python3_ldap import ldap
from dvadmin.system.models import Role
from django_python3_ldap.auth import LDAPBackend
from django.utils import timezone

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    Django原生认证方式
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        msg = '%s 正在使用本地登录...' % username
        print(password)
        logger.info(msg)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            check_password = user.check_password(password)
            if not check_password:
                check_password = user.check_password(hashlib.md5(password.encode(encoding='UTF-8')).hexdigest())
            if check_password and self.user_can_authenticate(user):
                user.last_login = timezone.now()
                user.save()
                return user


class NewLDAPBackend(LDAPBackend):
    """
        基于django_python3_ldap模块的ldap认证和创建更新用户功能，添加为新创建的用户添加
        public权限功能，这样用户能够进入后直接用于public开放的权限。
    """
    def authenticate(self, *args, **kwargs):
        user = ldap.authenticate(*args, **kwargs)
        if user and not user.role.values_list('id', flat=True):
            role_key = 'public'
            role_ids = Role.objects.filter(key=role_key).values_list('id',flat=True)
            user.role.set(role_ids)
            user.save()
            msg = '设置默认权限... %s' % role_key
            logger.info(msg)
        return user
