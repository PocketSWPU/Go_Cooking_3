<template>
  <div class="add-dish">
    <el-page-header :content="'新增菜品'" @back="$router.go(-1)" />
    
    <el-card class="form-card">
      <el-form 
        :model="dishForm" 
        :rules="rules" 
        ref="dishFormRef"
        label-width="100px" 
        style="max-width: 800px; margin: 0 auto;"
      >
        <el-form-item label="菜品名称" prop="dish_name">
          <el-input 
            v-model="dishForm.dish_name" 
            placeholder="请输入菜品名称" 
            size="large"
          />
        </el-form-item>

        <el-form-item label="难度等级" prop="difficult">
          <el-radio-group v-model="dishForm.difficult">
            <el-radio :label="1">简单</el-radio>
            <el-radio :label="2">中等</el-radio>
            <el-radio :label="3">复杂</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- Ingredients Section -->
        <el-form-item label="食材列表">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <el-button
              type="primary"
              @click="showAddIngredientDialog = true"
            >
              添加食材
            </el-button>

            <!-- 多选下拉框 -->
            <el-select
              ref="ingredientSelectRef"
              v-model="selectedIngredients"
              multiple
              filterable
              allow-create
              default-first-option
              placeholder="搜索或选择配料"
              style="flex: 1; min-width: 200px;"
              :loading="loadingIngredients"
            >
              <el-option
                v-for="ingredient in allIngredients"
                :key="ingredient.id"
                :label="ingredient.ingredient_name"
                :value="ingredient.id"
              />
            </el-select>

            <!-- 快速添加按钮 -->
            <el-input
              v-model="quickUsage"
              placeholder="用量，如：适量、100克"
              style="width: 120px;"
            />
            <el-button
              type="success"
              @click="quickAddIngredients"
            >
              快速添加
            </el-button>
          </div>

          <el-table
            :data="dishForm.ingredients"
            style="width: 100%"
            empty-text="暂无食材"
          >
            <el-table-column prop="ingredient_name" label="食材名称" width="150" />
            <el-table-column label="食材类型" width="120">
              <template #default="{ row, $index }">
                <div
                  class="type-cell"
                  @click="startEditingType($index)"
                  v-if="!row.editingType"
                >
                  {{ getIngredientTypeText(row.type) }}
                </div>
                <el-select
                  v-else
                  v-model="row.tempType"
                  @change="stopEditingType($index)"
                  @blur="stopEditingType($index)"
                  size="small"
                  style="width: 100px;"
                >
                  <el-option label="主料" :value="1" />
                  <el-option label="辅料" :value="2" />
                  <el-option label="调料" :value="3" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="用量" width="150">
              <template #default="{ row, $index }">
                <div
                  class="usage-cell"
                  @click="startEditingUsage($index)"
                  v-if="!row.editingUsage"
                >
                  {{ row.usage || '点击编辑' }}
                </div>
                <el-input
                  v-else
                  v-model="row.tempUsage"
                  @blur="stopEditingUsage($index)"
                  @keyup.enter="stopEditingUsage($index)"
                  size="small"
                  ref="usageInput"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row, $index }">
                <el-button
                  type="danger"
                  size="small"
                  @click="removeIngredient($index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>

        <!-- Steps Section -->
        <el-form-item label="制作步骤">
          <el-button 
            type="primary" 
            @click="showAddStepDialog = true"
            style="margin-bottom: 20px;"
          >
            添加步骤
          </el-button>

          <el-table 
            :data="dishForm.steps" 
            style="width: 100%" 
            empty-text="暂无步骤"
          >
            <el-table-column prop="step_order" label="步骤序号" width="100" />
            <el-table-column prop="step_text" label="步骤内容" />
            <el-table-column label="操作" width="100">
              <template #default="{ row, $index }">
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="removeStep($index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>

        <el-form-item style="margin-top: 30px; text-align: center;">
          <el-button type="primary" @click="submitForm" size="large" :loading="submitting">
            提交菜品
          </el-button>
          <el-button @click="$router.go(-1)" size="large">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Add Ingredient Dialog -->
    <el-dialog
      v-model="showAddIngredientDialog"
      title="添加食材"
      width="400px"
    >
      <el-form :model="ingredientForm" label-width="80px">
        <el-form-item label="食材名称" prop="ingredient_name">
          <el-input v-model="ingredientForm.ingredient_name" placeholder="请输入食材名称" />
        </el-form-item>
        <el-form-item label="食材类型" prop="type">
          <el-select v-model="ingredientForm.type" placeholder="请选择食材类型" style="width: 100%">
            <el-option label="主料" :value="1" />
            <el-option label="辅料" :value="2" />
            <el-option label="调料" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="用量" prop="usage">
          <el-input v-model="ingredientForm.usage" placeholder="请输入用量，如：2个、适量、100克等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddIngredientDialog = false">取消</el-button>
          <el-button type="primary" @click="addIngredient">添加</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Add Step Dialog -->
    <el-dialog 
      v-model="showAddStepDialog" 
      title="添加步骤" 
      width="600px"
    >
      <el-form :model="stepForm" label-width="80px">
        <el-form-item label="步骤序号" prop="step_order">
          <el-input-number 
            v-model="stepForm.step_order" 
            :min="1" 
            :max="99" 
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="步骤说明" prop="step_text">
          <el-input 
            v-model="stepForm.step_text" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入步骤说明" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddStepDialog = false">取消</el-button>
          <el-button type="primary" @click="addStep">添加</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AddDish',
  data() {
    return {
      submitting: false,
      showAddIngredientDialog: false,
      showAddStepDialog: false,
      dishForm: {
        dish_name: '',
        difficult: 1,
        ingredients: [],
        steps: []
      },
      ingredientForm: {
        ingredient_name: '',
        type: 1,
        usage: ''
      },
      stepForm: {
        step_order: 1,
        step_text: ''
      },
      // 新增配料下拉框相关数据
      allIngredients: [], // 所有配料列表
      selectedIngredients: [], // 当前选中的配料
      quickUsage: '', // 快速添加时的用量
      loadingIngredients: false, // 配料加载状态
      rules: {
        dish_name: [
          { required: true, message: '请输入菜品名称', trigger: 'blur' },
          { min: 1, max: 50, message: '菜品名称长度应在1-50个字符之间', trigger: 'blur' }
        ],
        difficult: [
          { required: true, message: '请选择难度等级', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    this.getAllIngredients()
  },
  methods: {
    // 获取所有配料列表
    async getAllIngredients() {
      try {
        this.loadingIngredients = true
        const response = await api.get('/ingredient/list')
        if (response.data.code === 0) {
          this.allIngredients = response.data.data
        } else {
          this.$message.error(response.data.message || '获取配料列表失败')
        }
      } catch (error) {
        console.error('Error getting ingredients:', error)
        this.$message.error('获取配料列表失败：' + (error.response?.data?.message || error.message))
      } finally {
        this.loadingIngredients = false
      }
    },

    getIngredientTypeText(type) {
      switch(type) {
        case 1: return '主料'
        case 2: return '辅料'
        case 3: return '调料'
        default: return '未知'
      }
    },
    // 快速添加配料
    quickAddIngredients() {
      if (this.selectedIngredients.length === 0) {
        this.$message.warning('请先选择配料')
        return
      }

      let addedCount = 0;

      // 处理每个选中的配料
      for (const ingredientValue of this.selectedIngredients) {
        let newIngredient = null;
        let ingredientName = ingredientValue;

        // 检查是否是现有的配料ID（数值类型）
        if (typeof ingredientValue === 'number') {
          const existingIngredient = this.allIngredients.find(ing => ing.id === ingredientValue);
          if (existingIngredient) {
            newIngredient = {
              id: existingIngredient.id,
              ingredient_name: existingIngredient.ingredient_name,
              type: existingIngredient.type,
              usage: this.quickUsage,
              editingUsage: false,
              editingType: false,
              tempUsage: this.quickUsage,
              tempType: existingIngredient.type
            };
            ingredientName = existingIngredient.ingredient_name;
          }
        } else {
          // 如果是新建的配料名（字符串类型）
          newIngredient = {
            id: null,  // 新创建的配料ID为null
            ingredient_name: ingredientValue,
            type: 3, // 新创建的配料默认为调料
            usage: this.quickUsage,
            editingUsage: false,
            editingType: false,
            tempUsage: this.quickUsage,
            tempType: 3
          };
          ingredientName = ingredientValue;
        }

        if (newIngredient) {
          // 检查是否已存在，避免重复添加
          const exists = this.dishForm.ingredients.some(ing =>
            ing.ingredient_name.toLowerCase() === ingredientName.toLowerCase()
          );

          if (!exists) {
            this.dishForm.ingredients.push(newIngredient);
            addedCount++;
          }
        }
      }

      // 清空选择和用量输入
      this.selectedIngredients = [];
      this.quickUsage = '';
      this.$message.success(`已快速添加 ${addedCount} 个配料`);

      // 在快速添加后清空选择器的输入内容
      this.$nextTick(() => {
        // 通过 ref 精确定位配料选择器
        if (this.$refs.ingredientSelectRef) {
          const selectWrapper = this.$refs.ingredientSelectRef.$el;
          const input = selectWrapper.querySelector('.el-select__input');
          if (input) {
            input.value = '';
          }
        }
      });
    },
    addIngredient() {
      if (!this.ingredientForm.ingredient_name) {
        this.$message.error('请输入食材名称')
        return
      }

      // Add editing state properties to the new ingredient
      const newIngredient = {
        ...this.ingredientForm,
        editingUsage: false,
        editingType: false,
        tempUsage: this.ingredientForm.usage,
        tempType: this.ingredientForm.type
      }

      this.dishForm.ingredients.push(newIngredient)
      this.ingredientForm = { ingredient_name: '', type: 1, usage: '' }
      this.showAddIngredientDialog = false
    },
    removeIngredient(index) {
      this.dishForm.ingredients.splice(index, 1)
    },
    startEditingUsage(index) {
      // Set the ingredient to editing mode
      this.dishForm.ingredients[index].editingUsage = true
      // Initialize tempUsage with current usage value
      this.dishForm.ingredients[index].tempUsage = this.dishForm.ingredients[index].usage || ''

      // Focus the input after the DOM update
      this.$nextTick(() => {
        const inputRef = this.$refs.usageInput
        if (inputRef && inputRef[index]) {
          inputRef[index].focus()
        }
      })
    },
    stopEditingUsage(index) {
      // Update the actual usage value
      this.dishForm.ingredients[index].usage = this.dishForm.ingredients[index].tempUsage
      // Exit editing mode
      this.dishForm.ingredients[index].editingUsage = false
    },
    startEditingType(index) {
      // Set the ingredient to editing mode
      this.dishForm.ingredients[index].editingType = true
      // Initialize tempType with current type value
      this.dishForm.ingredients[index].tempType = this.dishForm.ingredients[index].type
    },
    stopEditingType(index) {
      // Update the actual type value
      this.dishForm.ingredients[index].type = this.dishForm.ingredients[index].tempType
      // Exit editing mode
      this.dishForm.ingredients[index].editingType = false
    },
    addStep() {
      if (!this.stepForm.step_text) {
        this.$message.error('请输入步骤内容')
        return
      }

      // Check if step order already exists
      const existingStep = this.dishForm.steps.find(step => step.step_order === this.stepForm.step_order)
      if (existingStep) {
        this.$message.error(`步骤序号 ${this.stepForm.step_order} 已存在，请更换序号`)
        return
      }

      this.dishForm.steps.push({ ...this.stepForm })
      // Sort steps by order
      this.dishForm.steps.sort((a, b) => a.step_order - b.step_order)
      this.stepForm = { step_order: this.dishForm.steps.length + 1, step_text: '' }
      this.showAddStepDialog = false
    },
    removeStep(index) {
      this.dishForm.steps.splice(index, 1)
    },
    async submitForm() {
      this.$refs.dishFormRef.validate(async (valid) => {
        if (!valid) {
          this.$message.error('请检查表单内容')
          return
        }

        if (this.dishForm.ingredients.length === 0) {
          this.$message.error('请至少添加一个食材')
          return
        }

        if (this.dishForm.steps.length === 0) {
          this.$message.error('请至少添加一个制作步骤')
          return
        }

        this.submitting = true
        try {
          // 准备提交数据，确保ingredients格式正确
          const submitData = {
            ...this.dishForm,
            ingredients: this.dishForm.ingredients.map(ing => ({
              ingredient_name: ing.ingredient_name,
              type: ing.type,
              usage: ing.usage
            }))
          };

          const response = await api.post('/dish/add/raw', submitData)
          if (response.data.code === 0) {
            this.$message.success('菜品添加成功！')
            this.$router.push('/')
          } else {
            this.$message.error(response.data.message || '菜品添加失败')
          }
        } catch (error) {
          console.error('Error adding dish:', error)
          this.$message.error('菜品添加失败：' + (error.response?.data?.message || error.message))
        } finally {
          this.submitting = false
        }
      })
    }
  }
}
</script>

<style scoped>
.add-dish {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 80px);
}

.form-card {
  margin-top: 20px;
  background-color: #fff;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.usage-cell {
  cursor: pointer;
  padding: 5px;
  border-radius: 3px;
  transition: background-color 0.2s;
}

.usage-cell:hover {
  background-color: #f5f7fa;
}

.type-cell {
  cursor: pointer;
  padding: 5px;
  border-radius: 3px;
  transition: background-color 0.2s;
}

.type-cell:hover {
  background-color: #f5f7fa;
}
</style>