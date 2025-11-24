# 分支——经验版本

这是一个想要尝试的分支版本，我将加入一个经验值系统。

1. 首先是定义数据库表：

```postgresql
create table dish_history(
id bigint,
    dish_id bigint,
    cooking_time date,
    cooking_rating smallint (1很棒 2还行 3一般 4拉胯),
    create_time date,
    modify_time date
)
```

2. 在菜品详情页下方的tab增加一个“历史记录”tab，里边用时间线形式展示这个菜的烹饪历史，就是查新建的表
3. 在时间线上方有几个按钮，分别对应了cooking_rating的枚举值，点击按钮时，有一个确认框，然后会写一条对应数据到表里
4. 菜品详情页，制作难度下面加一栏“烹饪次数”，用dish_id去新表中count