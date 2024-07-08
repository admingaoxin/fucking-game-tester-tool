<template>
  <n-spin :show="loading">
    <div class="frame">
      <iframe :src="frameSrc" class="frame-iframe" ref="frameRef"></iframe>
    </div>
  </n-spin>
</template>
<script lang="ts" setup>
  import { ref, unref, onMounted, nextTick } from 'vue';
  import { useRoute } from 'vue-router';
  import { RunResultAPI } from '@/api/suite/http';

  const loading = ref(false);
  const frameRef = ref<HTMLFrameElement | null>(null);
  const frameSrc = ref<string>('');

  const route = useRoute();
  const dataId = parseInt(`${route.params.id}`);
  const api = new RunResultAPI();

  // frameSrc.value = `/result/report/${currentRoute.params.id}/index.html`;
  function hideLoading() {
    loading.value = false;
  }

  async function init() {
    const result = await api.getDataByID(dataId);

    frameSrc.value = result.report_url;

    nextTick(() => {
      const iframe = unref(frameRef);
      if (!iframe) return;
      const _frame = iframe as any;
      if (_frame.attachEvent) {
        _frame.attachEvent('onload', () => {
          hideLoading();
        });
      } else {
        iframe.onload = () => {
          hideLoading();
        };
      }
    });
  }

  onMounted(() => {
    setTimeout(() => {
      init();
    }, 1);
  });
</script>

<style lang="less" scoped>
  .frame {
    width: 100%;
    height: 100vh;

    &-iframe {
      width: 100%;
      height: 100%;
      overflow: hidden;
      border: 0;
      box-sizing: border-box;
    }
  }
</style>
