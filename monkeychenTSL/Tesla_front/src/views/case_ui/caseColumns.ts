import { h } from 'vue';
import { NAvatar, NSpace, NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '用例名称',
    key: 'name',
    width: 100,
  },

  {
    title: '所属项目',
    key: 'project_info.name',
    width: 100,
  },
  {
    title: '夹具列表',
    key: 'usefixtures',
    width: 100,
    render(row) {
      const tag_list = row.usefixtures.map((item) => h(NTag, { type: 'info' }, item));

      return h(NSpace, tag_list);
    }
  },
  {
    title: '步骤数量',
    key: 'steps',
    width: 100,
    render(row) {
      return row.steps.length;
    }
  },
];
