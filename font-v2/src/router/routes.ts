import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') },
      { path: 'login', component: () => import('pages/LoginPage.vue') }, // 添加登录页面的路由
      { path: 'register', component: () => import('pages/RegisterPage.vue') }, // 添加注册页面的路由
      { path: 'chatlog', component: () => import('pages/ChatLog.vue') }, // 添加聊天记录页面的路由
      { path: 'detail/:telephone', component: () => import('pages/DetailPage.vue'), name: 'detail' }, // 添加详情页的路由
      { path: 'xiaoshou', component: () => import('pages/XiaoshouPage.vue') }, // 注册 XiaoshouPage 页面
      { path: 'kehu', component: () => import('pages/CustomerPage.vue') }, // 注册 XiaoshouPage 页面
    ],
  },

  // 捕获所有未匹配路径（404页面）
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'), // 确保文件名与实际组件文件名匹配
  },
];

// 添加全局的路由守卫
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (token) {
    const expirationTime = new Date(token);
    expirationTime.setHours(expirationTime.getHours() + 24); // 添加24小时
    const currentTime = new Date();
    if (currentTime > expirationTime) {
      // token 过期，重定向到登录页面
      next('/login');
    } else {
      // token 未过期，继续导航
      next();
    }
  } else {
    // token 不存在，重定向到登录页面
    next('/login');
  }
});

export default routes;
