<template>
  <div class="container">
    <h1>AI智能简历筛选系统</h1>
    <el-upload
      class="upload-demo"
      drag
      action=""
      :auto-upload="false"
      :on-change="handleFileChange"
      multiple
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

const jobDescription = ref('');
const showResults = ref(false);
const candidates = ref([]);

const handleFileChange = (file) => {
  console.log('上传文件:', file);
};

const analyzeResumes = () => {
  // 模拟数据
  candidates.value = [
    { name: '张三', score: '85%', skills: 'Python, Java' },
    { name: '李四', score: '78%', skills: 'JavaScript, React' },
  ];
  showResults.value = true;
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