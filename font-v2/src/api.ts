/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosResponse } from 'axios';

const targetUrl="https://api.consultant.ai4c.cn/"
// const targetUrl = "http://localhost:5200/"
export async function registerUser(registerData: { telephone: string, compName: string, ID?: string | null }): Promise<AxiosResponse<any, any>> {
  const { telephone, compName, ID } = registerData;
  const requestBody = {
    telephone,
    compName,
    idCode: ID || '4',
  };

  try {
    const response = await axios.post(targetUrl+'register', requestBody);
    // console.log('注册成功：', response.data);
    return response;
  } catch (error) {
    console.error('注册失败：', error);
    throw error; // 可以选择抛出错误，以便在调用函数的地方处理错误
  }
}

export async function loginUser(loginData: { telephone: string }): Promise<AxiosResponse<any, any>> {
  const { telephone } = loginData;
  const requestBody = {
    telephone,
  };

  try {
    const response = await axios.post(targetUrl+'login', requestBody);
    return response;

    // 如果登录成功，可以在这里处理返回的 token，并保存到本地存储中
    // 例如：localStorage.setItem('token', response.data.token);
  } catch (error) {
    console.error('登录失败：', error);
    throw error; // 可以选择抛出错误，以便在调用函数的地方处理错误
  }
}

  export async function getUsers() {
    try {
      const response = await axios.post(targetUrl+'getUsers');
      console.log('获取用户数据成功：', response.data);
      return response.data; // 返回获取到的用户数据
    } catch (error) {
      console.error('获取用户数据失败：', error);
      throw error; // 抛出错误，以便在调用函数的地方处理错误
    }
}

export async function selectQuestionsByTel(telephone: any) {
  try {
    // 发起 POST 请求到 /select 接口，并传递电话号码作为请求体
    const response = await axios.post(targetUrl+'selectQuestions', { telephone });
    // 输出获取到的用户数据
    console.log('获取用户数据成功：', response.data);
    // 返回获取到的用户数据
    return response.data;
  } catch (error) {
    // 处理请求失败时的错误
    console.error('获取用户数据失败：', error);
    // 抛出错误，以便在调用函数的地方处理错误
    throw error;
  }
}

export async function selectTimetableByTel(telephone: any) {
  try {
    // 发起 POST 请求到 /select 接口，并传递电话号码作为请求体
    const response = await axios.post(targetUrl+'selectTimetable', { telephone });
    // 输出获取到的用户数据
    console.log('获取用户数据成功：', response.data);
    // 返回获取到的用户数据
    return response.data;
  } catch (error) {
    // 处理请求失败时的错误
    console.error('获取用户数据失败：', error);
    // 抛出错误，以便在调用函数的地方处理错误
    throw error;
  }
}