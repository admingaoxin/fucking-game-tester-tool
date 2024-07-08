<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="修改项目资料">
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
            <n-form-item label="项目名称" path="name">
              <n-input v-model:value="formValue.name" placeholder="输入项目名称" />
            </n-form-item>
            <n-form-item label="项目简介" path="intro">
              <n-input v-model:value="formValue.intro" placeholder="输入项目简介" />
            </n-form-item>
            <n-form-item label="项目地址" path="url">
              <n-input v-model:value="formValue.url" placeholder="输入项目地址" />
            </n-form-item>
            <n-form-item label="项目负责人" path="pm">
            <n-select
              v-model:value="formValue.pm" placeholder="请选择项目负责人"
              :options="options"
              :render-label="renderLabel"
              :render-tag="renderSingleSelectTag"
              filterable
              />
            </n-form-item>
            <n-form-item label="项目成员" path="user_list"> 
              <n-select
              v-model:value="formValue.user_list" placeholder="请选择项目负责人"
              :options="options"
              :render-label="renderLabel"
              :render-tag="renderSingleSelectTag"
              filterable
              multiple
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
  import { ref, unref, reactive ,onMounted, h} from 'vue';
  import { NAvatar, NText, SelectRenderLabel, SelectRenderTag, useMessage } from 'naive-ui';
  //import { useUser } from '@/store/modules/user';
  import { ProjectAPI } from '@/api/project/http';
  import { useRoute } from 'vue-router';
  import { Project } from '@/api/project/models';
  import { user_list } from '@/api/account/http';
 // import { de } from 'date-fns/locale';
  //import { number } from 'vue-types';
const rules = {
    name: {
      required: true,
      message: '请输入项目名称',
      trigger: 'change',
    },
    intro: {
      required: true,
      message: '请输入项目简介',
      trigger: 'change',
    },
  };
  const api= new ProjectAPI();
  const formRef: any = ref(null);
  const message = useMessage();
  //const userStore = useUser();
 // const token = userStore.getToken;
  const route=useRoute();
  const dataID=parseInt(`${route.params.id}`) //转成整数
//默认值设置
  let defaultValue={
      name: '',
      intro:'',
      url:'',
      pm:-1,
      user_list:[-1],
  };

  const  defaultValueRef = () => defaultValue;

  let formValue = reactive(defaultValueRef());
  let options= [
        {
          label: '07akioni',
          value: '07akioni'
        },
        {
          label: '08akioni',
          value: '08akioni'
        },
        {
          label: '09akioni',
          value: '09akioni'
        }
      ]

      
  const renderLabel: SelectRenderLabel = (option) => {
      return h(
        'div',
        {
          style: {
            display: 'flex',
            alignItems: 'center'
          }
        },
        [
          h(NAvatar, {
            src: option.head_img as string,
            round: true,
            size: 'small'
          }),
          h(
            'div',
            {
              style: {
                marginLeft: '12px',
                padding: '4px 0'
              }
            },
            [
              h('div', null, [option.label as string]),
              h(
                NText,
                { depth: 3, tag: 'div' },
                {
                  default: () => 'description'
                }
              )
            ]
          )
        ]
      )
    }
  const renderSingleSelectTag: SelectRenderTag = ({ option }) => {
    return h(
      'div',
      {
        style: {
          display: 'flex',
          alignItems: 'center'
        }
      },
      [
        h(NAvatar, {
          src: option.head_img as string ,
          round: true,
          size: 24,
          style: {
            marginRight: '12px'
          }
        }),
        option.label as string
      ]
    )
  }
  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const data={...formValue};
        if (dataID == 0) {
          console.log('增加数据');
          await api.createData(data as Project);
        } else {
          console.log('编辑数据');
          await api.upDataByID(dataID, data as Project);
        }
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

  async function get_data_by_api(){
    let user_list_by_api=await user_list();
    options =user_list_by_api.map((a) =>{
      return{value: a.user,label:a.name,head_img:a.head_img};
    });


    if (dataID == 0) {
      console.log('增加数据');
      defaultValue={...defaultValue};
      defaultValue.pm=null;
      defaultValue.user_list=[];
    } else {
      console.log('编辑数据');

      console.log('页面加载完成，正在请求接口获取数据');
      const data_by_api = await api.getDataByID(dataID); // 修改默认值
      console.log(data_by_api)
      let newDefaultValue = {...data_by_api};
      defaultValue = newDefaultValue;
      
    }
    resetForm(); // 让默认值修改表单值
    return;
  }
  onMounted(async ()=> {
      await get_data_by_api();
  });
  
</script>

