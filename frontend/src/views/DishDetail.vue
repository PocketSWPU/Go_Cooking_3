<template>
  <div class="dish-detail">
    <el-page-header 
      @back="goBack" 
      :content="dish?.dish_name || '菜品详情'"
      style="margin-bottom: 20px;"
    />

    <div class="detail-container" v-if="dish">
      <el-card class="dish-card">
        <template #header>
          <div class="card-header">
            <h2 class="dish-title">{{ dish.dish_name }}</h2>
            <el-tag 
              :type="getDifficultyType(dish.difficult)" 
              size="large"
              effect="dark"
            >
              {{ getDifficultyText(dish.difficult) }}
            </el-tag>
          </div>
        </template>

        <div class="detail-content">
          <el-descriptions title="菜品信息" :column="1" border :label-width="100">
            <el-descriptions-item label="菜品名称">{{ dish.dish_name }}</el-descriptions-item>
            <el-descriptions-item label="制作难度">
              <el-tag :type="getDifficultyType(dish.difficult)">
                {{ getDifficultyText(dish.difficult) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(dish.create_time) }}</el-descriptions-item>
            <el-descriptions-item label="最后修改">{{ formatDate(dish.modify_time) }}</el-descriptions-item>
          </el-descriptions>

          <el-tabs v-model="activeTab" class="dish-tabs">
            <el-tab-pane label="所需食材" name="ingredients">
              <!-- Group ingredients by type -->
              <div v-if="dish.ingredients && dish.ingredients.length > 0" class="ingredients-content">
                <div v-for="(ingredientsByType, type) in groupedIngredients" :key="type" class="ingredient-group">
                  <h4 class="ingredient-group-title">
                    <el-tag :type="getIngredientTypeTag(parseInt(type))" size="large">
                      {{ getIngredientTypeText(parseInt(type)) }}
                    </el-tag>
                  </h4>
                  <div class="ingredient-list">
                    <div
                      v-for="(ingredient, index) in ingredientsByType"
                      :key="index"
                      class="ingredient-item"
                    >
                      <span class="ingredient-name">{{ ingredient.ingredient_name }}</span>
                      <span class="ingredient-usage" v-if="ingredient.usage && ingredient.usage.trim() !== ''"> ({{ ingredient.usage }})</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="no-data">
                <el-empty description="暂无食材信息" :image-size="100" />
              </div>
            </el-tab-pane>

            <el-tab-pane label="制作步骤" name="steps">
              <div class="steps-content">
                <el-timeline>
                  <el-timeline-item
                    v-for="(step, index) in dish.steps"
                    :key="step.id"
                    :timestamp="`步骤 ${index + 1}`"
                    placement="top"
                    :color="index === 0 ? '#409EFF' : index === dish.steps.length - 1 ? '#67C23A' : '#909399'"
                  >
<!--                    <el-card>-->
                      <p>{{ step.step_text }}</p>
<!--                    </el-card>-->
                  </el-timeline-item>
                </el-timeline>

                <div v-if="dish.steps.length === 0" class="no-data">
                  <el-empty description="暂无制作步骤" :image-size="100" />
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>

    <div v-else class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'DishDetail',
  props: ['id'],
  data() {
    return {
      dish: null,
      activeTab: 'ingredients'  // 默认打开所需食材tab
    }
  },
  computed: {
    groupedIngredients() {
      if (!this.dish || !this.dish.ingredients) {
        return {}
      }

      const grouped = {}
      this.dish.ingredients.forEach(ingredient => {
        const type = ingredient.type
        if (!grouped[type]) {
          grouped[type] = []
        }
        grouped[type].push(ingredient)
      })

      return grouped
    }
  },
  mounted() {
    this.fetchDishDetail()
  },
  methods: {
    async fetchDishDetail() {
      try {
        const response = await api.get(`/dish/detail/${this.id}`)
        if (response.data.code === 0) {
          this.dish = response.data.data
        } else {
          this.$message.error('获取菜品详情失败')
        }
      } catch (error) {
        console.error('Error fetching dish detail:', error)
        this.$message.error('获取菜品详情失败')
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
        case 2: return 'warning' // Default for medium
        case 3: return 'danger' // Red for complex
        default: return 'info'
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    getIngredientTypeText(type) {
      switch(type) {
        case 1: return '主料'
        case 2: return '辅料'
        case 3: return '调料'
        default: return '未知'
      }
    },
    getIngredientTypeTag(type) {
      switch(type) {
        case 1: return 'success'  // 主料
        case 2: return 'warning'  // 辅料
        case 3: return 'info'  // 调料
        default: return 'info'
      }
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.dish-detail {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 80px);
}

.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.dish-card {
  background-color: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dish-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
  font-weight: bold;
}

.detail-content {
  padding: 20px 0;
}

.section {
  margin: 30px 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  padding-bottom: 10px;
  margin: 0 0 20px 0;
  border-bottom: 2px solid #e4e7ed;
}

.no-data {
  text-align: center;
  padding: 40px 0;
}

.loading-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 0 20px;
}

:deep(.el-descriptions__header) {
  margin-bottom: 20px;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

.dish-tabs {
  margin-top: 20px;
}

.ingredients-content {
  padding: 15px 0;
}

.steps-content {
  padding: 15px 0;
}

.ingredient-group {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
}

.ingredient-group-title {
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
}

.ingredient-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.ingredient-item {
  background-color: white;
  padding: 10px 15px;
  border-radius: 6px;
  margin-bottom: 8px;
  border: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.ingredient-name {
  font-weight: 500;
  color: #303133;
  font-size: 15px;
}

.ingredient-usage {
  color: #606266;
  margin-left: 8px;
  font-size: 14px;
  font-weight: normal;
  background-color: #f4f4f5;
  padding: 2px 6px;
  border-radius: 3px;
}

@media (max-width: 768px) {
  .dish-detail {
    padding: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-header .el-tag {
    margin-top: 10px;
  }

  .dish-tabs {
    margin-top: 10px;
  }

  .ingredient-list {
    flex-direction: column;
  }

  .ingredient-item {
    width: 100%;
  }
}
</style>