import json
from typing import Generator
import re

def read_and_sep(fp: str) -> Generator[list[str], None, None]:
    """
    读取文件，并将文件内容分割为多个项目。

    观察可得：每个项目开头为"打印  关闭    ENGLISH", 结尾固定为"添加笔记  调整分组..."等字样，以此为依据分割项目
    :param fp: 文件路径
    :return: 生成器，每次生成一个项目的内容，为一个列表，列表中的每个元素为项目的一行内容
    """
    item = []  # 用于存储当前项目的内容
    is_project = False  # 表示当前是否为项目内容
    with open(fp, encoding='GBK') as f:
        for line in f:
            line = line.strip()
            if is_project:
                if line.startswith("添加笔记"):  # 来到项目结尾
                    yield item  # 返回上一个项目的内容
                    item.clear()  # 清空item的内容
                    is_project = line.endswith("ENGLISH")  # 检查是否已经读到了下一个项目的开头
                else:
                    item.append(line.strip())
            elif line.endswith("ENGLISH"):  # 来到项目开头
                is_project = True


def extract_info(text: list[str]) -> dict[str, str]:
    def match_pattern(txt: str) -> tuple[str, str | None]:
        for s in ("\t", "：", ":"):
            separated = txt.split(s)
            if len(separated) == 2:
                key = separated[0].strip()
                value = separated[1].strip()
                return key, value
        return txt.strip(), None

    def get_unique_key(base_key: str) -> str:
        suffix = 1
        new_key = f"{base_key}_{suffix}"
        while new_key in info:
            suffix += 1
            new_key = f"{base_key}_{suffix}"
        return new_key

    info = {}
    multiline_key = None
    for line in text:
        line = line.strip()
        if line == "":
            continue
        key, value = match_pattern(line)
        if multiline_key is not None:
            if key == multiline_key and value is None:
                continue
            else:
                multiline_key = None

        if value is not None:
            if key in info:
                key = get_unique_key(key)
            info[key] = value
        else:
            multiline_key = key
            if multiline_key in info:
                multiline_key = get_unique_key(multiline_key)
            info[multiline_key] = ""

    return info




if __name__ == '__main__':
    input_file_path = 'C:\\Users\\114514\\PycharmProjects\\pythonProject3\\1.txt'
    output_file_path = 'C:\\Users\\114514\\PycharmProjects\\pythonProject3\\output.json'
    result = list(map(extract_info, read_and_sep(input_file_path)))

    new_result = []
    for project in result:
        new_project = {}
        for key, value in project.items():
            new_project[key] = value
            if key == "ProjectMaterial":
                for term in ["甲方", "设计", "承建商"]:
                    if value.endswith(term):
                        new_project[key] = value[:-len(term)].strip()
                        new_project[term] = ""
        new_result.append(new_project)

    with open(output_file_path, 'w', encoding='GBK') as output_file:
        json.dump(new_result, output_file, ensure_ascii=False, indent=2)

