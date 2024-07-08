<template>
  <n-card :bordered="false" class="proCard">
    <BasicTable title="表格列表" titleTooltip="这是一个提示" :columns="columns" :request="loadDataTable" :row-key="(row) => row.id"
      ref="actionRef" :actionColumn="actionColumn" :scroll-x="1360" @update:checked-row-keys="onCheckedRow">
      <template #toolbar>
        <n-button type="primary" @click="addDate">添加接口</n-button>
      </template>
    </BasicTable>
  </n-card>
</template>
  
<script lang="ts" setup>
import { reactive, ref, h } from 'vue';
import { BasicTable, TableAction } from '@/components/Table';
//import { getTableList } from '@/api/table/list';
import { useDialog, useMessage } from 'naive-ui';
import { DeleteOutlined, EditOutlined, CaretRightOutlined } from '@vicons/antd';
import { SuiteAPI } from '@/api/suite/http';
import { useRouter } from "vue-router";
import { columns } from './suiteColumns';

const message = useMessage();
const dialog = useDialog();
const actionRef = ref();
const api = new SuiteAPI();
const router = useRouter();

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
      // 根据业务控制是否显示 isShow 和 auth 是并且关系
      //ifShow: () => {
      //  return true;
      //},
      // 根据权限控制是否显示: 有权限，会显示，支持多个
      //auth: ['basic_list'],
    },
    {
      label: '编辑',
      type: 'primary',
      icon: EditOutlined,
      onClick: handleEdit.bind(null, record),
      // 根据业务控制是否显示 isShow 和 auth 是并且关系
      //ifShow: () => {
      //  return true;
      //},
      // 根据权限控制是否显示: 有权限，会显示，支持多个
      //auth: ['basic_list'],
    },
    {
      label: '运行',
      type: 'success',
      icon: CaretRightOutlined,
      onClick: handleRun.bind(null, record),
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
    content: `您想删除${record.name}`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      //调用删除接口
      await api.DelDataByID(record.id);
      message.success('删除成功');
      reloadTable();
    },
    onNegativeClick: () => { },
  });
}

function handleEdit(record) {
  console.log(record);
  //router.push({path: `/system/department/${record.id}`});
  router.push({ name: 'suite_suite_edit', params: { id: record.id } });
  message.success('您点击了编辑按钮');
}


function addDate() {

  router.push({ name: 'suite_suite_edit', params: { id: 0 } });
}
function handleRun(record) {
  console.log(record);
  dialog.info({
    title: '提示',
    content: `是否马上执行${record.name}的测试用例`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      //调用删除接口
      const resp=await api.runById(record.id);
      message.success(`任务提交成功,结果的ID:${resp.result_id}`);
    },
    onNegativeClick: () => { },
  });
}
</script>
  
<style lang="less" scoped></style>
  