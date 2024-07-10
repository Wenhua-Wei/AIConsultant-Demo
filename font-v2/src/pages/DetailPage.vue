<template>
  <q-header class="header" :elevated="false">
    <img class="header-logo" src="../assets/images/logo.png" style="width: 172.8px;height: auto;" />
    <div class="user-area">
      <div class="header-phone">{{ tel}}</div>
      <q-btn-dropdown flat round dense class="header-dropdown">
        <q-list>
          <q-item clickable v-close-popup>
            <q-item-section>客户信息</q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="logout">
            <q-item-section>登出</q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </div>
  </q-header>
  <!-- 返回按钮 -->
  <q-btn flat label="返回" @click="goBack" class="back-button" />
   <!-- 展开项 -->
   <q-expansion-item class="custom-expansion-item" @before-show="question">
    <template v-slot:header>
      <q-item-section avatar>
        <q-avatar>
          <img src="../../public/ai4clogo.ico">
        </q-avatar>
      </q-item-section>
      <q-item-section>
        问答情况
      </q-item-section>
    </template>
    <q-card>
      <q-card-section>
        <div v-for="(item, index) in questions" :key="index" class="question-container">
          <!-- 问题标题和内容在同一行显示 -->
          <div class="flex-container">
            <div class="question-title"><strong>问题{{ index + 1 }}:</strong></div>
            <div class="question-text">{{ item.question }}</div>
          </div>
          <!-- 根据问题类型动态显示答案 -->
          <div class="answers">
            <strong>回答:</strong>
            <template v-if="item.question_type === 'SCQ'">
              <!-- SCQ类型答案在同一行显示 -->
              <span class="inline-answer">{{ item.answer[0] }}</span>
            </template>
            <template v-else-if="item.question_type === 'short_answer'">
              <span class="inline-answer">{{ item.answer[0] }}</span>
            </template>
            <template v-else>
              <!-- MCQ类型答案分点显示 -->
              <ul>
                <li v-for="(answer, ansIndex) in item.answer" :key="ansIndex">
                  {{ answer }}
                </li>
              </ul>
            </template>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>

  <q-expansion-item class="custom-expansion-item" @before-show="Timetable">
    <template v-slot:header>
      <q-item-section avatar>
        <q-avatar>
          <img src="../../public/ai4clogo.ico">
        </q-avatar>
      </q-item-section>

      <q-item-section>
        Design Thinking Timetable
      </q-item-section>
    </template>

    <q-page padding>
      <q-card>
  <q-card-section>
    <div class="q-pa-xs row justify-center">
      <div>
        <table class="q-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>活动</th>
              <th>详情</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in timetable" :key="index">
              <td>{{ item.time }}</td>
              <td>{{ item.activity }}</td>
              <td>
                <div v-if="$q.screen.lt.md">
                  <q-btn icon="visibility" @click="viewDetails(item)" dense flat round color="primary" />
                </div>
                <div v-else>
                  <div v-if="item.description">
                    {{ item.description }}
                  </div>
                  <div v-else>
                    无详情
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </q-card-section>
</q-card>
<!-- 对话框组件 -->
<q-dialog v-model="detailsDialog">
      <q-card>
        <q-card-section class="row items-center">
          <div class="text-h6">{{ selectedItem.activity }}</div>
        </q-card-section>
        <q-card-section>
          <div><strong>时间:</strong> {{ selectedItem.time }}</div>
          <div class="flex-container">
  <div class="activity-title"><strong>活动详情:</strong></div>
  <div class="activity-description">{{ selectedItem.description }}</div>
</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="关闭" color="negative" @click="detailsDialog = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
</q-page>

  </q-expansion-item>
</template>

<script setup lang="ts">

let customerTel="";

interface Question {
  answer: string[]; // answer 属性是一个字符串数组
  question: string;
  question_id: number;
  question_type: string;
}
import { selectQuestionsByTel, selectTimetableByTel } from 'src/api';
import { ref, watch ,onMounted} from 'vue';
import { useRouter,useRoute } from 'vue-router';

interface Activity {
  time: string;
  activity: string;
  description:string;
}

const router = useRouter();
const route=useRoute();
const tel = localStorage.getItem('tel') || '';

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('tel');
  router.push('/login');
};

// 初始化时间表数据
const timetable = ref<Activity[]>([]); // 将前端时间表也初始化为空数组

const question=async () => {
  try {
    const response = await selectQuestionsByTel(customerTel); // 调用接口函数获取问答数据
    questions.value = response.questions; // 将接口返回的问答数据赋值给 questions
  } catch (error) {
    console.error('获取问答数据失败：', error);
  }
}

const Timetable=async () => {
  try {
    const response = await selectTimetableByTel(customerTel);
    timetable.value = response.timetable; 
  } catch (error) {
    console.error('获取timetable数据失败：', error);
  }
}

// 自动保存时间表到localStorage或发送到服务器
watch(timetable, (newTimetable) => {
  localStorage.setItem('timetable', JSON.stringify(newTimetable));
  // 或者发送到服务器...
}, { deep: true });

const detailsDialog = ref(false);
const selectedItem = ref<Activity>({ time: '', activity: '' ,description:''});

const goBack = () => {
  router.go(-1);
};

const viewDetails = (item: Activity) => {
  selectedItem.value = item;
  detailsDialog.value = true;
};

// 问答数据
const questions = ref<Question[]>([]);

// 页面加载时调用接口获取问答数据
onMounted(()=>{
  customerTel = route.params.telephone as string;
  console.log(customerTel)
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

.back-button {
  margin-top: 20px;
  /* 根据需要调整按钮位置 */
}

.custom-expansion-item {
  width: 85%;
  margin: 30px auto;
}

@media (max-width: 768px) {
  .custom-expansion-item {
    width: 85%;
    margin: 0 auto;
  }
}

.q-table th,
.q-table td {
  text-align: center;
}

@media (max-width: 599px) {
  .q-input {
    font-size: 14px;
  }
}

.flex-container {
  display: flex;
  align-items: baseline;
}

.question-title {
  white-space: nowrap;
  margin-right: 8px;
}

.question-text {
  white-space: pre-wrap;
  flex-grow: 1;
}

.answers {
  margin-top: 2px;
  margin-bottom: 10px;

}

.inline-answer {
  display: inline-block;
  margin-left: 4px;
}

.flex-container {
  display: flex;
  align-items: baseline; /* 确保基线对齐 */
  width: 100%; /* 确保容器可以占满全部宽度 */
}

.activity-title {
  white-space: nowrap; /* 防止标题换行 */
  margin-right: 4px; /* 标题和内容之间的间距 */
}

.activity-description {
  white-space: pre-wrap; /* 允许内容自然换行 */
  flex-grow: 1; /* 允许内容区域填充额外空间 */
}
</style>
