<template>
  <q-layout class="main" view="1Hh Lpr lFf">
    <q-header class="header" :elevated="false">
      <img class="header-logo" src="../assets/images/logo.png" style="width: 172.8px;height: auto;" />
      <div class="user-area">
        <div class="header-phone">{{ tel }}</div>
        <q-btn-dropdown flat round dense class="header-dropdown">
          <q-list>
            <q-item clickable v-close-popup @click="logout">
              <q-item-section>登出</q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
    </q-header>
    <q-page-container class="q-pa-md">
      <div class="home_container">
        <div class="interface">
          <div class="conversation">
            <el-scrollbar style="height: 100%;" ref="scrollbar">
              <div class="message" v-for="message in messages" :key="message.id">
                <div v-if="message.type === 'user'" class="user-message">
                  <div class="message-content">
                    {{ message.text }}
                  </div>
                  <img class="use_avatar" src="../assets/images/use.png" />
                </div>
                <div v-else-if="message.type === 'advertisement'" class="advertising-message">
                  <span>欢迎您点击下方链接体验我们研究院的产品</span>
                  <a href="https://zhiyong.ai4c.cn/" target="_blank">智多星AI</a>
                </div>
                <div v-else class="robot-message">
                  <img class="gpt_avatar" src="../assets/images/ai4c-icon.svg" />
                  <div v-if="message.status === 'text'" class="message-content">
                    {{ message.text }}
                  </div>
                  <div v-else-if="message.status === 'html'" class="message-content" v-html="htmltext">
                  </div>
                  <div v-else-if="message.status === 'generalQuestion'" class="questions">
                    <div class="questions general" v-if="generalQuestions.length > 0">
                      <div v-for="question in generalQuestions" :key="question.id" class="question">
                        <div v-if="question.type === 'MCQ'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text + " (多选)" }}</p>
                          <el-checkbox-group v-model="answersState.general.checked[question.id]">
                            <el-checkbox v-for="(option, index) in question.options" :value="option" :key="index">
                              {{ option }}
                            </el-checkbox>
                          </el-checkbox-group>
                        </div>
                        <div v-else-if="question.type === 'SCQ'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text + " (单选)" }}</p>
                          <el-radio-group v-model="answersState.general.scqAnswers[question.id]">
                            <el-radio v-for="option in question.options" :value="option" :key="option">
                              {{ option }}
                            </el-radio>
                          </el-radio-group>
                        </div>
                        <div v-else-if="question.type === 'short_answer'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text }}</p>
                          <el-input v-model="answersState.general.saAnswers[question.id]" class="sa_input" />
                        </div>
                      </div>
                      <button @click="submit" class="form_button">提交</button>
                    </div>
                  </div>
                  <div v-else-if="message.status === 'specializedQuestion'" class="questions">
                    <div class="questions specialized">
                      <div v-for="question in specializedQuestions" :key="`specialized-${question.id}`"
                        class="question">
                        <div v-if="question.type === 'MCQ'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text + " (多选)" }}</p>
                          <el-checkbox-group v-model="answersState.specialized.checked[question.id]">
                            <el-checkbox v-for="(option, index) in question.options" :value="option" :key="index">
                              {{ option }}
                            </el-checkbox>
                          </el-checkbox-group>
                        </div>
                        <div v-else-if="question.type === 'SCQ'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text + " (单选)" }}</p>
                          <el-radio-group v-model="answersState.specialized.scqAnswers[question.id]">
                            <el-radio v-for="option in question.options" :value="option" :key="option">
                              {{ option }}
                            </el-radio>
                          </el-radio-group>
                        </div>
                        <div v-else-if="question.type === 'short_answer'" class="question">
                          <p>{{ (question.id + 1) + ". " + question.text }}</p>
                          <el-input v-model="answersState.specialized.saAnswers[question.id]" class="sa_input" />
                        </div>
                      </div>
                      <button @click="getTimeTable" class="form_button">提交</button>
                    </div>
                  </div>
                  <div v-else-if="message.status === 'progress'" class="message-content progressdiv">
                    <span>{{ progressText }}</span>
                    <div class="loading">
                      <div></div>
                      <div></div>
                      <div></div>
                      <div></div>
                      <div></div>
                      <div></div>
                      <div></div>
                      <div></div>
                    </div>
                  </div>
                  <div v-else-if="message.status === 'table'" class="message-content">
                    <table>
                      <thead>
                        <tr>
                          <th>时间</th>
                          <th>活动</th>
                          <th>详情</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="activity in timetable" :key="activity.time">
                          <td>{{ activity.time }}</td>
                          <td>{{ activity.activity }}</td>
                          <td>{{ activity.description }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </div>
    </q-page-container>
    <q-footer style="background-color: #ffffff;height: auto;">
      <div class="input">
        <div class="input_container">
          <input class="user_input custom-input" v-model="input" :disabled="isInputDisabled"
            :autosize="{ minRows: 1, maxRows: 3 }" type="textarea" placeholder="Please input" resize=none
            @resize="adjustInputContainerHeight" size="large" :border="false" @keydown.enter.prevent="send" />
          <div class="btn" @click="send">
            <img class="input_icon" src="../assets/images/send.svg" alt="send SVG" />
          </div>
        </div>
      </div>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref, Ref } from 'vue';
