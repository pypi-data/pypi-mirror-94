# -*- coding:utf-8 -*-
# @Time: 2021/1/25 18:16
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: pm_client.py
import json
from typing import Any, Dict

from pyminer_comm.base import get, dict_to_b64, b64_to_dict, DataDesc, get_protocol


class SetDataDescError(Exception):
    pass


def modify_settings(items: Dict[str, Any]):
    """
    修改设置
    :param items:
    :return:
    """
    assert isinstance(items, dict), items
    res = get('modify_settings', dict_to_b64(items, protocol=get_protocol()), 12306, )


def set_data_desc_dic(data: Dict[str, Any]) -> None:
    for k, v in data.items():
        assert isinstance(v, DataDesc)
    res = get('set_data', dict_to_b64(data, protocol=get_protocol()), 12306)
    res_json = json.loads(res)
    if res_json['status'] == "failed":
        raise SetDataDescError(res_json['error'])


def get_settings() -> Dict[str, Any]:
    res = get('get_settings', '', 12306)
    return json.loads(res)


def get_style_sheet() -> str:
    res = get('get_stylesheet', '', 12306)
    return res.decode('utf-8', errors='replace')


def call_interface(interface: str, method: str, kwargs: dict) -> str:
    res = get('interface_call',
              dict_to_b64({'interface': interface, 'method': method, 'kwargs': kwargs}, protocol=get_protocol()), 12306)
    return res


def run_command(command: str, hint_text: str = '', hidden: bool = False):
    return call_interface('ipython_console', 'run_command',
                          {'hidden': hidden, 'command': command, 'hint_text': hint_text})


def test():
    res = get('test', '', 12306)
    print(res)


if __name__ == "__main__":
    set_data_desc_dic({'a': DataDesc(123)})
    try:
        set_data_desc_dic({'a': 123})
    except BaseException:
        import traceback

        traceback.print_exc()
    print(get_settings())
    print(get_style_sheet())
    print(run_command('a=1+2+5'))
