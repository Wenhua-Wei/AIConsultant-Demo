<template>
  <q-header class="header" :elevated="false">
    <img class="header-logo" src="../assets/images/logo.png" style="width: 172.8px; height: 32px;" />
    <div class="user-area">
      <div class="header-phone">{{ tel }}</div>
 
      <q-btn-dropdown flat round dense class="header-dropdown">
        <q-list>
          <q-item clickable v-close-popup>
            <q-item-section @click="goToXiaoshouPage">聊天页面</q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="logout">
                        <q-item-section>登出</q-item-section>
                    </q-item>
        </q-list>
      </q-btn-dropdown>
    </div>
  </q-header>
  <div class="q-pa-xs table">
    <q-markup-table separator="cell" flat bordered>
      <thead>
        <tr>
          <th class="text-center">公司名</th>
          <th class="text-center">客户名</th>
          <th class="text-center">职位</th>
          <th class="text-center">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in paginatedItems" :key="index">
          <td class="text-center">{{ item.company }}</td>
          <td class="text-center">{{ item.name }}</td>
          <td class="text-center">{{ item.position }}</td>
          <td class="text-center">
            <!-- 添加您的操作按钮或链接 -->
            <q-btn label="查看" @click="viewDetails(item.telephone)" />
          </td>
        </tr>
      </tbody>
    </q-markup-table>
    <q-pagination v-model="currentPage" :max="maxPages"  unelevated   color="black"  active-color="purple" direction-links  @update:model-value="updatePage" class="pagination-right" />
  </div>
</template>

<script setup lang="ts">
import { getUsers } from 'src/api';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';



const router = useRouter(); // 在这里调用
const tel = localStorage.getItem('tel') || '';

const logout = () => {
     // 清除本地存储的 token
     localStorage.removeItem('token');
     localStorage.removeItem('tel');
    // 导航到登录页面
    router.push('/login');
};

interface User {
  company: string;
  name: string;
  position: string;
  telephone:string;
}

const items = ref<User[]>([]);

const viewDetails = (telephone: string): void => {
  if (telephone) {
    console.log(telephone)
    router.push({ path: `/detail/${encodeURIComponent(telephone)}` });
  } else {
    console.error('Company not found!');
  }
};


const currentPage = ref(1);
let rowsPerPage = ref(5); // 默认为移动端每页5条

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  const end = start + rowsPerPage.value;
  return items.value.slice(start, end);
});

const maxPages = computed(() => Math.ceil(items.value.length / rowsPerPage.value));

const updatePage = (val: number) => {
  currentPage.value = val;
};

const goToXiaoshouPage = () => {
  router.push('xiaoshou');
};


// 根据屏幕宽度设置每页显示的行数
onMounted(async () => {
  // 根据屏幕宽度设置每页显示的行数
  const mediaQuery = window.matchMedia('(min-width: 768px)');
  if (mediaQuery.matches) {
    rowsPerPage.value = 10; // 在大屏幕（PC）上每页显示10条
  }

  try {
    const data = await getUsers();
    items.value = data.users.map((user: { company_name: string; name: string; position: string; telephone:string}) => ({
      company: user.company_name,
      name: user.name,
      position: user.position,
      telephone:user.telephone
      // 根据你的需求修改上述属性
    }));
  } catch (error) {
    console.error('Error fetching users:', error);
  }


});
</script>

<style scoped>
.header {
    display: flex;
    background-color: #ffffff;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 10px 12px;
}

.user-area {
  display: flex;
  align-items: center;
  color: rgba(0, 0, 0, 1);
  font-family: Alimama FangYuanTi VF;
  font-size: 14px;
  font-weight: 500;
}

.table {
  margin-top: 30px;
}

@media (min-width: 768px) {

  /* PC 端样式 */
  .table {
    width: 70%;
    /* 设置表格容器宽度为 80% */
    margin: 30px auto;
    /* 水平居中 */
  }
}

.q-markup-table .q-btn[data-v-0d2f6450] {
  color: black !important;
}


.q-markup-table .q-btn[data-v-0d2f6450]:before {
  box-shadow: none !important;
  background-color: #f3f4f6 !important;
}

.pagination-right {
  justify-content: flex-end;
  margin-top: 10px;
}
</style>