import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    {
/*       name: 'mock-api',
      configureServer(server) {
        // 模拟API响应
        server.middlewares.use((req, res, next) => {
          // 只处理/api开头的请求
          if (!req.url.startsWith('/api')) {
            return next();
          }

          // 设置响应头
          res.setHeader('Content-Type', 'application/json');
          
          // 处理不同的API路径
          if (req.url === '/api/products' || req.url.startsWith('/api/products?')) {
            return res.end(JSON.stringify({
              code: 200,
              message: 'success',
              data: products
            }));
          }
          
          if (req.url.startsWith('/api/products/')) {
            const id = parseInt(req.url.split('/').pop());
            const product = products.find(p => p.id === id);
            
            if (product) {
              return res.end(JSON.stringify({
                code: 200,
                message: 'success',
                data: product
              }));
            } else {
              res.statusCode = 404;
              return res.end(JSON.stringify({
                code: 404,
                message: '商品不存在'
              }));
            }
          }
          
          if (req.url.startsWith('/api/search')) {
            const url = new URL(req.url, 'http://localhost:3000');
            const keyword = url.searchParams.get('keyword') || '';
            
            const filteredProducts = products.filter(p => 
              p.title.includes(keyword) || 
              p.description.includes(keyword) || 
              p.category.includes(keyword)
            );
            
            return res.end(JSON.stringify({
              code: 200,
              message: 'success',
              data: {
                products: filteredProducts
              }
            }));
          }
          
          if (req.url === '/api/auth/login' && req.method === 'POST') {
            // 简单模拟登录，任何用户名密码组合都会成功
            const user = users[0];
            
            return res.end(JSON.stringify({
              code: 200,
              message: '登录成功',
              data: {
                user_id: user.id,
                username: user.username,
                email: user.email,
                avatar: user.avatar,
                token: 'mock_token_' + Date.now()
              }
            }));
          }
          
          if (req.url === '/api/auth/register' && req.method === 'POST') {
            return res.end(JSON.stringify({
              code: 200,
              message: '注册成功'
            }));
          }
          
          // 默认返回404
          res.statusCode = 404;
          res.end(JSON.stringify({
            code: 404,
            message: 'API not found'
          }));
        });
      } */
    }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      // 配置代理规则
      '/api': {
        target: 'http://localhost:8081',
        changeOrigin: true,
        headers: {
          Connection: 'keep-alive'
        }
      },
      // 处理Python服务的代理（如果需要）
/*       '/python': {
        target: 'http://localhost:5000', // Python服务地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/python/, '')
      } */
    }
  }
})