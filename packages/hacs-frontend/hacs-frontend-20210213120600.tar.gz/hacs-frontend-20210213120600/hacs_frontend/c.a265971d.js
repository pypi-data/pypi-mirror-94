import{_ as i,H as o,p as t,I as e,h as r,w as a,J as s,K as n,N as d,O as c,s as l,g as p,c as h}from"./e.2be12e9e.js";import"./c.2105f995.js";import"./c.f291fdd9.js";import"./c.d77ccf64.js";import"./c.b190b3c3.js";import"./c.291c2df3.js";import"./c.1cadb769.js";let u=i([h("hacs-custom-repositories-dialog")],(function(i,o){return{F:class extends o{constructor(...o){super(...o),i(this)}},d:[{kind:"field",decorators:[t()],key:"_inputRepository",value:void 0},{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[e("#add-input")],key:"_addInput",value:void 0},{kind:"field",decorators:[e("#category")],key:"_addCategory",value:void 0},{kind:"method",key:"shouldUpdate",value:function(i){return i.has("narrow")||i.has("active")||i.has("_error")||i.has("repositories")}},{kind:"method",key:"render",value:function(){var i;if(!this.active)return r``;const o=null===(i=this.repositories)||void 0===i?void 0:i.filter(i=>i.custom);return r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("dialog_custom_repositories.title")}
      >
        <div class="content">
          <div class="list">
            ${this._error?r`<div class="error">${this._error.message}</div>`:""}
            ${null==o?void 0:o.filter(i=>this.hacs.configuration.categories.includes(i.category)).map(i=>r`<paper-icon-item>
                  ${"integration"===i.category?r`
                        <img
                          src="https://brands.home-assistant.io/_/${i.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${a} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body
                    @click=${()=>this._showReopsitoryInfo(String(i.id))}
                    three-line
                    >${i.name}
                    <div secondary>${i.description}</div>
                    <div secondary>Category: ${i.category}</div></paper-item-body
                  ><hacs-icon-button
                    class="delete"
                    .icon=${s}
                    @click=${()=>this._removeRepository(i.id)}
                  ></hacs-icon-button>
                </paper-icon-item>`)}
          </div>
        </div>
        <input
          id="add-input"
          class="add-input"
          slot="secondaryaction"
          placeholder="${this.hacs.localize("dialog_custom_repositories.url_placeholder")}"
          .value=${this._inputRepository||""}
          @input=${this._inputValueChanged}
          ?narrow=${this.narrow}
        />

        <div class="add" slot="primaryaction" ?narrow=${this.narrow}>
          <paper-dropdown-menu
            ?narrow=${this.narrow}
            class="category"
            label="${this.hacs.localize("dialog_custom_repositories.category")}"
          >
            <paper-listbox id="category" slot="dropdown-content" selected="-1">
              ${this.hacs.configuration.categories.map(i=>r`
                  <paper-item class="categoryitem" .category=${i}>
                    ${this.hacs.localize("common."+i)}
                  </paper-item>
                `)}
            </paper-listbox>
          </paper-dropdown-menu>
          <mwc-button
            ?narrow=${this.narrow}
            slot="primaryaction"
            raised
            @click=${this._addRepository}
            >${this.hacs.localize("common.add")}</mwc-button
          >
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.hass.connection.subscribeEvents(i=>this._error=i.data,"hacs/error")}},{kind:"method",key:"_inputValueChanged",value:function(){var i;this._inputRepository=null===(i=this._addInput)||void 0===i?void 0:i.value}},{kind:"method",key:"_addRepository",value:async function(){var i,o;this._error=void 0;const t=this._inputRepository,e=null===(i=this._addCategory)||void 0===i||null===(o=i.selectedItem)||void 0===o?void 0:o.category;e?t?(await n(this.hass,t,e),this.repositories=await d(this.hass)):this._error={message:this.hacs.localize("dialog_custom_repositories.no_repository")}:this._error={message:this.hacs.localize("dialog_custom_repositories.no_category")}}},{kind:"method",key:"_removeRepository",value:async function(i){this._error=void 0,await c(this.hass,i),this.repositories=await d(this.hass)}},{kind:"method",key:"_onImageLoad",value:function(i){i.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(i){i.target.outerHTML='<ha-icon\n      icon="mdi:github-circle"\n      slot="item-icon"\n    ></ha-icon>'}},{kind:"method",key:"_showReopsitoryInfo",value:async function(i){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:i},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l,p`
        .content {
          width: 1024px;
          display: contents;
        }
        .list {
          position: relative;
          margin-top: 16px;
          max-height: 870px;
          overflow: auto;
        }
        ha-icon-button,
        ha-icon {
          color: var(--secondary-text-color);
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
          position: absolute;
        }
        .delete,
        paper-item-body {
          cursor: pointer;
        }
        .error {
          line-height: 0px;
          margin: 12px;
          color: var(--hacs-error-color, var(--google-red-500));
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add {
          display: flex;
          width: 100%;
          align-items: center;
        }

        .add-input {
          width: 100%;
          height: 40px;
          border: 0;
          border-bottom: 1px var(--mdc-theme-primary) solid;
          padding: 0;
          text-align: left;
          padding-right: 71px;
          font-size: initial;
          color: var(--sidebar-text-color);
          font-family: var(--paper-font-body1_-_font-family);
        }
        input:focus {
          outline-offset: 0;
          outline: 0;
        }
        input {
          background-color: var(--sidebar-background-color);
        }
        paper-dropdown-menu {
          width: 100%;
          left: -50px;
          top: -8px;
        }
        mwc-button {
          margin-right: 10px;
        }

        input[narrow],
        .add[narrow],
        paper-dropdown-menu[narrow],
        mwc-button[narrow] {
          margin: 0;
          padding: 0;
          left: 0;
          top: 0;
          width: 100%;
          max-width: 100%;
        }
        .add[narrow] {
          display: contents;
        }
      `]}}]}}),o);export{u as HacsCustomRepositoriesDialog};
