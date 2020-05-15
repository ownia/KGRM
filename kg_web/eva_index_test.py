import re

entity_list = []
eva_list2 = ['奥维云网', 'AVC', '海尔', '奥克斯', '格力', '美的']
eva_text = "根据奥维云网（AVC）推总数据显示，2018年6月空调零售额规模为331.5亿元，海尔BCD476FDGJds是谁的," \
           "同比增长19.5%，零售量规模为1004.4万套，同比增长13.7%。其中线上市场top品牌格局出现分化，奥克斯占比大幅度提升，零售额占比达到28.9%，领先第二名品牌7.1" \
           "%；而线下市场品牌格局依然稳定，格力、美的的份额继续提升，挤压二线品牌的生存空间。 "
for i in eva_list2:
    # eva_pattern = re.compile(str(i) + r'[a-zA-Z0-9-_]+')
    eva_pattern = re.compile(str(i) + r'[a-zA-Z0-9-_]+')
    eva_target = eva_pattern.findall(eva_text)
    # print(eva_target)
    if len(eva_target) > 0:
        entity_list.append(eva_target)
print(entity_list)
