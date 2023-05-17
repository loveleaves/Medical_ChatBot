(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0b9654"],{3386:function(e,r,t){"use strict";t.r(r);var a=function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("div",{staticClass:"app-container"},[t("el-form",{directives:[{name:"show",rawName:"v-show",value:e.showSearch,expression:"showSearch"}],ref:"queryForm",attrs:{model:e.queryParams,size:"small",inline:!0,"label-width":"68px"}},[t("el-form-item",{attrs:{label:"qq号",prop:"rcqQqCode"}},[t("el-input",{attrs:{placeholder:"请输入qq号",clearable:""},nativeOn:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.handleQuery(r)}},model:{value:e.queryParams.rcqQqCode,callback:function(r){e.$set(e.queryParams,"rcqQqCode",r)},expression:"queryParams.rcqQqCode"}})],1),t("el-form-item",{attrs:{label:"qq密码",prop:"rcqQqPassword"}},[t("el-input",{attrs:{placeholder:"请输入qq密码",clearable:""},nativeOn:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.handleQuery(r)}},model:{value:e.queryParams.rcqQqPassword,callback:function(r){e.$set(e.queryParams,"rcqQqPassword",r)},expression:"queryParams.rcqQqPassword"}})],1),t("el-form-item",{attrs:{label:"平台名称",prop:"rcqPlatformName"}},[t("el-input",{attrs:{placeholder:"请输入平台名称",clearable:""},nativeOn:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.handleQuery(r)}},model:{value:e.queryParams.rcqPlatformName,callback:function(r){e.$set(e.queryParams,"rcqPlatformName",r)},expression:"queryParams.rcqPlatformName"}})],1),t("el-form-item",{attrs:{label:"是否启动",prop:"rcqIsRun"}},[t("el-select",{attrs:{placeholder:"请选择是否启动",clearable:""},model:{value:e.queryParams.rcqIsRun,callback:function(r){e.$set(e.queryParams,"rcqIsRun",r)},expression:"queryParams.rcqIsRun"}},e._l(e.dict.type.is_run,(function(e){return t("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),t("el-form-item",{attrs:{label:"过期时间",prop:"rcqRepireTime"}},[t("el-date-picker",{attrs:{clearable:"",type:"date","value-format":"yyyy-MM-dd",placeholder:"请选择过期时间"},model:{value:e.queryParams.rcqRepireTime,callback:function(r){e.$set(e.queryParams,"rcqRepireTime",r)},expression:"queryParams.rcqRepireTime"}})],1),t("el-form-item",[t("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini"},on:{click:e.handleQuery}},[e._v("搜索")]),t("el-button",{attrs:{icon:"el-icon-refresh",size:"mini"},on:{click:e.resetQuery}},[e._v("重置")])],1)],1),t("el-row",{staticClass:"mb8",attrs:{gutter:10}},[t("el-col",{attrs:{span:1.5}},[t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:add"],expression:"['system:rcq:add']"}],attrs:{type:"primary",plain:"",icon:"el-icon-plus",size:"mini"},on:{click:e.handleAdd}},[e._v("新增")])],1),t("el-col",{attrs:{span:1.5}},[t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:edit"],expression:"['system:rcq:edit']"}],attrs:{type:"success",plain:"",icon:"el-icon-edit",size:"mini",disabled:e.single},on:{click:e.handleUpdate}},[e._v("修改")])],1),t("el-col",{attrs:{span:1.5}},[t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:remove"],expression:"['system:rcq:remove']"}],attrs:{type:"danger",plain:"",icon:"el-icon-delete",size:"mini",disabled:e.multiple},on:{click:e.handleDelete}},[e._v("删除")])],1),t("el-col",{attrs:{span:1.5}},[t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:export"],expression:"['system:rcq:export']"}],attrs:{type:"warning",plain:"",icon:"el-icon-download",size:"mini"},on:{click:e.handleExport}},[e._v("导出")])],1),t("right-toolbar",{attrs:{showSearch:e.showSearch},on:{"update:showSearch":function(r){e.showSearch=r},"update:show-search":function(r){e.showSearch=r},queryTable:e.getList}})],1),t("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.rcqList},on:{"selection-change":e.handleSelectionChange}},[t("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),t("el-table-column",{attrs:{label:"记录ID",align:"center",prop:"rcqId"}}),t("el-table-column",{attrs:{label:"qq号",align:"center",prop:"rcqQqCode"}}),t("el-table-column",{attrs:{label:"qq密码",align:"center",prop:"rcqQqPassword"}}),t("el-table-column",{attrs:{label:"平台名称",align:"center",prop:"rcqPlatformName"}}),t("el-table-column",{attrs:{label:"管理的qq群",align:"center",prop:"rcqManagerGorup"}}),t("el-table-column",{attrs:{label:"是否启动",align:"center",prop:"rcqIsRun"},scopedSlots:e._u([{key:"default",fn:function(r){return[t("dict-tag",{attrs:{options:e.dict.type.is_run,value:r.row.rcqIsRun}})]}}])}),t("el-table-column",{attrs:{label:"过期时间",align:"center",prop:"rcqRepireTime",width:"180"},scopedSlots:e._u([{key:"default",fn:function(r){return[t("span",[e._v(e._s(e.parseTime(r.row.rcqRepireTime,"{y}-{m}-{d}")))])]}}])}),t("el-table-column",{attrs:{label:"备注",align:"center",prop:"remark"}}),t("el-table-column",{attrs:{label:"操作",align:"center","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(r){return[t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:edit"],expression:"['system:rcq:edit']"}],attrs:{size:"mini",type:"text",icon:"el-icon-edit"},on:{click:function(t){return e.handleUpdate(r.row)}}},[e._v("修改")]),t("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["system:rcq:remove"],expression:"['system:rcq:remove']"}],attrs:{size:"mini",type:"text",icon:"el-icon-delete"},on:{click:function(t){return e.handleDelete(r.row)}}},[e._v("删除")])]}}])})],1),t("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.queryParams.pageNum,limit:e.queryParams.pageSize},on:{"update:page":function(r){return e.$set(e.queryParams,"pageNum",r)},"update:limit":function(r){return e.$set(e.queryParams,"pageSize",r)},pagination:e.getList}}),t("el-dialog",{attrs:{title:e.title,visible:e.open,width:"500px","append-to-body":""},on:{"update:visible":function(r){e.open=r}}},[t("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,"label-width":"80px"}},[t("el-form-item",{attrs:{label:"qq号",prop:"rcqQqCode"}},[t("el-input",{attrs:{placeholder:"请输入qq号"},model:{value:e.form.rcqQqCode,callback:function(r){e.$set(e.form,"rcqQqCode",r)},expression:"form.rcqQqCode"}})],1),t("el-form-item",{attrs:{label:"qq密码",prop:"rcqQqPassword"}},[t("el-input",{attrs:{placeholder:"请输入qq密码"},model:{value:e.form.rcqQqPassword,callback:function(r){e.$set(e.form,"rcqQqPassword",r)},expression:"form.rcqQqPassword"}})],1),t("el-form-item",{attrs:{label:"平台名称",prop:"rcqPlatformName"}},[t("el-input",{attrs:{placeholder:"请输入平台名称"},model:{value:e.form.rcqPlatformName,callback:function(r){e.$set(e.form,"rcqPlatformName",r)},expression:"form.rcqPlatformName"}})],1),t("el-form-item",{attrs:{label:"管理的qq群",prop:"rcqManagerGorup"}},[t("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.rcqManagerGorup,callback:function(r){e.$set(e.form,"rcqManagerGorup",r)},expression:"form.rcqManagerGorup"}})],1),t("el-form-item",{attrs:{label:"是否启动",prop:"rcqIsRun"}},[t("el-select",{attrs:{placeholder:"请选择是否启动"},model:{value:e.form.rcqIsRun,callback:function(r){e.$set(e.form,"rcqIsRun",r)},expression:"form.rcqIsRun"}},e._l(e.dict.type.is_run,(function(e){return t("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),t("el-form-item",{attrs:{label:"过期时间",prop:"rcqRepireTime"}},[t("el-date-picker",{attrs:{clearable:"",type:"date","value-format":"yyyy-MM-dd",placeholder:"请选择过期时间"},model:{value:e.form.rcqRepireTime,callback:function(r){e.$set(e.form,"rcqRepireTime",r)},expression:"form.rcqRepireTime"}})],1),t("el-form-item",{attrs:{label:"备注",prop:"remark"}},[t("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.remark,callback:function(r){e.$set(e.form,"remark",r)},expression:"form.remark"}})],1)],1),t("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[t("el-button",{attrs:{type:"primary"},on:{click:e.submitForm}},[e._v("确 定")]),t("el-button",{on:{click:e.cancel}},[e._v("取 消")])],1)],1)],1)},l=[],n=t("5530"),s=(t("d81d"),t("b775"));function o(e){return Object(s["a"])({url:"/system/rcq/list",method:"get",params:e})}function i(e){return Object(s["a"])({url:"/system/rcq/"+e,method:"get"})}function c(e){return Object(s["a"])({url:"/system/rcq",method:"post",data:e})}function u(e){return Object(s["a"])({url:"/system/rcq",method:"put",data:e})}function m(e){return Object(s["a"])({url:"/system/rcq/"+e,method:"delete"})}var p={name:"Rcq",dicts:["is_run"],data:function(){return{loading:!0,ids:[],single:!0,multiple:!0,showSearch:!0,total:0,rcqList:[],title:"",open:!1,queryParams:{pageNum:1,pageSize:10,rcqQqCode:null,rcqQqPassword:null,rcqPlatformName:null,rcqManagerGorup:null,rcqIsRun:null,rcqRepireTime:null},form:{},rules:{}}},created:function(){this.getList()},methods:{getList:function(){var e=this;this.loading=!0,o(this.queryParams).then((function(r){e.rcqList=r.rows,e.total=r.total,e.loading=!1}))},cancel:function(){this.open=!1,this.reset()},reset:function(){this.form={rcqId:null,rcqQqCode:null,rcqQqPassword:null,rcqPlatformName:null,rcqManagerGorup:null,rcqIsRun:null,rcqRepireTime:null,createBy:null,createTime:null,updateBy:null,updateTime:null,remark:null},this.resetForm("form")},handleQuery:function(){this.queryParams.pageNum=1,this.getList()},resetQuery:function(){this.resetForm("queryForm"),this.handleQuery()},handleSelectionChange:function(e){this.ids=e.map((function(e){return e.rcqId})),this.single=1!==e.length,this.multiple=!e.length},handleAdd:function(){this.reset(),this.open=!0,this.title="添加机器人配置"},handleUpdate:function(e){var r=this;this.reset();var t=e.rcqId||this.ids;i(t).then((function(e){r.form=e.data,r.open=!0,r.title="修改机器人配置"}))},submitForm:function(){var e=this;this.$refs["form"].validate((function(r){r&&(null!=e.form.rcqId?u(e.form).then((function(r){e.$modal.msgSuccess("修改成功"),e.open=!1,e.getList()})):c(e.form).then((function(r){e.$modal.msgSuccess("新增成功"),e.open=!1,e.getList()})))}))},handleDelete:function(e){var r=this,t=e.rcqId||this.ids;this.$modal.confirm('是否确认删除机器人配置编号为"'+t+'"的数据项？').then((function(){return m(t)})).then((function(){r.getList(),r.$modal.msgSuccess("删除成功")})).catch((function(){}))},handleExport:function(){this.download("system/rcq/export",Object(n["a"])({},this.queryParams),"rcq_".concat((new Date).getTime(),".xlsx"))}}},d=p,q=t("2877"),f=Object(q["a"])(d,a,l,!1,null,null,null);r["default"]=f.exports}}]);