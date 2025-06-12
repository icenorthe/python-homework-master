<template>
  <div class="container">
    <div class="form-section">
      <h2>账号密码登录</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="loginForm.username" type="text" placeholder="用户名" required />
        <input v-model="loginForm.password" type="password" placeholder="密码" required />
        <button type="submit">登录</button>
      </form>

      <h2>人脸识别登录</h2>
      <button @click="faceLogin">人脸登录</button>
      <div class="toggle" @click="goToRegister">没有账号？点击注册</div>
    </div>

    <div style="flex-shrink: 0;">
      <video ref="videoRef" autoplay></video>
      <canvas ref="canvasRef" style="display:none;"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted ,onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store/user'  // ✅ 引入 userStore

const router = useRouter()
const userStore = useUserStore()

const loginForm = reactive({
  username: '',
  password: ''
})

const videoRef = ref(null)
const mediaStream = ref(null)

const canvasRef = ref(null)

onMounted(() => {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      mediaStream.value = stream // ✅ 赋值给 ref
      if (videoRef.value) {
        videoRef.value.srcObject = stream
      }
    })
    .catch(err => {
      ElMessage.error('摄像头访问失败：' + err.message)
    })
})

onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => {
      track.stop()
    })
    mediaStream.value = null
  }
})

const handleLogin = async () => {
  const result = await userStore.login(loginForm.username, loginForm.password)
  if (result.success) {
    ElMessage.success('登录成功')
    router.push('/')
  } else {
    ElMessage.error(result.message || '登录失败')
  }
}

const captureFaceBlob = () => {
  const canvas = canvasRef.value
  const context = canvas.getContext('2d')
  canvas.width = videoRef.value.videoWidth
  canvas.height = videoRef.value.videoHeight
  context.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height)
  return new Promise(resolve => {
    canvas.toBlob(blob => {
      resolve(blob)
    }, 'image/jpeg')
  })
}
const faceLogin = async () => {
  const blob = await captureFaceBlob()
  const formData = new FormData()
  formData.append('face_image', blob, 'face.jpg')


  try {
    const res = await fetch('/api/auth/face_login', {
      method: 'POST',
      body: formData
    })
    const data = await res.json()

    if (data.code === 200) {
      // 和 login 方法一样的保存逻辑
      const userData = {
        ...data.data,
        userId: data.data.user_id || data.data.userId
      }
      userStore.user = userData        // Pinia 状态
      localStorage.setItem('user', JSON.stringify(userData)) // 持久化
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error(data.message || '登录失败')
    }
  } catch (err) {
    ElMessage.error('登录异常：' + err.message)
  }
}


const goToRegister = () => {
  router.push('/register')
}
</script>



<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(to right, #f6d365, #fda085);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.container {
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  padding: 24px;
  display: flex;
  gap: 32px;
  max-width: 1000px;
}

.form-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-section h2 {
  color: #444;
}

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

button {
  padding: 10px;
  border: none;
  border-radius: 8px;
  background-color: #f67280;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background-color: #c06c84;
}

video, canvas {
  width: 100%;
  height: auto;
  max-width: 320px;
  border-radius: 12px;
  object-fit: cover;
}

.toggle {
  text-align: right;
  font-size: 14px;
  cursor: pointer;
  color: #888;
  text-decoration: underline;
}
</style>


