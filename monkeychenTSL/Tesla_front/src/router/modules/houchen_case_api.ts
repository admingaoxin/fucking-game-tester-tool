import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { DingdingOutlined } from '@vicons/antd';
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
    path: '/case_api',
    name: 'Case_Api',
    redirect: '/case_api/403',
    component: Layout,
    meta: {
      title: '接口测试',
      icon: renderIcon(DingdingOutlined),
      sort: 17,
    },
    children: [
      {
        path: 'endpoint',
        name: 'case_api_endpoint',
        meta: {
          title: '接口管理',
        },
        component: () => import('@/views/case_api/endpoint.vue'),
      },
      {
        path: 'endpoint/:id?',
        name: 'case_api_endpoint_edit',
        meta: {
          title: '接口编辑',
          hidden:true,
          activeMenu:'case_api_endpoint',
        },
        component: () => import('@/views/case_api/endpoint_edit.vue'),
      },
      {
        path: 'case',
        name: 'case_api_case',
        meta: {
          title: '用例管理',
        },
        component: () => import('@/views/case_api/case.vue'),
      },
      {
        path: 'case/:id?',
        name: 'case_api_case_edit',
        meta: {
          title: '用例编辑',
          hidden:true,
          activeMenu:'case_api_case',
        },
        component: () => import('@/views/case_api/case_edit.vue'),
      },

    ],
  },
];

export default routes;
