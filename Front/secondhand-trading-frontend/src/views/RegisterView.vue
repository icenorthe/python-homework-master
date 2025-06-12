/* RegisterView.vue */
<template>
  <div class="container">
    <div class="form-section">
      <h2>注册</h2>
      <form @submit.prevent="register">
        <input v-model="registerForm.username" type="text" placeholder="用户名" required />
        <input v-model="registerForm.password" type="password" placeholder="密码" required />
        <button type="submit">注册</button>
      </form>
      <div class="toggle" @click="goToLogin">已有账号？返回登录</div>
    </div>

    <div style="flex-shrink: 0;">
      <video ref="videoRef" autoplay></video>
      <canvas ref="canvasRef" style="display:none;"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted ,onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store/user';

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter();
    const userStore = useUserStore();
    const registerForm = reactive({ username: '', password: '' });
    const videoRef = ref(null);
    const mediaStream = ref(null);
    const canvasRef = ref(null);

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
    

    const captureFaceBlob = () => {
      const canvas = canvasRef.value;
      const context = canvas.getContext('2d');
      canvas.width = videoRef.value.videoWidth;
      canvas.height = videoRef.value.videoHeight;
      context.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height);
      return new Promise(resolve => {
        canvas.toBlob(blob => {
          resolve(blob);
        }, 'image/jpeg');
      });
    };

    const register = async () => {
      const faceBlob = await captureFaceBlob();
      const formData = new FormData();
      formData.append('username', registerForm.username);
      formData.append('password', registerForm.password);
      formData.append('image', faceBlob, 'face.jpg');

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        if (data.success) {
          alert('注册成功');
          router.push('/login');
        } else {
          alert(data.message || '注册失败');
        }
      } catch (err) {
        alert('注册失败：' + err.message);
      }
    };

    const goToLogin = () => {
      router.push('/login');
    };

    return {
      registerForm,
      videoRef,
      canvasRef,
      register,
      goToLogin
    };
  }
};
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
