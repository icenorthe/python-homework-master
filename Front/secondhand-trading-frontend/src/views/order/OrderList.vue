<template>
  <div class="order-list">
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="我的购买" name="buyer">
        <el-table
          v-loading="loading"
          :data="orderList"
          style="width: 100%">
          <el-table-column
            prop="id"
            label="订单编号"
            width="180">
          </el-table-column>
          <el-table-column
            prop="createTime"
            label="创建时间"
            width="180">
          </el-table-column>
          <el-table-column
            prop="status"
            label="订单状态">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="totalAmount"
            label="订单金额"
            width="120">
            <template #default="scope">
              ¥{{ scope.row.totalAmount }}
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="200">
            <template #default="scope">
              <el-button
                size="small"
                @click="viewOrderDetail(scope.row.id)">
                查看详情
              </el-button>
              <el-button
                v-if="scope.row.status === 'PENDING'"
                size="small"
                type="danger"
                @click="cancelOrder(scope.row.id)">
                取消订单
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="我的出售" name="seller">
        <el-table
          v-loading="loading"
          :data="orderList"
          style="width: 100%">
          <el-table-column
            prop="id"
            label="订单编号"
            width="180">
          </el-table-column>
          <el-table-column
            prop="createTime"
            label="创建时间"
            width="180">
          </el-table-column>
          <el-table-column
            prop="status"
            label="订单状态">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="totalAmount"
            label="订单金额"
            width="120">
            <template #default="scope">
              ¥{{ scope.row.totalAmount }}
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="200">
            <template #default="scope">
              <el-button
                size="small"
                @click="viewOrderDetail(scope.row.id)">
                查看详情
              </el-button>
              <el-button
                v-if="scope.row.status === 'PENDING'"
                size="small"
                type="primary"
                @click="confirmOrder(scope.row.id)">
                确认订单
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useOrderStore } from '@/stores/order'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

export default defineComponent({
  name: 'OrderList',
  setup() {
    const orderStore = useOrderStore()
    const userStore = useUserStore()
    const router = useRouter()
    const activeTab = ref('buyer')
    
    // 获取当前用户ID
    const userId = computed(() => {
      console.log('当前用户信息:', userStore.user)
      console.log('当前用户ID:', userStore.userId)
      return userStore.userId
    })

    const loadOrders = async () => {
      try {
        if (!userId.value) {
          console.log('用户未登录或ID未获取')
          ElMessage.error('请先登录')
          router.push('/login')
          return
        }

        console.log('开始加载订单, 当前Tab:', activeTab.value)
        console.log('用户ID:', userId.value)

        if (activeTab.value === 'buyer') {
          console.log('加载买家订单')
          const response = await orderStore.getBuyerOrders({ buyerId: userId.value })
          console.log('买家订单数据:', response)
        } else {
          console.log('加载卖家订单')
          const response = await orderStore.getSellerOrders({ sellerId: userId.value })
          console.log('卖家订单数据:', response)
        }
      } catch (error) {
        console.error('加载订单列表失败:', error)
        console.error('错误详情:', {
          message: error.message,
          response: error.response,
          request: error.request
        })
        ElMessage.error(error.response?.data?.message || '获取订单列表失败')
      }
    }

    const handleTabClick = () => {
      loadOrders()
    }

    const viewOrderDetail = (orderId) => {
      router.push(`/order/detail/${orderId}`)
    }

    const cancelOrder = async (orderId) => {
      try {
        await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await orderStore.updateOrderStatus({
          orderId,
          status: 'cancelled'
        })
        ElMessage.success('订单已取消')
        loadOrders()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消订单失败')
        }
      }
    }

    const confirmOrder = async (orderId) => {
      try {
        await orderStore.updateOrderStatus({
          orderId,
          status: 'confirmed'
        })
        ElMessage.success('订单已确认')
        loadOrders()
      } catch (error) {
        ElMessage.error('确认订单失败')
      }
    }

    const getStatusType = (status) => {
      const statusMap = {
        'pending': 'warning',
        'confirmed': 'success',
        'cancelled': 'info',
        'completed': 'success'
      }
      return statusMap[status] || 'info'
    }

    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'cancelled': '已取消',
        'completed': '已完成'
      }
      return statusMap[status] || status
    }

    onMounted(() => {
      console.log('组件挂载完成，准备加载订单')
      loadOrders()
    })

    return {
      activeTab,
      loading: computed(() => {
        console.log('加载状态:', orderStore.loading)
        return orderStore.loading
      }),
      orderList: computed(() => {
        const list = orderStore.orderList || []
        console.log('订单列表:', list)
        return Array.isArray(list) ? list : []
      }),
      handleTabClick,
      viewOrderDetail,
      cancelOrder,
      confirmOrder,
      getStatusType,
      getStatusText
    }
  }
})
</script>

<style scoped>
.order-list {
  padding: 20px;
}
</style> 