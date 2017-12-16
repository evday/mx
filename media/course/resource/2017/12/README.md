## rbac权限管理大致流程

day1

	a: rbac/model.py 创建表(三个类，五张表)

	b: 基于django admin后台录入数据

	c: 用户登录程序：

		init_permission.py 获取用户权限，写入session

	d : 中间件

		设置白名单

		获取当前url与session中用户权限比较

day2

  	问题：页面是否显示添加，删除，修改等按钮

	a: 修改表结构，permission表中增加一列code,创建 group 表
	
	b: 生成数据结构id{code["list","add","edit","delete"],urls[/userinfo/,/userinfo/add/,/userinfo/edit/(\d+),/userinfo/delete/(\d+)]}

		将code 写入 request中 以此来解决是否显示添加，删除，修改等按钮
day3

	菜单展示，以及默认选中

	a:修改表结构，新增menu表，以及permission表中的自关联字段menu_gp
	
	b:构造数据结构
		init_permission 中获取相关数据
		
		新增自定义标签templatetags,使用inclusion_tags（base_sidbar.html)，先构建menu_dict，再根据menu_dict构建result,将result数据渲染到base_sidbar.html中
		
	c:配置base.html，{% load rbac %} {% menu_html %} 将自定义标签加入到base.html中
	
	d:继承模板base.html

## 简单的权限管理开发完毕