import type { Question } from "../static/ts/Question";
import { Message } from '../static/ts/Message';
import { webSocketService } from '../static/ts/WebSocket';
import { Answer } from '../static/ts/Answer';
import axios, { AxiosResponse } from 'axios';
import "element-plus/dist/index.css"
import { useRouter } from 'vue-router';

const router = useRouter();
const tel = ref(localStorage.getItem('tel') || '');
const input = ref('');
const messages: Ref<Message[]> = ref<Message[]>([]);
const generalQuestions = ref<Question[]>([]);
const specializedQuestions = ref<Question[]>([]);
const companyName = ref('');
const timetable: Ref<Activity[]> = ref([]);

const answersState = ref({
  general: {
    checked: {} as Record<number, boolean[]>,
    scqAnswers: {} as Record<number, string | null>,
    saAnswers: {} as Record<number, string>,
  },
  specialized: {
    checked: {} as Record<number, boolean[]>,
    scqAnswers: {} as Record<number, string | null>,
    saAnswers: {} as Record<number, string>,
  },
});

const answers = ref<Answer[]>([]);
const endpoint = ref('getGeneralQuestion');
const htmltext = ref("");
const progressText = ref("正在为您生成专属问卷，请稍候...")
const isInputDisabled = ref(false);
const isBtnDisabled = ref(false);
const targetUrl = "https://api.consultant.ai4c.cn/"
// const targetUrl = "http://localhost:5200/"

let step = 0;
let purpose = "";


const send = () => {
  if (isBtnDisabled.value) {
    return;
  }
  if (!input.value) {
    alert("输入不能为空");
    isInputDisabled.value = false;
    return;
  }
  purpose = "additionalQuery"

  var tem = input.value.trim()
  input.value = ''
  messages.value.push({ id: messages.value.length, type: "user", status: "text", text: tem });
  nextTick(() => { scrollToBottom() });
  isInputDisabled.value = true;
  isBtnDisabled.value = true;
  console.log("test1");
  if (webSocketService.isConnected) {
    webSocketService.sendMessage({ "user_message": tem, "purpose": purpose, "telephone": tel.value });
  } else {
    console.error('WebSocket is not ready to send message.');
    return;
  }
  messages.value.push({ id: messages.value.length, type: 'robot', status: "text", "text": '' });
  

  console.log("test2");
}

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('tel');
  router.push('/login');
};

let updating = false;

const handleMessage = async (message: string) => {
  if (updating) {
    console.log('Update in progress, skipping...');
    return;
  }
  updating = true;
  
  messages.value[messages.value.length - 1].text += message;
  await nextTick();
  scrollToBottom();

  updating = false;
};

