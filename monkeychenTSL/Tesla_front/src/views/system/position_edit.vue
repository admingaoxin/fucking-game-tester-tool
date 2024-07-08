<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="职位详情">
      <n-grid cols="2 s:1 m:3 l:3 xl:3 2xl:3" responsive="screen">
        <n-grid-item offset="0 s:0 m:1 l:1 xl:1 2xl:1">
          <n-form
            :label-width="80"
            :model="formValue"
            :rules="rules"
            label-placement="left"
            ref="formRef"
            class="py-8"
          >
            <n-form-item label="职位名称" path="name">
              <n-input v-model:value="formValue.name" placeholder="请输入职位名称" />
            </n-form-item>

            <n-form-item label="负责人" path="leader">
              <n-select v-model:value="formValue.is_leader" :options="bool_options" />
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
  import { ref, reactive, onMounted } from 'vue';
  import { useMessage } from 'naive-ui';
  import { PositionAPI } from '@/api/system/http';
  import { Position } from '@/api/system/models';

  import { useRoute } from 'vue-router';

  const api = new PositionAPI();
  const route = useRoute();
  const message = useMessage();

  const dataId = parseInt(`${route.params.id}`);

  const rules = {
    name: {
      required: true,
      message: '请输入职位名称',
      trigger: 'blur',
    },
    is_leader: {
      required: true,
      type: 'bool',
      trigger: 'blur',
    },
  };

  let defaultValue: Position = {
    id: 0,
    name: '',
    is_leader: false,
  };

  const bool_options = [
    {
      label: '是',
      value: true,
    },
    {
      label: '否',
      value: false,
    },
  ];

  const defaultValueDeepCopy = () => JSON.parse(JSON.stringify(defaultValue));

  const formRef: any = ref(null);

  let formValue = reactive(defaultValueDeepCopy());

  async function makeDefaultValue() {
    // 如果id>0，加载默认值
    if (dataId > 0) {
      defaultValue = await api.getDataByID(dataId);
      resetForm();
    }
  }

  function formSubmit() {
    formRef.value.restoreValidation();
    formRef.value.validate(async (errors) => {
      if (errors) {
        return message.error('验证失败，请填写完整信息');
      } else {
        let data = {
          name: formValue.name,
          is_leader: formValue.is_leader,
        };

        if (dataId == 0) {
          await api.createData(data as Position);
        } else {
          await api.upDataByID(dataId, data as Position);
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
    }, 16);
  });
</script>
