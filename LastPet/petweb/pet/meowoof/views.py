from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from meowoof.models import *
from django.urls import reverse
from meowoof.forms import *

# 登录页面，已完成
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/meowoof/index/')
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        message = '亲，好像内容不太对哦~'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('user_name')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(user_name=username)
            except:
                message = '亲，小生没有查到您的账户哦(⊙o⊙)'
                return render(request, 'meowoof/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                return redirect('/meowoof/index/')
            else:
                message = '亲，密码好像不对哦~'
                return render(request, 'meowoof/login.html', locals())
        else:
            return render(request, 'meowoof/login.html', locals())
    login_form = UserLoginForm()

    return render(request, 'meowoof/login.html', locals())


# 账户注册页面,已完成
def register(request):
    if request.session.get('is_login', None):
        return redirect('/meowoof/index/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('user_name')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')


            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'meowoof/register.html', locals())
            else:
                same_name_user = User.objects.filter(user_name=user_name)
                if same_name_user:
                    message = '该用户名已经存在'
                    return render(request, 'meowoof/register.html', locals())

                User.objects.create(user_name=user_name, password=password1)
                return redirect('/meowoof/login/')
        else:
            return render(request, 'meowoof/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'meowoof/register.html', locals())


# 退出登录，已完成
def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("/meowoof/login/")
    request.session.flush()
    return redirect("/meowoof/login/")


def index(request):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meowoof/login/')
    else:
        most_views_pet = Pet.objects.filter().order_by("-views")  # 按点赞数降序排列
        most_viwes_tool = Tool.objects.filter().order_by("-views")
        content = {'pet1': most_views_pet[0], 'pet2':  most_views_pet[1], 'pet3':  most_views_pet[2],
                   'tool1': most_viwes_tool[0], 'tool2': most_viwes_tool[1], 'tool3': most_viwes_tool[2]}
        return render(request, 'meowoof/index.html', content)


def pet_detail(request, pet_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meowoof/login/')

    pet = Pet.objects.get(id=pet_id)
    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id


    if request.method == 'GET':  # get请求让浏览量加一
        pet.views += 1
        pet.save()




    if CollectPet.objects.filter(user=user, pet=pet):
        collect = True
    else:
        collect = False

    content = {'pet': pet, 'collect': collect}
    return render(request, 'meowoof/pet_detail.html', content)


def tool_detail(request, tool_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meowoof/login/')

    tool = Tool.objects.get(id=tool_id)
    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    symbol = True
    if request.method == 'POST':  # post请求提交评论
        comment_content = request.POST.get('message')  # 获取前端输入内容
        if comment_content:
            Comment.objects.create(user=user, tool=tool, content=comment_content)
        else:
            symbol = False
    # 创建评论
    if request.method == 'GET':  # get请求让浏览量加一
        tool.views += 1
        tool.save()
    comments = Comment.objects.filter(tool=tool)

    current_user_like_comment_list = []  # 此列表将保存当前用户点过赞的评论的id
    for com in comments:
        current_comment = Comment.objects.filter(comment=com)
        for cc in current_comment:
            if cc.user == user:
                current_user_like_comment_list.append(com.id)



    if CollectTool.objects.filter(user=user, tool=tool):
        collect = True
    else:
        collect = False

    content = {'tool': tool, 'comments': comments, 'collect': collect, 'current_user_like_comment_list': current_user_like_comment_list, 'symbol': symbol}
    return render(request, 'meowoof/tool_detail.html', content)

def pet(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')
    all_pets = Pet.objects.filter().order_by("-views")
    return render(request, 'meowoof/pet.html', {'all_pets': all_pets})

def tool(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')
    all_tools = Tool.objects.filter().order_by("-views")
    return render(request, 'meowoof/tool.html', {'all_tools': all_tools})

def suggestion(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')
    all_suggestion = Suggestion.objects.filter().order_by("-views")
    return render(request, 'meowoof/suggestion.html',{'all_suggestion':all_suggestion})


def pet_search_result(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    if request.method == 'POST':
        search_text = request.POST.get('search_data')  # 从前端传入了字符串，没有使用表单
        search_text_len = len(search_text)
        if search_text_len == 0 :
            content = {'pet_search__result': []}
            return render(request, 'meowoof/pet_search_result.html', content)
        i=0
        search_result_list = [] #该列表用以储存单个字搜索的结果
        search_result_list_len = [] #该列表用以储存每个字搜索出的结果的数量
        while i<search_text_len :
            search_result_list.append(Pet.objects.filter(name__contains=search_text[i]))
            search_result_list_len.append(len(search_result_list[i]))
            i = i+1
        i=1
        search_result_list_final = [] #该列表用以进行链式搜索
        search_result_list_max = max(search_result_list_len)
        search_text_i = search_result_list_len.index(search_result_list_max)
        search_result_list_final.append(Pet.objects.filter(name__contains=search_text[search_text_i]))
        search_result_list_len[search_text_i] = 0
        #先获取单字搜索【结果数量最多】的字的下标，再对该下标对应的原字符串中的字进行filter，而后将该下标对应的搜索结果数量置0，标记为已搜索
        while i<search_text_len :
            search_result_list_max = max(search_result_list_len)
            if search_result_list_max == 0:
                break
            #该if语句为避免重复对已置0，即标记为已搜索字再次搜索
            search_text_i = search_result_list_len.index(search_result_list_max)
            if len(search_result_list_final[i - 1].filter(name__contains=search_text[search_text_i])) == 0:
                break
            #该if语句为当链式搜索中途无搜索结果时结束循环
            search_result_list_final.append(search_result_list_final[i-1].filter(name__contains=search_text[search_text_i]))
            i = i+1
        search__result = search_result_list_final[i-1] #获取链式搜索最终结果
        content = {'pet_search__result': search__result}

        return render(request, 'meowoof/pet_search_result.html', content)
    else:
        return render(request, 'meowoof/pet.html')

def tool_search_result(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    if request.method == 'POST':
        search_text = request.POST.get('search_data')  # 从前端传入了字符串，没有使用表单
        search_text_len = len(search_text)
        if search_text_len == 0 :
            content = {'tool_search__result': []}
            return render(request, 'meowoof/tool_search_result.html', content)
        i=0
        search_result_list = [] #该列表用以储存单个字搜索的结果
        search_result_list_len = [] #该列表用以储存每个字搜索出的结果的数量
        while i<search_text_len :
            search_result_list.append(Tool.objects.filter(name__contains=search_text[i]))
            search_result_list_len.append(len(search_result_list[i]))
            i = i+1
        i=1 #链式搜索第一步较特殊，需从Meal里filter，故单独写第一步
        search_result_list_final = [] #该列表用以进行链式搜索
        search_result_list_max = max(search_result_list_len)
        search_text_i = search_result_list_len.index(search_result_list_max)
        search_result_list_final.append(Tool.objects.filter(name__contains=search_text[search_text_i]))
        search_result_list_len[search_text_i] = 0
        #先获取单字搜索【结果数量最多】的字的下标，再对该下标对应的原字符串中的字进行filter，而后将该下标对应的搜索结果数量置0，标记为已搜索
        while i<search_text_len :
            search_result_list_max = max(search_result_list_len)
            if search_result_list_max == 0:
                break
            #该if语句为避免重复对已置0，即标记为已搜索字再次搜索
            search_text_i = search_result_list_len.index(search_result_list_max)
            if len(search_result_list_final[i - 1].filter(name__contains=search_text[search_text_i])) == 0:
                break
            #该if语句为当链式搜索中途无搜索结果时结束循环
            search_result_list_final.append(search_result_list_final[i-1].filter(name__contains=search_text[search_text_i]))
            i = i+1
        search__result = search_result_list_final[i-1] #获取链式搜索最终结果
        content = {'tool_search__result': search__result}

        return render(request, 'meowoof/tool_search_result.html', content)
    else:
        return render(request, 'meowoof/tool.html')

def myself(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    collected_pets = CollectPet.objects.filter(user=user)  # 某用户收藏的集合
    collected_tools = CollectTool.objects.filter(user=user)
    content = {'user': user, 'collect_pets': collected_pets, 'collect_tools': collected_tools}
    return render(request, 'meowoof/myself.html', content)

def myself_pet_collect(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    collected_pets = CollectPet.objects.filter(user=user)  # 某用户收藏集合
    content = {'user': user, 'collect_pets': collected_pets}
    return render(request, 'meowoof/myself_pet_collect.html', content)

def myself_tool_collect(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    collected_tools = CollectTool.objects.filter(user=user)  # 某用户收藏集合
    content = {'user': user, 'collect_tools': collected_tools}
    return render(request, 'meowoof/myself_tool_collect.html', content)

# 更新文章
def modify_myself(request):

    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')
    # 获取需要修改的具体对象
    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        modify_form =ModifyMyselfForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if modify_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            user.user_name = request.POST['user_name']
            user.password = request.POST['password']
            user.email = request.POST['email']
            user.telephone = request.POST['telephone']
            user.avatar = request.POST['avatar']
            user.save()

            return redirect('/meowoof/myself/')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        modify_form = ModifyMyselfForm()

        context = { 'user': user, 'modify_form':  modify_form }
        # 将响应返回到模板中
        return render(request, 'meowoof/modify_myself.html', context)

def collect_pet(request, pet_id):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        pet = Pet.objects.get(id=pet_id)
        collect_record = CollectPet.objects.filter(user=user, pet=pet)
        if collect_record:
            collect_record = CollectPet.objects.get(user=user, pet=pet)
            collect_record.delete()
        else:
            CollectPet.objects.create(user=user, pet=pet)
    return redirect('meowoof:pet_detail', pet_id=pet_id)

def collect_tool(request, tool_id):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        tool = Tool.objects.get(id=tool_id)
        collect_record = CollectPet.objects.filter(user=user, tool=tool)
        if collect_record:
            collect_record = CollectPet.objects.get(user=user, tool=tool)
            collect_record.delete()
        else:
            CollectPet.objects.create(user=user, tool=tool)
    return redirect('meowoof:tool_detail', tool_id=tool_id)

def like_comment(request, comment_id):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meowoof/login/')

    user = User.objects.get(id=request.session['user_id'])
    comment = Comment.objects.get(id=comment_id)
    tool_id = comment.tool.id
    if request.method == 'GET':
        like_record = Comment.objects.filter(user=user, comment=comment)
        if like_record:
            like_record = Comment.objects.get(user=user, comment=comment)
            like_record.delete()
            comment.likes -= 1
            comment.save()
        else:
            Comment.objects.create(user=user, comment=comment)
            comment.likes += 1
            comment.save()
    return redirect('meowoof:tool_detail', tool_id=tool_id)
