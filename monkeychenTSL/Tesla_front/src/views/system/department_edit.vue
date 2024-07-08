<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="修改部门资料">
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
            <n-form-item label="部门名称" path="name">
              <n-input v-model:value="formValue.name" placeholder="输入部门名称" />
            </n-form-item>
            <n-form-item label="部门简介" path="intro">
              <n-input v-model:value="formValue.intro" placeholder="输入部门简介" />
            </n-form-item>
            <n-form-item label="负责人" path="leader">
            <n-select
              v-model:value="formValue.leader" placeholder="请输入用户id"
              :options="options"
              :render-label="renderLabel"
              :render-tag="renderSingleSelectTag"
              filterable
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
  import { DepartmentAPI } from '@/api/system/http';
  import { useRoute } from 'vue-router';
  import { Department } from '@/api/system/models';
  import { user_list } from '@/api/account/http';
const rules = {
    name: {
      required: true,
      message: '请输入部门名称',
      trigger: 'change',
    },
  };
  const api= new DepartmentAPI();
  const formRef: any = ref(null);
  const message = useMessage();
  //const userStore = useUser();
 // const token = userStore.getToken;
  const route=useRoute();
  const dataID=parseInt(`${route.params.id}`) //转成整数

  let defaultValue={
      name: '',
      intro:'',
      leader:-1,

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
        const data={
          name: formValue.name,
          intro: formValue.intro,
          leader: formValue.leader,
        };
        if (dataID == 0) {
          console.log('增加数据');
          await api.createData(data as Department);
        } else {
          console.log('编辑数据');
          await api.upDataByID(dataID, data as Department);
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
      defaultValue.leader=null;

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

