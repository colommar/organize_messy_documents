import json
from typing import Generator


def read_and_sep(fp: str) -> Generator[list[str], None, None]:
    """
    读取文件，并将文件内容分割为多个项目。

    观察可得：每个项目开头为"打印  关闭    ENGLISH", 结尾固定为"添加笔记  调整分组..."等字样，以此为依据分割项目
    :param fp: 文件路径
    :return: 生成器，每次生成一个项目的内容，为一个列表，列表中的每个元素为项目的一行内容
    """
    item = []  # 用于存储当前项目的内容
    is_project = False  # 表示当前是否为项目内容
    with open(fp, encoding='utf-8') as f:
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
    """
    从项目内容中提取信息。
    :param text: 项目内容
    :return: 项目信息
    """

    def match_pattern(txt: str) -> str | None:
        """
        判断txt是否符合键值对的格式。
        :param txt: 项目内容中的一行
        :return: 若符合则返回None，否则返回txt.strip()
        """
        for s in ("\t", "：", ":"):
            separated = txt.split(s)
            if len(separated) == 2:
                key = separated[0].strip()
                value = separated[1].strip()
                if value != "":
                    info[key] = value
                    return None
        return txt.strip()

    info = {}  # 用于存储项目信息
    multiline_key = None  # 用于存储当前正在处理的多行键
    for line in text:
        if line.strip() == "":
            continue
        if multiline_key is None:
            multiline_key = match_pattern(line)
            if multiline_key is not None:
                info[multiline_key] = ""
        else:
            if (extra_value := match_pattern(line)) is None:
                multiline_key = None
            else:
                info[multiline_key] += extra_value
    return info


if __name__ == '__main__':
    input_file_path = 'path/to/input.txt'
    output_file_path = 'path/to/output.json'
    result = list(map(extract_info, read_and_sep(input_file_path)))
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=2)
