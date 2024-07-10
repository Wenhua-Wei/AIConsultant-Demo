<template>
  <q-layout class="main" view="1Hh Lpr lFf">
    <q-header class="header" :elevated="false">
      <img class="header-logo" src="../assets/images/logo.png" style="width: 172.8px;height: auto;" />
      <div class="user-area">
        <div class="header-phone">{{ tel }}</div>
        <q-btn-dropdown flat round dense class="header-dropdown">
          <q-list>
            <q-item clickable v-close-popup @click="goToChatLog">
              <q-item-section>客户信息</q-item-section>
            </q-item>
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
                <div v-else class="robot-message">
                  <img class="gpt_avatar" src="../assets/images/ai4c-icon.svg" />
                  <div v-if="message.status === 'text'" class="message-content">
                    {{ message.text }}
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
          <input class="user_input custom-input" v-model="input" :disabled="isInputDisabled" type="textarea"
            placeholder="Please input" @resizez="adjustInputHeight" size="large" :border="false"
            @keydown.enter.prevent="send" autosize="{ minRows: 1, maxRows: 3 }" />
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
import { useRouter } from 'vue-router';


const tel = ref(localStorage.getItem('tel') || '');
const router = useRouter();

const input = ref('');
const messages: Ref<Message[]> = ref<Message[]>([]);
const generalQuestions = ref<Question[]>([]);
const specializedQuestions = ref<Question[]>([]);
const progressText = ref("稍等，正在检索生成...")
var start: number, end: number;
const isInputDisabled = ref(false);
const isBtnDisabled = ref(false);

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

const targetUrl = "https://api.consultant.ai4c.cn/"
// const targetUrl = "http://localhost:5200/"
const endpoint = ref('');
const htmltext = ref("");
let purpose = "";
let step = 0;




const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('tel');
  router.push('/login');
};

const goToChatLog = () => {
  router.push('/chatlog');
};



const send = async () => {
  if (isBtnDisabled.value) {
    return;
  }
  isInputDisabled.value = true;
  isBtnDisabled.value = true;
  switch (step) {
    case 0:
      endpoint.value = "clientInfo";
      purpose = "collect"
      break;
    case 1:
      endpoint.value = "keywords";
      purpose = "isKeywords"
      break;
    case 2:
      endpoint.value = "requirements";
      purpose = "requirementlists"
      break;
    case 3:
      purpose = "additionalQuery";
      break;
    default:
      purpose = "additionalQuery";
      step = 3;
      break;
  }


  if (!input.value) {
    alert("输入不能为空");
    isInputDisabled.value = false;
    isBtnDisabled.value = false;
    return;
  }
  const user_input = input.value;
  messages.value.push({ id: messages.value.length, type: 'user', text: input.value, status: "text" });
  nextTick(() => scrollToBottom());
  input.value = '';
  if (step === 0) {
    messages.value.push({ id: messages.value.length, type: 'robot', status: "progress" });
    const telephone = tel.value;
    axios.post(targetUrl + endpoint.value, { user_input, purpose, telephone }).then((response) => {
      messages.value = messages.value.filter(message => message.status !== "progress");
      messages.value.push({ id: messages.value.length, type: 'robot', status: "text", text: response.data.message })
      step++;
      isInputDisabled.value = false;
      isBtnDisabled.value = false;
    })
  } else if (step === 1) {
    messages.value.push({ id: messages.value.length, type: 'robot', status: "progress" });
    nextTick(() => scrollToBottom());
    const telephone = tel.value;
    axios.post(targetUrl + endpoint.value, { "user_message": user_input, purpose, telephone });
  }
  else if (step === 2) {
    messages.value.push({ id: messages.value.length, type: 'robot', status: "progress" });
    if (webSocketService.isConnected) {
      webSocketService.sendMessage({ "user_message": user_input, "purpose": "requirementlists", "telephone": tel.value });
    } else {
      console.error('WebSocket is not ready to send message.');
      isInputDisabled.value = false;
      isBtnDisabled.value = false;
      return;
    }
  }
  else if (step == 3) {
    webSocketService.sendMessage({ "user_message": user_input, "purpose": purpose, "telephone": tel.value });
    messages.value.push({ id: messages.value.length, type: 'robot', status: "text", "text": '' });
  }

}



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

