import { h } from 'vue';
import { NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '名称',
    key: 'name',
    width: 100,
  },
  {
    title: '负责人',
    key: 'is_leader',
    width: 100,
    render(row) {
      return h(
        NTag,
        {
          type: row.is_leader ? 'success' : 'error',
        },
        {
          default: () => (row.is_leader ? '是' : '否'),
        }
      );
    },
  },
];
