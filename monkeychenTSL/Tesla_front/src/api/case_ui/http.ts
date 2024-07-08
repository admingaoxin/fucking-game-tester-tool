import { Element, CaseUI } from "./models";
import { BaseModelAPI } from "../base_api";
export class ElementAPI extends BaseModelAPI<Element>{
  base_url="/api_ui/element/";
}
export class CaseUIAPI extends BaseModelAPI<CaseUI>{
  base_url="/api_ui/case/";
}
