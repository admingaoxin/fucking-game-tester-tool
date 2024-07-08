import { h } from 'vue';
import { NAvatar, NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '项目名称',
    key: 'name',
    width: 100,
  },
  {
    title: '项目简介',
    key: 'intro',
    width: 100,
  },
  {
    title: '项目负责人头像',
    key: 'avatar',
    width: 100,
    render(row) {
      return h(NAvatar, {
        size: 48,
        src: row.pm_profile.head_img,
      });
    },
  },
  {
    title: '负责人昵称',
    key: 'pm_profile.name',
    width: 100,
  },
];
