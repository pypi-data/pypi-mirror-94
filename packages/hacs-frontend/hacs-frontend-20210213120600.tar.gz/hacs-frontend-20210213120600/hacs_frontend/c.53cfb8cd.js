import{_ as e,H as t,p as i,v as o,h as s,c as r}from"./e.2be12e9e.js";import{m as d}from"./c.213e64a1.js";import"./c.41e411dd.js";import"./c.2105f995.js";import"./c.f291fdd9.js";let a=e([r("hacs-generic-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[i()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[i()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"method",key:"render",value:function(){if(!this.active)return s``;const e=this._getRepository(this.repositories,this.repository);return s`
      <hacs-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?d.html(this.content||"",e):d.html(this.content||""):this.content||""}
      </hacs-dialog>
    `}}]}}),t);export{a as HacsGenericDialog};
