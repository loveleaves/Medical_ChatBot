(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5175a454"],{"1f4b":function(e,t,l){"use strict";l.d(t,"g",(function(){return a})),l.d(t,"e",(function(){return n})),l.d(t,"a",(function(){return o})),l.d(t,"i",(function(){return i})),l.d(t,"c",(function(){return s})),l.d(t,"h",(function(){return u})),l.d(t,"f",(function(){return c})),l.d(t,"b",(function(){return d})),l.d(t,"j",(function(){return m})),l.d(t,"d",(function(){return p}));var r=l("b775");function a(e){return Object(r["a"])({url:"/cricleai/roleChange/list",method:"get",params:e})}function n(e){return Object(r["a"])({url:"/cricleai/roleChange/"+e,method:"get"})}function o(e){return Object(r["a"])({url:"/cricleai/roleChange",method:"post",data:e})}function i(e){return Object(r["a"])({url:"/cricleai/roleChange",method:"put",data:e})}function s(e){return Object(r["a"])({url:"/cricleai/roleChange/"+e,method:"delete"})}function u(e){return Object(r["a"])({url:"/cricleai/roleChange/sys/list",method:"get",params:e})}function c(e){return Object(r["a"])({url:"/cricleai/roleChange/sys/"+e,method:"get"})}function d(e){return Object(r["a"])({url:"/cricleai/roleChange/sys",method:"post",data:e})}function m(e){return Object(r["a"])({url:"/cricleai/roleChange/sys",method:"put",data:e})}function p(e){return Object(r["a"])({url:"/cricleai/roleChange/sys/"+e,method:"delete"})}},"8d9f":function(e,t,l){"use strict";l.r(t);var r=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"app-container"},[l("el-form",{directives:[{name:"show",rawName:"v-show",value:e.showSearch,expression:"showSearch"}],ref:"queryForm",attrs:{model:e.queryParams,size:"small",inline:!0,"label-width":"68px"}},[l("el-form-item",{attrs:{label:"模型名称",prop:"modelName"}},[l("el-input",{attrs:{placeholder:"请输入模型名称",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleQuery(t)}},model:{value:e.queryParams.modelName,callback:function(t){e.$set(e.queryParams,"modelName",t)},expression:"queryParams.modelName"}})],1),l("el-form-item",{attrs:{label:"是否可用",prop:"isUse"}},[l("el-select",{attrs:{placeholder:"请选择是否可用",clearable:""},model:{value:e.queryParams.isUse,callback:function(t){e.$set(e.queryParams,"isUse",t)},expression:"queryParams.isUse"}},e._l(e.dict.type.is_run,(function(e){return l("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),l("el-form-item",{attrs:{label:"模型分类",prop:"dRoleId"}},[l("el-select",{attrs:{placeholder:"请选择模型分类",clearable:""},model:{value:e.queryParams.dRoleId,callback:function(t){e.$set(e.queryParams,"dRoleId",t)},expression:"queryParams.dRoleId"}},e._l(e.roleList,(function(e){return l("el-option",{key:e.id,attrs:{label:e.roleName,value:e.id}})})),1)],1),l("el-form-item",[l("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini"},on:{click:e.handleQuery}},[e._v("搜索")]),l("el-button",{attrs:{icon:"el-icon-refresh",size:"mini"},on:{click:e.resetQuery}},[e._v("重置")])],1)],1),l("el-row",{staticClass:"mb8",attrs:{gutter:10}},[l("el-col",{attrs:{span:1.5}},[l("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:usermodel:sys:add"],expression:"['chatgpt:usermodel:sys:add']"}],attrs:{type:"primary",plain:"",icon:"el-icon-plus",size:"mini"},on:{click:e.handleAdd}},[e._v("新增")])],1),l("el-col",{attrs:{span:1.5}},[l("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:usermodel:sys:edit"],expression:"['chatgpt:usermodel:sys:edit']"}],attrs:{type:"success",plain:"",icon:"el-icon-edit",size:"mini",disabled:e.single},on:{click:e.handleUpdate}},[e._v("修改")])],1),l("el-col",{attrs:{span:1.5}},[l("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:usermodel:sys:remove"],expression:"['chatgpt:usermodel:sys:remove']"}],attrs:{type:"danger",plain:"",icon:"el-icon-delete",size:"mini",disabled:e.multiple},on:{click:e.handleDelete}},[e._v("删除")])],1),l("right-toolbar",{attrs:{showSearch:e.showSearch},on:{"update:showSearch":function(t){e.showSearch=t},"update:show-search":function(t){e.showSearch=t},queryTable:e.getList}})],1),l("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.usermodelList},on:{"selection-change":e.handleSelectionChange}},[l("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),l("el-table-column",{attrs:{label:"主键",align:"center",prop:"id"}}),l("el-table-column",{attrs:{label:"模型名称",align:"center",prop:"modelName"}}),l("el-table-column",{attrs:{label:"模型设定语","show-overflow-tooltip":!0,align:"center",prop:"modelContent"}}),l("el-table-column",{attrs:{label:"是否可用",align:"center",prop:"isUse"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("dict-tag",{attrs:{options:e.dict.type.is_run,value:t.row.isUse}})]}}])}),l("el-table-column",{attrs:{label:"分类名称",align:"center",prop:"droleId"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("el-select",{attrs:{disabled:"",placeholder:"分类名称",clearable:""},model:{value:t.row.droleId,callback:function(l){e.$set(t.row,"droleId",l)},expression:"scope.row.droleId"}},e._l(e.roleList,(function(e){return l("el-option",{key:e.id,attrs:{label:e.roleName,value:e.id}})})),1)]}}])}),l("el-table-column",{attrs:{label:"操作",align:"center","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:usermodel:edit"],expression:"['chatgpt:usermodel:edit']"}],attrs:{size:"mini",type:"text",icon:"el-icon-edit"},on:{click:function(l){return e.handleUpdate(t.row)}}},[e._v("修改")]),l("el-button",{directives:[{name:"hasPermi",rawName:"v-hasPermi",value:["chatgpt:usermodel:remove"],expression:"['chatgpt:usermodel:remove']"}],attrs:{size:"mini",type:"text",icon:"el-icon-delete"},on:{click:function(l){return e.handleDelete(t.row)}}},[e._v("删除")])]}}])})],1),l("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.queryParams.pageNum,limit:e.queryParams.pageSize},on:{"update:page":function(t){return e.$set(e.queryParams,"pageNum",t)},"update:limit":function(t){return e.$set(e.queryParams,"pageSize",t)},pagination:e.getList}}),l("el-dialog",{attrs:{title:e.title,visible:e.open,width:"1000px","append-to-body":""},on:{"update:visible":function(t){e.open=t}}},[l("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,"label-width":"120px"}},[l("el-form-item",{attrs:{label:"模型名称",prop:"modelName"}},[l("el-input",{attrs:{placeholder:"请输入模型名称"},model:{value:e.form.modelName,callback:function(t){e.$set(e.form,"modelName",t)},expression:"form.modelName"}})],1),l("el-form-item",{attrs:{label:"模型设定语",prop:"modelContent"}},[l("el-input",{attrs:{type:"textarea",placeholder:"请输入内容"},model:{value:e.form.modelContent,callback:function(t){e.$set(e.form,"modelContent",t)},expression:"form.modelContent"}})],1),l("el-form-item",{attrs:{label:"是否可用",prop:"isUse"}},[l("el-select",{attrs:{placeholder:"请选择是否可用"},model:{value:e.form.isUse,callback:function(t){e.$set(e.form,"isUse",t)},expression:"form.isUse"}},e._l(e.dict.type.is_run,(function(e){return l("el-option",{key:e.value,attrs:{label:e.label,value:parseInt(e.value)}})})),1)],1),l("el-form-item",{attrs:{label:"模型分类",prop:"droleId"}},[l("el-select",{attrs:{placeholder:"请选择模型分类"},model:{value:e.form.droleId,callback:function(t){e.$set(e.form,"droleId",t)},expression:"form.droleId"}},e._l(e.roleList,(function(e){return l("el-option",{key:e.id,attrs:{label:e.roleName,value:parseInt(e.id)}})})),1)],1),l("el-form-item",{attrs:{label:"添加模型方式",prop:"usermodeliNSERTType"}},[l("el-select",{attrs:{placeholder:"请选择模型分类"},model:{value:e.usermodeliNSERTType,callback:function(t){e.usermodeliNSERTType=t},expression:"usermodeliNSERTType"}},e._l(e.addModelType,(function(e){return l("el-option",{key:e.value,attrs:{label:e.name,value:parseInt(e.value)}})})),1)],1),2==e.usermodeliNSERTType?l("el-form-item",{attrs:{label:"选择模型",prop:"usermodeliNSERTType"}},[l("el-table",{staticStyle:{width:"100%"},attrs:{height:"400",data:e.usermodelDataDefault}},[l("el-table-column",{attrs:{label:"模型名称",width:"180"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("div",{staticClass:"name-wrapper",attrs:{slot:"reference"},slot:"reference"},[l("el-tag",{attrs:{size:"medium"}},[e._v(e._s(t.row.key))])],1)]}}],null,!1,1500225293)}),l("el-table-column",{attrs:{"show-overflow-tooltip":!0,label:"模型描述",width:"500"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("div",{staticClass:"name-wrapper",attrs:{slot:"reference"},slot:"reference"},[l("el-tag",{attrs:{size:"medium"}},[e._v(e._s(t.row.value))])],1)]}}],null,!1,2576043313)}),l("el-table-column",{attrs:{label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[l("el-button",{attrs:{size:"mini"},on:{click:function(l){return e.selectModel(t.row)}}},[e._v("选择")])]}}],null,!1,490667765)})],1)],1):e._e()],1),l("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[l("el-button",{attrs:{type:"primary"},on:{click:e.submitForm}},[e._v("确 定")]),l("el-button",{on:{click:e.cancel}},[e._v("取 消")])],1)],1)],1)},a=[],n=l("5530"),o=(l("14d9"),l("d81d"),l("9908")),i=l("1f4b"),s={name:"Usermodel",dicts:["is_run"],data:function(){return{roleListDist:[],roleList:[],loading:!0,ids:[],single:!0,multiple:!0,showSearch:!0,total:0,usermodelList:[],title:"",open:!1,queryParams:{pageNum:1,pageSize:10,modelName:null,modelImage:null,modelContent:null,isUse:null,isDetele:null,dRoleId:null},queryParamRoles:{pageNum:1,pageSize:1e3},form:{},rules:{modelName:[{required:!0,message:"模型名称不能为空",trigger:"blur"}],modelContent:[{required:!0,message:"模型设定语不能为空",trigger:"blur"}],isUse:[{required:!0,message:"是否可用不能为空",trigger:"change"}],droleId:[{required:!0,message:"模型分类不能为空",trigger:"change"}]},roleId:"",usermodelDataDefault:[],usermodeliNSERTType:1,addModelType:[{name:"自定义模型",value:1},{name:"官方提供模型",value:2}]}},created:function(){this.getList(),this.getRoleList()},methods:{selectModel:function(e){this.form.modelName=e.key,this.form.modelContent=e.value},getList:function(){var e=this;this.loading=!0,Object(o["i"])(this.queryParams).then((function(t){e.usermodelList=t.rows,e.total=t.total,e.loading=!1}))},getModelAddressData:function(){var e=this;Object(o["e"])().then((function(t){e.usermodelDataDefault=t.data}))},getRoleList:function(){var e=this;Object(i["h"])(this.queryParamRoles).then((function(t){e.roleList=t.rows;for(var l=0;l<e.roleList.length;l++){console.log(e.roleList[l]);var r={label:e.roleList[l].roleName,value:e.roleList[l].id};e.roleListDist.push(r)}console.log(e.roleListDist)}))},cancel:function(){this.open=!1,this.reset()},reset:function(){this.form={id:null,modelName:null,modelImage:null,modelContent:null,isUse:null,isDetele:null,createBy:null,createTime:null,updateBy:null,updateTime:null,remark:null},this.resetForm("form")},handleQuery:function(){this.queryParams.pageNum=1,this.getList()},resetQuery:function(){this.resetForm("queryForm"),this.handleQuery()},handleSelectionChange:function(e){this.ids=e.map((function(e){return e.id})),this.single=1!==e.length,this.multiple=!e.length},handleAdd:function(){this.reset(),this.open=!0,this.title="添加模型建设"},handleUpdate:function(e){var t=this;this.getModelAddressData(),this.reset();var l=e.id||this.ids;Object(o["g"])(l).then((function(e){t.form=e.data,t.open=!0,t.title="修改模型建设"}))},submitForm:function(){var e=this;this.$refs["form"].validate((function(t){t&&(null!=e.form.id?Object(o["k"])(e.form).then((function(t){e.$modal.msgSuccess("修改成功"),e.open=!1,e.getList()})):Object(o["b"])(e.form).then((function(t){e.$modal.msgSuccess("新增成功"),e.open=!1,e.getList()})))}))},handleDelete:function(e){var t=this,l=e.id||this.ids;this.$modal.confirm('是否确认删除模型建设编号为"'+l+'"的数据项？').then((function(){return Object(o["d"])(l)})).then((function(){t.getList(),t.$modal.msgSuccess("删除成功")})).catch((function(){}))},handleExport:function(){this.download("cricleai/usermodel/sys/export",Object(n["a"])({},this.queryParams),"usermodel_".concat((new Date).getTime(),".xlsx"))}}},u=s,c=l("2877"),d=Object(c["a"])(u,r,a,!1,null,null,null);t["default"]=d.exports},9908:function(e,t,l){"use strict";l.d(t,"h",(function(){return a})),l.d(t,"f",(function(){return n})),l.d(t,"a",(function(){return o})),l.d(t,"j",(function(){return i})),l.d(t,"c",(function(){return s})),l.d(t,"i",(function(){return u})),l.d(t,"g",(function(){return c})),l.d(t,"b",(function(){return d})),l.d(t,"k",(function(){return m})),l.d(t,"d",(function(){return p})),l.d(t,"e",(function(){return f}));var r=l("b775");function a(e){return Object(r["a"])({url:"/cricleai/usermodel/list",method:"get",params:e})}function n(e){return Object(r["a"])({url:"/cricleai/usermodel/"+e,method:"get"})}function o(e){return Object(r["a"])({url:"/cricleai/usermodel",method:"post",data:e})}function i(e){return Object(r["a"])({url:"/cricleai/usermodel",method:"put",data:e})}function s(e){return Object(r["a"])({url:"/cricleai/usermodel/"+e,method:"delete"})}function u(e){return Object(r["a"])({url:"/cricleai/usermodel/sys/list",method:"get",params:e})}function c(e){return Object(r["a"])({url:"/cricleai/usermodel/sys/"+e,method:"get"})}function d(e){return Object(r["a"])({url:"/cricleai/usermodel/sys",method:"post",data:e})}function m(e){return Object(r["a"])({url:"/cricleai/usermodel/sys",method:"put",data:e})}function p(e){return Object(r["a"])({url:"/cricleai/usermodel/sys/"+e,method:"delete"})}function f(){return Object(r["a"])({url:"/cricleai/usermodel/getModelAddress",method:"get"})}}}]);