import { Endpoint, Case } from "./models";
import { BaseModelAPI } from "../base_api";
export class EndpointAPI extends BaseModelAPI<Endpoint>{
  base_url="/api_case/endpoint/";
}
export class CaseAPI extends BaseModelAPI<Case>{
  base_url="/api_case/case/";
}
