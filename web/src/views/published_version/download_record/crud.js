import * as api from './api'
import { urlPrefix as releaseVersionPrefix } from '../published_version/api'
import { urlPrefix as resourceTypeProfix } from '../type/api'
// import { urlPrefix as resourceProfix } from './api'

export const crudOptions = (vm) => {
  return {
    // pagination: false,
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      stripe: false,
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
      defaultExpandAll: true
    },
    rowHandle: {
      width: 180,
      view: {
        thin: true,
        text: '详情',
        title: '详情',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled (index, row) {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: '关键词',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入关键词'
          }
        },
        view: {
          // 查看对话框组件的单独配置
          disabled: true
        }
      },
      {
        title: 'ID',
        key: 'id',
        show: false,
        disabled: true,
        width: 20,
        form: {
          disabled: true
        }
      },
      {
        title: '发版名称',
        key: 'version',
        sortable: true,
        search: {
          disabled: false
        },
        minWidth: 100,
        type: 'select',
        dict: {
          cache: false,
          isTree: true,
          url: releaseVersionPrefix,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            pagination: true,
            props: { multiple: false }
          }
        }
      },
      // {
      //   title: '版本名称',
      //   key: 'version_name',
      //   sortable: true,
      //   search: {
      //     disabled: false
      //   },
      //   minWidth: 80,
      //   type: 'input',
      //   form: {
      //     rules: [
      //       // 表单校验规则
      //       { required: false, message: '版本名称必填项' }
      //     ],
      //     component: {
      //       span: 12,
      //       props: {
      //         clearable: true
      //       },
      //       placeholder: '请输入版本名称'
      //     },
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      // {
      //   title: '项目号',
      //   key: 'product_number',
      //   sortable: true,
      //   search: {
      //     disabled: false
      //   },
      //   minWidth: 60,
      //   type: 'input',
      //   form: {
      //     rules: [
      //       // 表单校验规则
      //       { required: true, message: '项目号必填项' }
      //     ],
      //     component: {
      //       span: 12,
      //       props: {
      //         clearable: true
      //       },
      //       placeholder: '请输入项目号'
      //     },
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      {
        title: '申请人',
        key: 'apply_user',
        sortable: true,
        search: {
          disabled: false
        },
        minWidth: 60,
        type: 'input',
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: '申请人必填项' }
          ],
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入申请人'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '描述',
        key: 'description',
        show: true,
        search: {
          disabled: true
        },
        minWidth: 120,
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入描述说明',
            showWordLimit: true,
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '文档配置',
        key: 'doc_info',
        show: false,
        search: {
          disabled: true
        },
        minWidth: 120,
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入配置内容',
            showWordLimit: true,
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '软件配置',
        key: 'sw_info',
        show: false,
        search: {
          disabled: true
        },
        minWidth: 120,
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入配置内容',
            showWordLimit: true,
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '申请下载时间',
        key: 'apply_time',
        width: 100,
        type: 'datetime',
        component: { name: 'date-format', props: { format: 'YYYY-MM-DD HH:MM' } }
      }
    ].concat(vm.commonEndColumns())
  }
}
