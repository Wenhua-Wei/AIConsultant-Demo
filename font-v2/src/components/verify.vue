<template>
    <div class="Container">
        <div class="verifyContainer">
            <div class="verify" id="verify">
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import SlideVerify from 'slide-verify';
import { onMounted } from 'vue';



onMounted(() => {
    const Slide = new SlideVerify({
        elementId: "verify", // DOM挂载点
        onSuccess: () => { console.log("success") }, // 成功回调
        onFail: () => { console.log("fail") }, // 失败回调
        onRefresh: () => { console.log("refresh") }, // 刷新回调
        photo: '../src/assets/images/test.jpg' // 背景图片地址
    })
})
</script>

<style>
.q-layout{
    width:100%;
    height:100%;
}

.q-page-container{
    width: 100% ;
    height: 100%;
}

.Container {
    width: 100%;
    height: 100%;
}


.verifyContainer{
    width:60%;
    height:80%;
    background-color:red
}


.verify{
    width:50%;
    height:60%;
}

canvas{
    width:50% !important;
    height:40% !important;
}

/* ._3atUiqrbtQXFF0E5CU-v8W{
    width:60%;
    height:30%
} */

._2xJLZvp5OLjY7nYZjVdsY6{
    width:10.65% !important;
    height:100% !important;
}
</style>