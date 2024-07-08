<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="元素详情">
      <n-grid cols="2 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
        <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
          <n-form :label-width="80" :model="formValue" :rules="rules" label-placement="left" ref="formRef" class="py-8">
            <n-form-item label="项目" path="project">
              <n-select v-model:value="formValue.project" :options="project_list" />
            </n-form-item>

            <n-form-item label="元素名称" path="name">
              <n-input v-model:value="formValue.name" placeholder="请输入元素名称" />
            </n-form-item>

            <n-form-item label="定位方式" path="by">
              <n-select v-model:value="formValue.by" :options="by_list" placeholder="请选择定位方式" />
            </n-form-item>

            <n-form-item label="表达式" path="value">
              <n-input v-model:value="formValue.value" placeholder="请输入定位表达式" />
            </n-form-item>
          </n-form>
        </n-grid-item>
      </n-grid>
    </n-card>

    <n-card class="mt-4 proCard">
      <n-space>
        <n-button type="primary" @click="formSubmit">提交</n-button>
        <n-button @click="resetForm">重置</n-button>
      </n-space>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useMessage } from 'naive-ui';
import { ProjectAPI } from '@/api/project/http';
import { ElementAPI } from '@/api/case_ui/http';
import { Element } from '@/api/case_ui/models';

const api = new ElementAPI();
const project_api = new ProjectAPI();
const route = useRoute();

const dataId = parseInt(`${route.params.id}`);

const rules = {
  project: {
    required: true,
    type: 'number',
    message: '请选择项目',
    trigger: 'blur',
  },
  name: {
    required: true,
    message: '请输入元素名称',
    trigger: 'blur',
  },
  by: {
    required: true,
    message: '请选择定位方式',
    trigger: 'blur',
  },
  value: {
    required: true,
    message: '请输入定位表达式',
    trigger: 'blur',
  },
};

let defaultValue: Element = {
  id: -1,
  project: -2,
  name: '未命名',
  by: 'XPATH',
  value: '',
};

let project_list = [{}];

let by_list = ['XPATH', 'CSS_SELECTOR', 'LINK_TEXT', 'PARTIAL_LINK_TEXT', 'TAG_NAME'].map((a) => {
  return { label: a, value: a };
});

const defaultValueDeepCopy = () => JSON.parse(JSON.stringify(defaultValue));

const formRef: any = ref(null);
const message = useMessage();

let formValue = reactive(defaultValueDeepCopy());

async function makeDefaultValue() {
  // 加载项目列表
  let project_by_api = await project_api.getDataList({});
  project_list = project_by_api.list.map((project) => {
    return { label: project.name, value: project.id };
  });

  // 如果id>0，加载默认值
  if (dataId > 0) {
    defaultValue = await api.getDataByID(dataId);
  } else {
    defaultValue.project = null;
  }

  resetForm();
}

function formSubmit() {
  formRef.value.restoreValidation();
  formRef.value.validate(async (errors) => {
    if (errors) {
      return message.error('验证失败，请填写完整信息');
    } else {
      let data = { ...formValue };

      if (dataId == 0) {
        await api.createData(data as Element);
      } else {
        await api.upDataByID(dataId, data as Element);
      }
      message.success('保存成功');
    }
  });
}

function resetForm() {
  const data = defaultValueDeepCopy();
  formRef.value.restoreValidation();
  Object.assign(formValue, data);
}

onMounted(() => {
  setTimeout(() => {
    makeDefaultValue();
  }, 1);
});
</script>
