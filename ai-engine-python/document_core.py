import os
import json
import re
import shutil
import traceback
import fitz
import base64
from config import WIKI_DIR, INDEX_FILE, PDF_LIBRARY_DIR, CATALOG_FILE, LLM_MODEL_NAME
from utils import write_log, clean_and_split_paper, format_references
from ai_client import client

IMAGE_DIR = os.path.join(WIKI_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)


def load_catalog() -> dict:
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_to_catalog(filename: str, category: str, summary: str, file_path: str):
    catalog = load_catalog()
    catalog[filename] = {"category": category, "summary": summary, "path": file_path}
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)


def extract_and_analyze_images(pdf_path: str, md_filename: str):
    """视觉提取引擎 (已包含上一轮优化的 IGNORE 拦截逻辑)"""
    try:
        doc = fitz.open(pdf_path)
        appended_md = "\n\n---\n## 🖼️ 文献核心图表与视觉特征\n\n"
        image_count = 0
        valid_image_count = 0

        print(f"👁️ [Vision] 开始智能扫描并过滤文献图片: {md_filename}")

        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            page_text = page.get_text("text").strip()
            context_text = page_text[:1500] if page_text else "本页无文字信息"

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                if len(image_bytes) < 15360:
                    continue

                image_count += 1
                img_name = f"{md_filename.replace('.md', '')}_p{page_num + 1}_{image_count}.{image_ext}"
                img_path = os.path.join(IMAGE_DIR, img_name)

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                print(f"🔍 [Vision] 正在鉴定第 {page_num + 1} 页的图片 {image_count}...")

                sys_prompt = "你是一个学术论文解析专家。结合当前页文字，判断图片是否是正文核心配图。如果是废图/Logo/装饰，请仅回复 IGNORE。如果是正规配图，请结合上下文用一段精炼的中文（约100-200字）总结核心内容，不要分点列举。"
                user_prompt = f"【当前页文本上下文】:\n{context_text}\n\n判断并总结："

                vision_response = client.chat.completions.create(
                    model="qwen-vl-plus",
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": [{"type": "text", "text": user_prompt}, {"type": "image_url",
                                                                                             "image_url": {
                                                                                                 "url": f"data:image/{image_ext};base64,{base64_image}"}}]}
                    ]
                )

                img_description = vision_response.choices[0].message.content.strip()

                if "IGNORE" in img_description.upper() or len(img_description) < 10:
                    if os.path.exists(img_path): os.remove(img_path)
                    continue

                valid_image_count += 1
                img_url = f"http://localhost:8000/api/wiki/images/{img_name}"
                appended_md += f"### 图表 (提取自第 {page_num + 1} 页)\n![文献插图]({img_url})\n\n**🤖 上下文视觉解析：**\n{img_description}\n\n"

        if valid_image_count > 0:
            md_path = os.path.join(WIKI_DIR, md_filename)
            with open(md_path, "a", encoding="utf-8") as f:
                f.write(appended_md)
            print(f"✅ [Vision] 共过滤并解析出 {valid_image_count} 张核心图表！")

    except Exception as e:
        print(f"❌ [Vision] 图片解析出错: {e}")


def background_ingest_task(filename: str, raw_text: str, options: str, temp_pdf_path: str):
    """文献入库与解析流水线"""
    try:
        write_log("ASYNC_START", f"开始高精度处理并智能路由: {filename}")
        main_body, references_text = clean_and_split_paper(raw_text)

        # 智能分类
        category_prompt = f"给出一个精准的中文分类标签（2-6个字）：\n{main_body[:1500]}"
        category = client.chat.completions.create(model=LLM_MODEL_NAME,
                                                  messages=[{"role": "user", "content": category_prompt}]).choices[
            0].message.content.strip().replace(" ", "_")

        # 移动文件
        category_dir = os.path.join(PDF_LIBRARY_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        final_pdf_path = os.path.join(category_dir, filename)
        if os.path.exists(final_pdf_path): os.remove(final_pdf_path)
        shutil.move(temp_pdf_path, final_pdf_path)

        # 提取特征
        structured_prompt = f"提取元数据、摘要翻译、特征项：{options}\n\n正文：\n{main_body[:6000]}"
        response = client.chat.completions.create(model=LLM_MODEL_NAME,
                                                  messages=[{"role": "user", "content": structured_prompt}])
        final_markdown = response.choices[0].message.content
        final_markdown = re.sub(r'##\s*(📚\s*)?(参考文献|References).*', '', final_markdown,
                                flags=re.IGNORECASE | re.DOTALL).strip()

        if references_text:
            final_markdown += "\n\n## 📚 参考文献 (References)\n\n" + format_references(references_text)

        # 摘要与记账
        summary = client.chat.completions.create(model=LLM_MODEL_NAME, messages=[
            {"role": "user", "content": f"一句话总结：\n{final_markdown[:1000]}"}]).choices[0].message.content.strip()
        save_to_catalog(filename, category, summary, final_pdf_path)

        # 写入 MD 纯文本
        md_filename = filename.replace(".pdf", ".md")
        with open(os.path.join(WIKI_DIR, md_filename), "w", encoding="utf-8") as f:
            f.write(final_markdown)

        # 🌟 调用视觉引擎追加图片
        extract_and_analyze_images(final_pdf_path, md_filename)

        # 更新索引
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                for line in lines:
                    if md_filename not in line: f.write(line)
        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"- [{md_filename}](./{md_filename}) | 分类: {category} | 摘要: {summary}\n")

        write_log("ASYNC_SUCCESS", f"✅ {filename} 解析完成！")
    except Exception as e:
        traceback.print_exc()
        write_log("ASYNC_ERROR", f"❌ 任务失败: {str(e)}")