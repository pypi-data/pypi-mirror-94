import{_ as t,H as s,h as i,c as o}from"./e.2be12e9e.js";import{m as e}from"./c.213e64a1.js";import"./c.41e411dd.js";import{v as n}from"./c.54dac331.js";import"./c.2105f995.js";import"./c.f291fdd9.js";let a=t([o("hacs-about-dialog")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?i`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.narrow?"HACS":"Home Assistant Community Store"}
        hideActions
      >
        <div class="content">
          ${e.html(`\n**${this.hacs.localize("dialog_about.integration_version")}:** | ${this.hacs.configuration.version}\n--|--\n**${this.hacs.localize("dialog_about.frontend_version")}:** | ${n}\n**${this.hacs.localize("common.repositories")}:** | ${this.repositories.length}\n**${this.hacs.localize("dialog_about.installed_repositories")}:** | ${this.repositories.filter(t=>t.installed).length}\n\n**${this.hacs.localize("dialog_about.useful_links")}:**\n\n- [General documentation](https://hacs.xyz/)\n- [Configuration](https://hacs.xyz/docs/configuration/start)\n- [FAQ](https://hacs.xyz/docs/faq/what)\n- [GitHub](https://github.com/hacs)\n- [Discord](https://discord.gg/apgchf8)\n- [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)\n- [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)\n\n***\n\n_Everything you find in HACS is **not** tested by Home Assistant, that includes HACS itself._\n_The HACS and Home Assistant teams do not support **anything** you find here._\n        `)}
        </div>
      </hacs-dialog>
    `:i``}}]}}),s);export{a as HacsAboutDialog};
