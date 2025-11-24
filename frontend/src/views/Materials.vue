<template>
  <div class="materials">
    <div class="materials-header">
      <h2>食材管理</h2>
      <p>管理您的食材信息</p>
    </div>

    <el-card class="materials-card">
      <div class="no-content">
        <el-empty description="功能开发中，敬请期待" :image-size="200" />
        <p class="placeholder-text">这里将显示食材相关信息</p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Materials',
  data() {
    return {
    }
  }
}
</script>

<style scoped>
.materials {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 150px);
}

.materials-header {
  margin-bottom: 30px;
  text-align: center;
}

.materials-header h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.materials-header p {
  margin: 0;
  color: #909399;
  font-size: 16px;
}

.materials-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.no-content {
  padding: 40px 20px;
}

.placeholder-text {
  margin-top: 20px;
  color: #909399;
  font-size: 16px;
}
</style>