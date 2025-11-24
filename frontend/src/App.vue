<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1 class="logo">🍳 Go Cooking</h1>
<!--          <p class="subtitle">Make cooking great again！</p>-->
        </div>
      </el-header>
      <el-menu
        :default-active="$route.path"
        mode="horizontal"
        router
        class="nav-menu"
      >
        <el-menu-item index="/">菜谱</el-menu-item>
        <el-menu-item index="/materials">材料</el-menu-item>
      </el-menu>
      <el-main class="main-content">
        <router-view />
      </el-main>
      <el-footer class="footer">
        <p>GoCooking 3 - 为烹饪新手打造的厨房助手 © 2025</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #FF9500 0%, #FF7A00 100%);  /* Orange gradient */
  color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
}

.logo {
  margin: 0;
  font-size: 28px;
  font-weight: bold;
}

.subtitle {
  margin: 0 0 0 10px;
  font-size: 18px;
  font-weight: 500;
  align-self: flex-end;
  margin-bottom: 5px;
}

.nav-menu {
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
}

.nav-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  font-size: 16px;
  font-weight: 500;
}

.nav-menu .el-menu-item:hover {
  color: #FF9500;
}

.nav-menu .el-menu-item.is-active {
  color: #FF9500;
  border-bottom: 2px solid #FF9500;
}

.main-content {
  padding: 0;
  background-color: #f5f7fa;
}

.footer {
  background-color: #f0f2f5;
  color: #909399;
  text-align: center;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

:deep(.el-menu--horizontal .el-menu-item) {
  height: 50px;
  line-height: 50px;
}
</style>