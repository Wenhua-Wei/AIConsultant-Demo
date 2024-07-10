<template>
  <q-page class="flex flex-center">
    <img src="../../public/icons/logo.png" alt="Logo" class="logo" />
    <q-card class="q-pa-xs" style="width: 300px">
      <q-card-section>
        <div class="text-h6">注册</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="onSubmit">
          <q-input filled v-model="register.telephone" label="手机号" mask="###########" :rules="phoneRules" dense required
            @keyup.enter="onSubmit" type="tel" />
          <q-input filled v-model="register.compName" dense label="公司名" required style="margin-bottom: 20px;" />
          <q-input filled v-model="register.ID" dense label="AI4C员工ID (选填)" />
          <div class="q-mt-md">
            <q-btn label="注册" type="submit" color="primary" style="display: flex; width: 100%;" />
          </div>
        </q-form>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn label="返回登录" color="secondary" @click="goToLogin" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { registerUser } from '../api'

export default defineComponent({
  data() {
    return {
      register: {
        telephone: '',
        compName: '',
        ID: '',
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
  computed: {
    isPhoneNumberValid(): boolean {
      return /^\d+$/.test(this.register.telephone);
    }
  },
  methods: {
    async onSubmit(): Promise<void> {
      try {
        var response = await registerUser(this.register);

        if (response.data.msg === 'True') {
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
          const tel = this.register.telephone;
          localStorage.setItem('tel', tel);
        }else{
          this.register.telephone='';
          this.register.compName='';
          this.register.ID='';
          alert("账号已存在，请直接登录");
          this.$router.push('/login');
        }
      } catch (error) {
        // 处理注册失败的逻辑
      }
    },
    goToLogin(): void {
      // 返回登录页面逻辑
      this.$router.push('/login');
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

@media only screen and (max-width: 767px) {

  /* Mobile devices */
  .logo {
    top: 25px;
  }
}

@media only screen and (min-width: 768px) {

  /* Desktop devices */
  .logo {
    top: 25px;
    left: 25px;
  }
}
</style>