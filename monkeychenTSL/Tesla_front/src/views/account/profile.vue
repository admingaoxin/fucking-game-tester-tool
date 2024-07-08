<template>
    <div>
      <n-card :bordered="false" class="mt-4 proCard" title="修改个人资料">
        <n-grid cols="1 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
          <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
            <n-form
              :label-width="80"
              :model="formValue"
              :rules="rules"
              label-placement="left"
              ref="formRef"
              class="py-8"
            >
              <n-form-item label="昵称" path="name">
                <n-input v-model:value="formValue.name" placeholder="输入昵称" />
              </n-form-item>
              <n-form-item label="图片" path="head_img">
                <BasicUpload
                  :action="'/api/account/profile/img_upload/'"
                  :headers="uploadHeaders"
                  :data="{ type: 0 }"
                  name="img"
                  :width="100"
                  :height="100"
                  @upload-change="uploadChange"
                  v-model:value="formValue.head_img"
                  helpText="单个文件不超过20MB，最多只能上传10个文件"
                />
              </n-form-item>
              <div style="margin-left: 80px">
                <n-space>
                  <n-button type="primary" @click="formSubmit">提交</n-button>
                  <n-button @click="resetForm">重置</n-button>
                </n-space>
              </div>
            </n-form>
          </n-grid-item>
        </n-grid>
      </n-card>
    </div>
  </template>
  
  <script lang="ts" setup>
    import { ref, unref, reactive ,onMounted} from 'vue';
    import { useMessage } from 'naive-ui';
    import { BasicUpload } from '@/components/Upload';
    import { profile,changeProfile} from '@/api/account/http';
    import { Profile} from '@/api/account/models';
    import { useUser } from '@/store/modules/user';
  
  
    const rules = {
      name: {
        required: true,
        message: '请输入昵称',
        trigger: 'change',
      },
      head_img: {
        required: true,
        message: '请上传图片',
        type: "array",
        trigger: 'change',
      },
    };
  
    const formRef: any = ref(null);
    const message = useMessage();
    const userStore = useUser();
    const token = userStore.getToken;
  
    let defaultValue={
        name: '8888',
        head_img: ['https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png'],
    };
    //let img_list=ref(['https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',]);
    const  defaultValueRef = () => defaultValue;
  
    let formValue = reactive(defaultValueRef());
    const uploadHeaders = reactive({
      Authorization: `token ${token}`,
    });
  
    function formSubmit() {
      formRef.value.validate(async (errors) => {
        if (!errors) {
          const data={
            name:formValue.name,
            head_img:formValue.head_img[0],
          };
          await changeProfile(data as Profile);
          message.success('提交成功');
        } else {
          message.error('验证失败，请填写完整信息');
        }
      });
    }
  
    function resetForm() {
      formRef.value.restoreValidation();
      formValue = Object.assign(unref(formValue), defaultValueRef());
    }
  
    function uploadChange(list: string[]) {
      console.log("图片的修改结果同步到表单中");
      formValue.head_img=list;
    }
    async function get_data_by_api(){
        console.log("页面加载完成，正在请求接口获取数据");
        const resp = await profile();
        console.log(resp)
        defaultValue = resp.result;
        defaultValue.head_img=[resp.result.head_img];
        resetForm();
    }
    onMounted(async ()=> {
        await get_data_by_api();
    });
  </script>
  
