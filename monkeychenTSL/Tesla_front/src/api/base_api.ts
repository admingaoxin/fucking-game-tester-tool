//先写出非面向对象的代码
//创建类，让代码建立关联
//修改类，让类变的更加抽象
import { http } from "@/utils/http/axios";



export class BaseModelAPI<T>{
    //base_url="/system/department";
    base_url="/";
//查询数据列表
getDataList(params?) {
  return http.request<T[]>({
    url: `${this.base_url}`,
    method: 'GET',
    params,
  });
}
//创建数据
createData(params: T) {
  return http.request<T>({
    url: `${this.base_url}`,
    method: 'POST',
    params,
  });
}
//查询数据详情
 getDataByID(id) {
    return http.request<T>(
      {
        url: `${this.base_url}${id}/`,
        method: 'GET',      
      },

    )
  }
//修改数据详情
 upDataByID(id,newData:T) {
    return http.request<T>(
      {
        url: `${this.base_url}${id}/`,
        method: 'PUT',  
        data:newData,    
      },

    )
  }
//删除数据
//查询数据详情
 DelDataByID(id) {
    return http.request<T>(
      {
        url: `${this.base_url}${id}/`,
        method: 'DELETE',      
      },
      {
        isTransformResponse: false,
      }
    )
  }
}