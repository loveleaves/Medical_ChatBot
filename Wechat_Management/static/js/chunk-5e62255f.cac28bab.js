(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5e62255f"],{"7b70":function(e,t,r){"use strict";r.d(t,"g",(function(){return a})),r.d(t,"e",(function(){return l})),r.d(t,"a",(function(){return o})),r.d(t,"i",(function(){return i})),r.d(t,"c",(function(){return s})),r.d(t,"h",(function(){return c})),r.d(t,"f",(function(){return u})),r.d(t,"b",(function(){return p})),r.d(t,"j",(function(){return m})),r.d(t,"d",(function(){return d}));var n=r("b775");function a(e){return Object(n["a"])({url:"/cricleai/frequentcylog/list",method:"get",params:e})}function l(e){return Object(n["a"])({url:"/cricleai/frequentcylog/"+e,method:"get"})}function o(e){return Object(n["a"])({url:"/cricleai/frequentcylog",method:"post",data:e})}function i(e){return Object(n["a"])({url:"/cricleai/frequentcylog",method:"put",data:e})}function s(e){return Object(n["a"])({url:"/cricleai/frequentcylog/"+e,method:"delete"})}function c(e){return Object(n["a"])({url:"/cricleai/frequentcylog/sys/list",method:"get",params:e})}function u(e){return Object(n["a"])({url:"/cricleai/frequentcylog/sys/"+e,method:"get"})}function p(e){return Object(n["a"])({url:"/cricleai/frequentcylog/sys",method:"post",data:e})}function m(e){return Object(n["a"])({url:"/cricleai/frequentcylog/sys",method:"put",data:e})}function d(e){return Object(n["a"])({url:"/cricleai/frequentcylog/sys/"+e,method:"delete"})}},"7cac":function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"app-container"},[r("el-form",{directives:[{name:"show",rawName:"v-show",value:e.showSearch,expression:"showSearch"}],ref:"queryForm",attrs:{model:e.queryParams,size:"small",inline:!0,"label-width":"68px"}},[r("el-form-item",{attrs:{label:"操作名称",prop:"operationName"}},[r("el-input",{attrs:{placeholder:"请输入操作名称",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.operationName,callback:function(t){e.$set(e.queryParams,"operationName",t)},expression:"queryParams.operationName"}})],1),r("el-form-item",{attrs:{label:"操作类型(1:对话)",prop:"operationType"}},[r("el-select",{attrs:{placeholder:"请选择操作类型(1:对话)",clearable:""},model:{value:e.queryParams.operationType,callback:function(t){e.$set(e.queryParams,"operationType",t)},expression:"queryParams.operationType"}},e._l(e.dict.type.operation_type,(function(e){return r("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),r("el-form-item",{attrs:{label:"对应的ID,如果对话则可以对应到具体内容",prop:"operationId"}},[r("el-input",{attrs:{placeholder:"请输入对应的ID,如果对话则可以对应到具体内容",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.operationId,callback:function(t){e.$set(e.queryParams,"operationId",t)},expression:"queryParams.operationId"}})],1),r("el-form-item",{attrs:{label:"变化内容",prop:"changeContent"}},[r("el-input",{attrs:{placeholder:"请输入变化内容",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.changeContent,callback:function(t){e.$set(e.queryParams,"changeContent",t)},expression:"queryParams.changeContent"}})],1),r("el-form-item",{attrs:{label:"影响用户",prop:"userId"}},[r("el-input",{attrs:{placeholder:"请输入影响用户",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.userId,callback:function(t){e.$set(e.queryParams,"userId",t)},expression:"queryParams.userId"}})],1),r("el-form-item",{attrs:{label:"是否删除",prop:"isDetele"}},[r("el-input",{attrs:{placeholder:"请输入是否删除",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.isDetele,callback:function(t){e.$set(e.queryParams,"isDetele",t)},expression:"queryParams.isDetele"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini"},on:{click:e.handleQuery}},[e._v("搜索")]),r("el-button",{attrs:{icon:"el-icon-refresh",size:"mini"},on:{click:e.resetQuery}},[e._v("重置")])],1)],1),r("el-row",{staticClass:"mb8",attrs:{gutter:10}},[r("el-col",{attrs:{span:1.5}},[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:add"],expression:"['chatgpt:frequentcylog:add']"}],attrs:{type:"primary",plain:"",icon:"el-icon-plus",size:"mini"},on:{click:e.handleAdd}},[e._v("新增")])],1),r("el-col",{attrs:{span:1.5}},[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:edit"],expression:"['chatgpt:frequentcylog:edit']"}],attrs:{type:"success",plain:"",icon:"el-icon-edit",size:"mini",disabled:e.single},on:{click:e.handleUpdate}},[e._v("修改")])],1),r("el-col",{attrs:{span:1.5}},[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:remove"],expression:"['chatgpt:frequentcylog:remove']"}],attrs:{type:"danger",plain:"",icon:"el-icon-delete",size:"mini",disabled:e.multiple},on:{click:e.handleDelete}},[e._v("删除")])],1),r("el-col",{attrs:{span:1.5}},[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:export"],expression:"['chatgpt:frequentcylog:export']"}],attrs:{type:"warning",plain:"",icon:"el-icon-download",size:"mini"},on:{click:e.handleExport}},[e._v("导出")])],1),r("right-toolbar",{attrs:{showSearch:e.showSearch},on:{"update:showSearch":function(t){e.showSearch=t},"update:show-search":function(t){e.showSearch=t},queryTable:e.getList}})],1),r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.frequentcylogList},on:{"selection-change":e.handleSelectionChange}},[r("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),r("el-table-column",{attrs:{label:"主键",align:"center",prop:"id"}}),r("el-table-column",{attrs:{label:"操作名称",align:"center",prop:"operationName"}}),r("el-table-column",{attrs:{label:"操作类型(1:对话)",align:"center",prop:"operationType"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("dict-tag",{attrs:{options:e.dict.type.operation_type,value:t.row.operationType}})]}}])}),r("el-table-column",{attrs:{label:"对应的ID,如果对话则可以对应到具体内容",align:"center",prop:"operationId"}}),r("el-table-column",{attrs:{label:"变化内容",align:"center",prop:"changeContent"}}),r("el-table-column",{attrs:{label:"影响用户",align:"center",prop:"userId"}}),r("el-table-column",{attrs:{label:"是否删除",align:"center",prop:"isDetele"}}),r("el-table-column",{attrs:{label:"备注",align:"center",prop:"remark"}}),r("el-table-column",{attrs:{label:"操作",align:"center","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:edit"],expression:"['chatgpt:frequentcylog:edit']"}],attrs:{size:"mini",type:"text",icon:"el-icon-edit"},on:{click:function(r){return e.handleUpdate(t.row)}}},[e._v("修改")]),r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:frequentcylog:remove"],expression:"['chatgpt:frequentcylog:remove']"}],attrs:{size:"mini",type:"text",icon:"el-icon-delete"},on:{click:function(r){return e.handleDelete(t.row)}}},[e._v("删除")])]}}])})],1),r("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.queryParams.pageNum,limit:e.queryParams.pageSize},on:{"update:page":function(t){return e.$set(e.queryParams,"pageNum",t)},"update:limit":function(t){return e.$set(e.queryParams,"pageSize",t)},pagination:e.getList}}),r("el-dialog",{attrs:{title:e.title,visible:e.open,width:"500px","append-to-body":""},on:{"update:visible":function(t){e.open=t}}},[r("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,"label-width":"80px"}},[r("el-form-item",{attrs:{label:"操作名称",prop:"operationName"}},[r("el-input",{attrs:{placeholder:"请输入操作名称"},model:{value:e.form.operationName,callback:function(t){e.$set(e.form,"operationName",t)},expression:"form.operationName"}})],1),r("el-form-item",{attrs:{label:"操作类型(1:对话)",prop:"operationType"}},[r("el-select",{attrs:{placeholder:"请选择操作类型(1:对话)"},model:{value:e.form.operationType,callback:function(t){e.$set(e.form,"operationType",t)},expression:"form.operationType"}},e._l(e.dict.type.operation_type,(function(e){return r("el-option",{key:e.value,attrs:{label:e.label,value:parseInt(e.value)}})})),1)],1),r("el-form-item",{attrs:{label:"对应的ID,如果对话则可以对应到具体内容",prop:"operationId"}},[r("el-input",{attrs:{placeholder:"请输入对应的ID,如果对话则可以对应到具体内容"},model:{value:e.form.operationId,callback:function(t){e.$set(e.form,"operationId",t)},expression:"form.operationId"}})],1),r("el-form-item",{attrs:{label:"变化内容",prop:"changeContent"}},[r("el-input",{attrs:{placeholder:"请输入变化内容"},model:{value:e.form.changeContent,callback:function(t){e.$set(e.form,"changeContent",t)},expression:"form.changeContent"}})],1),r("el-form-item",{attrs:{label:"影响用户",prop:"userId"}},[r("el-input",{attrs:{placeholder:"请输入影响用户"},model:{value:e.form.userId,callback:function(t){e.$set(e.form,"userId",t)},expression:"form.userId"}})],1),r("el-form-item",{attrs:{label:"是否删除",prop:"isDetele"}},[r("el-input",{attrs:{placeholder:"请输入是否删除"},model:{value:e.form.isDetele,callback:function(t){e.$set(e.form,"isDetele",t)},expression:"form.isDetele"}})],1),r("el-form-item",{attrs:{label:"备注",prop:"remark"}},[r("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.remark,callback:function(t){e.$set(e.form,"remark",t)},expression:"form.remark"}})],1)],1),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"primary"},on:{click:e.submitForm}},[e._v("确 定")]),r("el-button",{on:{click:e.cancel}},[e._v("取 消")])],1)],1)],1)},a=[],l=r("5530"),o=(r("d81d"),r("7b70")),i={name:"Frequentcylog",dicts:["operation_type"],data:function(){return{loading:!0,ids:[],single:!0,multiple:!0,showSearch:!0,total:0,frequentcylogList:[],title:"",open:!1,queryParams:{pageNum:1,pageSize:10,operationName:null,operationType:null,operationId:null,changeContent:null,userId:null,isDetele:null},form:{},rules:{}}},created:function(){this.getList()},methods:{getList:function(){var e=this;this.loading=!0,Object(o["g"])(this.queryParams).then((function(t){e.frequentcylogList=t.rows,e.total=t.total,e.loading=!1}))},cancel:function(){this.open=!1,this.reset()},reset:function(){this.form={id:null,operationName:null,operationType:null,operationId:null,changeContent:null,userId:null,isDetele:null,createBy:null,createTime:null,updateBy:null,updateTime:null,remark:null},this.resetForm("form")},handleQuery:function(){this.queryParams.pageNum=1,this.getList()},resetQuery:function(){this.resetForm("queryForm"),this.handleQuery()},handleSelectionChange:function(e){this.ids=e.map((function(e){return e.id})),this.single=1!==e.length,this.multiple=!e.length},handleAdd:function(){this.reset(),this.open=!0,this.title="添加次数消耗日志"},handleUpdate:function(e){var t=this;this.reset();var r=e.id||this.ids;Object(o["e"])(r).then((function(e){t.form=e.data,t.open=!0,t.title="修改次数消耗日志"}))},submitForm:function(){var e=this;this.$refs["form"].validate((function(t){t&&(null!=e.form.id?Object(o["i"])(e.form).then((function(t){e.$modal.msgSuccess("修改成功"),e.open=!1,e.getList()})):Object(o["a"])(e.form).then((function(t){e.$modal.msgSuccess("新增成功"),e.open=!1,e.getList()})))}))},handleDelete:function(e){var t=this,r=e.id||this.ids;this.$modal.confirm('是否确认删除次数消耗日志编号为"'+r+'"的数据项？').then((function(){return Object(o["c"])(r)})).then((function(){t.getList(),t.$modal.msgSuccess("删除成功")})).catch((function(){}))},handleExport:function(){this.download("cricleai/frequentcylog/export",Object(l["a"])({},this.queryParams),"frequentcylog_".concat((new Date).getTime(),".xlsx"))}}},s=i,c=r("2877"),u=Object(c["a"])(s,n,a,!1,null,null,null);t["default"]=u.exports}}]);