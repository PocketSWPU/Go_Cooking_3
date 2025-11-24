# GoCooking 3

## 项目描述

这是一个面向烹饪新手的厨房应用，主要功能包括记录菜品的原材料、切配时间、烹饪方法等。

技术架构：后端使用python，用fastAPI提供接口，前端使用vue 3 + Element Plus，前后端分别部署，数据库使用postgreSQL

遵循**RESTful**

表结构都要有默认值，integer = 0；numerric = 0.00; text = ""; date,time,timestamp = currenttime()，并且每个表都额外加上create_time和modify_time，都是timestamp类型，默认当前，且modify_time随修改更新

## 功能详情

### 主页板块

用分页+卡片形式展示菜品，只需要菜品名和一些关键标签，不需要图片，点击菜品后出现详情。

查询提供一些筛选项，比如菜名模糊查询



**接口**

```text
1、菜品查询接口
/cooking/ver3/dish/select
入参:
{
	"page": 0,
	"size": 10,
	"dishName": ""
}

出参:
{
	"code": 0,
	"data": [
		// 菜品信息，根据数据库结构决定
	]
}

2、菜品详情接口
/cooking/ver3/dish/detail/{id}
出参:
{
	"code": 0,
	"data": {
		// ...
	}
}

3、菜品新增接口
/cooking/ver3/dish/add/raw
在这个接口中，需要接收的一个新建的菜品，其中包含菜品的主料，辅料和配料，并且写入ingredient表，在插入这个表的时候应该先查询一下有没有相同的名字，一个名字在数据库里只需要一个，所以你需要一个mapping关系表来映射菜品和配料。
此外，还需要加入烹饪的步骤，步骤step_order是步骤的顺序，然后dish_id关联了菜品
```



**表结构**

```
1、dish
id primarykey bigint
dish_name text
difficult smallint 1简单 2中等 3复杂

2、ingredient
id primarykey bigint
ingredient_name text
type smallint 1主料 2辅料 3调料


3、dish_step
id primarykey bigint
dish_id bigint
step_order int
step_text text

4、dish_ingredients
dish_id bigint
ingredient_id bigint
usage text
```

