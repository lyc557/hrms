from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
from docx import Document
import numpy as np
from sentence_transformers import SentenceTransformer
import re

def extract_name(text):
    """从简历文本中提取姓名"""
    # 假设姓名在第一行
    first_line = text.split('\n')[0].strip()
    # 简单中文姓名匹配
    name_pattern = re.compile(r'[\u4e00-\u9fa5]{2,4}')
    match = name_pattern.search(first_line)
    return match.group(0) if match else ''

def extract_education(text):
    """从简历文本中提取教育背景"""
    # 匹配教育背景相关关键词
    edu_keywords = ['教育背景', '学历', '教育经历', '学校', '大学', '学院']
    for keyword in edu_keywords:
        if keyword in text:
            start = text.find(keyword)
            end = text.find('\n\n', start)  # 假设教育背景以双换行结束
            return text[start:end] if end != -1 else text[start:]
    return ''

def extract_experience(text):
    """从简历文本中提取工作经验"""
    # 匹配工作经验相关关键词
    exp_keywords = ['工作经历', '工作经验', '工作背景', '职业经历']
    for keyword in exp_keywords:
        if keyword in text:
            start = text.find(keyword)
            end = text.find('\n\n', start)  # 假设工作经验以双换行结束
            return text[start:end] if end != -1 else text[start:]
    return ''

def extract_skills(text):
    """从简历文本中提取技能"""
    # 匹配技能相关关键词
    skill_keywords = ['技能', '专业技能', '技术能力', '能力']
    skills = []
    for keyword in skill_keywords:
        if keyword in text:
            start = text.find(keyword)
            end = text.find('\n\n', start)
            skill_section = text[start:end] if end != -1 else text[start:]
            # 提取技能项
            skill_items = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', skill_section)
            skills.extend(item for item in skill_items if len(item) > 1)
    return list(set(skills))  # 去重

app = Flask(__name__)
CORS(app)

# 初始化模型
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def parse_pdf(file_path):
    """解析PDF简历并提取关键字段"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    # 提取关键字段
    result = {
        'raw_text': text,
        'name': extract_name(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
        'skills': extract_skills(text)
    }
    return result

def parse_docx(file_path):
    """解析DOCX简历并提取关键字段"""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    
    # 提取关键字段
    result = {
        'raw_text': text,
        'name': extract_name(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
        'skills': extract_skills(text)
    }
    return result

@app.route('/analyze', methods=['POST'])
def analyze():
    """处理简历分析请求"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400
    
    resume_file = request.files['resume']
    jd_text = request.form.get('jd', '')
    
    # 解析简历
    if resume_file.filename.endswith('.pdf'):
        resume_text = parse_pdf(resume_file)
    elif resume_file.filename.endswith('.docx'):
        resume_text = parse_docx(resume_file)
    else:
        return jsonify({'error': 'Unsupported file format'}), 400
    
    # 三层评分机制
    # 1. 整体文本相似度
    embeddings = model.encode([resume_text['raw_text'], jd_text])
    text_similarity = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    
    # 2. 技能匹配度
    skills_embeddings = model.encode([', '.join(resume_text['skills']), jd_text])
    skills_similarity = np.dot(skills_embeddings[0], skills_embeddings[1]) / (np.linalg.norm(skills_embeddings[0]) * np.linalg.norm(skills_embeddings[1]))
    
    # 3. 经验匹配度
    exp_embeddings = model.encode([resume_text['experience'], jd_text])
    exp_similarity = np.dot(exp_embeddings[0], exp_embeddings[1]) / (np.linalg.norm(exp_embeddings[0]) * np.linalg.norm(exp_embeddings[1]))
    
    # 综合评分
    score = round((text_similarity * 0.4 + skills_similarity * 0.3 + exp_similarity * 0.3) * 100, 2)
    
    return jsonify({
        'score': score,
        'score_details': {
            'text_similarity': round(text_similarity * 100, 2),
            'skills_match': round(skills_similarity * 100, 2),
            'experience_match': round(exp_similarity * 100, 2)
        },
        'resume_data': resume_text,
        'jd_text': jd_text
    })

if __name__ == '__main__':
    app.run(debug=True)