import { Project, Config } from "./models";
import { BaseModelAPI } from "../base_api";
export class ProjectAPI extends BaseModelAPI<Project>{
  base_url="/project/project/";
}
export class ConfigAPI extends BaseModelAPI<Config>{
  base_url="/project/config/";
}
