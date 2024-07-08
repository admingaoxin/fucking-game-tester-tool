<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="测试套件详情">
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
            <n-form-item label="项目" path="project">
              <n-select v-model:value="formValue.project" :options="project_list" />
            </n-form-item>

            <n-form-item label="套件名称" path="name">
              <n-input v-model:value="formValue.name" />
            </n-form-item>

            <n-form-item label="套件描述" path="description">
              <n-input v-model:value="formValue.description" />
            </n-form-item>

            <n-form-item label="执行模式" path="run_type">
              <n-select v-model:value="formValue.run_type" :options="run_type_list" />
            </n-form-item>

            <n-form-item label="Cron表达式" path="cron" v-if="formValue.run_type === 'C'">
              <n-input v-model:value="formValue.cron" />
            </n-form-item>

            <n-form-item label="Hook密钥" path="hook_key" v-if="formValue.run_type === 'W'">
              <n-input v-model:value="formValue.hook_key" />
            </n-form-item>
          </n-form>
        </n-grid-item>
      </n-grid>
    </n-card>

    <n-card title="UI测试用例">
      <SelectCase
        :func-load-case-data="() => case_ui_api.getDataList()"
        :ref-select-data="formValue.case_ui_list"
        @some-event="changeCaseUIList"
      />
    </n-card>

    <n-card title="API测试用例">
      <SelectCase
        :func-load-case-data="() => case_api_api.getDataList()"
        :ref-select-data="formValue.case_api_list"
        @some-event="changeCaseAPIList"
      />
    </n-card>

    <n-card>
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
  import { CaseAPI } from '@/api/case_api/http';
  import { CaseUIAPI } from '@/api/case_ui/http';
  import { SuiteAPI } from '@/api/suite/http';
  import { Suite } from '@/api/suite/models';

  import SelectCase from './SelectCase.vue';

  const route = useRoute();

  const dataID = parseInt(`${route.params.id}`); // 转成整数

  const api = new SuiteAPI();
  const project_api = new ProjectAPI();
  const case_api_api = new CaseAPI();
  const case_ui_api = new CaseUIAPI();

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
    run_type: {
      required: true,
      message: '请选择执行类型',
      trigger: 'blur',
    },
    cron: {
      required: true,
      message: '请输入cron格式定时规则',
      trigger: 'blur',
    },
    hook_key: {
      required: true,
      message: '请输入Hook密钥',
      trigger: 'blur',
    },
  };

  let defaultValue: Suite = {
    id: -1,
    project: -2,
    name: '',
    description: '',
    case_ui_list: [],
    case_api_list: [],
    run_type: 'O',
    cron: '',
    hook_key: '',
  };

  const run_type_list = [
    {
      value: 'O',
      label: '单次执行',
    },
    {
      value: 'C',
      label: 'Cron',
    },
    {
      value: 'W',
      label: 'WebHook',
    },
  ];

  let project_list = [{}];

  const defaultValueRef = () => defaultValue;

  let formValue = reactive(defaultValueRef()); // 表单显示的数据

  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const data = { ...formValue };

        if (dataID == 0) {
          console.log('增加数据');
          await api.createData(data as Suite);
        } else {
          console.log('编辑数据');
          await api.upDataByID(dataID, data as Suite);
        }
        message.success('提交成功');
      } else {
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
    project_list = project_by_api.list.map((project) => {
      return { label: project.name, value: project.id };
    });

    if (dataID == 0) {
      console.log('增加数据');
      defaultValue = { ...defaultValue, project: null, run_type: null };
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

  function changeCaseUIList(new_list) {
    formValue.case_ui_list = new_list.value;
  }

  function changeCaseAPIList(new_list) {
    formValue.case_api_list = new_list.value;
  }
  onMounted(async () => {
    await get_data_by_api();
  });
</script>
