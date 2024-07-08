<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="接口用例详情">
      <n-grid cols="1 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
        <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
          <n-form :label-width="80" :model="formValue" :rules="rules" label-placement="left" ref="formRef" class="py-8">
            <n-form-item label="项目" path="project">
              <n-select v-model:value="formValue.project" :options="project_list" />
            </n-form-item>
            <n-form-item label="接口" path="endpoint">
              <n-select v-model:value="formValue.endpoint" :options="endpoint_list" />
            </n-form-item>
            <n-form-item label="用例名称" path="name">
              <n-input v-model:value="formValue.name" />
            </n-form-item>
            <div>
              <n-card title="allure标注" style="margin-bottom: 16px">
                <DynamicDict :data="formValue.allure" @some-event="updateAllure" />
              </n-card>
            </div>
            <div>
              <n-card title="参数" style="margin-bottom: 16px">
                <EndpointEditor :request="formValue.api_args" @update="updateEndpoint" />
              </n-card>
            </div>
            <div>
              <n-card title="数据提取" style="margin-bottom: 16px">
                <APIExtract :data="formValue.extract" @some-event="updateExtract" />
              </n-card>
            </div>
            <div>
              <n-card title="断言" style="margin-bottom: 16px">
                <APIValidate :data2="formValue.validate" @some-event="updateValidate" />
              </n-card>
            </div>
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
import { ref, unref, reactive, onMounted } from 'vue';
import { FormRules, useMessage } from 'naive-ui';
import { useRoute } from 'vue-router';
import { ProjectAPI } from '@/api/project/http';
import { EndpointAPI, CaseAPI } from '@/api/case_api/http';
import { Endpoint, Case } from '@/api/case_api/models';
import { DynamicDict, EndpointEditor, APIExtract, APIValidate } from '@/components/Http';
import { number } from 'vue-types';
const route = useRoute();

const dataID = parseInt(`${route.params.id}`); // 转成整数

const api = new CaseAPI();
const project_api = new ProjectAPI();
const endpoint_api = new EndpointAPI;
const formRef: any = ref(null);
const message = useMessage();

const rules: FormRules = {
  project: {
    required: true,
    type: 'number',
    message: '请选择项目',
    trigger: 'blur',
  },
  endpoint: {
    required: true,
    type: 'number',
    message: '请选择接口',
    trigger: 'blur',
  },
  name: {
    required: true,
    message: '请输入接口名称',
    trigger: 'blur',
  },
  method: {
    required: true,
    message: '请输入请求方法',
    trigger: 'blur',
  },
  url: {
    required: true,
    message: '请输入请求地址',
    trigger: 'blur',
  },
  test_headers: {
    trigger: 'input',
    validator(rule: unknown, value: string) {
      if (value.length >= 5) return new Error('最多输入四个字符');
      return true;
    },
  },
};

let defaultValue: Case = {
  id: -1,
  project: -2,
  endpoint: -3,
  url: '',
  allure: {},
  api_args: {
    headers: {},
    cookies: {},
    params: {},
    data: {},
    json: {},
  },
  extract: {
    '': ['', '', 0],
  },
  validate: {
    equals: {
      '': ['', number],
    },
  },

};

let project_list = [{}];
let endpoint_list = [{}];
const defaultValueRef = () => defaultValue;

let formValue = reactive(defaultValueRef()); // 表单显示的数据

function formSubmit() {
  console.log('提交按钮被点击');

  formRef.value.validate(async (errors) => {
    if (!errors) {
      console.log('表单验证通过');
      const data = { ...formValue };

      if (dataID == 0) {
        console.log('增加数据');
        await api.createData(data as Endpoint);
      } else {
        console.log('编辑数据');
        await api.upDataByID(dataID, data as Endpoint);
      }
      message.success('提交成功');
      console.log('提交的数据：', formValue);
    } else {
      console.log('表单验证失败');
      message.error('验证失败，请填写完整信息');
    }
  });
}

function resetForm() {
  formRef.value.restoreValidation();
  formValue = Object.assign(unref(formValue), defaultValueRef()); //用新的默认值，修改原有变量
}

async function get_data_by_api() {
  // 加载项目列表
  let project_by_api = await project_api.getDataList({});
  console.log(project_by_api);
  project_list = project_by_api.list.map((project) => {
    return { label: project.name, value: project.id };
  });
  console.log(project_list);
  // 加载接口列表
  let endpoint_by_api = await endpoint_api.getDataList({});
  console.log("endpoint_by_api", endpoint_by_api);
  endpoint_list = endpoint_by_api.list.map((endpoint) => {
    return { label: endpoint.name, value: endpoint.id };
  });
  console.log(endpoint_list);
  if (dataID == 0) {
    console.log('增加数据');
    defaultValue = { ...defaultValue };
    defaultValue.project = null;
    defaultValue.endpoint = null;
  } else {
    console.log('编辑数据');
    console.log('页面加载完成，正在请求接口获取数据');
    const data_by_api = await api.getDataByID(dataID); // 修改默认值
    let newDefaultValue = { ...data_by_api };
    console.log("newDefaultValue的值=======", newDefaultValue)
    defaultValue = newDefaultValue;
    console.log("defultvalue的值是=======", defaultValue)
    console.log('要提交的数据：', formValue); // 添加这一行
  }

  resetForm(); // 让默认值修改表单值
}

function updateEndpoint(args_type, args_values) {
  formValue.api_args[args_type] = args_values;
}
function updateAllure(vals) {
  console.log(`updateAllure`, vals);
  formValue.allure = vals;
  console.log('更新后的formValue.allure', formValue.allure);
}
function updateExtract(vals) {
  console.log(`updateExtract`, vals);
  formValue.extract = vals;
}

function updateValidate(vals) {
  console.log(`updateValidate`, vals);
  formValue.validate = vals;
}
onMounted(async () => {
  await get_data_by_api();
});
</script>
