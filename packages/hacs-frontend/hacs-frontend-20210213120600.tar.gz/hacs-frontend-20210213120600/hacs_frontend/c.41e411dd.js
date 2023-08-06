import{_ as e,L as t,p as n,h as r,n as i,g as o,c as s}from"./e.2be12e9e.js";e([s("hacs-link")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[n({type:Boolean})],key:"newtab",value:()=>!1},{kind:"field",decorators:[n({type:Boolean})],key:"parent",value:()=>!1},{kind:"field",decorators:[n()],key:"title",value:void 0},{kind:"field",decorators:[n()],key:"url",value:void 0},{kind:"method",key:"render",value:function(){return r`<span title=${this.title||this.url} @click=${this._open}><slot></slot></span>`}},{kind:"method",key:"_open",value:function(){var e;if(this.url.startsWith("/"))return void i(this,this.url,!0);const t=null===(e=this.url)||void 0===e?void 0:e.includes("http");let n="",r="_blank";t&&(n="noreferrer=true"),t||this.newtab||(r="_top"),t||this.parent||(r="_parent"),window.open(this.url,r,n)}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      span {
        cursor: pointer;
        color: var(--hcv-text-color-link);
        text-decoration: var(--hcv-text-decoration-link);
      }
    `}}]}}),t);
