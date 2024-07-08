import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { SlackSquareOutlined } from '@vicons/antd';
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
    path: '/system',
    name: 'System',
    redirect: '/system/403',
    component: Layout,
    meta: {
      title: '系统设置',
      icon: renderIcon(SlackSquareOutlined),
      sort: 21,
    },
    children: [
      {
        path: 'department',
        name: 'system_department',
        meta: {
          title: '部门',
        },
        component: () => import('@/views/system/department.vue'),
      },
      {
        path: 'department/:id?',
        name: 'system_department_edit',
        meta: {
          title: '部门详情',
          hidden:true,
          activeMenu:'system_department',
        },
        component: () => import('@/views/system/department_edit.vue'),
      },
      {
        path: 'position',
        name: 'system_position',
        meta: {
          title: '职位',
        },
        component: () => import('@/views/system/position.vue'),
      },
      {
        path: 'position/:id?',
        name: 'system_position_edit',
        meta: {
          title: '职位详情',
          hidden: true,
          activeMenu: 'system_position',
        },
        component: () => import('@/views/system/position_edit.vue'),
      },
      {
        path: 'role',
        name: 'system_role',
        meta: {
          title: '角色',
        },
        component: () => import('@/views/system/role.vue'),
      },
      {
        path: 'role/:id?',
        name: 'system_role_edit',
        meta: {
          title: '角色详情',
          hidden: true,
          activeMenu: 'system_role',
        },
        component: () => import('@/views/system/role_edit.vue'),
      },
    ],
  },
];

export default routes;
