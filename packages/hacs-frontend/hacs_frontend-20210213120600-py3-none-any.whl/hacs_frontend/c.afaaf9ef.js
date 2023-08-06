import{M as e,B as t,Q as i,h as r,d as o,_ as s,g as n,c as a,R as c,a as l,t as d,p as h,e as p,f as u,H as m,I as f,v as y,S as g,N as b,T as v,U as w,V as _}from"./e.2be12e9e.js";import"./c.41e411dd.js";import{o as k}from"./c.2105f995.js";import"./c.f291fdd9.js";import"./c.d77ccf64.js";import"./c.b190b3c3.js";import"./c.291c2df3.js";import"./c.1cadb769.js";import{u as x}from"./c.3b165dd4.js";function E(e,t,i,r){var o,s=arguments.length,n=s<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var a=e.length-1;a>=0;a--)(o=e[a])&&(n=(s<3?o(n):s>3?o(t,i,n):o(t,i))||n);return s>3&&n&&Object.defineProperty(t,i,n),n}window.JSCompiler_renameProperty=(e,t)=>e;const S=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?Object.assign(Object.assign({},t),{finisher(i){i.createProperty(t.key,e)}}):{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(i){i.createProperty(t.key,e)}};function R(e){return(t,i)=>void 0!==i?((e,t,i)=>{t.constructor.createProperty(i,e)})(e,t,i):S(e,t)}function C(e){return(t,i)=>{const r={get(){return this.renderRoot.querySelector(e)},enumerable:!0,configurable:!0};return void 0!==i?$(r,t,i):O(r,t)}}const $=(e,t,i)=>{Object.defineProperty(t,i,e)},O=(e,t)=>({kind:"method",placement:"prototype",key:t.key,descriptor:e}),j="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,P=Symbol();class z{constructor(e,t){if(t!==P)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return void 0===this._styleSheet&&(j?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}(window.litElementVersions||(window.litElementVersions=[])).push("2.3.1");var A=function(e,t){return(A=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var i in t)t.hasOwnProperty(i)&&(e[i]=t[i])})(e,t)};var D=function(){return(D=Object.assign||function(e){for(var t,i=1,r=arguments.length;i<r;i++)for(var o in t=arguments[i])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e}).apply(this,arguments)},H={ROOT:"mdc-form-field"},I={LABEL_SELECTOR:".mdc-form-field > label"},T=function(e){function t(i){var r=e.call(this,D(D({},t.defaultAdapter),i))||this;return r.click=function(){r.handleClick()},r}return function(e,t){function i(){this.constructor=e}A(e,t),e.prototype=null===t?Object.create(t):(i.prototype=t.prototype,new i)}(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return H},enumerable:!0,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return I},enumerable:!0,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!0,configurable:!0}),t.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},t.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},t.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},t}(e);class L extends t{createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(e){this.formElement&&this.formElement.setAttribute("aria-label",e)}firstUpdated(){super.firstUpdated(),this.mdcRoot.addEventListener("change",e=>{this.dispatchEvent(new Event("change",e))})}}class B extends t{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=T}createAdapter(){return{registerInteractionHandler:(e,t)=>{this.labelEl.addEventListener(e,t)},deregisterInteractionHandler:(e,t)=>{this.labelEl.removeEventListener(e,t)},activateInputRipple:async()=>{const e=this.input;if(e instanceof L){const t=await e.ripple;t&&t.startPress()}},deactivateInputRipple:async()=>{const e=this.input;if(e instanceof L){const t=await e.ripple;t&&t.endPress()}}}}get input(){return i(this.slotEl,"*")}render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return r`
      <div class="mdc-form-field ${o(e)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const e=this.input;e&&(e.focus(),e.click())}}E([R({type:Boolean})],B.prototype,"alignEnd",void 0),E([R({type:Boolean})],B.prototype,"spaceBetween",void 0),E([R({type:Boolean})],B.prototype,"nowrap",void 0),E([R({type:String}),k((async function(e){const t=this.input;t&&("input"===t.localName?t.setAttribute("aria-label",e):t instanceof L&&(await t.updateComplete,t.setAriaLabel(e)))}))],B.prototype,"label",void 0),E([C(".mdc-form-field")],B.prototype,"mdcRoot",void 0),E([C("slot")],B.prototype,"slotEl",void 0),E([C("label")],B.prototype,"labelEl",void 0);const F=((e,...t)=>{const i=t.reduce((t,i,r)=>t+(e=>{if(e instanceof z)return e.cssText;if("number"==typeof e)return e;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${e}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(i)+e[r+1],e[0]);return new z(i,P)})`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch)[dir=rtl]{margin-left:10px}`;let U=class extends B{};var N;U.styles=F,U=E([(N="mwc-formfield",e=>"function"==typeof e?((e,t)=>(window.customElements.define(e,t),t))(N,e):((e,t)=>{const{kind:i,elements:r}=t;return{kind:i,elements:r,finisher(t){window.customElements.define(e,t)}}})(N,e))],U);const M=customElements.get("mwc-formfield");s([a("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"get",static:!0,key:"styles",value:function(){return[F,n`
        :host(:not([alignEnd])) ::slotted(ha-switch) {
          margin-right: 10px;
        }
        :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {
          margin-left: 10px;
          margin-right: auto;
        }
      `]}}]}}),M);function V(e,t,i,r){var o,s=arguments.length,n=s<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var a=e.length-1;a>=0;a--)(o=e[a])&&(n=(s<3?o(n):s>3?o(t,i,n):o(t,i))||n);return s>3&&n&&Object.defineProperty(t,i,n),n}window.JSCompiler_renameProperty=(e,t)=>e;const K=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?Object.assign(Object.assign({},t),{finisher(i){i.createProperty(t.key,e)}}):{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(i){i.createProperty(t.key,e)}};function X(e){return(t,i)=>void 0!==i?((e,t,i)=>{t.constructor.createProperty(i,e)})(e,t,i):K(e,t)}function q(e){return(t,i)=>{const r={get(){return this.renderRoot.querySelector(e)},enumerable:!0,configurable:!0};return void 0!==i?J(r,t,i):Q(r,t)}}const J=(e,t,i)=>{Object.defineProperty(t,i,e)},Q=(e,t)=>({kind:"method",placement:"prototype",key:t.key,descriptor:e});function G(e){return(t,i)=>void 0!==i?((e,t,i)=>{Object.assign(t[i],e)})(e,t,i):((e,t)=>Object.assign(Object.assign({},t),{finisher(i){Object.assign(i.prototype[t.key],e)}}))(e,t)}const W="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Y=Symbol();class Z{constructor(e,t){if(t!==Y)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return void 0===this._styleSheet&&(W?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}(window.litElementVersions||(window.litElementVersions=[])).push("2.3.1");var ee=function(e,t){return(ee=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var i in t)t.hasOwnProperty(i)&&(e[i]=t[i])})(e,t)};var te,ie,re=function(){return(re=Object.assign||function(e){for(var t,i=1,r=arguments.length;i<r;i++)for(var o in t=arguments[i])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e}).apply(this,arguments)},oe={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},se={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"},ne=function(e){function t(i){return e.call(this,re(re({},t.defaultAdapter),i))||this}return function(e,t){function i(){this.constructor=e}ee(e,t),e.prototype=null===t?Object.create(t):(i.prototype=t.prototype,new i)}(t,e),Object.defineProperty(t,"strings",{get:function(){return se},enumerable:!0,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return oe},enumerable:!0,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!0,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked_(e),this.updateCheckedStyling_(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(oe.DISABLED):this.adapter.removeClass(oe.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked_(t.checked),this.updateCheckedStyling_(t.checked)},t.prototype.updateCheckedStyling_=function(e){e?this.adapter.addClass(oe.CHECKED):this.adapter.removeClass(oe.CHECKED)},t.prototype.updateAriaChecked_=function(e){this.adapter.setNativeControlAttr(se.ARIA_CHECKED_ATTR,""+!!e)},t}(e);class ae extends L{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=ne,this.rippleHandlers=new c(()=>(this.shouldRenderRipple=!0,this.ripple))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},l(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?r`
        <mwc-ripple 
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}render(){return r`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}V([X({type:Boolean}),k((function(e){this.mdcFoundation.setChecked(e)}))],ae.prototype,"checked",void 0),V([X({type:Boolean}),k((function(e){this.mdcFoundation.setDisabled(e)}))],ae.prototype,"disabled",void 0),V([q(".mdc-switch")],ae.prototype,"mdcRoot",void 0),V([q("input")],ae.prototype,"formElement",void 0),V([(te="mwc-ripple",(e,t)=>{const i={async get(){return await this.updateComplete,this.renderRoot.querySelector(te)},enumerable:!0,configurable:!0};return void 0!==t?J(i,e,t):Q(i,e)})],ae.prototype,"ripple",void 0),V([X({attribute:!1,hasChanged:null==ie?void 0:ie.hasChanged})],ae.prototype,"shouldRenderRipple",void 0),V([G({passive:!0})],ae.prototype,"handleRippleMouseDown",null),V([G({passive:!0})],ae.prototype,"handleRippleTouchStart",null);const ce=((e,...t)=>{const i=t.reduce((t,i,r)=>t+(e=>{if(e instanceof Z)return e.cssText;if("number"==typeof e)return e;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${e}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(i)+e[r+1],e[0]);return new Z(i,Y)})`.mdc-switch__thumb-underlay{left:-18px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-18px}.mdc-switch__native-control{width:68px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:32px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(20px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-20px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-20px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(20px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none}`;let le=class extends ae{};le.styles=ce,le=V([(e=>t=>"function"==typeof t?((e,t)=>(window.customElements.define(e,t),t))(e,t):((e,t)=>{const{kind:i,elements:r}=t;return{kind:i,elements:r,finisher(t){window.customElements.define(e,t)}}})(e,t))("mwc-switch")],le);const de=customElements.get("mwc-switch");s([a("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[h({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){p(u(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",()=>{this.haptic&&d(window,"haptic","light")})}},{kind:"get",static:!0,key:"styles",value:function(){return[ce,n`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),de);let he=s([a("hacs-install-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[h()],key:"repository",value:void 0},{kind:"field",decorators:[h()],key:"_repository",value:void 0},{kind:"field",decorators:[h()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[h()],key:"_installing",value:()=>!1},{kind:"field",decorators:[h()],key:"_error",value:void 0},{kind:"field",decorators:[f("#version")],key:"_version",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return e.forEach((e,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===t&&(this._repository=this._getRepository(this.repositories,this.repository))}),e.has("sidebarDocked")||e.has("narrow")||e.has("active")||e.has("_toggle")||e.has("_error")||e.has("_repository")||e.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>y((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"field",key:"_getInstallPath",value:()=>y(e=>{let t=e.local_path;return"theme"===e.category&&(t=`${t}/${e.file_name}`),t})},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await g(this.hass,this._repository.id),this.repositories=await b(this.hass)),this._toggle=!1,this.hass.connection.subscribeEvents(e=>this._error=e.data,"hacs/error")}},{kind:"method",key:"render",value:function(){if(!this.active)return r``;const e=this._getInstallPath(this._repository);return r`
      <hacs-dialog
        .active=${this.active}
        .narrow=${this.narrow}
        .hass=${this.hass}
        .secondary=${this.secondary}
        .title=${this._repository.name}
        dynamicHeight
      >
        <div class="content">
          ${"version"===this._repository.version_or_commit?r`<div class="beta-container">
                  <ha-formfield .label=${this.hacs.localize("dialog_install.show_beta")}>
                    <ha-switch
                      ?disabled=${this._toggle}
                      .checked=${this._repository.beta}
                      @change=${this._toggleBeta}
                    ></ha-switch>
                  </ha-formfield>
                </div>
                <div class="version-select-container">
                  <paper-dropdown-menu
                    ?disabled=${this._toggle}
                    class="version-select-dropdown"
                    label="${this.hacs.localize("dialog_install.select_version")}"
                  >
                    <paper-listbox
                      id="version"
                      class="version-select-list"
                      slot="dropdown-content"
                      selected="0"
                    >
                      ${this._repository.releases.map(e=>r`<paper-item .version=${e} class="version-select-item"
                          >${e}</paper-item
                        >`)}
                      ${"hacs/integration"===this._repository.full_name||this._repository.hide_default_branch?"":r`
                            <paper-item
                              .version=${this._repository.default_branch}
                              class="version-select-item"
                              >${this._repository.default_branch}</paper-item
                            >
                          `}
                    </paper-listbox>
                  </paper-dropdown-menu>
                </div>`:""}
          ${this._repository.can_install?"":r`<p class="error">
                ${this.hacs.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",this._repository.homeassistant)}
              </p>`}
          <div class="note">
            ${this.hacs.localize("repository.note_installed")}
            <code>'${e}'</code>
            ${"plugin"===this._repository.category&&"storage"!==this.hacs.status.lovelace_mode?r`
                  <p>${this.hacs.localize("repository.lovelace_instruction")}</p>
                  <pre>
                url: ${this._lovelaceUrl()}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?r`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          </div>
          ${this._error?r`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!this._repository.can_install||this._toggle}
          @click=${this._installRepository}
          >${this._installing?r`<ha-circular-progress active></ha-circular-progress>`:this.hacs.localize("common.install")}</mwc-button
        >
        <hacs-link slot="secondaryaction" .url="https://github.com/${this._repository.full_name}"
          ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
        >
      </hacs-dialog>
    `}},{kind:"method",key:"_lovelaceUrl",value:function(){var e,t;return`/hacsfiles/${null===(e=this._repository)||void 0===e?void 0:e.full_name.split("/")[1]}/${null===(t=this._repository)||void 0===t?void 0:t.file_name}`}},{kind:"method",key:"_toggleBeta",value:async function(){this._toggle=!0,await v(this.hass,this.repository),this.repositories=await b(this.hass),this._toggle=!1}},{kind:"method",key:"_installRepository",value:async function(){if(this._installing=!0,"commit"!==this._repository.version_or_commit){var e,t;const i=(null===(e=this._version)||void 0===e||null===(t=e.selectedItem)||void 0===t?void 0:t.version)||this._repository.available_version||this._repository.default_branch;await w(this.hass,this._repository.id,i)}else await _(this.hass,this._repository.id);this.hacs.log.debug(this._repository.category,"_installRepository"),this.hacs.log.debug(this.hacs.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&await x(this.hass,this._repository),this._installing=!1,this.dispatchEvent(new Event("hacs-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"reload"},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[n`
        .version-select-dropdown {
          width: 100%;
        }
        .content {
          padding: 32px 8px;
        }
        .note {
          margin-bottom: -32px;
          margin-top: 12px;
        }
        .lovelace {
          margin-top: 8px;
        }
        .error {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        paper-menu-button {
          color: var(--secondary-text-color);
          padding: 0;
        }
        paper-item {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }
        pre {
          white-space: pre-line;
          user-select: all;
        }
      `]}}]}}),m);export{he as HacsInstallDialog};
