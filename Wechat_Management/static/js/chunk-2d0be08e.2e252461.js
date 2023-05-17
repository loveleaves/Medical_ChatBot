(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0be08e"],{"2f15":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container"},[a("el-form",{directives:[{name:"show",rawName:"v-show",value:e.showSearch,expression:"showSearch"}],ref:"queryForm",attrs:{model:e.queryParams,size:"small",inline:!0,"label-width":"68px"}},[a("el-form-item",{attrs:{label:"是否展示",prop:"isShow"}},[a("el-select",{attrs:{placeholder:"请选择是否展示",clearable:""},model:{value:e.queryParams.isShow,callback:function(t){e.$set(e.queryParams,"isShow",t)},expression:"queryParams.isShow"}},e._l(e.dict.type.is_use,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini"},on:{click:e.handleQuery}},[e._v("搜索")]),a("el-button",{attrs:{icon:"el-icon-refresh",size:"mini"},on:{click:e.resetQuery}},[e._v("重置")])],1)],1),a("el-row",{staticClass:"mb8",attrs:{gutter:10}},[a("el-col",{attrs:{span:1.5}},[a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:sys:add"],expression:"['chatgpt:employ:sys:add']"}],attrs:{type:"primary",plain:"",icon:"el-icon-plus",size:"mini"},on:{click:e.handleAdd}},[e._v("新增")])],1),a("el-col",{attrs:{span:1.5}},[a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:sys:edit"],expression:"['chatgpt:employ:sys:edit']"}],attrs:{type:"success",plain:"",icon:"el-icon-edit",size:"mini",disabled:e.single},on:{click:e.handleUpdate}},[e._v("修改")])],1),a("el-col",{attrs:{span:1.5}},[a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:sys:remove"],expression:"['chatgpt:employ:sys:remove']"}],attrs:{type:"danger",plain:"",icon:"el-icon-delete",size:"mini",disabled:e.multiple},on:{click:e.handleDelete}},[e._v("删除")])],1),a("el-col",{attrs:{span:1.5}},[a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:sys:export"],expression:"['chatgpt:employ:sys:export']"}],attrs:{type:"warning",plain:"",icon:"el-icon-download",size:"mini"},on:{click:e.handleExport}},[e._v("导出")])],1),a("right-toolbar",{attrs:{showSearch:e.showSearch},on:{"update:showSearch":function(t){e.showSearch=t},"update:show-search":function(t){e.showSearch=t},queryTable:e.getList}})],1),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.employList},on:{"selection-change":e.handleSelectionChange}},[a("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),a("el-table-column",{attrs:{label:"名单主键",align:"center",prop:"anserId"}}),a("el-table-column",{attrs:{label:"询问名称",align:"center",prop:"anserTitle","show-overflow-tooltip":!0}}),a("el-table-column",{attrs:{label:"询问内容",align:"center",prop:"anserContent","show-overflow-tooltip":!0}}),a("el-table-column",{attrs:{label:"回答时间",align:"center",prop:"createTime","show-overflow-tooltip":!0}}),a("el-table-column",{attrs:{label:"操作",align:"center","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:edit"],expression:"['chatgpt:employ:edit']"}],attrs:{size:"mini",type:"text",icon:"el-icon-edit"},on:{click:function(a){return e.handleUpdate(t.row)}}},[e._v("修改")]),a("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:employ:remove"],expression:"['chatgpt:employ:remove']"}],attrs:{size:"mini",type:"text",icon:"el-icon-delete"},on:{click:function(a){return e.handleDelete(t.row)}}},[e._v("删除")])]}}])})],1),a("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.queryParams.pageNum,limit:e.queryParams.pageSize},on:{"update:page":function(t){return e.$set(e.queryParams,"pageNum",t)},"update:limit":function(t){return e.$set(e.queryParams,"pageSize",t)},pagination:e.getList}}),a("el-dialog",{attrs:{title:e.title,visible:e.open,width:"500px","append-to-body":""},on:{"update:visible":function(t){e.open=t}}},[a("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"询问名称",prop:"anserTitle"}},[a("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.anserTitle,callback:function(t){e.$set(e.form,"anserTitle",t)},expression:"form.anserTitle"}})],1),a("el-form-item",{attrs:{label:"询问内容"}},[a("editor",{attrs:{"min-height":192},model:{value:e.form.anserContent,callback:function(t){e.$set(e.form,"anserContent",t)},expression:"form.anserContent"}})],1),a("el-form-item",{attrs:{label:"是否展示",prop:"isShow"}},[a("el-select",{attrs:{placeholder:"请选择是否展示"},model:{value:e.form.isShow,callback:function(t){e.$set(e.form,"isShow",t)},expression:"form.isShow"}},e._l(e.dict.type.is_use,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:parseInt(e.value)}})})),1)],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{type:"primary"},on:{click:e.submitForm}},[e._v("确 定")]),a("el-button",{on:{click:e.cancel}},[e._v("取 消")])],1)],1)],1)},n=[],i=a("5530"),s=(a("d81d"),a("b775"));function o(e){return Object(s["a"])({url:"/cricleai/employ/sys/list",method:"get",params:e})}function r(e){return Object(s["a"])({url:"/cricleai/employ/sys/"+e,method:"get"})}function c(e){return Object(s["a"])({url:"/cricleai/employ/sys",method:"post",data:e})}function u(e){return Object(s["a"])({url:"/cricleai/employ/sys",method:"put",data:e})}function m(e){return Object(s["a"])({url:"/cricleai/employ/sys/"+e,method:"delete"})}var p={name:"Employ",dicts:["is_use"],data:function(){return{loading:!0,ids:[],single:!0,multiple:!0,showSearch:!0,total:0,employList:[],title:"",open:!1,queryParams:{pageNum:1,pageSize:10,anserTitle:null,anserContent:null,isShow:null},form:{},rules:{}}},created:function(){this.getList()},methods:{getList:function(){var e=this;this.loading=!0,o(this.queryParams).then((function(t){e.employList=t.rows,e.total=t.total,e.loading=!1}))},cancel:function(){this.open=!1,this.reset()},reset:function(){this.form={anserId:null,anserTitle:null,anserContent:null,userId:null,isShow:null,createBy:null,createTime:null,updateBy:null,updateTime:null,remark:null},this.resetForm("form")},handleQuery:function(){this.queryParams.pageNum=1,this.getList()},resetQuery:function(){this.resetForm("queryForm"),this.handleQuery()},handleSelectionChange:function(e){this.ids=e.map((function(e){return e.anserId})),this.single=1!==e.length,this.multiple=!e.length},handleAdd:function(){this.reset(),this.open=!0,this.title="添加回答收录列"},handleUpdate:function(e){var t=this;this.reset();var a=e.anserId||this.ids;r(a).then((function(e){t.form=e.data,t.open=!0,t.title="修改回答收录列"}))},submitForm:function(){var e=this;this.$refs["form"].validate((function(t){t&&(null!=e.form.anserId?u(e.form).then((function(t){e.$modal.msgSuccess("修改成功"),e.open=!1,e.getList()})):c(e.form).then((function(t){e.$modal.msgSuccess("新增成功"),e.open=!1,e.getList()})))}))},handleDelete:function(e){var t=this,a=e.anserId||this.ids;this.$modal.confirm('是否确认删除回答收录列编号为"'+a+'"的数据项？').then((function(){return m(a)})).then((function(){t.getList(),t.$modal.msgSuccess("删除成功")})).catch((function(){}))},handleExport:function(){this.download("cricleai/employ/sys/export",Object(i["a"])({},this.queryParams),"employ_".concat((new Date).getTime(),".xlsx"))}}},h=p,d=a("2877"),f=Object(d["a"])(h,l,n,!1,null,null,null);t["default"]=f.exports}}]);