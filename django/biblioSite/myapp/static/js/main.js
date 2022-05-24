class BibApp extends MinzeElement {
  css = () => `
    :host {
      width: 100%;
      min-height: 100vh;
      display: flex;
    }
  `
}
BibApp.define()

class BibMain extends MinzeElement {
  css = () => `
    :host {
      height: 100vh;
      flex-grow: 1;
      overflow-y: scroll;
    }
  `
}
BibMain.define()

class BibSidebar extends MinzeElement {
  attrs = ['active']

  html = () => `
    <div class="logo">
      <img width="80%" height="auto" src="/static/assets/logo.svg">
    </div>

    <nav class="nav">
      <div class="nav__entry ${this.active == "index" ? "nav__entry--active" : ''}">
        <a href="/"><img src="/static/assets/icon-home.svg"></a>
      </div>
      
      <div class="nav__entry ${this.active == "home" ? "nav__entry--active" : ''}">
        <a href="/home"><img src="/static/assets/icon-user.svg"></a>
      </div>

      <!-- -------------- COMMENTATO -----------------

      <div class="nav__entry">
        <img src="static/assets/icon-view-grid.svg">
      </div>

      <div class="nav__entry">
        <img src="static/assets/icon-cog.svg">
      </div>
      
      -->
    </nav>
  `

  css = () => `
    :host {
      width: 100px;
      height: 100vh;
      flex-shrink: 0;
      background: rgb(39 39 42);
      box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.25);
    }

    @media (min-width: 768px) {
      :host {
        width: 120px;
      }
    }
    
    .logo {
      width: 100%;
      height: 120px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-bottom: 1px solid rgb(82 82 91);
      
    }

    .nav {
      padding: 32px 0;
    }

    .nav__entry {
      width: 100%;
      height: 64px;
      display: flex;
      justify-content: center;
      align-items: center;
      opacity: 50%;
      position: relative;
      margin: 16px 0;
    }

    .nav__entry--active {
      opacity: 100%;
    }

    .nav__entry--active::before {
      content: '';
      width: 8px;
      height: 100%;
      background: rgb(255 255 255);
      border-radius: 0 9999px 9999px 0;
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
    }
  `
}
BibSidebar.define()

class BibHeader extends MinzeElement {
  html = () => `
    <div>
      <h1 class="headline"><slot name="headline"></slot></h1>
      <p class="sub-headline"><slot name="sub-headline"></slot></p>
    </div>

    <slot name="nav"></slot>
  `

  css = () => `
    :host {
      width: 100%;
      height: 120px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgb(212 212 216);
      padding: 0 24px;
    }

    @media (min-width: 768px) {
      :host {
        padding: 0 48px;
      }
    }

    .headline {
      font-size: 30px;
      font-weight: bold;
      margin: 0;
    }

    .sub-headline {
      font-size: 18px;
      margin: 0;
    }

    ::slotted(nav) {
      display: flex;
      gap: 16px;
    }
  `
}
BibHeader.define()

class BibWrap extends MinzeElement {
  attrs = ['headline', 'vertical', 'width', 'nowrap']

  html = () => `
    <h2 class="headline">${this.headline ?? ''}</h2>

    <div class="wrap">
      <slot></slot>
    </div>
  `

  css = () => `
    :host {
      width: 100%;
      margin-bottom: 4px;
    }

    @media (min-width: 768px) {
      :host {
        margin-bottom: 8px;
      }
    }

    @media (min-width: 768px) {
      :host {
        width: ${this.width ?? '100%'};
      }
    }

    .headline {
      margin: 0 0 14px;
    }

    .wrap {
      display: flex;
      flex-wrap: wrap;
      flex-direction: ${this.vertical ? 'column' : 'row'};
      gap: 14px;
    }

    @media (min-width: 768px) {
      .wrap {
        flex-wrap: ${this.nowrap ? 'nowrap' : 'wrap'};
      }
    }
  `
}
BibWrap.define()

