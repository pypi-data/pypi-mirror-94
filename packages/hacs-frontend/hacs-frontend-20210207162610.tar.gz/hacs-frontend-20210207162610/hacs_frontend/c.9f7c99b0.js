import{_ as s,H as t,p as e,v as i,a2 as a,h as o,d as r,U as l,V as c,s as n,g as h,c as d}from"./e.0123aca4.js";import{m as p}from"./c.4868acff.js";import"./c.4d00419f.js";import"./c.1f852ac8.js";import"./c.f038c8a3.js";import{u}from"./c.beb6c164.js";let m=s([d("hacs-update-dialog")],(function(s,t){return{F:class extends t{constructor(...t){super(...t),s(this)}},d:[{kind:"field",decorators:[e()],key:"repository",value:void 0},{kind:"field",decorators:[e()],key:"_updating",value:()=>!1},{kind:"field",decorators:[e()],key:"_error",value:void 0},{kind:"field",decorators:[e()],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>i((s,t)=>null==s?void 0:s.find(s=>s.id===t))},{kind:"method",key:"firstUpdated",value:async function(){const s=this._getRepository(this.repositories,this.repository);"commit"!==s.version_or_commit&&(this._releaseNotes=await a(this.hass,s.id),this._releaseNotes=this._releaseNotes.filter(t=>t.tag>s.installed_version)),this.hass.connection.subscribeEvents(s=>this._error=s.data,"hacs/error")}},{kind:"method",key:"render",value:function(){if(!this.active)return o``;const s=this._getRepository(this.repositories,this.repository);return o`
      <hacs-dialog
        .active=${this.active}
        .title=${this.hacs.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${r({content:!0,narrow:this.narrow})}>
          ${s.name}
          <p>
            <b>${this.hacs.localize("dialog_update.installed_version")}:</b>
            ${s.installed_version}
          </p>
          <p>
            <b>${this.hacs.localize("dialog_update.available_version")}:</b>
            ${s.available_version}
          </p>
          ${this._releaseNotes.length>0?this._releaseNotes.map(s=>o`<details>
                  <summary>${s.name}</summary>
                  ${p.html(s.body)}
                </details>`):""}
          ${s.can_install?"":o`<p class="error">
                ${this.hacs.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",s.homeassistant)}
              </p>`}
          ${"integration"===s.category?o`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          ${this._error?o`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!s.can_install}
          @click=${this._updateRepository}
          >${this._updating?o`<ha-circular-progress active></ha-circular-progress>`:this.hacs.localize("common.update")}</mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <hacs-link .url=${this._getChanglogURL()}
            ><mwc-button>${this.hacs.localize("dialog_update.changelog")}</mwc-button></hacs-link
          >
          <hacs-link .url="https://github.com/${s.full_name}"
            ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
          >
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const s=this._getRepository(this.repositories,this.repository);"commit"!==s.version_or_commit?await l(this.hass,s.id,s.available_version):await c(this.hass,s.id),"plugin"===s.category&&"storage"===this.hacs.status.lovelace_mode&&await u(this.hass,s),this._updating=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===s.category&&this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"reload"},bubbles:!0,composed:!0}))}},{kind:"method",key:"_getChanglogURL",value:function(){const s=this._getRepository(this.repositories,this.repository);return"commit"===s.version_or_commit?`https://github.com/${s.full_name}/compare/${s.installed_version}...${s.available_version}`:`https://github.com/${s.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[n,h`
        .content {
          padding: 32px 8px;
        }
        .error {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        details {
          padding: 12px 0;
        }
        summary {
          padding: 4px;
          cursor: pointer;
        }
        .secondary {
          display: flex;
        }
      `]}}]}}),t);export{m as HacsUpdateDialog};
