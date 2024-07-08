<template>
  <n-tabs type="line" animated>
    <n-tab-pane name="headers" tab="请求头">
      <DynamicInput :data="request.headers" @some-event="(vals) => update('headers', vals)" />
    </n-tab-pane>

    <n-tab-pane name="cookies" tab="Cookie">
      <DynamicInput :data="request.cookies" @some-event="(vals) => update('cookies', vals)" />
    </n-tab-pane>

    <n-tab-pane name="params" tab="查询字符串">
      <DynamicInput :data="request.params" @some-event="(vals) => update('params', vals)" />
    </n-tab-pane>

    <n-tab-pane name="data" tab="From表单">
      <DynamicInput :data="request.data" @some-event="(vals) => update('data', vals)" />
    </n-tab-pane>

    <n-tab-pane name="json" tab="JSON">
      <JsonEditorVue
        :modelValue="request.json"
        v-model:mode="jsonEditor.mode"
        @update:modelValue="jsonOnChenge"
        v-bind="{
          /* local props & attrs */
        }"
      />
    </n-tab-pane>
  </n-tabs>
</template>

<script lang="ts" setup>
  import { PropType, reactive } from 'vue';
  import JsonEditorVue from 'json-editor-vue';
  import DynamicInput from './DynamicDict.vue';

  const props = defineProps({
    request: {
      type: Object as PropType<any>,
      required: true,
    },
  });

  console.log('request', props.request);
  const emit = defineEmits(['update']);

  const jsonEditor = reactive({
    mode: 'text',
    readOnly: false,
  });

  function update(attr, vals) {
    // console.log(attr, vals);
    emit('update', attr, vals);
  }

  function jsonOnChenge(vals) {
    // console.log(vals);
    // console.log(jsonEditor.mode);
    emit('update', 'json', JSON.parse(vals));
  }
</script>

<style>
  .jse-main {
    height: 440px;
  }
</style>
