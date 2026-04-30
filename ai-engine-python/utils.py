import re
import time
from config import LOG_FILE


def write_log(action: str, detail: str):
    """写入格式化操作日志"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"- `{timestamp}` **[{action}]** : {detail}\n")
    print(f"📝 [Log] {action}: {detail}")


def format_references(ref_text: str):
    """🌟 加强版：清理并格式化参考文献，精准处理断字与序号"""
    if not ref_text: return ""

    # 1. 剔除原本由于正则截取带来的冗余 "References" 标题文字
    ref_text = re.sub(r'^\s*(References|REFERENCES|Bibliography|BIBLIOGRAPHY|参考文献)\s*\n?', '', ref_text,
                      flags=re.IGNORECASE)

    # 2. 🌟 修复断字问题：识别 "单词末尾的连字符 + 换行"，直接拼接 (如 inter-\nface -> interface)
    ref_text = re.sub(r'-\n\s*', '', ref_text)

    # 3. 将其余剩余的换行符替换为空格，把支离破碎的段落压成一整行
    flat_text = ref_text.replace('\n', ' ')
    flat_text = re.sub(r'\s+', ' ', flat_text)  # 顺手清除多余的连续空格

    # 4. 🌟 精准切分：只匹配 [1] 或者 1. (限制1-3位数字，完美避开 2004.)
    # (?:^|\s) 确保匹配的是段落开头或者前面有空格的序号
    formatted = re.sub(r'(?:^|\s)(\[\d+\]|\d{1,3}\.)\s', r'\n\n\1 ', flat_text)

    return formatted.strip()


def clean_and_split_paper(text: str):
    """智能清洗：剔除目录，分离参考文献"""
    main_body = text
    references_text = ""

    ref_patterns = [r'\nReferences\s*\n', r'\nREFERENCES\s*\n', r'\nBibliography\s*\n', r'\n参考文献\s*\n']
    for pattern in ref_patterns:
        matches = list(re.finditer(pattern, main_body))
        if matches:
            last_match = matches[-1]
            references_text = main_body[last_match.start():]
            main_body = main_body[:last_match.start()]
            break

    toc_match = re.search(r'(Table of Contents|TABLE OF CONTENTS|Contents|CONTENTS|目录)\s*\n', main_body[:5000])
    intro_match = re.search(r'\n(1\.?\s*Introduction|INTRODUCTION|引言)\s*\n', main_body[:10000])
    if toc_match and intro_match and toc_match.start() < intro_match.start():
        main_body = main_body[intro_match.start():]

    return main_body, references_text