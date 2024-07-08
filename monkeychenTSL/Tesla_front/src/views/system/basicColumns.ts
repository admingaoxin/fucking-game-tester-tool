import { h } from 'vue';
import { NAvatar, NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '部门名称',
    key: 'name',
    width: 100,
  },
  {
    title: '部门简介',
    key: 'intro',
    width: 100,
  },
  {
    title: '头像',
    key: 'avatar',
    width: 100,
    render(row) {
      return h(NAvatar, {
        size: 48,
        src: row.leader_img,
      });
    },
  },
  {
    title: '负责人名称',
    key: 'leader_name',
    width: 100,
  },
];