async function axios_send(answers?: Answer[]): Promise<void> {
  try {
    var response;
    if (answers) {
      const dataToSend = {
        answers: answers,
        telephone: tel.value
      };
      isInputDisabled.value = true;
      isBtnDisabled.value = true;
      messages.value.push({ id: messages.value.length, type: 'robot', status: "progress" });
      nextTick(() => { scrollToBottom() });

      await axios.post(targetUrl + 'getSpecializedQuestion', dataToSend).then((response) => {
        addandPop();
        loadQuestions(response);
        isInputDisabled.value = false;
        isBtnDisabled.value = false;
      });
    } else {
      response = await axios.post(targetUrl + endpoint.value, { "company_name": companyName.value, "telephone": tel.value });
      messages.value.push({ id: messages.value.length, type: 'robot', status: "generalQuestion" });
      loadQuestions(response);
    }
  } catch (error) {
    console.error(error);
    isInputDisabled.value = false;
  }
}

const loadQuestions = async (response: AxiosResponse<any, any>) => {
  const newQuestions: Question[] = response.data
  let type: "general" | "specialized" = "general";
  console.log(step)
  if (step === 0) {
    generalQuestions.value = newQuestions;
  } else {
    specializedQuestions.value = newQuestions;
    type = "specialized"
  }

  newQuestions.forEach(question => {
    answersState.value[type].checked[question.id] = [];
    answersState.value[type].scqAnswers[question.id] = null;
    answersState.value[type].saAnswers[question.id] = '';
  });
  console.log(answersState.value)
  step++;
};


var tem = 0;
const gain = () => {
  const getAnswerState = (questionId: number, questionType: 'SCQ' | 'MCQ' | 'short_answer', isSpecialized: boolean) => {
    const type = isSpecialized ? 'specialized' : 'general';
    switch (questionType) {
      case 'SCQ':
        return answersState.value[type].scqAnswers[questionId] ?? "未作答";
      case 'MCQ':
        const mcqIndexes = answersState.value[type].checked[questionId];
        return mcqIndexes && mcqIndexes.length > 0 ? mcqIndexes.map(index => index.toString()) : ["未作答"];
      case 'short_answer':
        const shortAnswer = answersState.value[type].saAnswers[questionId];
        return shortAnswer !== "" ? shortAnswer : "未作答";
      default:
        return "未作答";
    }
  };

  const allQuestions = [...generalQuestions.value, ...specializedQuestions.value];
  let answeredQuestions = 0;

  answers.value = allQuestions.map((question) => {
    const isSpecialized = specializedQuestions.value.includes(question);
    const answerDisplay = getAnswerState(question.id, question.type, isSpecialized);
    const answerString = Array.isArray(answerDisplay) ? answerDisplay.join(", ") : answerDisplay;

    if (answerString && answerString !== "未作答" && answerString.trim() !== "") {
      answeredQuestions++;
    }

    if (question.type === 'MCQ') {
      return {
        subject: question.text,
        answers: answerDisplay,
        type: question.type
      };
    } else {

      return {
        subject: question.text,
        answer: answerDisplay,
        type: question.type
      };
    }
  });

  return answeredQuestions
}


const submit = () => {
  tem = gain()
  if (tem === 0) {
    messages.value.push({
      id: messages.value.length,
      type: 'robot',
      status: "text",
      text: "请先回答问卷"
    });
    nextTick(() => { scrollToBottom() });
  } else {
    axios_send(answers.value);
  }
};


interface Activity {
  time: string;
  activity: string;
  description: string;
}

const getTimeTable = () => {
  isInputDisabled.value = true;
  if ((gain() - tem) === 0) {
    messages.value.push({
      id: messages.value.length,
      type: 'robot',
      status: "text",
      text: "请先回答问卷"
    });
  } else {

    progressText.value = "正在为您生成Timetable，请稍后~";
    messages.value.push({ id: messages.value.length, type: 'robot', status: "progress" });
    nextTick(() => { scrollToBottom() });
    axios.post(targetUrl + 'getTimetable', { questions: answers.value, telephone: tel.value })
      .then(response => {
        const result: Activity[] = response.data.timetable;
        timetable.value = result;
        messages.value = messages.value.filter(message => message.status !== "progress");
        messages.value.push({ id: messages.value.length, type: 'robot', status: "table" });
        messages.value.push({ id: messages.value.length, type: 'advertisement', status: "saas" })
        isInputDisabled.value = false;
      })
      .catch(error => {
        console.error('Error fetching timetable:', error);
        isInputDisabled.value = false;
      });
  }
}



