<template>
  <div class="order-detail" v-loading="loading">
    <div class="page-header">
      <el-page-header @back="goBack" :content="'订单详情 #' + orderId" />
    </div>

    <el-card class="order-info" v-if="orderDetail">
      <template #header>
        <div class="card-header">
          <span>订单信息</span>
          <el-tag :type="getStatusType(orderDetail.status)">
            {{ getStatusText(orderDetail.status) }}
          </el-tag>
        </div>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单编号">
          {{ orderDetail.id }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ orderDetail.createTime }}
        </el-descriptions-item>
        <el-descriptions-item label="商品名称">
          {{ orderDetail.productName }}
        </el-descriptions-item>
        <el-descriptions-item label="商品价格">
          ¥{{ orderDetail.totalAmount }}
        </el-descriptions-item>
        <el-descriptions-item label="买家">
          {{ orderDetail.buyerName }}
        </el-descriptions-item>
        <el-descriptions-item label="卖家">
          {{ orderDetail.sellerName }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="order-actions" v-if="orderDetail.status === 'PENDING'">
        <el-button
          v-if="isCurrentUserBuyer"
          type="danger"
          @click="cancelOrder">
          取消订单
        </el-button>
        <el-button
          v-if="isCurrentUserSeller"
          type="primary"
          @click="confirmOrder">
          确认订单
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useOrderStore } from '@/stores/order'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

export default defineComponent({
  name: 'OrderDetail',
  setup() {
    const orderStore = useOrderStore()
    const userStore = useUserStore()
    const route = useRoute()
    const router = useRouter()
    
    const orderId = ref(route.params.id)
    const userId = computed(() => userStore.userId)
    
    const orderDetail = computed(() => orderStore.currentOrder)
    const loading = computed(() => orderStore.loading)

    const isCurrentUserBuyer = computed(() => {
      return orderDetail.value?.buyerId === userId.value
    })

    const isCurrentUserSeller = computed(() => {
      return orderDetail.value?.sellerId === userId.value
    })

    const loadOrderDetail = async () => {
      try {
        await orderStore.getOrderDetail(orderId.value)
      } catch (error) {
        ElMessage.error('获取订单详情失败')
      }
    }

    const cancelOrder = async () => {
      try {
        await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await orderStore.updateOrderStatus({
          orderId: orderId.value,
          status: 'CANCELLED'
        })
        ElMessage.success('订单已取消')
        loadOrderDetail()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消订单失败')
        }
      }
    }

    const confirmOrder = async () => {
      try {
        await orderStore.updateOrderStatus({
          orderId: orderId.value,
          status: 'CONFIRMED'
        })
        ElMessage.success('订单已确认')
        loadOrderDetail()
      } catch (error) {
        ElMessage.error('确认订单失败')
      }
    }

    const getStatusType = (status) => {
      const statusMap = {
        'PENDING': 'warning',
        'CONFIRMED': 'success',
        'CANCELLED': 'info',
        'COMPLETED': 'success'
      }
      return statusMap[status] || 'info'
    }

    const getStatusText = (status) => {
      const statusMap = {
        'PENDING': '待确认',
        'CONFIRMED': '已确认',
        'CANCELLED': '已取消',
        'COMPLETED': '已完成'
      }
      return statusMap[status] || status
    }

    const goBack = () => {
      router.back()
    }

    onMounted(() => {
      loadOrderDetail()
    })

    return {
      orderId,
      orderDetail,
      loading,
      isCurrentUserBuyer,
      isCurrentUserSeller,
      cancelOrder,
      confirmOrder,
      getStatusType,
      getStatusText,
      goBack
    }
  }
})
</script>

<style scoped>
.order-detail {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info {
  margin-bottom: 20px;
}

.order-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 