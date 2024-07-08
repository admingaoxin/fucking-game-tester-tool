<template>
  <div>
    <n-card :bordered="false" class="mt-4 proCard" title="角色详情">
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
            <n-form-item label="用户" path="user">
              <n-select
                v-model:value="formValue.user"
                :options="user_new_list"
                :render-label="renderLabel"
                :render-tag="renderSingleSelectTag"
              />
            </n-form-item>

            <n-form-item label="部门" path="department">
              <n-select v-model:value="formValue.department" :options="department_list" />
            </n-form-item>

            <n-form-item label="职位" path="position">
              <n-select v-model:value="formValue.position" :options="position_list" />
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
  import { ref, reactive, onMounted, h } from 'vue';
  import { useMessage, NAvatar, SelectRenderTag, SelectRenderLabel } from 'naive-ui';
  import { useRoute } from 'vue-router';
  import { user_list } from '@/api/account/http';
  import { RoleAPI, DepartmentAPI, PositionAPI } from '@/api/system/http';
  import { Role } from '@/api/system/models';

  const api = new RoleAPI();
  const department_api = new DepartmentAPI();
  const position_api = new PositionAPI();
  const route = useRoute();
  const message = useMessage();

  const dataId = parseInt(`${route.params.id}`);

  const rules = {
    user: {
      required: true,
      type: 'number',
      message: '请选择用户',
      trigger: 'blur',
    },
    department: {
      required: true,
      type: 'number',
      message: '请选择部门',
      trigger: 'blur',
    },
    position: {
      required: true,
      type: 'number',
      message: '请选择职位',
      trigger: 'blur',
    },
  };

  let defaultValue = {
    user: -1,
    department: -2,
    position: -3,
  };

  let user_new_list = [
    {
      user: -1,
      name: 'xxx',
      head_img: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg',
      label: 'xxx',
      value: -1,
    },
    {
      user: -2,
      name: 'yyy',
      head_img: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg',
      label: 'yyy',
      value: -2,
    },
  ];

  const renderSingleSelectTag: SelectRenderTag = ({ option }) => {
    return h(
      'div',
      {
        style: {
          display: 'flex',
          alignItems: 'center',
        },
      },
      [
        h(NAvatar, {
          src: option.head_img as string,
          round: true,
          size: 24,
          style: {
            marginRight: '12px',
          },
        }),
        option.name as string,
      ]
    );
  };

  const renderLabel: SelectRenderLabel = (option) => {
    return h(
      'div',
      {
        style: {
          display: 'flex',
          alignItems: 'center',
        },
      },
      [
        h(NAvatar, {
          src: option.head_img as string,
          round: true,
          size: 'small',
        }),
        h(
          'div',
          {
            style: {
              marginLeft: '12px',
              padding: '4px 0',
            },
          },
          [h('div', null, [option.name as string])]
        ),
      ]
    );
  };

  let department_list = [
    {
      label: 'A部门',
      value: -1,
    },
    {
      label: 'B部门',
      value: -2,
    },
  ];

  let position_list = [
    {
      label: '经理',
      value: -3,
    },
    {
      label: '员工',
      value: -4,
    },
  ];
  const defaultValueDeepCopy = () => JSON.parse(JSON.stringify(defaultValue));

  const formRef: any = ref(null);

  let formValue = reactive(defaultValueDeepCopy());

  async function makeDefaultValue() {
    // 加载用户列表,需要增加接口
    let user_by_api = await user_list();
    user_new_list = user_by_api.map((user) => {
      return { ...user, label: user.name, value: user.user };
    });

    // 加载部门列表
    let department_by_api = await department_api.getDataList();
    console.log(department_by_api);
    department_list = department_by_api.list.map((department) => {
      return { label: department.name, value: department.id };
    });

    // 加载职位列表
    let position_by_api = await position_api.getDataList({});
    position_list = position_by_api.list.map((position) => {
      return { label: position.name, value: position.id };
    });

    // 如果id>0，加载默认值
    if (dataId > 0) {
      defaultValue = await api.getDataByID(dataId);
    } else {
      defaultValue = { ...defaultValue };
      defaultValue.user = null;
      defaultValue.department = null;
      defaultValue.position = null;
    }

    resetForm();
  }

  function formSubmit() {
    formRef.value.restoreValidation();
    formRef.value.validate(async (errors) => {
      
      if (errors) {
        return message.error('验证失败，请填写完整信息');
      } else {
        let data = {
          
          user: formValue.user,
          department: formValue.department,
          position: formValue.position,
        };
        
        if (dataId == 0) {
          await api.createData(data as Role);
        } else {
          await api.upDataByID(dataId, data as Role);
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
