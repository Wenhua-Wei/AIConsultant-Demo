import { App } from 'vue';
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as Icons from '@element-plus/icons-vue';

// 显式地为函数参数指定类型
export default ({ app }: { app: App<Element> }) => {
  app.use(ElementPlus);
  for (const name in Icons) {
    // 如果 TypeScript 仍然报错说 Icons[name] 的类型可能不正确，
    // 你可能需要为 Icons 添加更具体的类型注解或者使用类型断言。
    app.component(name, Icons[name] as any);
  }
};
