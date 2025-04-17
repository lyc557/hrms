<template>
  <div class="container">
    <h1>AI智能简历筛选系统</h1>
    <el-upload
      class="upload-demo"
      drag
      :action="UPLOAD_API"
      :auto-upload="true"
      :file-list="fileList"
      :on-change="handleFileChange"
      :before-upload="beforeUpload"
      multiple
      accept=".pdf,.docx"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        拖拽简历文件到此处或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持PDF、DOCX格式文件
        </div>
      </template>
    </el-upload>
    
    <el-input
      v-model="jobDescription"
      :rows="5"
      type="textarea"
      placeholder="请输入职位描述(JD)"
    />
    
    <el-button type="primary" @click="analyzeResumes">开始分析</el-button>
    
    <div class="result-container" v-if="showResults">
      <h2>候选人匹配结果</h2>
      <el-table :data="candidates" style="width: 100%">
        <el-table-column prop="name" label="姓名" width="180" />
        <el-table-column prop="score" label="匹配度" width="180" />
        <el-table-column prop="skills" label="技能匹配" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 从环境变量获取后端地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const UPLOAD_API = `${API_BASE_URL}/api/upload`;
const ANALYZE_API = `${API_BASE_URL}/api/analyze`;

const jobDescription = ref('');
const showResults = ref(false);
const candidates = ref([]);
const fileList = ref([]);

const handleFileChange = (file, files) => {
  fileList.value = files;
  const formData = new FormData();
  formData.append('file', file.raw);
  
  axios.post(UPLOAD_API, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    console.log('上传成功:', response.data);
  }).catch(error => {
    console.error('上传失败:', error);
    fileList.value = fileList.value.filter(f => f.uid !== file.uid);
  });
};

const analyzeResumes = () => {
  axios.post(ANALYZE_API, {
    job_description: jobDescription.value
  }).then(response => {
    candidates.value = response.data;
    showResults.value = true;
  }).catch(error => {
    console.error('分析失败:', error);
  });
};

const beforeUpload = (file) => {
  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  const isAllowed = allowedTypes.includes(file.type);
  
  if (!isAllowed) {
    ElMessage.error('只支持上传PDF和DOCX格式的文件');
    return false;
  }
  
  return true;
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.upload-demo {
  margin: 20px 0;
}

.result-container {
  margin-top: 30px;
}
</style>
