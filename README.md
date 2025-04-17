# HRMS - AI智能简历筛选系统

## 项目概述
开发一个AI智能化简历筛选网站，功能包括简历上传、职位要求输入、AI分析匹配度、自动评分排名和可视化展示。

## 技术栈
- 前端: Vue3 + Element UI
- 后端: Python Flask
- AI模型: BERT + 规则引擎
- 数据库: PostgreSQL

## 功能模块
1. 简历上传与解析
2. JD分析与匹配
3. 评分与排名
4. 可视化展示

## 快速开始

``` bash
conda create --name myenv python=3.12
conda activate myenv
```
```bash
# 前端
cd frontend
npm install
npm run dev

npm install @vitejs/plugin-vue 
npm install vite@latest
npm install @vitejs/plugin-vue@latest

# 后端
cd backend
conda activate testenv
pip install -r requirements.txt
python app.py
```