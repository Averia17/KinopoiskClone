(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{19:function(e,t,n){},38:function(e,t,n){},40:function(e,t,n){"use strict";n.r(t);var c=n(2),i=n.n(c),s=n(12),r=n.n(s),a=(n(19),n(14)),o=n(13),l=n.n(o),j=(n(38),n(1));var u=function(){var e=Object(c.useState)([]),t=Object(a.a)(e,2),n=t[0],i=t[1];return Object(c.useEffect)((function(){l()({method:"GET",url:"http://127.0.0.1:8000/api/top-films/"}).then((function(e){i(e.data)}))}),[]),Object(j.jsx)("div",{children:Object(j.jsx)("ul",{className:"films",children:n.map((function(e){return Object(j.jsxs)("div",{className:"item",children:[Object(j.jsx)("img",{src:e.posterUrl,className:"img"}),Object(j.jsx)("h1",{children:e.nameRu}),Object(j.jsx)("h2",{className:"filmInfo",children:e.year}),Object(j.jsx)("h2",{className:"filmInfo",children:e.rating})]})}))})})},f=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,41)).then((function(t){var n=t.getCLS,c=t.getFID,i=t.getFCP,s=t.getLCP,r=t.getTTFB;n(e),c(e),i(e),s(e),r(e)}))};r.a.render(Object(j.jsx)(i.a.StrictMode,{children:Object(j.jsx)(u,{})}),document.getElementById("root")),f()}},[[40,1,2]]]);
//# sourceMappingURL=main.051f8027.chunk.js.map