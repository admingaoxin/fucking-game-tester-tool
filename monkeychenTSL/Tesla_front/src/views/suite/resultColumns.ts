import { NTag } from 'naive-ui';
import { h } from 'vue';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '套件名称',
    key: 'suite_name',
    width: 100,
  },
  {
    title: '所属项目',
    key: 'project_name',
    width: 100,
  },
  {
    title: '运行模式',
    key: 'run_type',
    width: 100,
  },
  {
    title: '执行状态',
    key: 'status',
    width: 100,
  },
  {
    title: '是否通过',
    key: 'is_pass',
    width: 100,
    render(row) {
      return h(
        NTag,
        {
          type: row.is_pass ? 'success' : 'error',
        },
        {
          default: () => (row.is_pass ? '通过' : '失败'),
        }
      );
    },
  },
  {
    title: '更新时间',
    key: 'update_datetime',
    width: 100,
  },
];
