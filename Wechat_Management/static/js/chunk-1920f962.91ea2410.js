(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1920f962"],{"32c9":function(e,t,r){"use strict";r.d(t,"g",(function(){return n})),r.d(t,"e",(function(){return i})),r.d(t,"a",(function(){return l})),r.d(t,"i",(function(){return o})),r.d(t,"c",(function(){return s})),r.d(t,"h",(function(){return u})),r.d(t,"f",(function(){return c})),r.d(t,"b",(function(){return d})),r.d(t,"j",(function(){return m})),r.d(t,"d",(function(){return p}));var a=r("b775");function n(e){return Object(a["a"])({url:"/cricleai/diglogue/list",method:"get",params:e})}function i(e){return Object(a["a"])({url:"/cricleai/diglogue/"+e,method:"get"})}function l(e){return Object(a["a"])({url:"/cricleai/diglogue",method:"post",data:e})}function o(e){return Object(a["a"])({url:"/cricleai/diglogue",method:"put",data:e})}function s(e){return Object(a["a"])({url:"/cricleai/diglogue/"+e,method:"delete"})}function u(e){return Object(a["a"])({url:"/cricleai/diglogue/sys/list",method:"get",params:e})}function c(e){return Object(a["a"])({url:"/cricleai/diglogue/sys/"+e,method:"get"})}function d(e){return Object(a["a"])({url:"/cricleai/diglogue/sys",method:"post",data:e})}function m(e){return Object(a["a"])({url:"/cricleai/diglogue/sys",method:"put",data:e})}function p(e){return Object(a["a"])({url:"/cricleai/diglogue/sys/"+e,method:"delete"})}},"7b26":function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"app-container"},[r("el-form",{directives:[{name:"show",rawName:"v-show",value:e.showSearch,expression:"showSearch"}],ref:"queryForm",attrs:{model:e.queryParams,size:"small",inline:!0,"label-width":"68px"}},[r("el-form-item",{attrs:{label:"话题名称",prop:"dialogueName"}},[r("el-input",{attrs:{placeholder:"请输入话题名称",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.dialogueName,callback:function(t){e.$set(e.queryParams,"dialogueName",t)},expression:"queryParams.dialogueName"}})],1),r("el-form-item",{attrs:{label:"对话ID",prop:"sessionId"}},[r("el-input",{attrs:{placeholder:"请输入对话ID",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.sessionId,callback:function(t){e.$set(e.queryParams,"sessionId",t)},expression:"queryParams.sessionId"}})],1),r("el-form-item",{attrs:{label:"用户ID",prop:"userId"}},[r("el-input",{attrs:{placeholder:"请输入用户ID",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.userId,callback:function(t){e.$set(e.queryParams,"userId",t)},expression:"queryParams.userId"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini"},on:{click:e.handleQuery}},[e._v("搜索")]),r("el-button",{attrs:{icon:"el-icon-refresh",size:"mini"},on:{click:e.resetQuery}},[e._v("重置")])],1)],1),r("el-row",{staticClass:"mb8",attrs:{gutter:10}},[r("el-col",{attrs:{span:1.5}},[r("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:diglogue:sys:export"],expression:"['chatgpt:diglogue:sys:export']"}],attrs:{type:"warning",plain:"",icon:"el-icon-download",size:"mini"},on:{click:e.handleExport}},[e._v("导出 ")])],1),r("right-toolbar",{attrs:{showSearch:e.showSearch},on:{"update:showSearch":function(t){e.showSearch=t},"update:show-search":function(t){e.showSearch=t},queryTable:e.getList}})],1),r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.diglogueList},on:{"selection-change":e.handleSelectionChange}},[r("el-table-column",{attrs:{label:"对话ID",align:"center",prop:"id"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{cursor:"pointer",color:"#409eff"},on:{click:function(r){return e.goToDetilPage(t.row.id)}}},[e._v(e._s(t.row.id))])]}}])}),r("el-table-column",{attrs:{label:"话题名称",align:"center",prop:"dialogueName"}}),r("el-table-column",{attrs:{label:"用户ID",align:"center",prop:"userId"}})],1),r("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.queryParams.pageNum,limit:e.queryParams.pageSize},on:{"update:page":function(t){return e.$set(e.queryParams,"pageNum",t)},"update:limit":function(t){return e.$set(e.queryParams,"pageSize",t)},pagination:e.getList}}),r("el-dialog",{attrs:{title:e.title,visible:e.open,width:"500px","append-to-body":""},on:{"update:visible":function(t){e.open=t}}},[r("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,"label-width":"80px"}},[r("el-form-item",{attrs:{label:"话题名称",prop:"dialogueName"}},[r("el-input",{attrs:{placeholder:"请输入话题名称"},model:{value:e.form.dialogueName,callback:function(t){e.$set(e.form,"dialogueName",t)},expression:"form.dialogueName"}})],1),r("el-form-item",{attrs:{label:"对话ID",prop:"sessionId"}},[r("el-input",{attrs:{placeholder:"请输入对话ID"},model:{value:e.form.sessionId,callback:function(t){e.$set(e.form,"sessionId",t)},expression:"form.sessionId"}})],1),r("el-form-item",{attrs:{label:"用户ID",prop:"userId"}},[r("el-input",{attrs:{placeholder:"请输入用户ID"},model:{value:e.form.userId,callback:function(t){e.$set(e.form,"userId",t)},expression:"form.userId"}})],1),r("el-form-item",{attrs:{label:"是否删除",prop:"isDetele"}},[r("el-input",{attrs:{placeholder:"请输入是否删除"},model:{value:e.form.isDetele,callback:function(t){e.$set(e.form,"isDetele",t)},expression:"form.isDetele"}})],1),r("el-form-item",{attrs:{label:"备注",prop:"remark"}},[r("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.remark,callback:function(t){e.$set(e.form,"remark",t)},expression:"form.remark"}})],1)],1),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"primary"},on:{click:e.submitForm}},[e._v("确 定")]),r("el-button",{on:{click:e.cancel}},[e._v("取 消")])],1)],1)],1)},n=[],i=r("5530"),l=(r("14d9"),r("d81d"),r("32c9")),o={name:"Diglogue",data:function(){return{loading:!0,ids:[],single:!0,multiple:!0,showSearch:!0,total:0,diglogueList:[],title:"",open:!1,queryParams:{pageNum:1,pageSize:10,dialogueName:null,sessionId:null,userId:null,isDetele:null},form:{},rules:{}}},created:function(){this.getList()},methods:{goToDetilPage:function(e){this.$router.push({path:"/chatGpt/diglogueprocesssys",query:{sessionId:e}})},getList:function(){var e=this;this.loading=!0,Object(l["h"])(this.queryParams).then((function(t){e.diglogueList=t.rows,e.total=t.total,e.loading=!1}))},cancel:function(){this.open=!1,this.reset()},reset:function(){this.form={id:null,dialogueName:null,sessionId:null,userId:null,isDetele:null,createBy:null,createTime:null,updateBy:null,updateTime:null,remark:null},this.resetForm("form")},handleQuery:function(){this.queryParams.pageNum=1,this.getList()},resetQuery:function(){this.resetForm("queryForm"),this.handleQuery()},handleSelectionChange:function(e){this.ids=e.map((function(e){return e.id})),this.single=1!==e.length,this.multiple=!e.length},handleAdd:function(){this.reset(),this.open=!0,this.title="添加对话列-主"},handleUpdate:function(e){var t=this;this.reset();var r=e.id||this.ids;Object(l["f"])(r).then((function(e){t.form=e.data,t.open=!0,t.title="修改对话列-主"}))},submitForm:function(){var e=this;this.$refs["form"].validate((function(t){t&&(null!=e.form.id?Object(l["j"])(e.form).then((function(t){e.$modal.msgSuccess("修改成功"),e.open=!1,e.getList()})):Object(l["b"])(e.form).then((function(t){e.$modal.msgSuccess("新增成功"),e.open=!1,e.getList()})))}))},handleDelete:function(e){var t=this,r=e.id||this.ids;this.$modal.confirm('是否确认删除对话列-主编号为"'+r+'"的数据项？').then((function(){return Object(l["d"])(r)})).then((function(){t.getList(),t.$modal.msgSuccess("删除成功")})).catch((function(){}))},handleExport:function(){this.download("cricleai/diglogue/sys/export",Object(i["a"])({},this.queryParams),"diglogue_".concat((new Date).getTime(),".xlsx"))}}},s=o,u=r("2877"),c=Object(u["a"])(s,a,n,!1,null,null,null);t["default"]=c.exports}}]);