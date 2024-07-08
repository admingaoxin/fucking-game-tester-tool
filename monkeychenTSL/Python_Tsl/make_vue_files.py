from pathlib import Path
import shutil

base_dir = Path(r"F:\AutoWeb\Tesla_front\src")
files = """views/account/profile.vue
views/account/reset_password.vue
views/case_api/endpoint.vue
views/case_api/case.vue
views/case_ui/element.vue
views/case_ui/case.vue
views/project/project.vue
views/project/config.vue
views/suite/suite.vue
views/suite/run_result.vue
views/system/department.vue
views/system/position.vue
views/system/role.vue"""
for file in files.split("\n"):
    path = base_dir / file
    # print(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"""<template>{file}
</template>
<script lang="ts" setup>
</script>
<style lang="less" scoped>
</style>

""")
