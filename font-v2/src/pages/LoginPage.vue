<template>
  <q-page v-if="false" class="flex flex-center">
    <img src="../../public/icons/logo.png" alt="Logo" class="logo" />
    <q-card class="q-pa-xs" style="width: 300px">
      <q-card-section>
        <div class="text-h6">登录</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="onSubmit">
          <q-input filled v-model="login.phonenumber" label="手机号" mask="###########" :rules="phoneRules" required
            @keyup.enter="onSubmit" type="tel" style="margin-bottom:3%"/>
          <q-input filled v-model="login.identification" label="验证码" mask="###########" :rules="phoneRules" required
            @keyup.enter="onSubmit" type="text" />
          <div class="q-mt-md">
            <q-btn label="登录" type="submit" color="primary" style="display: flex; width: 100%;" />
          </div>
        </q-form>
      </q-card-section>
      <q-card-section align="right">
        <q-btn flat label="注册账号" @click="goToRegister" color="primary" />
      </q-card-section>
    </q-card>
  </q-page>
  <verify></verify>
</template>

<script lang="ts">
import { loginUser } from 'src/api';
import { defineComponent } from 'vue';
import verify from '../components/ verify.vue';

export default defineComponent({
  data() {
    return {
      login: {
        phonenumber: '',
        identification: ''
      },
    };
  },
  setup() {
    // 定义手机号验证规则
    const phoneRules = [
      (val: string) => val.length === 11 || '请输入正确的手机号',
    ];

    return {
      phoneRules,
    };
  },
  methods: {
    async onSubmit(): Promise<void> {
      try {
        // 验证手机号是否满足要求
        if (this.login.phonenumber.length !== 11) {
          this.$q.notify({
            message: '请输入正确的手机号',
            color: 'negative',
            position: 'bottom'
          });
          return; // 如果手机号不符合要求，停止后续操作
        }

        var response = await loginUser({ telephone: this.login.phonenumber })
        if (response.data.status === 1001) {
          this.$q.notify({
            message: '账号不存在，请先注册',
            color: 'negative',
            position: 'top',
          });
          this.login.phonenumber = '';
          return;
        }

        // 获取返回数据中的 UserType 属性
        const userType = response.data.UserType;

        // 根据 UserType 进行页面跳转
        switch (userType) {
          case 0:
            // 跳转到 UserType 为 1 的页面
            this.$router.push('kehu');
            break;
          case 1:
            this.$router.push('xiaoshou');
            break;
          // 可以根据需要添加更多的情况
          default:
            // 默认情况下跳转到某个通用页面或执行其他逻辑
            break;
        }


        // 获取当前时间作为 token
        const currentTime = new Date().toISOString();

        // 将 token 存储到本地存储中
        localStorage.setItem('token', currentTime);

        // 将手机号存储到本地存储中
        const tel = this.login.phonenumber;
        localStorage.setItem('tel', tel);

        // 在这里处理其他登录成功后的逻辑，比如跳转到其他页面或执行其他操作
      } catch (error) {
        console.error('An error occurred during login:', error);
      }
    },
    goToRegister(): void {
      this.$router.push('register');
    },
    notifyAccountNotFound() {
      this.$q.notify({
        message: '账号不存在，请先注册',
        color: 'negative',
        position: 'bottom',
      });
      this.$router.push('/register'); // 确保这里是正确的路由
    },
  },
});
</script>


<style>
.logo {
  position: absolute;
  max-width: 300px;
  height: auto;
}

.q-layout{
    width:100%;
    height:100%;
}

.q-page-container{
    width: 100% ;
    height: 100%;
}


@media only screen and (max-width: 768px) {

  /* Mobile devices */
  .logo {
    top: 60px;
  }
}

@media only screen and (min-width: 769px) {

  /* Desktop devices */
  .logo {
    top: 25px;
    left: 25px;
  }
}
</style>