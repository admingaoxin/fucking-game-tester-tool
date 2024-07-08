import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { YoutubeOutlined } from '@vicons/antd';
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
    path: '/case_ui',
    name: 'Case_Ui',
    redirect: '/case_ui/403',
    component: Layout,
    meta: {
      title: 'UI测试',
      icon: renderIcon(YoutubeOutlined),
      sort: 18,
    },
    children: [
      {
        path: 'element',
        name: 'case_ui_element',
        meta: {
          title: '元素管理',
        },
        component: () => import('@/views/case_ui/element.vue'),
      },
      {
        path: 'element/:id?',
        name: 'case_ui_element_edit',
        meta: {
          title: '元素详情',
          hidden: true,
          activeMenu: 'case_ui_element',
        },
        component: () => import('@/views/case_ui/element_edit.vue'),
      },
      {
        path: 'case',
        name: 'case_ui_case',
        meta: {
          title: '用例管理',
        },
        component: () => import('@/views/case_ui/case.vue'),
      },
      {
        path: 'case/:id?',
        name: 'case_ui_case_edit',
        meta: {
          title: '用例编辑',
          hidden:true,
          activeMenu:'case_ui_case',
        },
        component: () => import('@/views/case_ui/case_edit.vue'),
      },
    ],
  },
];

export default routes;
