# docker 镜像打包

### 打包测试环境docker(注意更改版本号，下次换成art-internal.test.com下)

~~~sh
# 前端docker
docker build -f ./docker_env/web/Dockerfile_test -t hub.test.com/builder/support_platform_web:1.0.0 .
docker push hub.test.com/builder/support_platform_web:1.0.0
# 后端docker
docker build -f ./docker_env/django/Dockerfile_test -t hub.test.com/builder/support_platform_backend_test:1.0.0 .
docker push hub.test.com/builder/support_platform_backend_test:1.0.0
~~~

### 打包线上环境docker(注意更改版本号)

~~~sh
# 前端docker
docker build -f ./docker_env/web/Dockerfile_prod -t art-internal.test.com/scm-docker/support_platform_web:1.0.1 .
docker push art-internal.test.com/scm-docker/support_platform_web:1.0.1
# 后端docker
docker build -f ./docker_env/django/Dockerfile_prod -t art-internal.test.com/scm-docker/support_platform_backend:1.0.0 .
docker push art-internal.test.com/scm-docker/support_platform_backend:1.0.0
~~~



## docker-compose 运行

~~~
# 先安装docker-compose (自行百度安装),执行此命令等待安装，如有使用celery插件请打开docker-compose.yml中celery 部分注释
docker-compose up -d
# 初始化后端数据(第一次执行即可)
docker exec -ti dvadmin-django bash
python manage.py makemigrations 
python manage.py migrate
python manage.py init -y
exit

前端地址：http://127.0.0.1:8080
后端地址：http://127.0.0.1:8000
# 在服务器上请把127.0.0.1 换成自己公网ip
账号：superadmin 密码：admin123456

# docker-compose 停止
docker-compose down
#  docker-compose 重启
docker-compose restart
#  docker-compose 启动时重新进行 build
docker-compose up -d --build

~~~

