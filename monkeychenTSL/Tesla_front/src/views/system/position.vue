<template>
  <n-card :bordered="false" class="proCard">
    <BasicTable
      title="职位设置"
      titleTooltip=""
      :columns="columns"
      :request="loadDataTable"
      :row-key="(row) => row.id"
      ref="actionRef"
      :actionColumn="actionColumn"
      :scroll-x="1360"
      @update:checked-row-keys="onCheckedRow"
    >
      <template #toolbar>
        <n-button type="primary" @click="newData">添加数据</n-button>
      </template>
    </BasicTable>
  </n-card>
</template>

<script lang="ts" setup>
  import { reactive, ref, h } from 'vue';
  import { useDialog, useMessage } from 'naive-ui';
  import { useRouter } from 'vue-router';
  import { DeleteOutlined, EditOutlined } from '@vicons/antd';
  import { BasicTable, TableAction } from '@/components/Table';
  import { PositionAPI } from '@/api/system/http';
  import { columns } from './positionColumns';

  const router = useRouter();
  const message = useMessage();
  const dialog = useDialog();
  const actionRef = ref();
  const api = new PositionAPI();

  const params = reactive({
    pageSize: 1,
  });

  const actionColumn = reactive({
    width: 150,
    title: '操作',
    key: 'action',
    fixed: 'right',
    align: 'center',
    render(record) {
      return h(TableAction as any, {
        style: 'text',
        actions: createActions(record),
      });
    },
  });

  function createActions(record) {
    return [
      {
        label: '删除',
        type: 'error',
        // 配置 color 会覆盖 type
        color: 'red',
        icon: DeleteOutlined,
        onClick: handleDelete.bind(null, record),
        // 根据业务控制是否显示 isShow 和 auth 是并且关系
        ifShow: () => {
          return true;
        },
      },
      {
        label: '编辑',
        type: 'primary',
        icon: EditOutlined,
        onClick: handleEdit.bind(null, record),
        ifShow: () => {
          return true;
        },
      },
    ];
  }

  const loadDataTable = async (res) => {
    return await api.getDataList({ ...params, ...res });
  };

  function onCheckedRow(rowKeys) {
    console.log(rowKeys);
  }

  function newData() {
    router.push({ name: 'system_position_edit', params: { id: 0 } });
  }

  function handleDelete(record) {
    console.log(record);
    dialog.info({
      title: '提示',
      content: `正在删除数据：【${record.name}】`,
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        // 调用删除接口
        await api.DelDataByID(record.id);
        message.success('删除成功');
        actionRef.value.reload();
      },
      onNegativeClick: () => {},
    });
  }

  function handleEdit(record) {
    // 跳转编辑页面
    router.push({ name: 'system_position_edit', params: { id: record.id } });
  }
</script>

<style lang="less" scoped></style>
