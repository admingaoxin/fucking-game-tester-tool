<template>
  <n-card :bordered="false" class="proCard">
    <BasicTable
      title="表格列表"
      titleTooltip="这是一个提示"
      :columns="columns"
      :request="loadDataTable"
      :row-key="(row) => row.id"
      ref="actionRef"
      :actionColumn="actionColumn"
      :scroll-x="1360"
      @update:checked-row-keys="onCheckedRow"
    >
      <template #toolbar>
        <n-button type="primary" @click="addData">添加数据</n-button>
      </template>
    </BasicTable>
  </n-card>
</template>

<script lang="ts" setup>
  import { reactive, ref, h } from 'vue';
  import { BasicTable, TableAction } from '@/components/Table';
  import { columns } from './configColumns';
  import { useDialog, useMessage } from 'naive-ui';
  import { DeleteOutlined, EditOutlined } from '@vicons/antd';
  import { useRouter } from 'vue-router';
  import { ConfigAPI } from '@/api/project/http';

  const message = useMessage();
  const dialog = useDialog();
  const actionRef = ref();
  const router = useRouter();

  const api = new ConfigAPI();

  const params = reactive({
    pageSize: 5,
    name: 'xiaoMa',
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
      },
      {
        label: '编辑',
        type: 'primary',
        icon: EditOutlined,
        onClick: handleEdit.bind(null, record),
      },
    ];
  }

  const loadDataTable = async (res) => {
    return await api.getDataList({ ...params, ...res });
  };

  function onCheckedRow(rowKeys) {
    console.log(rowKeys);
  }

  function reloadTable() {
    actionRef.value.reload();
  }

  function handleDelete(record) {
    console.log(record);
    dialog.info({
      title: '提示',
      content: `您想删除【${record.project_name}】`,
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        await api.DelDataByID(record.id); // 调用删除接口
        message.success('删除成功'); // 提示操作成功
        reloadTable(); // 自动刷新表格
      },
      onNegativeClick: () => {},
    });
  }

  function handleEdit(record) {
    console.log(record);
    message.success('您点击了编辑按钮');
    router.push({ name: 'project_config_edit', params: { id: record.id } });
  }

  function addData() {
    router.push({ name: 'project_config_edit', params: { id: 0 } });
  }
</script>

<style lang="less" scoped></style>
