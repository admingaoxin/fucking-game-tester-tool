<template>
  <div class="top-btn-container">
    <div class="left-buttons">
      <n-button @click="del_row">删除选中行</n-button>
      <n-button @click="add_col">增加空列</n-button>
      <n-button @click="clear_col">移除空列</n-button>
      <n-button @click="rest_table">清空</n-button>
    </div>

    <div class="right-buttons">
      <n-upload ref="upload" action="#" @default-upload="false" @before-upload="beforeUpload">
        <n-button>从excel中导入</n-button>
      </n-upload>
    </div>
  </div>
  <div>
    <n-data-table
      :columns="tableColumn"
      :data="tableData"
      :pagination="false"
      :bordered="false"
      :row-key="rowKey"
      :checked-row-keys="checkedRowKeysRef"
      @update:checked-row-keys="handleCheck"
    />

    <n-button @click="add_row">增加步骤</n-button>
  </div>
</template>

<script lang="ts" setup>
  import { h, ref } from 'vue';
  import { NInput, NSelect } from 'naive-ui';
  import { read, utils } from 'xlsx';

  // const steps_keys = ['序号', '步骤名', '关键字', '参数', '_BlankField'];

  const defaultColumn = () => [
    {
      title: 'X',
      type: 'selection',
    },
    {
      title: '序号',
      key: '序号',
      // sortOrder: false,
      // sorter(rowA, rowB) {
      //   return rowA.序号 - rowB.序号
      // },
    },
    {
      title: '步骤名',
      key: '步骤名',
      render(row, index) {
        return h(NInput, {
          value: row.步骤名,
          onUpdateValue(v) {
            tableData.value[index].步骤名 = v;
          },
        });
      },
    },
    {
      title: '关键字',
      key: '关键字',
      render(row, index) {
        return h(NSelect, {
          value: row.关键字,
          filterable: true,
          options: key_word_options.value,
          onUpdateValue(v) {
            tableData.value[index].关键字 = v;
          },
        });
      },
    },
    {
      title: '参数',
      key: '参数',
      render(row, index) {
        return h(NInput, {
          value: row.参数,
          onUpdateValue(v) {
            tableData.value[index].参数 = v;
          },
        });
      },
    },
  ];
  const defaultData = () => [
    { 序号: 1, 步骤名: '', 关键字: '', 参数: '', _BlankField: [] },
    { 序号: 2, 步骤名: '', 关键字: '', 参数: '', _BlankField: [] },
  ];
  const defaultColumnNames = defaultColumn().map((item) => item.title);

  const checkedRowKeysRef = ref([]);
  const tableColumn = ref(defaultColumn());
  const tableData = ref(defaultData());

  const key_word_options = ref([
    {
      type: 'group',
      label: 'selenium',
      key: 'selenium',
      children: [
        {
          label: '设置浏览器',
          value: 'set_driver',
        },
        {
          label: '页面跳转',
          value: 'goto',
        },
        {
          label: '输入内容',
          value: 'input',
        },
        {
          label: '清空内容',
          value: 'clear',
        },
        {
          label: '点击元素',
          value: 'click',
        },
        {
          label: '文本保存到变量',
          value: 'save_text',
        },
        {
          label: '执行断言',
          value: 'assert',
        },
        {
          label: '进入iframe',
          value: 'iframe_enter',
        },
        {
          label: '退出iframe',
          value: 'iframe_exit',
        },
        {
          label: '下拉选择文本',
          value: 'select',
        },
        {
          label: '执行JavaScript',
          value: 'js_code',
        },
        {
          label: '强制等待',
          value: 'sleep',
        },
        {
          label: '更多关键字待添加',
          value: 'todo',
          disabled: true,
        },
      ],
    },
    {
      type: 'group',
      label: 'appium',
      key: 'appium',
      children: [
        {
          label: '更多关键字待添加',
          value: 'todo',
          disabled: true,
        },
      ],
    },
  ]);
  const new_col_name = ref('列');
  const new_col_num = ref(0);

  const beforeUpload = (data) => {
    const file_type = data.file.file?.type;
    const isExcel =
      file_type === 'application/vnd.ms-excel' ||
      file_type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    if (isExcel) {
      loadByXlsx(data);
    } else {
      // message.error("只能上传xlsx格式的文件，请重新上传");
      alert('只能上传xlsx格式的文件,请重新上传');
    }

    return false;
  };

  const loadByXlsx = (options) => {
    // const workbook = read(options.file, {type: 'array'});
    let reader = new FileReader();
    let workbook;
    reader.onload = function (event) {
      const row_data = new Uint8Array(event.target?.result);
      workbook = read(row_data, { type: 'array' });

      // 在此处处理工作簿数据，例如将其转换为JSON格式
      // console.log(workbook);
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const data: Array<any> = utils.sheet_to_json(worksheet, { header: 1 });
      const ColumnNames = tableColumn.value.map((item) => item.title);
      data[0].forEach((item) => {
        if (item && !ColumnNames.includes(item)) {
          add_col(); //增加扩展列
        }
      });
      // todo
      // tableData.value = data.slice(1).map((row, row_id) =>
      //   row.reduce((acc, cur, i) => {
      //     acc[tableColumn.value[i + 1].key] = cur;
      //     acc.序号 = row_id + 1; // 重写序号
      //     return acc;
      //   }, {})
      // );
      tableData.value = data.slice(1).map((row, row_id) => {
        let row_data = row.reduce((acc, cur, i) => {
          let column = tableColumn.value[i + 1].key;

          if (column) {
            acc[column] = cur;
            acc.序号 = row_id + 1; // 重写序号
          }
          return acc;
        }, {});
        // console.log(row_data);
        return row_data;
      });
    };
    reader.readAsArrayBuffer(options.file.file);
  };

  const add_col = () => {
    new_col_num.value++;
    const d = `${new_col_name.value}${new_col_num.value}`;
    tableColumn.value.push({
      title: d,
      key: d,
      render(_row, index) {
        // const { [d]: value } = row;

        return h(NInput, {
          value: tableData.value[index][d],
          onUpdateValue(new_value) {
            tableData.value[index][d] = new_value;
          },
        });
      },
    });
  };
  const add_row = () => {
    tableData.value.push({
      序号: tableData.value.length + 1,
      步骤名: '',
      关键字: '',
      参数: '',
      _BlankField: [],
    });
  };
  const del_row = () => {
    // console.log(checkedRowKeysRef.value)
    const index_list = Object.values(checkedRowKeysRef.value);
    tableData.value = tableData.value.filter((item) => !index_list.includes(item.序号));
    tableData.value.forEach((item, index) => {
      console.log(item, (item.序号 = index + 1));
    });
    checkedRowKeysRef.value = [];
  };

  const clear_col = () => {
    let not_empty_list: string[] = [];
    tableColumn.value.forEach((ClomunItem) => {
      // console.log(ClomunItem.title)
      for (let RowItem of tableData.value) {
        const { [ClomunItem.title]: value } = RowItem;
        console.log(`title = ${ClomunItem.title} , value = ${value}`);

        let can_break = false;

        if (defaultColumnNames.includes(ClomunItem.title)) {
          can_break = true;
        }

        if (typeof value === 'string') {
          if (value !== '') {
            can_break = true;
          }
        } else {
          if (typeof value != 'undefined') {
            can_break = true;
          }
        }

        if (can_break === true) {
          // 默认列和非空列不进行移除
          not_empty_list.push(ClomunItem.title);
          break;
        }
      }
    });

    tableColumn.value = tableColumn.value.filter((item) => not_empty_list.includes(item.title));

    console.log(not_empty_list);
    // todo 重新计算 new_col_num
  };
  const rest_table = () => {
    console.log('rest_table');
    tableColumn.value = defaultColumn();
    tableData.value = defaultData();
    new_col_num.value = 0;
    checkedRowKeysRef.value = [];
  };

  const rowKey = (row) => row.序号;
  function handleCheck(rowKeys) {
    checkedRowKeysRef.value = rowKeys;
  }

  function setData(data) {
    rest_table();
    // 解析_BlankField列
    let max_BlankField_len = 0;

    data.map((step) => {
      let _BlankField_len = 0;

      step._BlankField.forEach((value) => {
        _BlankField_len++;
        let key = `${new_col_name.value}${_BlankField_len}`;
        step[key] = value;
        // return key;
      });

      if (_BlankField_len > max_BlankField_len) {
        max_BlankField_len = _BlankField_len;
      }
    });

    tableData.value = data;
    for (let i = 0; i < max_BlankField_len; i++) {
      add_col(); //增加扩展列
    }
  }

  function getData() {
    clear_col();

    let data = JSON.parse(JSON.stringify(tableData.value));
    const _BlankField_keys: string[] = Array.from(
      { length: new_col_num.value },
      (_, i) => `${new_col_name.value}${i + 1}`
    );

    data.map((step) => {
      step._BlankField = [];
      _BlankField_keys.forEach((key) => {
        if (step.hasOwnProperty(key) && step[key] !== '') {
          step._BlankField.push(step[key]);
          delete step[key];
        }
        // return key;
      });
    });
    return data;
  }

  defineExpose({
    getData,
    setData,
  });
</script>

<style>
  .top-btn-container {
    display: flex;
    justify-content: space-between;
  }

  .left-buttons {
    display: flex;
    justify-content: flex-start;
  }

  .right-buttons {
    display: flex;
    justify-content: flex-end;
  }
</style>
