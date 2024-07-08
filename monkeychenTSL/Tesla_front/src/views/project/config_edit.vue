<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="部门详情">
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

            <n-form-item label="conftest" path="conftest">
              <n-input
                v-model:value="formValue.conftest"
                placeholder="请输入pytets conftest脚本"
                type="textarea"
                :autosize="{
                  minRows: 3,
                }"
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
  import { ref, unref, reactive, onMounted } from 'vue';
  import { FormRules, useMessage } from 'naive-ui';
  import { useRoute } from 'vue-router';
  import { ConfigAPI, ProjectAPI } from '@/api/project/http';
  import { Config } from '@/api/project/models';

  const route = useRoute();

  const dataID = parseInt(`${route.params.id}`); // 转成整数

  const api = new ConfigAPI();
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
    conftest: {
      required: true,
      message: '请输入配置脚本',
      trigger: 'blur',
    },
  };

  let defaultValue: Config = {
    id: -1,
    project: -2,
    conftest: '',
  };

  let project_list = [{}];

  const defaultValueRef = () => defaultValue;

  let formValue = reactive(defaultValueRef()); // 表单显示的数据

  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const data = { ...formValue };

        if (dataID == 0) {
          console.log('增加数据');
          await api.createData(data as Config);
        } else {
          console.log('编辑数据');
          await api.upDataByID(dataID, data as Config);
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
    console.log(project_list);
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
  });
</script>
