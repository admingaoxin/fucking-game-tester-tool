import { http } from '@/utils/http/axios';

import { Suite, RunResult } from './models';
import { BaseModelAPI } from '../base_api';

export class SuiteAPI extends BaseModelAPI<Suite> {
  base_url = '/suite/suite/';

  runById(id) {
    return http.request({
      url: `${this.base_url}${id}/run/`,
      method: 'post',
    });
  }
}

export class RunResultAPI extends BaseModelAPI<RunResult> {
runById(id: any) {
throw new Error('Method not implemented.');
}
  base_url = '/suite/run_result/';
}
