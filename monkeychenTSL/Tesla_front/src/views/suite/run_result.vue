<template>
    <n-card :bordered="false" class="proCard">
        <BasicTable title="表格列表" titleTooltip="这是一个提示" :columns="columns" :request="loadDataTable"
            :row-key="(row) => row.id" ref="actionRef" :actionColumn="actionColumn" :scroll-x="1360"
            @update:checked-row-keys="onCheckedRow" />
    </n-card>
</template>
  
<script lang="ts" setup>
import { reactive, ref, h } from 'vue';
import { BasicTable, TableAction } from '@/components/Table';
import { useMessage } from 'naive-ui';
import {BarChartOutlined, DownloadOutlined } from '@vicons/antd';
import { useRouter } from 'vue-router';
import { RunResultAPI } from '@/api/suite/http';
import { columns } from './resultColumns';

const message = useMessage();
const actionRef = ref();
const router = useRouter();

const api = new RunResultAPI();

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
            label: '下载归档',
            type: 'primary',
            icon: DownloadOutlined,
            onClick: () => {
                // console.log(window)
                window.open(`${record.artifacts_url}`);
                message.success('开始下载');
            },
            ifShow: () => {
                return true;
            },
        },
        {
            label: '查看报告',
            type: 'primary',
            icon: BarChartOutlined,
            onClick: () => {
                router.push({
                    name: 'suite_report',
                    params: { id: record.id },
                });
            },
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




</script>
  
<style lang="less" scoped></style>
  