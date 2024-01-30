import re

# 从文件中读取内容
def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# 将内容写入文件
def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# 输入文件路径
input_file_path = 'C:\\Users\\114514\\PycharmProjects\\pythonProject3\\1.txt'

# 输出文件路径
output_file_path = 'C:\\Users\\114514\\PycharmProjects\\pythonProject3\\output.txt'

# 读取内容
text = read_from_file(input_file_path)

def extract_info(text):
    if(text == '\\n'):
        return {
            "项目名称": None,
            "地址": None,
            "外资参与": None,
            "项目描述": None,
            "项目时间": None,
            "项目更新": None,
            "甲方": None,
            "设计": None,
            "承建商": None
        }

    party_flag ,desgin_flag , contractor_flag = True, True, True

    if "甲方" in text: party_flag = True
    else: party_flag = False

    if "设计" in text: desgin_flag = True
    else: desgin_flag = False

    if "承建商" in text: contractor_flag = True
    else: contractor_flag = False

    party,design,contractor = None, None, None
    # 提取项目名称
    name_pattern = r"ENGLISH\n\s*(.*?)\n"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1).strip() if name_match else None

    # 提取地址
    address_pattern = r'地址\s*(.*?)地图'
    address_match = re.search(address_pattern, text)
    address = address_match.group(1).strip() if address_match else None

    # 提取外资参与
    foreign_pattern = r'外资参与\s*(.*?)\n'
    foreign_match = re.search(foreign_pattern, text)
    foreign = foreign_match.group(1).strip() if foreign_match else None

    # 提取项目描述
    description_pattern = r'项目描述\s*\n(.*?)\n'
    description_match = re.search(description_pattern, text, re.DOTALL)
    description = description_match.group(1).strip() if description_match else None

    # 提取开工时间和竣工时间
    start_time_pattern = r'开工时间：(.*?)\n'
    end_time_pattern = r'竣工时间：(.*?)\n'
    start_time_match = re.search(start_time_pattern, text)
    end_time_match = re.search(end_time_pattern, text)
    start_time = start_time_match.group(1).strip() if start_time_match else '未知'
    end_time = end_time_match.group(1).strip() if end_time_match else '未知'
    timeofitem = "开工时间：" + start_time + ",竣工时间：" + end_time

    # 提取项目更新
    if party_flag:
        update_pattern = r'项目更新\n(.*?)\n甲方\n'
        update_match = re.search(update_pattern, text, re.DOTALL)
        update = update_match.group(1).strip() if update_match else None
    elif desgin_flag:
        # 提取项目更新
        update_pattern = r'项目更新\n(.*?)\n设计\n'
        update_match = re.search(update_pattern, text, re.DOTALL)
        update = update_match.group(1).strip() if update_match else None
    elif contractor_flag:
        # 提取项目更新
        update_pattern = r'项目更新\n(.*?)\n承建商\n'
        update_match = re.search(update_pattern, text, re.DOTALL)
        update = update_match.group(1).strip() if update_match else None
    else:
        # 提取项目更新
        update_pattern = r'项目更新\n(.*?)\n添加笔记\n'
        update_match = re.search(update_pattern, text, re.DOTALL)
        update = update_match.group(1).strip() if update_match else None


    # 甲方，设计，承建商排列组合
    if party_flag and desgin_flag and contractor_flag:
        # 提取甲方
        party_pattern = r'甲方\n(.*?)\n设计\n'
        party_match = re.search(party_pattern, text, re.DOTALL)
        party = party_match.group(1).strip() if party_match else None

        # 提取设计
        design_pattern = r'设计\n(.*?)\n承建商\n'
        design_match = re.search(design_pattern, text, re.DOTALL)
        design = design_match.group(1).strip() if design_match else None

        # 提取承建商
        contractor_pattern = r'承建商\n(.*?)\n添加笔记'
        contractor_match = re.search(contractor_pattern, text, re.DOTALL)
        contractor = contractor_match.group(1).strip() if contractor_match else None

    elif party_flag and desgin_flag and not contractor_flag:
        # 提取甲方
        party_pattern = r'甲方\n(.*?)\n设计\n'
        party_match = re.search(party_pattern, text, re.DOTALL)
        party = party_match.group(1).strip() if party_match else None

        # 提取设计
        design_pattern = r'设计\n(.*?)\添加笔记'
        design_match = re.search(design_pattern, text, re.DOTALL)
        design = design_match.group(1).strip() if design_match else None

    elif party_flag and not desgin_flag and contractor_flag:
        # 提取甲方
        party_pattern = r'甲方\n(.*?)\n承建商\n'
        party_match = re.search(party_pattern, text, re.DOTALL)
        party = party_match.group(1).strip() if party_match else None

        # 提取承建商
        contractor_pattern = r'承建商\n(.*?)\n添加笔记'
        contractor_match = re.search(contractor_pattern, text, re.DOTALL)
        contractor = contractor_match.group(1).strip() if contractor_match else None

    elif not party_flag and desgin_flag and contractor_flag:

        # 提取设计
        design_pattern = r'设计\n(.*?)\n承建商\n'
        design_match = re.search(design_pattern, text, re.DOTALL)
        design = design_match.group(1).strip() if design_match else None

        # 提取承建商
        contractor_pattern = r'承建商\n(.*?)\n添加笔记'
        contractor_match = re.search(contractor_pattern, text, re.DOTALL)
        contractor = contractor_match.group(1).strip() if contractor_match else None

    elif not party_flag and not desgin_flag and contractor_flag:
        # 提取承建商
        contractor_pattern = r'承建商\n(.*?)\n添加笔记'
        contractor_match = re.search(contractor_pattern, text, re.DOTALL)
        contractor = contractor_match.group(1).strip() if contractor_match else None

    elif not party_flag and desgin_flag and not contractor_flag :
        # 提取设计
        design_pattern = r'设计\n(.*?)\n添加笔记'
        design_match = re.search(design_pattern, text, re.DOTALL)
        design = design_match.group(1).strip() if design_match else None

    elif party_flag and not desgin_flag and not contractor_flag:
        # 提取甲方
        party_pattern = r'甲方\s*\n(.*?)\n添加笔记'
        party_match = re.search(party_pattern, text, re.DOTALL)
        party = party_match.group(1).strip() if party_match else None

    return {
        "项目名称": name,
        "地址": address,
        "外资参与": foreign,
        "项目描述": description,
        "项目时间": timeofitem,
        "项目更新": update,
        "甲方": party,
        "设计": design,
        "承建商": contractor
    }


def extract_multiple_blocks(text):
    # 分块
    blocks = re.split(r'打印  关闭', text)
    infos = []
    for block in blocks:
        # 对每个文本块提取信息
        info = extract_info(block)
        infos.append(info)
    return infos

# 提取多个文本块的信息
infos = extract_multiple_blocks(text)

# 准备要写入文件的内容
output_content = ""
for i, info in enumerate(infos, start=1):
    output_content += f"项目{i}：\n\n"
    output_content += f"项目名称：{info['项目名称']} \n\n"
    output_content += f"地址：{info['地址']} \n\n"
    output_content += f"外资参与：{info['外资参与']} \n\n"
    output_content += f"项目描述：{info['项目描述']} \n\n"
    output_content += f"项目时间：{info['项目时间']} \n\n"
    output_content += f"项目更新：{info['项目更新']} \n\n"
    output_content += f"甲方：{info['甲方']} \n\n"
    output_content += f"设计：{info['设计']} \n\n"
    output_content += f"承建商：{info['承建商']} \n\n"
    output_content += "\n\n\n"

# 将提取的信息写入新的文件
write_to_file(output_file_path, output_content)
