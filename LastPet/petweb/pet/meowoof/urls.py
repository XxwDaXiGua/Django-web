from django.urls import path

from . import views

app_name = 'meowoof'  # 使用名字空间

urlpatterns = [

    # 首页
    path('index/', views.index, name='index'),

    # 宠物图鉴详情页面
    path('pet_detail/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    # 宠物用品详情界面
    path('tool_detail/<int:tool_id>/', views.tool_detail, name='tool_detail'),
    # 登录页面
    path('login/', views.login, name='login'),

    # 注册页面
    path('register/', views.register, name='register'),

    # 退出登录
    path('logout/', views.logout, name='logout'),

    # 展示界面
    path('pet/', views.pet, name='pet'),
    path('tool/', views.tool, name='tool'),
    path('suggestion/', views.suggestion, name='suggestion'),


    # 用户个人主页
    path('myself/', views.myself, name='myself'),
    path('myself_pet_collect/', views.myself_pet_collect, name='myself_pet_collect'),
    path('myself_tool_collect/', views.myself_tool_collect, name='myself_tool_collect'),
    # 更改个人信息
    path('modify_myself/', views.modify_myself, name='modify_myself'),

    # 处理用户点赞,收藏
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('collect_pet/<int:pet_id>/', views.collect_pet, name='collect_meal'),
    path('collect_tool/<int:tool_id>/', views.collect_tool, name='collect_meal'),

    # 搜索结果界面
    path('pet_search_result/', views.pet_search_result, name='pet_search_result'),
    path('tool_search_result/', views.tool_search_result, name='tool_search_result'),
]
