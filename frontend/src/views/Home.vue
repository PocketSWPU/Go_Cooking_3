<template>
  <div class="home">
    <div class="search-container">
      <el-input
        v-model="searchForm.dishName"
        placeholder="输入菜名搜索"
        @keyup.enter="fetchDishes"
        size="large"
        style="max-width: 300px;"
        clearable
      />
      <el-select
        v-model="searchForm.difficult"
        placeholder="选择难度"
        size="large"
        style="margin-left: 10px; width: 120px;"
        clearable
      >
        <el-option label="简单" value="1"></el-option>
        <el-option label="中等" value="2"></el-option>
        <el-option label="复杂" value="3"></el-option>
      </el-select>
      <el-button type="primary" @click="fetchDishes" size="large" style="margin-left: 10px;">搜索</el-button>
      <el-button @click="clearFilters" size="large" style="margin-left: 10px;">清空</el-button>
      <el-button type="success" @click="$router.push('/add')" size="large" style="margin-left: 10px;">新增</el-button>
    </div>

    <div class="content-container">
      <el-card v-if="dishes.length === 0" class="no-data-card">
        <el-empty description="暂无菜品数据" />
      </el-card>

      <el-row :gutter="20" v-else>
        <el-col 
          v-for="dish in dishes" 
          :key="dish.id" 
          :xs="24" :sm="12" :md="8" :lg="6"
          style="margin-bottom: 20px;"
        >
          <el-card 
            @click="goToDetail(dish.id)"
            class="dish-card"
            shadow="hover"
          >
            <div class="dish-content">
              <div class="dish-header">
                <h3 class="dish-title">{{ dish.dish_name }}</h3>
                <el-tag 
                  :type="getDifficultyType(dish.difficult)" 
                  size="small"
                  effect="dark"
                >
                  {{ getDifficultyText(dish.difficult) }}
                </el-tag>
              </div>
              
              <div class="dish-ingredients" v-if="dish.main_ingredients && dish.main_ingredients.length">
                <el-tag
                  v-for="ingredient in dish.main_ingredients"
                  :key="ingredient"
                  size="small"
                  style="margin-right: 5px; margin-top: 8px;"
                  type="warning"
                >
                  {{ ingredient }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="pagination-container" v-if="dishes.length > 0">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[12, 24, 36, 48]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total || dishes.length"
        background
        style="margin-top: 20px; text-align: center;"
      />
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'Home',
  data() {
    return {
      dishes: [],
      searchForm: {
        page: 0,
        size: 12,
        dishName: '',
        difficult: null
      },
      currentPage: 1,
      pageSize: 12,
      total: 0
    }
  },
  mounted() {
    this.fetchDishes()
  },
  methods: {
    async fetchDishes() {
      try {
        const params = {
          ...this.searchForm,
          page: this.currentPage - 1, // Backend uses 0-based pagination
          size: this.pageSize,
          dishName: this.searchForm.dishName,
          difficult: this.searchForm.difficult !== null && this.searchForm.difficult !== '' ? parseInt(this.searchForm.difficult) : null
        }

        const response = await api.post('/dish/select', params)
        if (response.data.code === 0) {
          // Handle the new paginated response format
          if (response.data.data && response.data.data.items) {
            this.dishes = response.data.data.items
            this.total = response.data.data.total || 0
          } else {
            // Fallback to previous format in case of compatibility
            this.dishes = response.data.data || []
            // Try to get total if available in other ways
          }
        } else {
          this.$message.error('获取菜品数据失败')
        }
      } catch (error) {
        console.error('Error fetching dishes:', error)
        this.$message.error('获取菜品数据失败')
      }
    },
    getDifficultyText(difficulty) {
      switch(difficulty) {
        case 1: return '简单'
        case 2: return '中等'
        case 3: return '复杂'
        default: return '未知'
      }
    },
    getDifficultyType(difficulty) {
      switch(difficulty) {
        case 1: return 'success' // Green for simple
        case 2: return '' // Default for medium
        case 3: return 'danger' // Red for complex
        default: return 'info'
      }
    },
    goToDetail(id) {
      this.$router.push(`/dish/${id}`)
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.fetchDishes()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchDishes()
    },
    clearFilters() {
      this.searchForm.dishName = ''
      this.searchForm.difficult = null
      this.currentPage = 1
      this.fetchDishes()
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 80px);
}

.search-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  padding: 0 20px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.no-data-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  background-color: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.dish-card {
  cursor: pointer;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
}

.dish-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
}

.dish-content {
  width: 100%;
  padding: 15px;
}

.dish-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.dish-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
}

.dish-ingredients {
  margin-top: 15px;
}

.pagination-container {
  max-width: 1200px;
  margin: 30px auto 0;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .search-container {
    flex-direction: column;
    align-items: center;
  }
  
  .search-container .el-button {
    margin-left: 0 !important;
    margin-top: 10px;
  }
  
  .dish-card {
    height: auto;
    margin-bottom: 15px;
  }
}
</style>