import json

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class CodeResultMessageRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: Response = renderer_context.get("response")
        response_dict = {
            "code": response.status_code,
            "message": "ok",
            "result": data
        }
        # 状态码200-300
        if 300 >= response.status_code >= 200:
            pass
        # 状态码400以上
        elif response.status_code >= 400:
            if "detail" in data:
                response_dict["message"] = data["detail"]
            elif isinstance(data, dict):
                try:
                    msg = list(data.values())[0][0]
                except Exception:
                    msg = json.dumps(data)
                response_dict["message"] = msg
            elif isinstance(data, list):
                msg = str(data[0])
                response_dict["message"] = msg
        return super().render(response_dict, accepted_media_type, renderer_context)
