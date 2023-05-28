from django.test import TestCase, Client
from django.urls import resolve, reverse
from .views import *
from .models import *
from .forms import *
from django.db.utils import IntegrityError as Integrity1Error

class TestLoginLogoutRegister(TestCase):  # 测试登录注册相关的功能， 主要是测试服务器是否处理了用户请求，是否返回了正确的html文件
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('meowoof:login')  # 先通过reverse获取url路径
        self.register_url = reverse('meowoof:register')
        self.logout_url = reverse('meowoof:logout')

    def test_register(self):
        user1 = {'user_name': 'user1', 'password': '123', 'telephone': '123456',
                 'email': 'user1@qq.com'}
        response = self.client.post(self.register_url, data=user1)
        self.assertEqual(response.status_code, 200)  # 状态码为200表示服务器成功处理了注册请求
        self.assertTemplateUsed(response, 'meowoof/register.html')  # 检测使用的模板是否为register.html

    def test_login(self):
        user2 = {'user_name': 'user2', 'password': '123', 'telephone': '1234556',
                 'email': 'user2@qq.com'}
        response = self.client.post(self.login_url, data=user2)
        self.assertEqual(response.status_code, 200)  # 状态码为200表示服务器成功处理了注册请求
        self.assertTemplateUsed(response, 'meowoof/login.html')  # 使用的template是否为login.html

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # 302表示请求的网页暂时跳转到其他页面， 也就是logout跳转到login页面

    def tearDown(self):
        pass

class TestModel(TestCase):  # 这部分是对models中的模型实例进行测试，包含测试创建评论，测试用户名不能重名等。

    def test_comment(self):  # 测试评论创建
        example = Comment(tool=Tool(id=1), user=User(id=1), content='good')
        self.assertEqual(example.tool.id, 1)
        self.assertEqual(example.user.id, 1)
        self.assertEqual(example.content, 'good')
        self.assertEqual(example.likes, 0)  # 测试评论点赞数的默认值是否为0

    def test_user_unique(self):  # 测试user_name的unique=True
        u1 = User(user_name='a')
        u1.save()  # 先保存一个用户名为a的用户
        with self.assertRaises(Integrity1Error):
            User.objects.create(user_name='a')  # 此时若再创建一个用户名为a的用户， 则会引发数据库的IntegrityError,
            # 表示产生了预期的错误，即用户名不能重名

    def test_tool(self):   #测试宠物用品界面
        a = Tool(name='test', info='for cat')
        self.assertEqual(a.name, 'test')
        self.assertEqual(a.info, 'for cat')
        self.assertEqual(a.views, 0)

    def test_pet(self):   # 测试宠物图鉴界面
        a = Pet(name='test', character='mild')
        self.assertEqual(a.name, 'test')
        self.assertEqual(a.character, 'mild')
        self.assertEqual(a.views, 0)





    def test_collect_pet(self):  # 测试用户收藏宠物图鉴的创建
        c = CollectPet(user=User(id=1), pet=Pet(id=1))
        self.assertEqual(c.user, User(id=1))
        self.assertEqual(c.pet, Pet(id=1))

    def test_collect_tool(self):  # 测试用户收藏宠物用品的创建
        c = CollectTool(user=User(id=1),tool=Tool(id=1))
        self.assertEqual(c.user, User(id=1))
        self.assertEqual(c.tool, Tool(id=1))


class TestViews(TestCase):  # 测试视图函数中其他函数的功能
    def setUp(self):        # 先创建相关的实例
        Tool.objects.create(id=1)
        Pet.objects.create(id=2)
        User.objects.create(id=3)
        Comment.objects.create(id=4, tool= Tool(id=1), user=User(id=3))
        User.objects.create(user_name='test', password='test')
        self.client = Client()   # 使用POST方式登录，方便之后测试的运行
        self.client.post('/meowoof/login/', {'user_name': 'test', 'password': 'test'})  # 使用post发送请求，登录一个实例用户以便测试





    def test_myself_pet_collect(self):  # 测试用于显示用户收藏的宠物图鉴的函数
        response = self.client.get('/meowoof/myself_pet_collect/')
        self.assertEqual(response.status_code, 200)  # 200表示服务器成功处理了get请求
        self.assertTemplateUsed(response, 'meowoof/myself_pet_collect.html')

    def test_myself_tool_collect(self):  # 测试用于显示用户收藏的宠物用品的函数
        response = self.client.get('/meowoof/myself_tool_collect/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meowoof/myself_tool_collect.html')

    def test_pet(self):   # 测试显示宠物图鉴的函数
        response = self.client.get('/meowoof/pet/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meowoof/pet.html')

    def test_tool(self):   # 测试显示宠物用品的函数
        response = self.client.get('/meowoof/tool/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meowoof/tool.html')

    def test_suggestion(self):   # 测试显示喂养建议的函数
        response = self.client.get('/meowoof/suggestion/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meowoof/suggestion.html')


    def test_collect_pet(self):  #  测试收藏宠物的函数

        response = self.client.get('/meowoof/collect_pet/2/')
        self.assertEqual(response.status_code, 302)




    def test_myself(self):  # 测试用户主页函数

        response = self.client.get('/meowoof/myself/')
        self.assertTemplateUsed(response, 'meowoof/myself.html')  # 测试使用的是否为对应的html文件
        self.assertEqual(response.status_code, 200)  # 200表示服务器成功处理了请求


    def test_pet_search(self):  # 测试宠物图鉴的搜索功能
        response = self.client.post('/meowoof/pet_search_result/', {'search_data': '猫'})  # 用户输入设置为‘辣’
        self.assertTemplateUsed(response, 'meowoof/pet_search_result.html')  # 是否使用了对应的html文件
        self.assertEqual(response.status_code, 200)  # 200表示服务器正确处理了post请求

    def test_tool_search(self):  # 测试宠物用品的搜索功能
        response = self.client.post('/meowoof/tool_search_result/', {'search_data': '猫爬架'})  # 用户输入设置为‘辣’
        self.assertTemplateUsed(response, 'meowoof/tool_search_result.html')  # 是否使用了对应的html文件
        self.assertEqual(response.status_code, 200)  # 200表示服务器正确处理了post请求


    def tearDown(self):
        pass

