(this["webpackJsonptabool-website"]=this["webpackJsonptabool-website"]||[]).push([[25],{1108:function(e,t,n){"use strict";n.r(t);var i=n(2),r=n(1),c=n(50),a=n(40),s=n(1036),u=n(20),o=n(948),b=n(61),l=n(67),d=n(200),j=n(516),O=n(232),m=n(1032),h=function(e){var t=e.onSubmit,n=Object(o.a)().t,r=Object(u.n)().placeName,c=d.d({place:d.g().required().matches(/^(([A-Z]{1,2}[0-9]?)|([0-9]){3})|([A-Z][A-Z ]{62})$/,n("Ung\xfcltiger Ortname. Benutze die Kurzform deines Orts. Bei Ziffern benutze insgesamt 3 Zahlen (0 am Anfang wenn die Zahl kleiner als 100 ist)."))});return Object(i.jsx)(l.d,{validationSchema:c,initialValues:{place:"string"===typeof r?r:""},onSubmit:t,children:function(e){var t=e.isSubmitting,r=e.errors;return Object(i.jsx)(l.c,{children:Object(i.jsxs)(b.F,{isLoading:t,children:[Object(i.jsxs)(j.a,{mb:2,children:[Object(i.jsx)(l.b,{required:!0,fullWidth:!0,component:O.b,name:"place",type:"text",label:n("Ortsname"),variant:"outlined"}),r.nonFieldErrors&&Object(i.jsx)(m.a,{severity:"error",children:r.nonFieldErrors})]}),Object(i.jsx)(b.L,{disabled:t,type:"submit",children:n("Raum hinzuf\xfcgen")})]})})}})},f=Object(r.memo)(h);t.default=function(){var e=Object(o.a)().t,t=Object(c.h)(),n=Object(a.O)(),r=Object(u.o)().addSuccess,l=Object(s.a)(n,{onSuccess:function(){t.goBack(),r(e("Ort hinzugef\xfcgt!"))}}).mutateAsync;return Object(i.jsx)(b.r,{title:e("Ort hinzuf\xfcgen"),children:Object(i.jsx)(f,{onSubmit:function(e,t){var n=t.setSubmitting,i=t.setErrors;return l(e).catch((function(e){var t;return i(null===(t=e.response)||void 0===t?void 0:t.data)})).finally((function(){return n(!1)}))}})})}}}]);