const addandPop = () => {
  setTimeout(() => {
    messages.value.pop()
    messages.value.push({ id: messages.value.length, type: 'robot', status: "specializedQuestion" });
    isInputDisabled.value = false;
  }, 1000);
}



onMounted(async () => {
  messages.value.push({ id: 0, type: "robot", text: "\t尊敬的参与者，您好！我们是一家专注于人工智能垂直领域应用落地的研究院，此问卷由我们精心设计。在当今商业环境中，AI技术正成为企业转型升级的重要驱动力。为了更好地理解企业对AI技术的需求和期望，我们特此开展此项深度调查。我们诚邀您分享您的见解，您的反馈将帮助我们为您提供更加精准和有效的AI解决方案，助力您的企业在市场中保持竞争力。我们重视您的时间和经验，承诺所有收集到的信息将被严格保密，并仅用于提升我们的服务质量。\n\t通过参与此次调查，您将有机会深入了解AI技术如何优化您的业务流程，提高运营效率，并探索新的增长机会。请根据您的实际经验，详细且真实地回答以下问题。您的参与对我们至关重要，感谢您的宝贵时间和支持！", status: "text" });
  webSocketService.beforeConnected(loadGeneralQuestion);
  webSocketService.connect(tel.value);
  webSocketService.setRecoveryHandle(recovery);
  webSocketService.setMessageHandler(handleMessage);
});




const loadGeneralQuestion = async () => {
  try {
    const response = await axios.post(targetUrl + 'getCompanyNameByTelephone', { telephone: tel.value });
    if (response.data.status === 200) {
      companyName.value = response.data.companyName;
      axios_send();
    } else {
      console.error('Error:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching company name:', error);
  }
}



const handleSocketMessage = (message: string) => {
  htmltext.value += message;
  nextTick(() => scrollToBottom());
};



const scrollToBottom = () => {
  const scrollbar = document.querySelector('.el-scrollbar__wrap');
  if (scrollbar) {
    scrollbar.scrollTop = scrollbar.scrollHeight;
  }
};

const adjustInputContainerHeight = () => {
  const inputContainer = document.querySelector('.input_container');
  const elInput = document.querySelector('.el-input__inner');
  const homeContainer = document.querySelector('.home_container');
  if (inputContainer && elInput && homeContainer) {
    (inputContainer as HTMLElement).style.height = `${(elInput as HTMLElement).offsetHeight}px`;
    requestAnimationFrame(() => {
      homeContainer.scrollTo(0, homeContainer.scrollHeight);
    });
  }
};


const recovery = () => {
  isInputDisabled.value = false;
  isBtnDisabled.value = false;
}


defineOptions({
  name: 'MainLayout'
});

</script>





<style>
@import "../static/css/interface.css";
@import "../static/css/top.css";
@import "../static/css/input.css";

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

.home_container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background-color: #fffffff5;
}

.question {
  width: auto;
  height: 30%;
}

.questions {
  display: flex;
  flex-direction: column;
  width: auto;
  max-width: 90%;
  background-color: hsl(270, 18%, 96%);
  border-radius: 8px;
  padding: 10px;
  word-wrap: break-word;
  font-size: 18px;
}

.radio {
  width: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.radio /deep/ .el-radio__label {
  color: rgb(75, 75, 75);
  font-size: 15px !important;
}

.q-layout {
  height: 100%;
}

.q-page-container {
  height: 100%;
}

.q-layout--standard {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.q-header {
  height: 5%;
}

.q-pa-md {
  height: 94%;
  padding-bottom: 10px !important;
  padding: 16px 3px 5px 10px
}

.is-vertical {
  display: block !important;
}
</style>
