from opencc import OpenCC


def convert_traditional_to_simplified(traditional_text):
    # 创建一个转换器实例，用于繁体转简体
    cc = OpenCC('t2s')  

    # 执行转换
    simplified_text = cc.convert(traditional_text)
    
    return simplified_text

