import { h } from 'vue';
import { NAvatar, NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '用户',
    key: 'user',
    width: 100,
    render(row) {
      return h(NAvatar, {
        size: 48,
        src: row.user_profile.head_img,
      });
    },
    
  },
  {
    title: '部门',
    key: 'department',
    width: 100,
  },
  {
    title: '职位',
    key: 'position.name',
    width: 150,
  },
  {
    title: '是否负责人',
    key: 'status',
    width: 100,
    render(row) {
      return h(
        NTag,
        {
          type: row.position.is_leader ? 'success' : 'error',
        },
        {
          default: () => (row.status ? '是' : '否'),
        }
      );
    },
  },
];
