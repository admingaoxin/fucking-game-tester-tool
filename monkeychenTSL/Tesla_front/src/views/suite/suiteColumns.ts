import { h } from 'vue';

export const columns = [
  {
    title: 'id',
    key: 'id',
    width: 100,
  },
  {
    title: '套件名称',
    key: 'name',
    width: 100,
  },
  {
    title: '所属项目',
    key: 'project_name',
    width: 100,
  },
  {
    title: '描述',
    key: 'description',
    width: 100,
  },
  {
    title: '运行模式',
    key: 'run_type_display',
    width: 100,
  },
  {
    title: 'UI用例数',
    key: 'case_ui_count',
    width: 100,
  },
  {
    title: 'API用例数',
    key: 'case_api_count',
    width: 100,
  },
];
