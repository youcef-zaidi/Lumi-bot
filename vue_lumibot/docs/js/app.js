(function(e){function t(t){for(var r,a,i=t[0],u=t[1],s=t[2],l=0,f=[];l<i.length;l++)a=i[l],Object.prototype.hasOwnProperty.call(o,a)&&o[a]&&f.push(o[a][0]),o[a]=0;for(r in u)Object.prototype.hasOwnProperty.call(u,r)&&(e[r]=u[r]);d&&d(t);while(f.length)f.shift()();return c.push.apply(c,s||[]),n()}function n(){for(var e,t=0;t<c.length;t++){for(var n=c[t],r=!0,a=1;a<n.length;a++){var u=n[a];0!==o[u]&&(r=!1)}r&&(c.splice(t--,1),e=i(i.s=n[0]))}return e}var r={},o={app:0},c=[];function a(e){return i.p+"js/"+({}[e]||e)+".js"}function i(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,i),n.l=!0,n.exports}i.e=function(e){var t=[],n=o[e];if(0!==n)if(n)t.push(n[2]);else{var r=new Promise((function(t,r){n=o[e]=[t,r]}));t.push(n[2]=r);var c,u=document.createElement("script");u.charset="utf-8",u.timeout=120,i.nc&&u.setAttribute("nonce",i.nc),u.src=a(e);var s=new Error;c=function(t){u.onerror=u.onload=null,clearTimeout(l);var n=o[e];if(0!==n){if(n){var r=t&&("load"===t.type?"missing":t.type),c=t&&t.target&&t.target.src;s.message="Loading chunk "+e+" failed.\n("+r+": "+c+")",s.name="ChunkLoadError",s.type=r,s.request=c,n[1](s)}o[e]=void 0}};var l=setTimeout((function(){c({type:"timeout",target:u})}),12e4);u.onerror=u.onload=c,document.head.appendChild(u)}return Promise.all(t)},i.m=e,i.c=r,i.d=function(e,t,n){i.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},i.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.t=function(e,t){if(1&t&&(e=i(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(i.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)i.d(n,r,function(t){return e[t]}.bind(null,r));return n},i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,"a",t),t},i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},i.p="/vue-crypto-dashboard/",i.oe=function(e){throw console.error(e),e};var u=window["webpackJsonp"]=window["webpackJsonp"]||[],s=u.push.bind(u);u.push=t,u=u.slice();for(var l=0;l<u.length;l++)t(u[l]);var d=s;c.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"0734":function(e){e.exports=JSON.parse('[{"cid":1,"symbol":"BTCUSDT","base":"BTC","quote":"USDT","name":"Bitcoin"},{"cid":74,"symbol":"DOGEBTC","base":"DOGE","quote":"BTC","name":"Dogecoin"},{"cid":1027,"symbol":"ETHUSDT","base":"ETH","quote":"USDT","name":"Ethereum"},{"cid":52,"symbol":"XRPUSDT","base":"XRP","quote":"USDT","name":"XRP"},{"cid":1027,"symbol":"ETHBTC","base":"ETH","quote":"BTC","name":"Ethereum"},{"cid":5161,"symbol":"WRXBTC","base":"WRX","quote":"BTC","name":"WazirX"},{"cid":2416,"symbol":"TFUELBTC","base":"TFUEL","quote":"BTC","name":"Theta Fuel"},{"cid":6636,"symbol":"DOTBNB","base":"DOT","quote":"BNB","name":"Polkadot"},{"cid":10188,"symbol":"ATABNB","base":"ATA","quote":"BNB","name":"Automata Network"},{"cid":3890,"symbol":"MATICBNB","base":"MATIC","quote":"BNB","name":"Polygon"},{"cid":1839,"symbol":"BTCGBP","base":"BTC","quote":"GBP","name":"Binance Coin"},{"cid":5994,"symbol":"SHIBEUR","base":"SHIB","quote":"EUR","name":"SHIBA INU"}]')},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var r=n("2b0e"),o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"app"}},[n("LayoutPage")],1)},c=[],a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"layout-container"},[n("header",{staticClass:"page-header bg-primary"},["infoview"===e.currentPage?n("button",{staticClass:"back-btn",on:{click:function(t){return e.$router.push({path:"/"})}}},[n("i",{staticClass:"fa fa-angle-left fa-2x"})]):e._e(),n("span",{staticClass:"page-title"},[e._v("VUE CRYPTO DASHBOARD")])]),n("div",{staticClass:"page-container"},[n("transition",{attrs:{name:"fade",mode:"out-in"}},[n("keep-alive",{attrs:{include:"dashboard"}},[n("router-view")],1)],1)],1)])},i=[],u=(n("b0c0"),{name:"LayoutPage",data:function(){return{currentPage:"dashboard"}},watch:{$route:{deep:!0,handler:function(e){this.currentPage=e.name}}}}),s=u,l=n("2877"),d=Object(l["a"])(s,a,i,!1,null,null,null),f=d.exports,p={components:{LayoutPage:f}},b=p,m=Object(l["a"])(b,o,c,!1,null,null,null),y=m.exports,v=(n("d3b7"),n("3ca3"),n("ddb0"),n("8c4f"));r["a"].use(v["a"]);var h=new v["a"]({base:"/vue-crypto-dashboard/",mode:"history",routes:[{path:"/",name:"dashboard",component:function(){return n.e("chunk-b76e42e8").then(n.bind(null,"7277"))}},{path:"/view/:symbol",name:"infoview",component:function(){return n.e("chunk-60bb78bb").then(n.bind(null,"686e"))},props:!0}]});h.beforeEach((function(e,t,n){n()}));var g=h,T=n("c0d6"),B=n("9483");Object(B["a"])("".concat("/vue-crypto-dashboard/","service-worker.js"),{ready:function(){console.log("App is being served from cache by a service worker.\nFor more details, visit https://goo.gl/AFskqB")},cached:function(){console.log("Content has been cached for offline use.")},updated:function(){console.log("New content is available; please refresh.")},offline:function(){console.log("No internet connection found. App is running in offline mode.")},error:function(e){console.error("Error during service worker registration:",e)}});n("d5a0"),n("a89b");var E={bind:function(e,t,n){e.clickOutsideEvent=function(r){e==r.target||e.contains(r.target)||n.context[t.expression](r)},document.body.addEventListener("click",e.clickOutsideEvent)},unbind:function(e){document.body.removeEventListener("click",e.clickOutsideEvent)}};r["a"].config.productionTip=!1,r["a"].directive("click-outside",E),new r["a"]({router:g,store:T["a"],render:function(e){return e(y)}}).$mount("#app")},a89b:function(e,t,n){},c0d6:function(e,t,n){"use strict";n("7db0"),n("a434"),n("c740");var r=n("2b0e"),o=n("2f62"),c=n("0734");r["a"].use(o["a"]),t["a"]=new o["a"].Store({strict:!0,state:{currencies:localStorage.getItem("vue-crypto-currencies-new")?JSON.parse(localStorage.getItem("vue-crypto-currencies-new")):c,tickers:{},chartData:[]},getters:{getSymbolById:function(e){return function(t){return e.currencies.find((function(e){return e.symbol===t}))}},getTickerById:function(e){return function(t){return e.tickers[t]}}},mutations:{SET_DEFAULT:function(e){e.currencies=c},UPDATE_TICKER:function(e,t){var n=e.tickers[t.symbol];t.pchg=n?t.price>n.price?1:-1:1,r["a"].set(e.tickers,t.symbol,t)},ADD_COIN_PAIR:function(e,t){e.tickers[t.symbol]||(e.currencies.push(t),localStorage.setItem("vue-crypto-currencies-new",JSON.stringify(e.currencies))),r["a"].set(e.tickers,t.symbol,{pchg:1})},REMOVE_COIN_PAIR:function(e,t){r["a"].delete(e.tickers,t),e.currencies.splice(e.currencies.findIndex((function(e){return e.symbol===t})),1),localStorage.setItem("vue-crypto-currencies-new",JSON.stringify(e.currencies))}}})},d5a0:function(e,t,n){}});
//# sourceMappingURL=app.js.map