class BibContent extends MinzeElement {
  css = () => `
    :host {
      max-width: 1600px;
      padding: 24px;
      margin: 0 auto;
    }

    @media (min-width: 768px) {
      :host {
        padding: 48px;
      }
    }
  `
}
BibContent.define()

class BibWelcome extends MinzeElement {
  attrs = ['name', 'biblio']

  html = () => `
    <div>
      <p class="text">Bentornato,</p>
      <h2 class="headline">${this.name ?? ''}</h2>
    </div>

    <div>
      <p class="text-consiglio">Oggi ti consiglio di andare in <b>${this.biblio ?? ''}</b></p>
      <h2 class="headline"></h2>
    </div>

    

    <img src="/static/assets/icon-sun.svg" class="icon">
  `

  css = () => `
    :host {
      width: 100%;
      background: rgb(228 228 231);
      border-radius: 2px;
      overflow: hidden;
      position: relative;
      padding: 24px;
      margin-bottom: 48px;
    }

    .text {
      font-size: 18px;
      margin: 0;
    }

    .text-consiglio {
      font-size: 18px;
      margin-top: 50px;
    }

    .headline {
      font-size: 30px;
      margin: 0;
    }

    .button {
      margin-top: 32px;
    }

    .icon {
      width: 512px;
      height: 512px;
      opacity: 5%;
      position: absolute;
      right: 0;
      bottom: 0;
      transform: translate(0, 50%);
    }
  `
}
BibWelcome.define()

class BibButton extends MinzeElement {
  attrs = ['href', 'target', 'rel']

  html = () => `
    <a
      ${this.href ? `href="${this.href}"` : ''}
      ${this.target ? `href="${this.target}"` : ''}
      ${this.rel ? `href="${this.rel}"` : ''}
    >
      <slot></slot>
    </a>
  `

  css = () => `
    :host {
      display: inline-block;
      background: rgb(63, 63, 70);
      color: rgb(255 255 255);
      cursor: pointer;
      border-radius: 2px;
      transition: background 0.2s ease-in-out;
      padding: 8px 16px;
    }

    :host(:hover) {
      background: rgb(82, 82, 91);
    }
  `
}
BibButton.define()

class InfoCard extends MinzeElement {
  attrs = ['top-line', 'headline', 'value', 'background']

  html = () => `
    <div class="top-line">${this.topLine ?? ''}</div>
    <div class="headline">${this.headline ?? ''}</div>

    <slot>
      <div class="value">${this.value ?? ''}</div>
    </slot>
  `

  css = () => `
    :host {
      width: 200px;
      height: 180px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      background: ${this.background ?? 'transparent'};
      font-family: sans-serif;
      border-radius: 2px;
      padding: 24px 24px 16px;
    }

    .top-line {
      font-size: 16px;
      margin-top: 2px;
    }

    .headline {
      font-size: 20px;
      font-weight: bold;
    }

    .value {
      font-size: 36px;
      font-weight: bold;
      margin-top: auto;
    }

    ::slotted(*) {
      margin-top: auto;
      margin-bottom: 12px;
    }
  `
}

InfoCard.define()

class ExtraCard extends MinzeElement {
  attrs = ['first-line', 'second-line', 'background']

  html = () => `
    <div class="container">
      <div class="first-line">${this.firstLine ?? ''}</div>
      <div class="second-line">${this.secondLine ?? ''}</div>
    </div>
  `

  css = () => `
    :host {
      width: 200px;
      height: 180px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      background: ${this.background ?? 'transparent'};
      font-family: sans-serif;
      border-radius: 2px;
      padding: 24px 24px 16px;
    }

    .container {
      font-size: 16px;
      margin: auto 0;
      font-weight: bold;
    }

    .first-line {
      font-size: 16px;
      
      font-weight: bold;
    }

    .second-line {
      font-size: 16px;
      margin-top: 5px;
      font-weight: bold;
    }

  `
}

ExtraCard.define()