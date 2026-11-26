/* Load in <head> WITHOUT defer: applies saved theme + colour pattern before first paint (no white flash).
   URL ?p=<pattern>&mode=dark|light overrides (handy for screenshots). */
(function(){var P={profiz:['solid','outline','light'],tropic:['solid','3d','light'],jewel:['solid','gold','light'],
 pastel:['pastel','tint','light'],sunset:['solid','frost','light'],neon:['glass','neon','dark']};
 var q=new URLSearchParams(location.search),s={};try{s=JSON.parse(localStorage.getItem('sr-theme-v1')||'{}')}catch(e){}
 var p=q.get('p')||s.pattern||'profiz';if(!P[p])p='profiz';
 var m=q.get('mode')||s.mode||P[p][2];var h=document.documentElement;
 h.dataset.pattern=p;h.dataset.kind=P[p][0];h.dataset.ghost=P[p][1];h.classList.toggle('dark',m==='dark');
 window.SR_PATTERNS=P;})();
