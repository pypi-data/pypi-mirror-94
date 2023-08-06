import{_ as o,H as t,h as c,c as e}from"./e.2be12e9e.js";import"./c.2105f995.js";import"./c.f291fdd9.js";let i=o([e("hacs-reload-dialog")],(function(o,t){return{F:class extends t{constructor(...t){super(...t),o(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?c`
      <hacs-dialog .active=${this.active} .hass=${this.hass} title="Reload">
        <div class="content">
          ${this.hacs.localize("dialog.reload.description")}
          </br>
          ${this.hacs.localize("dialog.reload.confirm")}
        </div>
        <mwc-button slot="secondaryaction" @click=${this._close}>
          ${this.hacs.localize("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._reload}>
          ${this.hacs.localize("common.reload")}
        </mwc-button>
      </hacs-dialog>
    `:c``}},{kind:"method",key:"_reload",value:function(){window.top.location.reload(!0)}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),t);export{i as HacsReloadDialog};
