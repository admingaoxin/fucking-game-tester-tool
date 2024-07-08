import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { SkypeOutlined } from '@vicons/antd';
import { renderIcon } from '@/utils/index';

/**
 * @param name 路由名称, 必须设置,且不能重名
 * @param meta 路由元信息（路由附带扩展信息）
 * @param redirect 重定向地址, 访问这个路由时,自定进行重定向
 * @param meta.disabled 禁用整个菜单
 * @param meta.title 菜单名称
 * @param meta.icon 菜单图标
 * @param meta.keepAlive 缓存该路由
 * @param meta.sort 排序越小越排前
 *
 * */
const routes: Array<RouteRecordRaw> = [
  {
    path: '/suite',
    name: 'Suite',
    redirect: '/suite/suite',
    component: Layout,
    meta: {
      title: '测试套件',
      icon: renderIcon(SkypeOutlined),
      sort: 19,
    },
    children: [
      {
        path: 'suite',
        name: 'suite_suite',
        meta: {
          title: '套件名称',
        },
        component: () => import('@/views/suite/suite.vue'),
      },
      {
        path: 'suite/:id?',
        name: 'suite_suite_edit',
        meta: {
          title: '套件详情',
          hidden: true,
          activeMenu: 'suite_suite',
        },
        component: () => import('@/views/suite/suite_edit.vue'),
      },
      {
        path: 'run_result',
        name: 'suite_run_result',
        meta: {
          title: '运行结果',
        },
        component: () => import('@/views/suite/run_result.vue'),
      },
      {
        path: 'report/:id(.*)',
        name: 'suite_report',
        meta: {
          title: '测试报告',
          hidden: true,
          activeMenu: 'suite_result',
        },
        component: () => import('@/views/suite/report.vue'),
      },
    ],
  },
];

export default routes;
