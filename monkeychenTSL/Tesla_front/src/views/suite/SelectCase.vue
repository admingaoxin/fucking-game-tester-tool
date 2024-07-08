<template>
  <n-transfer
    ref="transfer"
    source-title="全部用例"
    target-title="已选用例"
    :value="value"
    :options="options"
    :on-update:value="handleChange"
    virtual-scroll
    source-filterable
    target-filterable
  />
</template>

<script lang="ts" setup>
  import { ref, defineProps, onMounted, computed, PropType } from 'vue';

  const props = defineProps({
    suiteId: {
      type: Number,
      required: false,
    },
    refSelectData: {
      type: Array as PropType<number[]>,
      required: true,
    },
    funcLoadCaseData: {
      type: Function,
      required: true,
    },
  });
  const emit = defineEmits(['someEvent']);

  const options = ref<{ label: string; value: number }[]>([{ label: 'sss', value: 123 }]);
  const value = computed<number[]>(() => props.refSelectData);

  async function loadAllData() {
    const data_list = await props.funcLoadCaseData();
    options.value = data_list.list.map((v) => ({
      label: `ID：${v.id} - 用例名称：${v.name}`,
      value: v.id,
    }));
  }

  function handleChange(value) {
    // 把value发送给父组件，让父组件修改refSelectData
    emit('someEvent', { value });
  }

  onMounted(() => {
    setTimeout(() => {
      loadAllData();
    }, 16);
  });
</script>
