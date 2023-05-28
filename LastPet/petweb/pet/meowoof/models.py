from django.db import models

# Create your models here.

# 用户类
# duhao sjtusjtu 超级管理员的账号和密码
class User(models.Model):
    user_name = models.CharField(max_length=20, unique=True, verbose_name='用户名', blank=False, null=False)
    password = models.CharField(max_length=200, verbose_name='密码', null=False, blank=False)
    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='头像', blank=True, null=True,
                               default='user_avatar/default0.jpg')
    telephone = models.CharField(max_length=11, null=True, verbose_name='电话号', blank=True)
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.user_name

    class Meta:
        ordering = ['-create_time']  # 按时间递减排序
        verbose_name = "用户"
        verbose_name_plural = "用户"



class Pet(models.Model):
    name = models.CharField(max_length=30)  # 宠物名
    picture = models.ImageField(upload_to='pet_picture/', default='default_pet_picture.jpg')  # 宠物图片
    origin = models.CharField(max_length=30) # 宠物发源地
    character = models.CharField(max_length=30) # 宠物性格
    size = models.CharField(max_length=30) # 宠物体型
    info = models.CharField(max_length=2000) # 宠物详细信息

    views = models.IntegerField(default=0, verbose_name='浏览量')

    def __str__(self):  # 返回对象时显示字符串
        return self.name

    class Meta:
        ordering = ['-views']  # 按点赞数递减排序
        verbose_name = "宠物"
        verbose_name_plural = "宠物"

class Tool(models.Model):
    name = models.CharField(max_length=30)  # 宠物用品名
    picture = models.ImageField(upload_to='tool_picture/', default='default_tool_picture.jpg')  # 图片

    info = models.CharField(max_length=2000) # 宠物用品详细信息

    views = models.IntegerField(default=0, verbose_name='浏览量')

    def __str__(self):  # 返回对象时显示字符串
        return self.name

    class Meta:
        ordering = ['-views']  # 按点赞数递减排序
        verbose_name = "用品"
        verbose_name_plural = "用品"



# 这是评论类
class Comment(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)  # 每一条评论所归属的宠物用品名

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)  # 评论内容
    pub_date = models.DateField(auto_now_add=True)  # 发布日期,自动保存评论的创建日期
    pub_time = models.TimeField(auto_now_add=True)  # 发布时间，自动保存评论的创建时间
    likes = models.IntegerField(default=0)  # 评论点赞数

    def __str__(self):
        return '%s Comment:%s' % (self.tool.name, self.content)

    class Meta:
        ordering = ['-pub_date', '-pub_time']  # 按时间递减排序
        verbose_name = "评论"
        verbose_name_plural = "评论"

class Suggestion(models.Model):
    name = models.CharField(max_length=30)  # 建议标题

    info = models.CharField(max_length=2000) #建议内容

    picture = models.ImageField(upload_to='tool_picture/', default='default_tool_picture.jpg')

    views = models.IntegerField(default=0, verbose_name='浏览量')

    def __str__(self):  # 返回对象时显示字符串
        return self.name

    class Meta:
        ordering = ['-views']  # 按点赞数递减排序
        verbose_name = "建议"
        verbose_name_plural = "建议"

class CollectPet(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s收藏了宠物%s' % (self.user.user_name, self.pet.name)

class CollectTool(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s收藏了宠物用品%s' % (self.user.user_name, self.tool.name)
