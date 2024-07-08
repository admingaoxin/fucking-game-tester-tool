import { http } from "@/utils/http/axios";
import { Profile, ResetPass } from "./models";
//登录接口
export function login(params) {
    return http.request<Profile>(
      {
        url: '/account/profile/login/',
        method: 'POST',
        params,
      },
      {
        isTransformResponse: false,
      }
    );
  }
//查询个人资料接口
export function profile(params?) {
    return http.request<Profile>(
      {
        url: '/account/profile/profile/',
        method: 'GET',
        params,
      },
    );
  }
//修改个人资料接口
export function changeProfile(params:Profile) {
  return http.request<Profile>(
    {
      url: '/account/profile/change/',
      method: 'POST',
      params,
    },
  );
}
//修改密码接口
export function reset_password(params:ResetPass) {
  return http.request(
    {
      url: '/account/profile/reset_password/',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
//查询用户接口
export function user_list() {
  return http.request<Profile[]>(
    {
      url: '/account/profile/all_user/',
      method: 'GET',
    },
  );
}