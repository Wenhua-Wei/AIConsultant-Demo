import { boot } from 'quasar/wrappers'
import {ElTree} from "element-plus/lib/components/tree/index"
import 'element-plus/theme-chalk/el-tree.css'
import 'element-plus/theme-chalk/base.css'
import { ElDatePicker } from 'element-plus/lib/components/date-picker/index.js'
import 'element-plus/theme-chalk/el-date-picker.css'
// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ app }) => {
  // something to do
  app.use(ElTree)
  app.use(ElDatePicker)
})
