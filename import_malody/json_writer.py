import json


def write_json(project_data: dict, json_path: str) -> None:
    """
    将谱面数据写入 json 项目文件。
    """

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f)
