<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="UI用例详情">
      <n-grid cols="1 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
        <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
          <n-form :label-width="80" :model="formValue" :rules="rules" label-placement="left" ref="formRef" class="py-8">
            <n-form-item label="项目" path="project">
              <n-select v-model:value="formValue.project" :options="project_list" />
            </n-form-item>

            <n-form-item label="用例名称" path="name">
              <n-input v-model:value="formValue.name" />
            </n-form-item>

            <div>
              <n-card title="夹具" style="margin-bottom: 16px">
                <n-dynamic-input v-model:value="formValue.usefixtures" placeholder="请输入" />
              </n-card>
            </div>
          </n-form>
        </n-grid-item>
      </n-grid>
    </n-card>

    <n-card :bordered="false" title="用例步骤" class="mt-4 proCard">
      <ExcelUploader ref="actionRef" />
    </n-card>

    <n-card>
      <n-grid cols="1 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
        <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
          <n-form :label-width="80" :model="formValue" :rules="rules" label-placement="left" ref="formRef" class="py-8">
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
import { ref, unref, reactive, onMounted, } from 'vue';
import { FormRules, NInput, useMessage } from 'naive-ui';
import { useRoute } from 'vue-router';
import { ProjectAPI } from '@/api/project/http';
import { CaseUIAPI } from '@/api/case_ui/http';
import { CaseUI } from '@/api/case_ui/models';
import ExcelUploader from './ExcelUploader.vue';

const route = useRoute();

const dataID = parseInt(`${route.params.id}`); // 转成整数

const api = new CaseUIAPI();
const project_api = new ProjectAPI();

const formRef: any = ref(null);
const message = useMessage();

const rules: FormRules = {
  project: {
    required: true,
    type: 'number',
    message: '请选择项目',
    trigger: 'blur',
  },
  name: {
    required: true,
    message: '请选择输入用例名称',
    trigger: 'blur',
  },
};

let defaultValue: CaseUI = {
  id: -1,
  project: -2,
  name: '',
  usefixtures: [],
  steps: [],
};

let project_list = [{}];

const defaultValueRef = () => defaultValue;

let formValue = reactive(defaultValueRef()); // 表单显示的数据

const actionRef = ref();

function formSubmit() {
  formValue.steps = actionRef.value?.getData();

  formRef.value.restoreValidation();

  formRef.value.validate(async (errors) => {
    if (!errors) {
      const data = { ...formValue };

      if (dataID == 0) {
        console.log('增加数据');
        await api.createData(data as CaseUI);
      } else {
        console.log('编辑数据');
        await api.upDataByID(dataID, data as CaseUI);
      }
      message.success('提交成功');
    } else {
      message.error('验证失败，请填写完整信息');
    }
  });
}

function resetForm() {
  const data = defaultValueRef();

  formRef.value.restoreValidation();
  formValue = Object.assign(unref(formValue), data); //用新的默认值，修改原有变量
  actionRef.value?.setData(data.steps);
}

async function get_data_by_api() {
  // 加载项目列表
  let project_by_api = await project_api.getDataList({});
  project_list = project_by_api.list.map((project) => {
    return { label: project.name, value: project.id };
  });

  if (dataID == 0) {
    console.log('增加数据');
    defaultValue = { ...defaultValue, project: null };
    // defaultValue.project = null;
  } else {
    console.log('编辑数据');

    console.log('页面加载完成，正在请求接口获取数据');
    const data_by_api = await api.getDataByID(dataID); // 修改默认值
    let newDefaultValue = { ...data_by_api };
    defaultValue = newDefaultValue;
  }

  resetForm(); // 让默认值修改表单值
}

onMounted(async () => {
  await get_data_by_api();
  // tableData.value = [];
});
</script>