const addandPop = () => {
  setTimeout(() => {
    messages.value.pop();
    messages.value.push({ id: messages.value.length, type: 'robot', status: "text", text: "" });
  }, 1000);
};



async function axios_send(answers?: Answer[]): Promise<void> {
  try {
    var response;
    if (answers) {
      response = await axios.post(targetUrl + 'getSpecializedQuestion', answers);
      messages.value.push({ id: messages.value.length, type: 'robot', status: "specializedQuestion" });
    } else {
      response = await axios.post(targetUrl + endpoint.value);
      messages.value.push({ id: messages.value.length, type: 'robot', status: "generalQuestion" });
    }
    loadQuestions(response);
  } catch (error) {
    console.error(error);
  }
}

const loadQuestions = async (response: AxiosResponse<any, any>) => {
  const newQuestions: Question[] = response.data
  let type: "general" | "specialized" = "general";
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
  step++;
};

const recovery = () => {
  isInputDisabled.value = false;
  isBtnDisabled.value = false;
}

const submit = () => {
  const getAnswerState = (questionId: number, questionType: 'SCQ' | 'MCQ' | 'short_answer', isSpecialized: boolean) => {
    const type = isSpecialized ? 'specialized' : 'general';
    switch (questionType) {
      case 'SCQ':
        return answersState.value[type].scqAnswers[questionId] ?? "未作答";
      case 'MCQ':
        const mcqIndexes = answersState.value[type].checked[questionId];
        return mcqIndexes && mcqIndexes.length > 0 ? mcqIndexes.join(", ") : "未作答";
      case 'short_answer':
        return answersState.value[type].saAnswers[questionId] ?? "未作答";
      default:
        return "未作答";
    }
  };

  const allQuestions = [...generalQuestions.value, ...specializedQuestions.value];
  answers.value = allQuestions.map((question) => {
    const isSpecialized = specializedQuestions.value.includes(question);
    const answerDisplay = getAnswerState(question.id, question.type, isSpecialized);

    return {
      subject: question.text,
      answer: answerDisplay
    };
  });
  axios_send(answers.value)
};

const setStep = () => {
  step++;
}

const getTimeTable = () => {
  if (webSocketService.isConnected) {
    const answersData = answers.value.map(item => ({ subject: item.subject, answer: item.answer }));
    const answersString = JSON.stringify(answersData);
    webSocketService.sendMessage({ "user_message": answersString, "purpose": "workshop", "telephone": tel.value });
  } else {
    console.error('WebSocket is not ready to send message.');
    return;
  }
  messages.value.push({ id: messages.value.length, type: 'robot', status: "html" });
  webSocketService.setlistHandler(handlelistMessage);
}


onMounted(() => {
  messages.value.push({ id: 0, type: "robot", text: "您好，请输入客户公司名您好", status: "text" });
  webSocketService.connect(tel.value);
  webSocketService.setRecoveryHandle(recovery);
  webSocketService.setPopHandle(addandPop);
  webSocketService.setlistHandler(handlelistMessage);
  webSocketService.setMessageHandler(handleMessage);
  webSocketService.setStepHandler(setStep);
});



const handleSocketMessage = (message: string) => {
  htmltext.value += message;
  nextTick(() => scrollToBottom());
};

const handlelistMessage = (message: string) => {
  messages.value[messages.value.length - 1].text += message;
  nextTick(() => scrollToBottom());

};


const scrollToBottom = () => {
  const scrollbar = document.querySelector('.el-scrollbar__wrap');
  if (scrollbar) {
    scrollbar.scrollTop = scrollbar.scrollHeight;
  }
};


const adjustInputHeight = () => {
  const inputElement = document.querySelector('.user_input') as HTMLInputElement;
  if (inputElement) {
    const lineHeight = parseInt(window.getComputedStyle(inputElement).lineHeight);
    const rows = Math.ceil(inputElement.scrollHeight / lineHeight);
    inputElement.style.height = `${lineHeight * Math.min(rows, 3)}px`;
  }
};




defineOptions({
  name: 'XiaoshouPage'
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
