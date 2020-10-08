!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define.amd ? define(["exports"], t) : (e = e || self, t(e.FullCalendar = {}))
}(this, function (e) {
    "use strict";

    function t(e, t, n) {
        var r = document.createElement(e);
        if (t)
            for (var i in t) "style" === i ? g(r, t[i]) : mi[i] ? r[i] = t[i] : r.setAttribute(i, t[i]);
        return "string" == typeof n ? r.innerHTML = n : null != n && a(r, n), r
    }

    function n(e) {
        e = e.trim();
        var t = document.createElement(o(e));
        return t.innerHTML = e, t.firstChild
    }

    function r(e) {
        return Array.prototype.slice.call(i(e))
    }

    function i(e) {
        e = e.trim();
        var t = document.createElement(o(e));
        return t.innerHTML = e, t.childNodes
    }

    function o(e) {
        return Ei[e.substr(0, 3)] || "div"
    }

    function a(e, t) {
        for (var n = l(t), r = 0; r < n.length; r++) e.appendChild(n[r])
    }

    function s(e, t) {
        for (var n = l(t), r = e.firstChild || null, i = 0; i < n.length; i++) e.insertBefore(n[i], r)
    }

    function u(e, t) {
        for (var n = l(t), r = e.nextSibling || null, i = 0; i < n.length; i++) e.parentNode.insertBefore(n[i], r)
    }

    function l(e) {
        return "string" == typeof e ? r(e) : e instanceof Node ? [e] : Array.prototype.slice.call(e)
    }

    function c(e) {
        e.parentNode && e.parentNode.removeChild(e)
    }

    function d(e, t) {
        return Di.call(e, t)
    }

    function f(e, t) {
        return Si.call(e, t)
    }

    function p(e, t) {
        for (var n = e instanceof HTMLElement ? [e] : e, r = [], i = 0; i < n.length; i++)
            for (var o = n[i].querySelectorAll(t), a = 0; a < o.length; a++) r.push(o[a]);
        return r
    }

    function h(e, t) {
        for (var n = e instanceof HTMLElement ? [e] : e, r = [], i = 0; i < n.length; i++)
            for (var o = n[i].children, a = 0; a < o.length; a++) {
                var s = o[a];
                t && !f(s, t) || r.push(s)
            }
        return r
    }

    function v(e, t, n) {
        n ? e.classList.add(t) : e.classList.remove(t)
    }

    function g(e, t) {
        for (var n in t) y(e, n, t[n])
    }

    function y(e, t, n) {
        null == n ? e.style[t] = "" : "number" == typeof n && bi.test(t) ? e.style[t] = n + "px" : e.style[t] = n
    }

    function m(e, t) {
        return e.left >= t.left && e.left < t.right && e.top >= t.top && e.top < t.bottom
    }

    function E(e, t) {
        var n = {
            left: Math.max(e.left, t.left),
            right: Math.min(e.right, t.right),
            top: Math.max(e.top, t.top),
            bottom: Math.min(e.bottom, t.bottom)
        };
        return n.left < n.right && n.top < n.bottom && n
    }

    function S(e, t, n) {
        return {
            left: e.left + t,
            right: e.right + t,
            top: e.top + n,
            bottom: e.bottom + n
        }
    }

    function D(e, t) {
        return {
            left: Math.min(Math.max(e.left, t.left), t.right),
            top: Math.min(Math.max(e.top, t.top), t.bottom)
        }
    }

    function b(e) {
        return {
            left: (e.left + e.right) / 2,
            top: (e.top + e.bottom) / 2
        }
    }

    function T(e, t) {
        return {
            left: e.left - t.left,
            top: e.top - t.top
        }
    }

    function w() {
        return null === Ti && (Ti = R()), Ti
    }

    function R() {
        var e = t("div", {
            style: {
                position: "absolute",
                top: -1e3,
                left: 0,
                border: 0,
                padding: 0,
                overflow: "scroll",
                direction: "rtl"
            }
        }, "<div></div>");
        document.body.appendChild(e);
        var n = e.firstChild,
            r = n.getBoundingClientRect().left > e.getBoundingClientRect().left;
        return c(e), r
    }

    function I(e) {
        return e = Math.max(0, e), e = Math.round(e)
    }

    function C(e, t) {
        void 0 === t && (t = !1);
        var n = window.getComputedStyle(e),
            r = parseInt(n.borderLeftWidth, 10) || 0,
            i = parseInt(n.borderRightWidth, 10) || 0,
            o = parseInt(n.borderTopWidth, 10) || 0,
            a = parseInt(n.borderBottomWidth, 10) || 0,
            s = I(e.offsetWidth - e.clientWidth - r - i),
            u = I(e.offsetHeight - e.clientHeight - o - a),
            l = {
                borderLeft: r,
                borderRight: i,
                borderTop: o,
                borderBottom: a,
                scrollbarBottom: u,
                scrollbarLeft: 0,
                scrollbarRight: 0
            };
        return w() && "rtl" === n.direction ? l.scrollbarLeft = s : l.scrollbarRight = s, t && (l.paddingLeft = parseInt(n.paddingLeft, 10) || 0, l.paddingRight = parseInt(n.paddingRight, 10) || 0, l.paddingTop = parseInt(n.paddingTop, 10) || 0, l.paddingBottom = parseInt(n.paddingBottom, 10) || 0), l
    }

    function M(e, t) {
        void 0 === t && (t = !1);
        var n = k(e),
            r = C(e, t),
            i = {
                left: n.left + r.borderLeft + r.scrollbarLeft,
                right: n.right - r.borderRight - r.scrollbarRight,
                top: n.top + r.borderTop,
                bottom: n.bottom - r.borderBottom - r.scrollbarBottom
            };
        return t && (i.left += r.paddingLeft, i.right -= r.paddingRight, i.top += r.paddingTop, i.bottom -= r.paddingBottom), i
    }

    function k(e) {
        var t = e.getBoundingClientRect();
        return {
            left: t.left + window.pageXOffset,
            top: t.top + window.pageYOffset,
            right: t.right + window.pageXOffset,
            bottom: t.bottom + window.pageYOffset
        }
    }

    function O() {
        return {
            left: window.pageXOffset,
            right: window.pageXOffset + document.documentElement.clientWidth,
            top: window.pageYOffset,
            bottom: window.pageYOffset + document.documentElement.clientHeight
        }
    }

    function _(e) {
        var t = window.getComputedStyle(e);
        return e.getBoundingClientRect().height + parseInt(t.marginTop, 10) + parseInt(t.marginBottom, 10)
    }

    function P(e) {
        for (var t = []; e instanceof HTMLElement;) {
            var n = window.getComputedStyle(e);
            if ("fixed" === n.position) break;
            /(auto|scroll)/.test(n.overflow + n.overflowY + n.overflowX) && t.push(e), e = e.parentNode
        }
        return t
    }

    function H(e) {
        return P(e).map(function (e) {
            return M(e)
        }).concat(O()).reduce(function (e, t) {
            return E(e, t) || t
        })
    }

    function x(e) {
        e.preventDefault()
    }

    function N(e, t, n, r) {
        function i(e) {
            var t = d(e.target, n);
            t && r.call(t, e, t)
        }

        return e.addEventListener(t, i),
            function () {
                e.removeEventListener(t, i)
            }
    }

    function z(e, t, n, r) {
        var i;
        return N(e, "mouseover", t, function (e, t) {
            if (t !== i) {
                i = t, n(e, t);
                var o = function (e) {
                    i = null, r(e, t), t.removeEventListener("mouseleave", o)
                };
                t.addEventListener("mouseleave", o)
            }
        })
    }

    function U(e, t) {
        var n = function (r) {
            t(r), wi.forEach(function (t) {
                e.removeEventListener(t, n)
            })
        };
        wi.forEach(function (t) {
            e.addEventListener(t, n)
        })
    }

    function L(e, t) {
        var n = ie(e);
        return n[2] += 7 * t, oe(n)
    }

    function A(e, t) {
        var n = ie(e);
        return n[2] += t, oe(n)
    }

    function V(e, t) {
        var n = ie(e);
        return n[6] += t, oe(n)
    }

    function B(e, t) {
        return F(e, t) / 7
    }

    function F(e, t) {
        return (t.valueOf() - e.valueOf()) / 864e5
    }

    function W(e, t) {
        return (t.valueOf() - e.valueOf()) / 36e5
    }

    function Z(e, t) {
        return (t.valueOf() - e.valueOf()) / 6e4
    }

    function j(e, t) {
        return (t.valueOf() - e.valueOf()) / 1e3
    }

    function Y(e, t) {
        var n = X(e),
            r = X(t);
        return {
            years: 0,
            months: 0,
            days: Math.round(F(n, r)),
            milliseconds: t.valueOf() - r.valueOf() - (e.valueOf() - n.valueOf())
        }
    }

    function q(e, t) {
        var n = G(e, t);
        return null !== n && n % 7 == 0 ? n / 7 : null
    }

    function G(e, t) {
        return se(e) === se(t) ? Math.round(F(e, t)) : null
    }

    function X(e) {
        return oe([e.getUTCFullYear(), e.getUTCMonth(), e.getUTCDate()])
    }

    function J(e) {
        return oe([e.getUTCFullYear(), e.getUTCMonth(), e.getUTCDate(), e.getUTCHours()])
    }

    function K(e) {
        return oe([e.getUTCFullYear(), e.getUTCMonth(), e.getUTCDate(), e.getUTCHours(), e.getUTCMinutes()])
    }

    function Q(e) {
        return oe([e.getUTCFullYear(), e.getUTCMonth(), e.getUTCDate(), e.getUTCHours(), e.getUTCMinutes(), e.getUTCSeconds()])
    }

    function $(e, t, n) {
        var r = e.getUTCFullYear(),
            i = ee(e, r, t, n);
        if (i < 1) return ee(e, r - 1, t, n);
        var o = ee(e, r + 1, t, n);
        return o >= 1 ? Math.min(i, o) : i
    }

    function ee(e, t, n, r) {
        var i = oe([t, 0, 1 + te(t, n, r)]),
            o = X(e),
            a = Math.round(F(i, o));
        return Math.floor(a / 7) + 1
    }

    function te(e, t, n) {
        var r = 7 + t - n;
        return -(7 + oe([e, 0, r]).getUTCDay() - t) % 7 + r - 1
    }

    function ne(e) {
        return [e.getFullYear(), e.getMonth(), e.getDate(), e.getHours(), e.getMinutes(), e.getSeconds(), e.getMilliseconds()]
    }

    function re(e) {
        return new Date(e[0], e[1] || 0, null == e[2] ? 1 : e[2], e[3] || 0, e[4] || 0, e[5] || 0)
    }

    function ie(e) {
        return [e.getUTCFullYear(), e.getUTCMonth(), e.getUTCDate(), e.getUTCHours(), e.getUTCMinutes(), e.getUTCSeconds(), e.getUTCMilliseconds()]
    }

    function oe(e) {
        return 1 === e.length && (e = e.concat([0])), new Date(Date.UTC.apply(Date, e))
    }

    function ae(e) {
        return !isNaN(e.valueOf())
    }

    function se(e) {
        return 1e3 * e.getUTCHours() * 60 * 60 + 1e3 * e.getUTCMinutes() * 60 + 1e3 * e.getUTCSeconds() + e.getUTCMilliseconds()
    }

    function ue(e, t) {
        var n;
        return "string" == typeof e ? le(e) : "object" == typeof e && e ? ce(e) : "number" == typeof e ? ce((n = {}, n[t || "milliseconds"] = e, n)) : null
    }

    function le(e) {
        var t = Ci.exec(e);
        if (t) {
            var n = t[1] ? -1 : 1;
            return {
                years: 0,
                months: 0,
                days: n * (t[2] ? parseInt(t[2], 10) : 0),
                milliseconds: n * (60 * (t[3] ? parseInt(t[3], 10) : 0) * 60 * 1e3 + 60 * (t[4] ? parseInt(t[4], 10) : 0) * 1e3 + 1e3 * (t[5] ? parseInt(t[5], 10) : 0) + (t[6] ? parseInt(t[6], 10) : 0))
            }
        }
        return null
    }

    function ce(e) {
        return {
            years: e.years || e.year || 0,
            months: e.months || e.month || 0,
            days: (e.days || e.day || 0) + 7 * de(e),
            milliseconds: 60 * (e.hours || e.hour || 0) * 60 * 1e3 + 60 * (e.minutes || e.minute || 0) * 1e3 + 1e3 * (e.seconds || e.second || 0) + (e.milliseconds || e.millisecond || e.ms || 0)
        }
    }

    function de(e) {
        return e.weeks || e.week || 0
    }

    function fe(e, t) {
        return e.years === t.years && e.months === t.months && e.days === t.days && e.milliseconds === t.milliseconds
    }

    function pe(e) {
        return 0 === e.years && 0 === e.months && 1 === e.days && 0 === e.milliseconds
    }

    function he(e, t) {
        return {
            years: e.years + t.years,
            months: e.months + t.months,
            days: e.days + t.days,
            milliseconds: e.milliseconds + t.milliseconds
        }
    }

    function ve(e, t) {
        return {
            years: e.years - t.years,
            months: e.months - t.months,
            days: e.days - t.days,
            milliseconds: e.milliseconds - t.milliseconds
        }
    }

    function ge(e, t) {
        return {
            years: e.years * t,
            months: e.months * t,
            days: e.days * t,
            milliseconds: e.milliseconds * t
        }
    }

    function ye(e) {
        return Ee(e) / 365
    }

    function me(e) {
        return Ee(e) / 30
    }

    function Ee(e) {
        return be(e) / 864e5
    }

    function Se(e) {
        return be(e) / 6e4
    }

    function De(e) {
        return be(e) / 1e3
    }

    function be(e) {
        return 31536e6 * e.years + 2592e6 * e.months + 864e5 * e.days + e.milliseconds
    }

    function Te(e, t) {
        for (var n = null, r = 0; r < Ii.length; r++) {
            var i = Ii[r];
            if (t[i]) {
                var o = e[i] / t[i];
                if (!Ze(o) || null !== n && n !== o) return null;
                n = o
            } else if (e[i]) return null
        }
        return n
    }

    function we(e, t) {
        var n = e.milliseconds;
        if (n) {
            if (n % 1e3 != 0) return {
                unit: "millisecond",
                value: n
            };
            if (n % 6e4 != 0) return {
                unit: "second",
                value: n / 1e3
            };
            if (n % 36e5 != 0) return {
                unit: "minute",
                value: n / 6e4
            };
            if (n) return {
                unit: "hour",
                value: n / 36e5
            }
        }
        return e.days ? t || e.days % 7 != 0 ? {
            unit: "day",
            value: e.days
        } : {
            unit: "week",
            value: e.days / 7
        } : e.months ? {
            unit: "month",
            value: e.months
        } : e.years ? {
            unit: "year",
            value: e.years
        } : {
            unit: "millisecond",
            value: 0
        }
    }

    function Re(e, t) {
        t.left && g(e, {
            borderLeftWidth: 1,
            marginLeft: t.left - 1
        }), t.right && g(e, {
            borderRightWidth: 1,
            marginRight: t.right - 1
        })
    }

    function Ie(e) {
        g(e, {
            marginLeft: "",
            marginRight: "",
            borderLeftWidth: "",
            borderRightWidth: ""
        })
    }

    function Ce() {
        document.body.classList.add("fc-not-allowed")
    }

    function Me() {
        document.body.classList.remove("fc-not-allowed")
    }

    function ke(e, t, n) {
        var r = Math.floor(t / e.length),
            i = Math.floor(t - r * (e.length - 1)),
            o = [],
            a = [],
            s = [],
            u = 0;
        Oe(e), e.forEach(function (t, n) {
            var l = n === e.length - 1 ? i : r,
                c = _(t);
            c < l ? (o.push(t), a.push(c), s.push(t.offsetHeight)) : u += c
        }), n && (t -= u, r = Math.floor(t / o.length), i = Math.floor(t - r * (o.length - 1))), o.forEach(function (e, t) {
            var n = t === o.length - 1 ? i : r,
                u = a[t],
                l = s[t],
                c = n - (u - l);
            u < n && (e.style.height = c + "px")
        })
    }

    function Oe(e) {
        e.forEach(function (e) {
            e.style.height = ""
        })
    }

    function _e(e) {
        var t = 0;
        return e.forEach(function (e) {
            var n = e.firstChild;
            if (n instanceof HTMLElement) {
                var r = n.offsetWidth;
                r > t && (t = r)
            }
        }), t++, e.forEach(function (e) {
            e.style.width = t + "px"
        }), t
    }

    function Pe(e, t) {
        var n = {
            position: "relative",
            left: -1
        };
        g(e, n), g(t, n);
        var r = e.offsetHeight - t.offsetHeight,
            i = {
                position: "",
                left: ""
            };
        return g(e, i), g(t, i), r
    }

    function He(e) {
        e.classList.add("fc-unselectable"), e.addEventListener("selectstart", x)
    }

    function xe(e) {
        e.classList.remove("fc-unselectable"), e.removeEventListener("selectstart", x)
    }

    function Ne(e) {
        e.addEventListener("contextmenu", x)
    }

    function ze(e) {
        e.removeEventListener("contextmenu", x)
    }

    function Ue(e) {
        var t, n, r = [],
            i = [];
        for ("string" == typeof e ? i = e.split(/\s*,\s*/) : "function" == typeof e ? i = [e] : Array.isArray(e) && (i = e), t = 0; t < i.length; t++) n = i[t], "string" == typeof n ? r.push("-" === n.charAt(0) ? {
            field: n.substring(1),
            order: -1
        } : {
            field: n,
            order: 1
        }) : "function" == typeof n && r.push({
            func: n
        });
        return r
    }

    function Le(e, t, n) {
        var r, i;
        for (r = 0; r < n.length; r++)
            if (i = Ae(e, t, n[r])) return i;
        return 0
    }

    function Ae(e, t, n) {
        return n.func ? n.func(e, t) : Ve(e[n.field], t[n.field]) * (n.order || 1)
    }

    function Ve(e, t) {
        return e || t ? null == t ? -1 : null == e ? 1 : "string" == typeof e || "string" == typeof t ? String(e).localeCompare(String(t)) : e - t : 0
    }

    function Be(e) {
        return e.charAt(0).toUpperCase() + e.slice(1)
    }

    function Fe(e, t) {
        var n = String(e);
        return "000".substr(0, t - n.length) + n
    }

    function We(e, t) {
        return e - t
    }

    function Ze(e) {
        return e % 1 == 0
    }

    function je(e, t, n) {
        if ("function" == typeof e && (e = [e]), e) {
            var r = void 0,
                i = void 0;
            for (r = 0; r < e.length; r++) i = e[r].apply(t, n) || i;
            return i
        }
    }

    function Ye() {
        for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
        for (var n = 0; n < e.length; n++)
            if (void 0 !== e[n]) return e[n]
    }

    function qe(e, t) {
        var n, r, i, o, a, s = function () {
            var u = (new Date).valueOf() - o;
            u < t ? n = setTimeout(s, t - u) : (n = null, a = e.apply(i, r), i = r = null)
        };
        return function () {
            return i = this, r = arguments, o = (new Date).valueOf(), n || (n = setTimeout(s, t)), a
        }
    }

    function Ge(e, t, n, r) {
        void 0 === n && (n = {});
        var i = {};
        for (var o in t) {
            var a = t[o];
            void 0 !== e[o] ? a === Function ? i[o] = "function" == typeof e[o] ? e[o] : null : i[o] = a ? a(e[o]) : e[o] : void 0 !== n[o] ? i[o] = n[o] : a === String ? i[o] = "" : a && a !== Number && a !== Boolean && a !== Function ? i[o] = a(null) : i[o] = null
        }
        if (r)
            for (var o in e) void 0 === t[o] && (r[o] = e[o]);
        return i
    }

    function Xe(e) {
        return Array.isArray(e) ? Array.prototype.slice.call(e) : e
    }

    function Je(e) {
        var t = Math.floor(F(e.start, e.end)) || 1,
            n = X(e.start);
        return {
            start: n,
            end: A(n, t)
        }
    }

    function Ke(e, t) {
        void 0 === t && (t = ue(0));
        var n = null,
            r = null;
        if (e.end) {
            r = X(e.end);
            var i = e.end.valueOf() - r.valueOf();
            i && i >= be(t) && (r = A(r, 1))
        }
        return e.start && (n = X(e.start), r && r <= n && (r = A(n, 1))), {
            start: n,
            end: r
        }
    }

    function Qe(e) {
        var t = Ke(e);
        return F(t.start, t.end) > 1
    }

    function $e(e, t, n, r) {
        return "year" === r ? ue(n.diffWholeYears(e, t), "year") : "month" === r ? ue(n.diffWholeMonths(e, t), "month") : Y(e, t)
    }

    function et(e, t) {
        function n() {
            this.constructor = e
        }

        Mi(e, t), e.prototype = null === t ? Object.create(t) : (n.prototype = t.prototype, new n)
    }

    function tt(e, t, n, r, i) {
        for (var o = 0; o < r.length; o++) {
            var a = {},
                s = r[o].parse(e, a, n);
            if (s) {
                var u = a.allDay;
                return delete a.allDay, null == u && null == (u = t) && null == (u = s.allDayGuess) && (u = !1), ki(i, a), {
                    allDay: u,
                    duration: s.duration,
                    typeData: s.typeData,
                    typeId: o
                }
            }
        }
        return null
    }

    function nt(e, t, n, r) {
        var i = r[e.recurringDef.typeId],
            o = i.expand(e.recurringDef.typeData, t, n);
        return e.allDay && (o = o.map(X)), o
    }

    function rt(e, t) {
        var n, r, i, o, a, s, u = {};
        if (t)
            for (n = 0; n < t.length; n++) {
                for (r = t[n], i = [], o = e.length - 1; o >= 0; o--)
                    if ("object" == typeof (a = e[o][r]) && a) i.unshift(a);
                    else if (void 0 !== a) {
                        u[r] = a;
                        break
                    }
                i.length && (u[r] = rt(i))
            }
        for (n = e.length - 1; n >= 0; n--) {
            s = e[n];
            for (r in s) r in u || (u[r] = s[r])
        }
        return u
    }

    function it(e, t) {
        var n = {};
        for (var r in e) t(e[r], r) && (n[r] = e[r]);
        return n
    }

    function ot(e, t) {
        var n = {};
        for (var r in e) n[r] = t(e[r], r);
        return n
    }

    function at(e) {
        for (var t = {}, n = 0, r = e; n < r.length; n++) {
            t[r[n]] = !0
        }
        return t
    }

    function st(e) {
        var t = [];
        for (var n in e) t.push(e[n]);
        return t
    }

    function ut(e, t, n, r) {
        for (var i = vt(), o = 0, a = e; o < a.length; o++) {
            var s = a[o],
                u = On(s, t, n, r);
            u && lt(u, i)
        }
        return i
    }

    function lt(e, t) {
        return void 0 === t && (t = vt()), t.defs[e.def.defId] = e.def, e.instance && (t.instances[e.instance.instanceId] = e.instance), t
    }

    function ct(e, t, n) {
        var r = n.dateEnv,
            i = e.defs,
            o = e.instances;
        o = it(o, function (e) {
            return !i[e.defId].recurringDef
        });
        for (var a in i) {
            var s = i[a];
            if (s.recurringDef) {
                var u = nt(s, t, n.dateEnv, n.pluginSystem.hooks.recurringTypes),
                    l = s.recurringDef.duration;
                l || (l = s.allDay ? n.defaultAllDayEventDuration : n.defaultTimedEventDuration);
                for (var c = 0, d = u; c < d.length; c++) {
                    var f = d[c],
                        p = Pn(a, {
                            start: f,
                            end: r.add(f, l)
                        });
                    o[p.instanceId] = p
                }
            }
        }
        return {
            defs: i,
            instances: o
        }
    }

    function dt(e, t) {
        var n = e.instances[t];
        if (n) {
            var r = e.defs[n.defId],
                i = yt(e, function (e) {
                    return ft(r, e)
                });
            return i.defs[r.defId] = r, i.instances[n.instanceId] = n, i
        }
        return vt()
    }

    function ft(e, t) {
        return Boolean(e.groupId && e.groupId === t.groupId)
    }

    function pt(e, t, n) {
        var r = n.opt("eventDataTransform"),
            i = t ? t.eventDataTransform : null;
        return i && (e = ht(e, i)), r && (e = ht(e, r)), e
    }

    function ht(e, t) {
        var n;
        if (t) {
            n = [];
            for (var r = 0, i = e; r < i.length; r++) {
                var o = i[r],
                    a = t(o);
                a ? n.push(a) : null == a && n.push(o)
            }
        } else n = e;
        return n
    }

    function vt() {
        return {
            defs: {},
            instances: {}
        }
    }

    function gt(e, t) {
        return {
            defs: ki({}, e.defs, t.defs),
            instances: ki({}, e.instances, t.instances)
        }
    }

    function yt(e, t) {
        var n = it(e.defs, t),
            r = it(e.instances, function (e) {
                return n[e.defId]
            });
        return {
            defs: n,
            instances: r
        }
    }

    function mt(e, t) {
        var n = null,
            r = null;
        return e.start && (n = t.createMarker(e.start)), e.end && (r = t.createMarker(e.end)), n || r ? n && r && r < n ? null : {
            start: n,
            end: r
        } : null
    }

    function Et(e, t) {
        var n, r, i = [],
            o = t.start;
        for (e.sort(St), n = 0; n < e.length; n++) r = e[n], r.start > o && i.push({
            start: o,
            end: r.start
        }), r.end > o && (o = r.end);
        return o < t.end && i.push({
            start: o,
            end: t.end
        }), i
    }

    function St(e, t) {
        return e.start.valueOf() - t.start.valueOf()
    }

    function Dt(e, t) {
        var n = e.start,
            r = e.end,
            i = null;
        return null !== t.start && (n = null === n ? t.start : new Date(Math.max(n.valueOf(), t.start.valueOf()))), null != t.end && (r = null === r ? t.end : new Date(Math.min(r.valueOf(), t.end.valueOf()))), (null === n || null === r || n < r) && (i = {
            start: n,
            end: r
        }), i
    }

    function bt(e, t) {
        return (null === e.start ? null : e.start.valueOf()) === (null === t.start ? null : t.start.valueOf()) && (null === e.end ? null : e.end.valueOf()) === (null === t.end ? null : t.end.valueOf())
    }

    function Tt(e, t) {
        return (null === e.end || null === t.start || e.end > t.start) && (null === e.start || null === t.end || e.start < t.end)
    }

    function wt(e, t) {
        return (null === e.start || null !== t.start && t.start >= e.start) && (null === e.end || null !== t.end && t.end <= e.end)
    }

    function Rt(e, t) {
        return (null === e.start || t >= e.start) && (null === e.end || t < e.end)
    }

    function It(e, t) {
        return null != t.start && e < t.start ? t.start : null != t.end && e >= t.end ? new Date(t.end.valueOf() - 1) : e
    }

    function Ct(e, t) {
        for (var n = 0, r = 0; r < e.length;) e[r] === t ? (e.splice(r, 1), n++) : r++;
        return n
    }

    function Mt(e, t) {
        var n, r = e.length;
        if (r !== t.length) return !1;
        for (n = 0; n < r; n++)
            if (e[n] !== t[n]) return !1;
        return !0
    }

    function kt(e) {
        var t, n;
        return function () {
            return t && Mt(t, arguments) || (t = arguments, n = e.apply(this, arguments)), n
        }
    }

    function Ot(e, t) {
        var n = null;
        return function () {
            var r = e.apply(this, arguments);
            return (null === n || n !== r && !t(n, r)) && (n = r), n
        }
    }

    function _t(e, t, n) {
        var r = Object.keys(e).length;
        return 1 === r && "short" === e.timeZoneName ? function (e) {
            return Wt(e.timeZoneOffset)
        } : 0 === r && t.week ? function (e) {
            return zt(n.computeWeekNumber(e.marker), n.weekLabel, n.locale, t.week)
        } : Pt(e, t, n)
    }

    function Pt(e, t, n) {
        e = ki({}, e), t = ki({}, t), Ht(e, t), e.timeZone = "UTC";
        var r, i = new Intl.DateTimeFormat(n.locale.codes, e);
        if (t.omitZeroMinute) {
            var o = ki({}, e);
            delete o.minute, r = new Intl.DateTimeFormat(n.locale.codes, o)
        }
        return function (o) {
            var a, s = o.marker;
            return a = r && !s.getUTCMinutes() ? r : i, xt(a.format(s), o, e, t, n)
        }
    }

    function Ht(e, t) {
        e.timeZoneName && (e.hour || (e.hour = "2-digit"), e.minute || (e.minute = "2-digit")), "long" === e.timeZoneName && (e.timeZoneName = "short"), t.omitZeroMinute && (e.second || e.millisecond) && delete t.omitZeroMinute
    }

    function xt(e, t, n, r, i) {
        return e = e.replace(Ni, ""), "short" === n.timeZoneName && (e = Nt(e, "UTC" === i.timeZone || null == t.timeZoneOffset ? "UTC" : Wt(t.timeZoneOffset))), r.omitCommas && (e = e.replace(Hi, "").trim()), r.omitZeroMinute && (e = e.replace(":00", "")), !1 === r.meridiem ? e = e.replace(Pi, "").trim() : "narrow" === r.meridiem ? e = e.replace(Pi, function (e, t) {
            return t.toLocaleLowerCase()
        }) : "short" === r.meridiem ? e = e.replace(Pi, function (e, t) {
            return t.toLocaleLowerCase() + "m"
        }) : "lowercase" === r.meridiem && (e = e.replace(Pi, function (e) {
            return e.toLocaleLowerCase()
        })), e = e.replace(xi, " "), e = e.trim()
    }

    function Nt(e, t) {
        var n = !1;
        return e = e.replace(zi, function () {
            return n = !0, t
        }), n || (e += " " + t), e
    }

    function zt(e, t, n, r) {
        var i = [];
        return "narrow" === r ? i.push(t) : "short" === r && i.push(t, " "), i.push(n.simpleNumberFormat.format(e)), n.options.isRtl && i.reverse(), i.join("")
    }

    function Ut(e, t, n) {
        return n.getMarkerYear(e) !== n.getMarkerYear(t) ? 5 : n.getMarkerMonth(e) !== n.getMarkerMonth(t) ? 4 : n.getMarkerDay(e) !== n.getMarkerDay(t) ? 2 : se(e) !== se(t) ? 1 : 0
    }

    function Lt(e, t) {
        var n = {};
        for (var r in e) r in _i && !(_i[r] <= t) || (n[r] = e[r]);
        return n
    }

    function At(e, t, n, r) {
        for (var i = 0; i < e.length;) {
            var o = e.indexOf(t, i);
            if (-1 === o) break;
            var a = e.substr(0, o);
            i = o + t.length;
            for (var s = e.substr(i), u = 0; u < n.length;) {
                var l = n.indexOf(r, u);
                if (-1 === l) break;
                var c = n.substr(0, l);
                u = l + r.length;
                var d = n.substr(u);
                if (a === c && s === d) return {
                    before: a,
                    after: s
                }
            }
        }
        return null
    }

    function Vt(e, t) {
        return "object" == typeof e && e ? ("string" == typeof t && (e = ki({
            separator: t
        }, e)), new Ui(e)) : "string" == typeof e ? new Li(e, t) : "function" == typeof e ? new Ai(e) : void 0
    }

    function Bt(e, t, n) {
        void 0 === n && (n = !1);
        var r = e.toISOString();
        return r = r.replace(".000", ""), n && (r = r.replace("T00:00:00Z", "")), r.length > 10 && (null == t ? r = r.replace("Z", "") : 0 !== t && (r = r.replace("Z", Wt(t, !0)))), r
    }

    function Ft(e) {
        return Fe(e.getUTCHours(), 2) + ":" + Fe(e.getUTCMinutes(), 2) + ":" + Fe(e.getUTCSeconds(), 2)
    }

    function Wt(e, t) {
        void 0 === t && (t = !1);
        var n = e < 0 ? "-" : "+",
            r = Math.abs(e),
            i = Math.floor(r / 60),
            o = Math.round(r % 60);
        return t ? n + Fe(i, 2) + ":" + Fe(o, 2) : "GMT" + n + i + (o ? ":" + Fe(o, 2) : "")
    }

    function Zt(e, t, n, r) {
        var i = jt(e, n.calendarSystem);
        return {
            date: i,
            start: i,
            end: t ? jt(t, n.calendarSystem) : null,
            timeZone: n.timeZone,
            localeCodes: n.locale.codes,
            separator: r
        }
    }

    function jt(e, t) {
        var n = t.markerToArray(e.marker);
        return {
            marker: e.marker,
            timeZoneOffset: e.timeZoneOffset,
            array: n,
            year: n[0],
            month: n[1],
            day: n[2],
            hour: n[3],
            minute: n[4],
            second: n[5],
            millisecond: n[6]
        }
    }

    function Yt(e, t, n, r) {
        var i = {},
            o = {},
            a = {},
            s = [],
            u = [],
            l = Kt(e.defs, t);
        for (var c in e.defs) {
            var d = e.defs[c];
            "inverse-background" === d.rendering && (d.groupId ? (i[d.groupId] = [], a[d.groupId] || (a[d.groupId] = d)) : o[c] = [])
        }
        for (var f in e.instances) {
            var p = e.instances[f],
                d = e.defs[p.defId],
                h = l[d.defId],
                v = p.range,
                g = !d.allDay && r ? Ke(v, r) : v,
                y = Dt(g, n);
            y && ("inverse-background" === d.rendering ? d.groupId ? i[d.groupId].push(y) : o[p.defId].push(y) : ("background" === d.rendering ? s : u).push({
                def: d,
                ui: h,
                instance: p,
                range: y,
                isStart: g.start && g.start.valueOf() === y.start.valueOf(),
                isEnd: g.end && g.end.valueOf() === y.end.valueOf()
            }))
        }
        for (var m in i)
            for (var E = i[m], S = Et(E, n), D = 0, b = S; D < b.length; D++) {
                var T = b[D],
                    d = a[m],
                    h = l[d.defId];
                s.push({
                    def: d,
                    ui: h,
                    instance: null,
                    range: T,
                    isStart: !1,
                    isEnd: !1
                })
            }
        for (var c in o)
            for (var E = o[c], S = Et(E, n), w = 0, R = S; w < R.length; w++) {
                var T = R[w];
                s.push({
                    def: e.defs[c],
                    ui: l[c],
                    instance: null,
                    range: T,
                    isStart: !1,
                    isEnd: !1
                })
            }
        return {
            bg: s,
            fg: u
        }
    }

    function qt(e) {
        return "background" === e.rendering || "inverse-background" === e.rendering
    }

    function Gt(e, t, n) {
        e.hasPublicHandlers("eventRender") && (t = t.filter(function (t) {
            var r = e.publiclyTrigger("eventRender", [{
                event: new Bi(e.calendar, t.eventRange.def, t.eventRange.instance),
                isMirror: n,
                isStart: t.isStart,
                isEnd: t.isEnd,
                el: t.el,
                view: e
            }]);
            return !1 !== r && (r && !0 !== r && (t.el = r), !0)
        }));
        for (var r = 0, i = t; r < i.length; r++) {
            var o = i[r];
            Xt(o.el, o)
        }
        return t
    }

    function Xt(e, t) {
        e.fcSeg = t
    }

    function Jt(e) {
        return e.fcSeg || null
    }

    function Kt(e, t) {
        return ot(e, function (e) {
            return Qt(e, t)
        })
    }

    function Qt(e, t) {
        var n = [];
        return t[""] && n.push(t[""]), t[e.defId] && n.push(t[e.defId]), n.push(e.ui), Mn(n)
    }

    function $t(e, t, n, r) {
        var i = Kt(e.defs, t),
            o = vt();
        for (var a in e.defs) {
            var s = e.defs[a];
            o.defs[a] = en(s, i[a], n, r.pluginSystem.hooks.eventDefMutationAppliers, r)
        }
        for (var u in e.instances) {
            var l = e.instances[u],
                s = o.defs[l.defId];
            o.instances[u] = nn(l, s, i[l.defId], n, r)
        }
        return o
    }

    function en(e, t, n, r, i) {
        var o = n.standardProps || {};
        null == o.hasEnd && t.durationEditable && tn(t.startEditable ? n.startDelta : null, n.endDelta || null) && (o.hasEnd = !0);
        var a = ki({}, e, o, {
            ui: ki({}, e.ui, o.ui)
        });
        n.extendedProps && (a.extendedProps = ki({}, a.extendedProps, n.extendedProps));
        for (var s = 0, u = r; s < u.length; s++) {
            (0, u[s])(a, n, i)
        }
        return !a.hasEnd && i.opt("forceEventDuration") && (a.hasEnd = !0), a
    }

    function tn(e, t) {
        return e && !be(e) && (e = null), t && !be(t) && (t = null), !(!e && !t) && (Boolean(e) !== Boolean(t) || !fe(e, t))
    }

    function nn(e, t, n, r, i) {
        var o = i.dateEnv,
            a = r.standardProps && !0 === r.standardProps.allDay,
            s = r.standardProps && !1 === r.standardProps.hasEnd,
            u = ki({}, e);
        return a && (u.range = Je(u.range)), r.startDelta && n.startEditable && (u.range = {
            start: o.add(u.range.start, r.startDelta),
            end: u.range.end
        }), s ? u.range = {
            start: u.range.start,
            end: i.getDefaultEventEnd(t.allDay, u.range.start)
        } : !r.endDelta || !n.durationEditable && tn(n.startEditable ? r.startDelta : null, r.endDelta) || (u.range = {
            start: u.range.start,
            end: o.add(u.range.end, r.endDelta)
        }), t.allDay && (u.range = {
            start: X(u.range.start),
            end: X(u.range.end)
        }), u.range.end < u.range.start && (u.range.end = i.getDefaultEventEnd(t.allDay, u.range.start)), u
    }

    function rn(e, t, n, r, i) {
        switch (t.type) {
            case "RECEIVE_EVENTS":
                return on(e, n[t.sourceId], t.fetchId, t.fetchRange, t.rawEvents, i);
            case "ADD_EVENTS":
                return an(e, t.eventStore, r ? r.activeRange : null, i);
            case "MERGE_EVENTS":
                return gt(e, t.eventStore);
            case "PREV":
            case "NEXT":
            case "SET_DATE":
            case "SET_VIEW_TYPE":
                return r ? ct(e, r.activeRange, i) : e;
            case "CHANGE_TIMEZONE":
                return sn(e, t.oldDateEnv, i.dateEnv);
            case "MUTATE_EVENTS":
                return un(e, t.instanceId, t.mutation, t.fromApi, i);
            case "REMOVE_EVENT_INSTANCES":
                return cn(e, t.instances);
            case "REMOVE_EVENT_DEF":
                return yt(e, function (e) {
                    return e.defId !== t.defId
                });
            case "REMOVE_EVENT_SOURCE":
                return ln(e, t.sourceId);
            case "REMOVE_ALL_EVENT_SOURCES":
                return yt(e, function (e) {
                    return !e.sourceId
                });
            case "REMOVE_ALL_EVENTS":
                return vt();
            case "RESET_EVENTS":
                return {
                    defs: e.defs, instances: e.instances
                };
            default:
                return e
        }
    }

    function on(e, t, n, r, i, o) {
        if (t && n === t.latestFetchId) {
            var a = ut(pt(i, t, o), t.sourceId, o);
            return r && (a = ct(a, r, o)), gt(ln(e, t.sourceId), a)
        }
        return e
    }

    function an(e, t, n, r) {
        return n && (t = ct(t, n, r)), gt(e, t)
    }

    function sn(e, t, n) {
        var r = e.defs,
            i = ot(e.instances, function (e) {
                var i = r[e.defId];
                return i.allDay || i.recurringDef ? e : ki({}, e, {
                    range: {
                        start: n.createMarker(t.toDate(e.range.start, e.forcedStartTzo)),
                        end: n.createMarker(t.toDate(e.range.end, e.forcedEndTzo))
                    },
                    forcedStartTzo: n.canComputeOffset ? null : e.forcedStartTzo,
                    forcedEndTzo: n.canComputeOffset ? null : e.forcedEndTzo
                })
            });
        return {
            defs: r,
            instances: i
        }
    }

    function un(e, t, n, r, i) {
        var o = dt(e, t);
        return o = $t(o, r ? {
            "": {
                startEditable: !0,
                durationEditable: !0,
                constraints: [],
                overlap: null,
                allows: [],
                backgroundColor: "",
                borderColor: "",
                textColor: "",
                classNames: []
            }
        } : i.eventUiBases, n, i), gt(e, o)
    }

    function ln(e, t) {
        return yt(e, function (e) {
            return e.sourceId !== t
        })
    }

    function cn(e, t) {
        return {
            defs: e.defs,
            instances: it(e.instances, function (e) {
                return !t[e.instanceId]
            })
        }
    }

    function dn(e, t) {
        return pn({
            eventDrag: e
        }, t)
    }

    function fn(e, t) {
        return pn({
            dateSelection: e
        }, t)
    }

    function pn(e, t) {
        var n = t.view,
            r = ki({
                businessHours: n ? n.props.businessHours : vt(),
                dateSelection: "",
                eventStore: t.state.eventStore,
                eventUiBases: t.eventUiBases,
                eventSelection: "",
                eventDrag: null,
                eventResize: null
            }, e);
        return (t.pluginSystem.hooks.isPropsValid || hn)(r, t)
    }

    function hn(e, t, n, r) {
        return void 0 === n && (n = {}), !(e.eventDrag && !vn(e, t, n, r)) && !(e.dateSelection && !gn(e, t, n, r))
    }

    function vn(e, t, n, r) {
        var i = e.eventDrag,
            o = i.mutatedEvents,
            a = o.defs,
            s = o.instances,
            u = Kt(a, i.isEvent ? e.eventUiBases : {
                "": t.selectionConfig
            });
        r && (u = ot(u, r));
        var l = cn(e.eventStore, i.affectedEvents.instances),
            c = l.defs,
            d = l.instances,
            f = Kt(c, e.eventUiBases);
        for (var p in s) {
            var h = s[p],
                v = h.range,
                g = u[h.defId],
                y = a[h.defId];
            if (!yn(g.constraints, v, l, e.businessHours, t)) return !1;
            var m = t.opt("eventOverlap");
            "function" != typeof m && (m = null);
            for (var E in d) {
                var S = d[E];
                if (Tt(v, S.range)) {
                    if (!1 === f[S.defId].overlap && i.isEvent) return !1;
                    if (!1 === g.overlap) return !1;
                    if (m && !m(new Bi(t, c[S.defId], S), new Bi(t, y, h))) return !1
                }
            }
            for (var D = 0, b = g.allows; D < b.length; D++) {
                var T = b[D],
                    w = ki({}, n, {
                        range: h.range,
                        allDay: y.allDay
                    }),
                    R = e.eventStore.defs[y.defId],
                    I = e.eventStore.instances[p],
                    C = void 0;
                if (C = R ? new Bi(t, R, I) : new Bi(t, y), !T(t.buildDateSpanApi(w), C)) return !1
            }
        }
        return !0
    }

    function gn(e, t, n, r) {
        var i = e.eventStore,
            o = i.defs,
            a = i.instances,
            s = e.dateSelection,
            u = s.range,
            l = t.selectionConfig;
        if (r && (l = r(l)), !yn(l.constraints, u, i, e.businessHours, t)) return !1;
        var c = t.opt("selectOverlap");
        "function" != typeof c && (c = null);
        for (var d in a) {
            var f = a[d];
            if (Tt(u, f.range)) {
                if (!1 === l.overlap) return !1;
                if (c && !c(new Bi(t, o[f.defId], f))) return !1
            }
        }
        for (var p = 0, h = l.allows; p < h.length; p++) {
            var v = h[p],
                g = ki({}, n, s);
            if (!v(t.buildDateSpanApi(g), null)) return !1
        }
        return !0
    }

    function yn(e, t, n, r, i) {
        for (var o = 0, a = e; o < a.length; o++) {
            if (!Sn(mn(a[o], t, n, r, i), t)) return !1
        }
        return !0
    }

    function mn(e, t, n, r, i) {
        return "businessHours" === e ? En(ct(r, t, i)) : "string" == typeof e ? En(yt(n, function (t) {
            return t.groupId === e
        })) : "object" == typeof e && e ? En(ct(e, t, i)) : []
    }

    function En(e) {
        var t = e.instances,
            n = [];
        for (var r in t) n.push(t[r].range);
        return n
    }

    function Sn(e, t) {
        for (var n = 0, r = e; n < r.length; n++) {
            if (wt(r[n], t)) return !0
        }
        return !1
    }

    function Dn(e, t) {
        return Array.isArray(e) ? ut(e, "", t, !0) : "object" == typeof e && e ? ut([e], "", t, !0) : null != e ? String(e) : null
    }

    function bn(e) {
        return (e + "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/'/g, "&#039;").replace(/"/g, "&quot;").replace(/\n/g, "<br />")
    }

    function Tn(e) {
        var t = [];
        for (var n in e) {
            var r = e[n];
            null != r && "" !== r && t.push(n + ":" + r)
        }
        return t.join(";")
    }

    function wn(e) {
        var t = [];
        for (var n in e) {
            var r = e[n];
            null != r && t.push(n + '="' + bn(r) + '"')
        }
        return t.join(" ")
    }

    function Rn(e) {
        return Array.isArray(e) ? e : "string" == typeof e ? e.split(/\s+/) : []
    }

    function In(e, t, n) {
        var r = Ge(e, Fi, {}, n),
            i = Dn(r.constraint, t);
        return {
            startEditable: null != r.startEditable ? r.startEditable : r.editable,
            durationEditable: null != r.durationEditable ? r.durationEditable : r.editable,
            constraints: null != i ? [i] : [],
            overlap: r.overlap,
            allows: null != r.allow ? [r.allow] : [],
            backgroundColor: r.backgroundColor || r.color,
            borderColor: r.borderColor || r.color,
            textColor: r.textColor,
            classNames: r.classNames.concat(r.className)
        }
    }

    function Cn(e, t, n, r) {
        var i = {},
            o = {};
        for (var a in Fi) {
            var s = e + Be(a);
            i[a] = t[s], o[s] = !0
        }
        if ("event" === e && (i.editable = t.editable), r)
            for (var a in t) o[a] || (r[a] = t[a]);
        return In(i, n)
    }

    function Mn(e) {
        return e.reduce(kn, Wi)
    }

    function kn(e, t) {
        return {
            startEditable: null != t.startEditable ? t.startEditable : e.startEditable,
            durationEditable: null != t.durationEditable ? t.durationEditable : e.durationEditable,
            constraints: e.constraints.concat(t.constraints),
            overlap: "boolean" == typeof t.overlap ? t.overlap : e.overlap,
            allows: e.allows.concat(t.allows),
            backgroundColor: t.backgroundColor || e.backgroundColor,
            borderColor: t.borderColor || e.borderColor,
            textColor: t.textColor || e.textColor,
            classNames: e.classNames.concat(t.classNames)
        }
    }

    function On(e, t, n, r) {
        var i = zn(t, n),
            o = {},
            a = tt(e, i, n.dateEnv, n.pluginSystem.hooks.recurringTypes, o);
        if (a) {
            var s = _n(o, t, a.allDay, Boolean(a.duration), n);
            return s.recurringDef = {
                typeId: a.typeId,
                typeData: a.typeData,
                duration: a.duration
            }, {
                def: s,
                instance: null
            }
        }
        var u = {},
            l = Hn(e, i, n, u, r);
        if (l) {
            var s = _n(u, t, l.allDay, l.hasEnd, n);
            return {
                def: s,
                instance: Pn(s.defId, l.range, l.forcedStartTzo, l.forcedEndTzo)
            }
        }
        return null
    }

    function _n(e, t, n, r, i) {
        var o = {},
            a = Nn(e, i, o);
        a.defId = String(Yi++), a.sourceId = t, a.allDay = n, a.hasEnd = r;
        for (var s = 0, u = i.pluginSystem.hooks.eventDefParsers; s < u.length; s++) {
            var l = u[s],
                c = {};
            l(a, o, c), o = c
        }
        return a.extendedProps = ki(o, a.extendedProps || {}), Object.freeze(a.ui.classNames), Object.freeze(a.extendedProps), a
    }

    function Pn(e, t, n, r) {
        return {
            instanceId: String(Yi++),
            defId: e,
            range: t,
            forcedStartTzo: null == n ? null : n,
            forcedEndTzo: null == r ? null : r
        }
    }

    function Hn(e, t, n, r, i) {
        var o, a, s = xn(e, r),
            u = s.allDay,
            l = null,
            c = !1,
            d = null;
        if (o = n.dateEnv.createMarkerMeta(s.start)) l = o.marker;
        else if (!i) return null;
        return null != s.end && (a = n.dateEnv.createMarkerMeta(s.end)), null == u && (u = null != t ? t : (!o || o.isTimeUnspecified) && (!a || a.isTimeUnspecified)), u && l && (l = X(l)), a && (d = a.marker, u && (d = X(d)), l && d <= l && (d = null)), d ? c = !0 : i || (c = n.opt("forceEventDuration") || !1, d = n.dateEnv.add(l, u ? n.defaultAllDayEventDuration : n.defaultTimedEventDuration)), {
            allDay: u,
            hasEnd: c,
            range: {
                start: l,
                end: d
            },
            forcedStartTzo: o ? o.forcedTzo : null,
            forcedEndTzo: a ? a.forcedTzo : null
        }
    }

    function xn(e, t) {
        var n = Ge(e, ji, {}, t);
        return n.start = null !== n.start ? n.start : n.date, delete n.date, n
    }

    function Nn(e, t, n) {
        var r = {},
            i = Ge(e, Zi, {}, r),
            o = In(r, t, n);
        return i.publicId = i.id, delete i.id, i.ui = o, i
    }

    function zn(e, t) {
        var n = null;
        if (e) {
            n = t.state.eventSources[e].allDayDefault
        }
        return null == n && (n = t.opt("allDayDefault")), n
    }

    function Un(e, t) {
        return ut(Ln(e), "", t)
    }

    function Ln(e) {
        var t;
        return t = !0 === e ? [{}] : Array.isArray(e) ? e.filter(function (e) {
            return e.daysOfWeek
        }) : "object" == typeof e && e ? [e] : [], t = t.map(function (e) {
            return ki({}, qi, e)
        })
    }

    function An(e, t, n) {
        function r() {
            if (a) {
                for (var e = 0, n = s; e < n.length; e++) {
                    n[e].unrender()
                }
                t && t.apply(o, a), a = null
            }
        }

        function i() {
            a && Mt(a, arguments) || (r(), o = this, a = arguments, e.apply(this, arguments))
        }

        void 0 === n && (n = []);
        var o, a, s = [];
        i.dependents = s, i.unrender = r;
        for (var u = 0, l = n; u < l.length; u++) {
            l[u].dependents.push(i)
        }
        return i
    }

    function Vn(e, t, n) {
        return void 0 === n && (n = 1), e === t || (Array.isArray(e) && Array.isArray(t) ? Bn(e, t, n) : !("object" != typeof e || !e || "object" != typeof t || !t) && Fn(e, t, n))
    }

    function Bn(e, t, n) {
        if (void 0 === n && (n = 1), e === t) return !0;
        if (n > 0) {
            if (e.length !== t.length) return !1;
            for (var r = 0; r < e.length; r++)
                if (!Vn(e[r], t[r], n - 1)) return !1;
            return !0
        }
        return !1
    }

    function Fn(e, t, n) {
        if (void 0 === n && (n = 1), e === t) return !0;
        if (n > 0) {
            for (var r in e)
                if (!(r in t)) return !1;
            for (var r in t) {
                if (!(r in e)) return !1;
                if (!Vn(e[r], t[r], n - 1)) return !1
            }
            return !0
        }
        return !1
    }

    function Wn(e, t, n) {
        void 0 === n && (n = 1);
        var r = {};
        for (var i in t) i in e && Vn(e[i], t[i], n - 1) || (r[i] = t[i]);
        return r
    }

    function Zn(e, t) {
        for (var n in e)
            if (!(n in t)) return !0;
        return !1
    }

    function jn(e, t, n) {
        var r = [];
        e && r.push(e), t && r.push(t);
        var i = {
            "": Mn(r)
        };
        return n && ki(i, n), i
    }

    function Yn(e, t, n, r) {
        var i, o, a, s, u = e.dateEnv;
        return t instanceof Date ? i = t : (i = t.date, o = t.type, a = t.forceOff), s = {
            date: u.formatIso(i, {
                omitTime: !0
            }),
            type: o || "day"
        }, "string" == typeof n && (r = n, n = null), n = n ? " " + wn(n) : "", r = r || "", !a && e.opt("navLinks") ? "<a" + n + ' data-goto="' + bn(JSON.stringify(s)) + '">' + r + "</a>" : "<span" + n + ">" + r + "</span>"
    }

    function qn(e) {
        return e.opt("allDayHtml") || bn(e.opt("allDayText"))
    }

    function Gn(e, t, n, r) {
        var i, o, a = n.calendar,
            s = n.view,
            u = n.theme,
            l = n.dateEnv,
            c = [];
        return Rt(t.activeRange, e) ? (c.push("fc-" + Ri[e.getUTCDay()]), s.opt("monthMode") && l.getMonth(e) !== l.getMonth(t.currentRange.start) && c.push("fc-other-month"), i = X(a.getNow()), o = A(i, 1), e < i ? c.push("fc-past") : e >= o ? c.push("fc-future") : (c.push("fc-today"), !0 !== r && c.push(u.getClass("today")))) : c.push("fc-disabled-day"), c
    }

    function Xn(e, t, n) {
        var r = !1,
            i = function () {
                r || (r = !0, t.apply(this, arguments))
            },
            o = function () {
                r || (r = !0, n && n.apply(this, arguments))
            },
            a = e(i, o);
        a && "function" == typeof a.then && a.then(i, o)
    }

    function Jn(e, t, n) {
        (e[t] || (e[t] = [])).push(n)
    }

    function Kn(e, t, n) {
        n ? e[t] && (e[t] = e[t].filter(function (e) {
            return e !== n
        })) : delete e[t]
    }

    function Qn(e, t, n) {
        var r = {},
            i = !1;
        for (var o in t) o in e && (e[o] === t[o] || n[o] && n[o](e[o], t[o])) ? r[o] = e[o] : (r[o] = t[o], i = !0);
        for (var o in e)
            if (!(o in t)) {
                i = !0;
                break
            }
        return {
            anyChanges: i,
            comboProps: r
        }
    }

    function $n(e) {
        return {
            id: String(so++),
            deps: e.deps || [],
            reducers: e.reducers || [],
            eventDefParsers: e.eventDefParsers || [],
            eventDragMutationMassagers: e.eventDragMutationMassagers || [],
            eventDefMutationAppliers: e.eventDefMutationAppliers || [],
            dateSelectionTransformers: e.dateSelectionTransformers || [],
            datePointTransforms: e.datePointTransforms || [],
            dateSpanTransforms: e.dateSpanTransforms || [],
            views: e.views || {},
            viewPropsTransformers: e.viewPropsTransformers || [],
            isPropsValid: e.isPropsValid || null,
            externalDefTransforms: e.externalDefTransforms || [],
            eventResizeJoinTransforms: e.eventResizeJoinTransforms || [],
            viewContainerModifiers: e.viewContainerModifiers || [],
            eventDropTransformers: e.eventDropTransformers || [],
            componentInteractions: e.componentInteractions || [],
            calendarInteractions: e.calendarInteractions || [],
            themeClasses: e.themeClasses || {},
            eventSourceDefs: e.eventSourceDefs || [],
            cmdFormatter: e.cmdFormatter,
            recurringTypes: e.recurringTypes || [],
            namedTimeZonedImpl: e.namedTimeZonedImpl,
            defaultView: e.defaultView || "",
            elementDraggingImpl: e.elementDraggingImpl,
            optionChangeHandlers: e.optionChangeHandlers || {}
        }
    }

    function er(e, t) {
        return {
            reducers: e.reducers.concat(t.reducers),
            eventDefParsers: e.eventDefParsers.concat(t.eventDefParsers),
            eventDragMutationMassagers: e.eventDragMutationMassagers.concat(t.eventDragMutationMassagers),
            eventDefMutationAppliers: e.eventDefMutationAppliers.concat(t.eventDefMutationAppliers),
            dateSelectionTransformers: e.dateSelectionTransformers.concat(t.dateSelectionTransformers),
            datePointTransforms: e.datePointTransforms.concat(t.datePointTransforms),
            dateSpanTransforms: e.dateSpanTransforms.concat(t.dateSpanTransforms),
            views: ki({}, e.views, t.views),
            viewPropsTransformers: e.viewPropsTransformers.concat(t.viewPropsTransformers),
            isPropsValid: t.isPropsValid || e.isPropsValid,
            externalDefTransforms: e.externalDefTransforms.concat(t.externalDefTransforms),
            eventResizeJoinTransforms: e.eventResizeJoinTransforms.concat(t.eventResizeJoinTransforms),
            viewContainerModifiers: e.viewContainerModifiers.concat(t.viewContainerModifiers),
            eventDropTransformers: e.eventDropTransformers.concat(t.eventDropTransformers),
            calendarInteractions: e.calendarInteractions.concat(t.calendarInteractions),
            componentInteractions: e.componentInteractions.concat(t.componentInteractions),
            themeClasses: ki({}, e.themeClasses, t.themeClasses),
            eventSourceDefs: e.eventSourceDefs.concat(t.eventSourceDefs),
            cmdFormatter: t.cmdFormatter || e.cmdFormatter,
            recurringTypes: e.recurringTypes.concat(t.recurringTypes),
            namedTimeZonedImpl: t.namedTimeZonedImpl || e.namedTimeZonedImpl,
            defaultView: e.defaultView || t.defaultView,
            elementDraggingImpl: e.elementDraggingImpl || t.elementDraggingImpl,
            optionChangeHandlers: ki({}, e.optionChangeHandlers, t.optionChangeHandlers)
        }
    }

    function tr(e, t, n, r, i) {
        e = e.toUpperCase();
        var o = null;
        "GET" === e ? t = nr(t, n) : o = rr(n);
        var a = new XMLHttpRequest;
        a.open(e, t, !0), "GET" !== e && a.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"), a.onload = function () {
            if (a.status >= 200 && a.status < 400) try {
                var e = JSON.parse(a.responseText);
                r(e, a)
            } catch (e) {
                i("Failure parsing JSON", a)
            } else i("Request failed", a)
        }, a.onerror = function () {
            i("Request failed", a)
        }, a.send(o)
    }

    function nr(e, t) {
        return e + (-1 === e.indexOf("?") ? "?" : "&") + rr(t)
    }

    function rr(e) {
        var t = [];
        for (var n in e) t.push(encodeURIComponent(n) + "=" + encodeURIComponent(e[n]));
        return t.join("&")
    }

    function ir(e, t, n) {
        var r, i, o, a, s = n.dateEnv,
            u = {};
        return r = e.startParam, null == r && (r = n.opt("startParam")), i = e.endParam, null == i && (i = n.opt("endParam")), o = e.timeZoneParam, null == o && (o = n.opt("timeZoneParam")), a = "function" == typeof e.extraParams ? e.extraParams() : e.extraParams || {}, ki(u, a), u[r] = s.formatIso(t.start), u[i] = s.formatIso(t.end), "local" !== s.timeZone && (u[o] = s.timeZone), u
    }

    function or(e, t, n, r) {
        for (var i = e ? at(e) : null, o = X(n.start), a = n.end, s = []; o < a;) {
            var u = void 0;
            i && !i[o.getUTCDay()] || (u = t ? r.add(o, t) : o, s.push(u)), o = A(o, 1)
        }
        return s
    }

    function ar(e, t) {
        for (var n = st(t.state.eventSources), r = [], i = 0, o = e; i < o.length; i++) {
            for (var a = o[i], s = !1, u = 0; u < n.length; u++)
                if (Vn(n[u]._raw, a, 2)) {
                    n.splice(u, 1), s = !0;
                    break
                }
            s || r.push(a)
        }
        for (var l = 0, c = n; l < c.length; l++) {
            var d = c[l];
            t.dispatch({
                type: "REMOVE_EVENT_SOURCE",
                sourceId: d.sourceId
            })
        }
        for (var f = 0, p = r; f < p.length; f++) {
            var h = p[f];
            t.addEventSource(h)
        }
    }

    function sr(e, t) {
        t.addPluginInputs(e)
    }

    function ur(e) {
        return rt(e, bo)
    }

    function lr(e) {
        for (var t = [], n = 0, r = e; n < r.length; n++) {
            var i = r[n];
            if ("string" == typeof i) {
                var o = "FullCalendar" + Be(i);
                window[o] ? t.push(window[o].default) : console.warn("Plugin file not loaded for " + i)
            } else t.push(i)
        }
        return To.concat(t)
    }

    function cr(e) {
        for (var t = e.length > 0 ? e[0].code : "en", n = window.FullCalendarLocalesAll || [], r = window.FullCalendarLocales || {}, i = n.concat(st(r), e), o = {
            en: wo
        }, a = 0, s = i; a < s.length; a++) {
            var u = s[a];
            o[u.code] = u
        }
        return {
            map: o,
            defaultCode: t
        }
    }

    function dr(e, t) {
        return "object" != typeof e || Array.isArray(e) ? fr(e, t) : hr(e.code, [e.code], e)
    }

    function fr(e, t) {
        var n = [].concat(e || []);
        return hr(e, n, pr(n, t) || wo)
    }

    function pr(e, t) {
        for (var n = 0; n < e.length; n++)
            for (var r = e[n].toLocaleLowerCase().split("-"), i = r.length; i > 0; i--) {
                var o = r.slice(0, i).join("-");
                if (t[o]) return t[o]
            }
        return null
    }

    function hr(e, t, n) {
        var r = rt([wo, n], ["buttonText"]);
        delete r.code;
        var i = r.week;
        return delete r.week, {
            codeArg: e,
            codes: t,
            week: i,
            simpleNumberFormat: new Intl.NumberFormat(e),
            options: r
        }
    }

    function vr(e) {
        return new Io[e]
    }

    function gr(e) {
        var t = null,
            n = !1,
            r = Mo.exec(e);
        r && (n = !r[1], n ? e += "T00:00:00Z" : e = e.replace(ko, function (e, n, r, i, o) {
            return t = n ? 0 : (60 * parseInt(i, 10) + parseInt(o || 0, 10)) * ("-" === r ? -1 : 1), ""
        }) + "Z");
        var i = new Date(e);
        return ae(i) ? {
            marker: i,
            isTimeUnspecified: n,
            timeZoneOffset: t
        } : null
    }

    function yr(e, t) {
        return !t.pluginSystem.hooks.eventSourceDefs[e.sourceDefId].ignoreRange
    }

    function mr(e, t) {
        for (var n = t.pluginSystem.hooks.eventSourceDefs, r = n.length - 1; r >= 0; r--) {
            var i = n[r],
                o = i.parseMeta(e);
            if (o) {
                var a = Er("object" == typeof e ? e : {}, o, r, t);
                return a._raw = Xe(e), a
            }
        }
        return null
    }

    function Er(e, t, n, r) {
        var i = {},
            o = Ge(e, _o, {}, i),
            a = {},
            s = In(i, r, a);
        return o.isFetching = !1, o.latestFetchId = "", o.fetchRange = null, o.publicId = String(e.id || ""), o.sourceId = String(Po++), o.sourceDefId = n, o.meta = t, o.ui = s, o.extendedProps = a, o
    }

    function Sr(e, t, n, r) {
        switch (t.type) {
            case "ADD_EVENT_SOURCES":
                return Dr(e, t.sources, n ? n.activeRange : null, r);
            case "REMOVE_EVENT_SOURCE":
                return br(e, t.sourceId);
            case "PREV":
            case "NEXT":
            case "SET_DATE":
            case "SET_VIEW_TYPE":
                return n ? Tr(e, n.activeRange, r) : e;
            case "FETCH_EVENT_SOURCES":
            case "CHANGE_TIMEZONE":
                return Rr(e, t.sourceIds ? at(t.sourceIds) : Mr(e, r), n ? n.activeRange : null, r);
            case "RECEIVE_EVENTS":
            case "RECEIVE_EVENT_ERROR":
                return Cr(e, t.sourceId, t.fetchId, t.fetchRange);
            case "REMOVE_ALL_EVENT_SOURCES":
                return {};
            default:
                return e
        }
    }

    function Dr(e, t, n, r) {
        for (var i = {}, o = 0, a = t; o < a.length; o++) {
            var s = a[o];
            i[s.sourceId] = s
        }
        return n && (i = Tr(i, n, r)), ki({}, e, i)
    }

    function br(e, t) {
        return it(e, function (e) {
            return e.sourceId !== t
        })
    }

    function Tr(e, t, n) {
        return Rr(e, it(e, function (e) {
            return wr(e, t, n)
        }), t, n)
    }

    function wr(e, t, n) {
        return yr(e, n) ? !n.opt("lazyFetching") || !e.fetchRange || t.start < e.fetchRange.start || t.end > e.fetchRange.end : !e.latestFetchId
    }

    function Rr(e, t, n, r) {
        var i = {};
        for (var o in e) {
            var a = e[o];
            t[o] ? i[o] = Ir(a, n, r) : i[o] = a
        }
        return i
    }

    function Ir(e, t, n) {
        var r = n.pluginSystem.hooks.eventSourceDefs[e.sourceDefId],
            i = String(Ho++);
        return r.fetch({
            eventSource: e,
            calendar: n,
            range: t
        }, function (r) {
            var o, a, s = r.rawEvents,
                u = n.opt("eventSourceSuccess");
            e.success && (a = e.success(s, r.xhr)), u && (o = u(s, r.xhr)), s = a || o || s, n.dispatch({
                type: "RECEIVE_EVENTS",
                sourceId: e.sourceId,
                fetchId: i,
                fetchRange: t,
                rawEvents: s
            })
        }, function (r) {
            var o = n.opt("eventSourceFailure");
            console.warn(r.message, r), e.failure && e.failure(r), o && o(r), n.dispatch({
                type: "RECEIVE_EVENT_ERROR",
                sourceId: e.sourceId,
                fetchId: i,
                fetchRange: t,
                error: r
            })
        }), ki({}, e, {
            isFetching: !0,
            latestFetchId: i
        })
    }

    function Cr(e, t, n, r) {
        var i, o = e[t];
        return o && n === o.latestFetchId ? ki({}, e, (i = {}, i[t] = ki({}, o, {
            isFetching: !1,
            fetchRange: r
        }), i)) : e
    }

    function Mr(e, t) {
        return it(e, function (e) {
            return yr(e, t)
        })
    }

    function kr(e, t) {
        return bt(e.activeRange, t.activeRange) && bt(e.validRange, t.validRange) && fe(e.minTime, t.minTime) && fe(e.maxTime, t.maxTime)
    }

    function Or(e, t, n) {
        for (var r = _r(e.viewType, t), i = Pr(e.dateProfile, t, e.currentDate, r, n), o = Sr(e.eventSources, t, i, n), a = ki({}, e, {
            viewType: r,
            dateProfile: i,
            currentDate: Hr(e.currentDate, t, i),
            eventSources: o,
            eventStore: rn(e.eventStore, t, o, i, n),
            dateSelection: xr(e.dateSelection, t, n),
            eventSelection: Nr(e.eventSelection, t),
            eventDrag: zr(e.eventDrag, t, o, n),
            eventResize: Ur(e.eventResize, t, o, n),
            eventSourceLoadingLevel: Lr(o),
            loadingLevel: Lr(o)
        }), s = 0, u = n.pluginSystem.hooks.reducers; s < u.length; s++) {
            a = (0, u[s])(a, t, n)
        }
        return a
    }

    function _r(e, t) {
        switch (t.type) {
            case "SET_VIEW_TYPE":
                return t.viewType;
            default:
                return e
        }
    }

    function Pr(e, t, n, r, i) {
        var o;
        switch (t.type) {
            case "PREV":
                o = i.dateProfileGenerators[r].buildPrev(e, n);
                break;
            case "NEXT":
                o = i.dateProfileGenerators[r].buildNext(e, n);
                break;
            case "SET_DATE":
                e.activeRange && Rt(e.currentRange, t.dateMarker) || (o = i.dateProfileGenerators[r].build(t.dateMarker, void 0, !0));
                break;
            case "SET_VIEW_TYPE":
                var a = i.dateProfileGenerators[r];
                if (!a) throw new Error(r ? 'The FullCalendar view "' + r + '" does not exist. Make sure your plugins are loaded correctly.' : "No available FullCalendar view plugins.");
                o = a.build(t.dateMarker || n, void 0, !0)
        }
        return !o || !o.isValid || e && kr(e, o) ? e : o
    }

    function Hr(e, t, n) {
        switch (t.type) {
            case "PREV":
            case "NEXT":
                return Rt(n.currentRange, e) ? e : n.currentRange.start;
            case "SET_DATE":
            case "SET_VIEW_TYPE":
                var r = t.dateMarker || e;
                return n.activeRange && !Rt(n.activeRange, r) ? n.currentRange.start : r;
            default:
                return e
        }
    }

    function xr(e, t, n) {
        switch (t.type) {
            case "SELECT_DATES":
                return t.selection;
            case "UNSELECT_DATES":
                return null;
            default:
                return e
        }
    }

    function Nr(e, t) {
        switch (t.type) {
            case "SELECT_EVENT":
                return t.eventInstanceId;
            case "UNSELECT_EVENT":
                return "";
            default:
                return e
        }
    }

    function zr(e, t, n, r) {
        switch (t.type) {
            case "SET_EVENT_DRAG":
                var i = t.state;
                return {
                    affectedEvents: i.affectedEvents,
                    mutatedEvents: i.mutatedEvents,
                    isEvent: i.isEvent,
                    origSeg: i.origSeg
                };
            case "UNSET_EVENT_DRAG":
                return null;
            default:
                return e
        }
    }

    function Ur(e, t, n, r) {
        switch (t.type) {
            case "SET_EVENT_RESIZE":
                var i = t.state;
                return {
                    affectedEvents: i.affectedEvents,
                    mutatedEvents: i.mutatedEvents,
                    isEvent: i.isEvent,
                    origSeg: i.origSeg
                };
            case "UNSET_EVENT_RESIZE":
                return null;
            default:
                return e
        }
    }

    function Lr(e) {
        var t = 0;
        for (var n in e) e[n].isFetching && t++;
        return t
    }

    function Ar(e, t, n) {
        var r = Vr(e, t),
            i = r.range;
        if (!i.start) return null;
        if (!i.end) {
            if (null == n) return null;
            i.end = t.add(i.start, n)
        }
        return r
    }

    function Vr(e, t) {
        var n = {},
            r = Ge(e, No, {}, n),
            i = r.start ? t.createMarkerMeta(r.start) : null,
            o = r.end ? t.createMarkerMeta(r.end) : null,
            a = r.allDay;
        return null == a && (a = i && i.isTimeUnspecified && (!o || o.isTimeUnspecified)), n.range = {
            start: i ? i.marker : null,
            end: o ? o.marker : null
        }, n.allDay = a, n
    }

    function Br(e, t) {
        return bt(e.range, t.range) && e.allDay === t.allDay && Fr(e, t)
    }

    function Fr(e, t) {
        for (var n in t)
            if ("range" !== n && "allDay" !== n && e[n] !== t[n]) return !1;
        for (var n in e)
            if (!(n in t)) return !1;
        return !0
    }

    function Wr(e, t) {
        return {
            start: t.toDate(e.range.start),
            end: t.toDate(e.range.end),
            startStr: t.formatIso(e.range.start, {
                omitTime: e.allDay
            }),
            endStr: t.formatIso(e.range.end, {
                omitTime: e.allDay
            }),
            allDay: e.allDay
        }
    }

    function Zr(e, t) {
        return {
            date: t.toDate(e.range.start),
            dateStr: t.formatIso(e.range.start, {
                omitTime: e.allDay
            }),
            allDay: e.allDay
        }
    }

    function jr(e, t, n) {
        var r = _n({
            editable: !1
        }, "", e.allDay, !0, n);
        return {
            def: r,
            ui: Qt(r, t),
            instance: Pn(r.defId, e.range),
            range: e.range,
            isStart: !0,
            isEnd: !0
        }
    }

    function Yr(e, t) {
        var n, r = {};
        for (n in e) qr(n, r, e, t);
        for (n in t) qr(n, r, e, t);
        return r
    }

    function qr(e, t, n, r) {
        if (t[e]) return t[e];
        var i = Gr(e, t, n, r);
        return i && (t[e] = i), i
    }

    function Gr(e, t, n, r) {
        var i = n[e],
            o = r[e],
            a = function (e) {
                return i && null !== i[e] ? i[e] : o && null !== o[e] ? o[e] : null
            },
            s = a("class"),
            u = a("superType");
        !u && s && (u = Xr(s, r) || Xr(s, n));
        var l = u ? qr(u, t, n, r) : null;
        return !s && l && (s = l.class), s ? {
            type: e,
            class: s,
            defaults: ki({}, l ? l.defaults : {}, i ? i.options : {}),
            overrides: ki({}, l ? l.overrides : {}, o ? o.options : {})
        } : null
    }

    function Xr(e, t) {
        var n = Object.getPrototypeOf(e.prototype);
        for (var r in t) {
            var i = t[r];
            if (i.class && i.class.prototype === n) return r
        }
        return ""
    }

    function Jr(e) {
        return ot(e, Kr)
    }

    function Kr(e) {
        "function" == typeof e && (e = {
            class: e
        });
        var t = {},
            n = Ge(e, zo, {}, t);
        return {
            superType: n.type,
            class: n.class,
            options: t
        }
    }

    function Qr(e, t) {
        var n = Jr(e),
            r = Jr(t.overrides.views);
        return ot(Yr(n, r), function (e) {
            return $r(e, r, t)
        })
    }

    function $r(e, t, n) {
        var r = e.overrides.duration || e.defaults.duration || n.dynamicOverrides.duration || n.overrides.duration,
            i = null,
            o = "",
            a = "",
            s = {};
        if (r && (i = ue(r))) {
            var u = we(i, !de(r));
            o = u.unit, 1 === u.value && (a = o, s = t[o] ? t[o].options : {})
        }
        var l = function (t) {
            var n = t.buttonText || {},
                r = e.defaults.buttonTextKey;
            return null != r && null != n[r] ? n[r] : null != n[e.type] ? n[e.type] : null != n[a] ? n[a] : void 0
        };
        return {
            type: e.type,
            class: e.class,
            duration: i,
            durationUnit: o,
            singleUnit: a,
            options: ki({}, So, e.defaults, n.dirDefaults, n.localeDefaults, n.overrides, s, e.overrides, n.dynamicOverrides),
            buttonTextOverride: l(n.dynamicOverrides) || l(n.overrides) || e.overrides.buttonText,
            buttonTextDefault: l(n.localeDefaults) || l(n.dirDefaults) || e.defaults.buttonText || l(So) || e.type
        }
    }

    function ei(e, t) {
        var n;
        return n = /^(year|month)$/.test(e.currentRangeUnit) ? e.currentRange : e.activeRange, this.dateEnv.formatRange(n.start, n.end, Vt(t.titleFormat || ti(e), t.titleRangeSeparator), {
            isEndExclusive: e.isRangeAllDay
        })
    }

    function ti(e) {
        var t = e.currentRangeUnit;
        if ("year" === t) return {
            year: "numeric"
        };
        if ("month" === t) return {
            year: "numeric",
            month: "long"
        };
        var n = G(e.currentRange.start, e.currentRange.end);
        return null !== n && n > 1 ? {
            year: "numeric",
            month: "short",
            day: "numeric"
        } : {
            year: "numeric",
            month: "long",
            day: "numeric"
        }
    }

    function ni(e) {
        return e.map(function (e) {
            return new e
        })
    }

    function ri(e, t) {
        return {
            component: e,
            el: t.el,
            useEventCenter: null == t.useEventCenter || t.useEventCenter
        }
    }

    function ii(e) {
        var t;
        return t = {}, t[e.component.uid] = e, t
    }

    function oi(e, t, n, r, i, o, a) {
        return new Oo({
            calendarSystem: "gregory",
            timeZone: t,
            namedTimeZoneImpl: n,
            locale: e,
            weekNumberCalculation: i,
            firstDay: r,
            weekLabel: o,
            cmdFormatter: a
        })
    }

    function ai(e) {
        return new (this.pluginSystem.hooks.themeClasses[e.themeSystem] || Wo)(e)
    }

    function si(e) {
        var t = this.tryRerender.bind(this);
        return null != e && (t = qe(t, e)), t
    }

    function ui(e) {
        return ot(e, function (e) {
            return e.ui
        })
    }

    function li(e, t, n) {
        var r = {
            "": t
        };
        for (var i in e) {
            var o = e[i];
            o.sourceId && n[o.sourceId] && (r[i] = n[o.sourceId])
        }
        return r
    }

    function ci(e) {
        var t = e.eventRange.def,
            n = e.eventRange.instance.range,
            r = n.start ? n.start.valueOf() : 0,
            i = n.end ? n.end.valueOf() : 0;
        return ki({}, t.extendedProps, t, {
            id: t.publicId,
            start: r,
            end: i,
            duration: i - r,
            allDay: Number(t.allDay),
            _seg: e
        })
    }

    function di(e, t) {
        void 0 === t && (t = {});
        var n = pi(t),
            r = Vt(t),
            i = n.createMarkerMeta(e);
        return i ? n.format(i.marker, r, {
            forcedTzo: i.forcedTzo
        }) : ""
    }

    function fi(e, t, n) {
        var r = pi("object" == typeof n && n ? n : {}),
            i = Vt(n, So.defaultRangeSeparator),
            o = r.createMarkerMeta(e),
            a = r.createMarkerMeta(t);
        return o && a ? r.formatRange(o.marker, a.marker, i, {
            forcedStartTzo: o.forcedTzo,
            forcedEndTzo: a.forcedTzo,
            isEndExclusive: n.isEndExclusive
        }) : ""
    }

    function pi(e) {
        var t = dr(e.locale || "en", cr([]).map);
        return e = ki({
            timeZone: So.timeZone,
            calendarSystem: "gregory"
        }, e, {
            locale: t
        }), new Oo(e)
    }

    function hi(e) {
        var t = {},
            n = Ge(e, Jo, Ko, t);
        return n.leftoverProps = t, n
    }

    function vi(e, t) {
        return !e || t > 10 ? {
            weekday: "short"
        } : t > 1 ? {
            weekday: "short",
            month: "numeric",
            day: "numeric",
            omitCommas: !0
        } : {
            weekday: "long"
        }
    }

    function gi(e, t, n, r, i, o, a, s) {
        var u, l = o.view,
            c = o.dateEnv,
            d = o.theme,
            f = o.options,
            p = Rt(t.activeRange, e),
            h = ["fc-day-header", d.getClass("widgetHeader")];
        return u = "function" == typeof f.columnHeaderHtml ? f.columnHeaderHtml(c.toDate(e)) : bn("function" == typeof f.columnHeaderText ? f.columnHeaderText(c.toDate(e)) : c.format(e, i)), n ? h = h.concat(Gn(e, t, o, !0)) : h.push("fc-" + Ri[e.getUTCDay()]), '<th class="' + h.join(" ") + '"' + (p && n ? ' data-date="' + c.formatIso(e, {
            omitTime: !0
        }) + '"' : "") + (a > 1 ? ' colspan="' + a + '"' : "") + (s ? " " + s : "") + ">" + (p ? Yn(l, {
            date: e,
            forceOff: !n || 1 === r
        }, u) : u) + "</th>"
    }

    function yi(e, t) {
        var n = e.activeRange;
        return t ? n : {
            start: V(n.start, e.minTime.milliseconds),
            end: V(n.end, e.maxTime.milliseconds - 864e5)
        }
    }

    var mi = {
            className: !0,
            colSpan: !0,
            rowSpan: !0
        },
        Ei = {
            "<tr": "tbody",
            "<td": "tr"
        },
        Si = Element.prototype.matches || Element.prototype.matchesSelector || Element.prototype.msMatchesSelector,
        Di = Element.prototype.closest || function (e) {
            var t = this;
            if (!document.documentElement.contains(t)) return null;
            do {
                if (f(t, e)) return t;
                t = t.parentElement || t.parentNode
            } while (null !== t && 1 === t.nodeType);
            return null
        },
        bi = /(top|left|right|bottom|width|height)$/i,
        Ti = null,
        wi = ["webkitTransitionEnd", "otransitionend", "oTransitionEnd", "msTransitionEnd", "transitionend"],
        Ri = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"],
        Ii = ["years", "months", "days", "milliseconds"],
        Ci = /^(-?)(?:(\d+)\.)?(\d+):(\d\d)(?::(\d\d)(?:\.(\d\d\d))?)?/,
        Mi = function (e, t) {
            return (Mi = Object.setPrototypeOf || {
                    __proto__: []
                }
                instanceof Array && function (e, t) {
                    e.__proto__ = t
                } || function (e, t) {
                    for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n])
                })(e, t)
        },
        ki = function () {
            return ki = Object.assign || function (e) {
                for (var t, n = 1, r = arguments.length; n < r; n++) {
                    t = arguments[n];
                    for (var i in t) Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i])
                }
                return e
            }, ki.apply(this, arguments)
        },
        Oi = {
            week: 3,
            separator: 0,
            omitZeroMinute: 0,
            meridiem: 0,
            omitCommas: 0
        },
        _i = {
            timeZoneName: 7,
            era: 6,
            year: 5,
            month: 4,
            day: 2,
            weekday: 2,
            hour: 1,
            minute: 1,
            second: 1
        },
        Pi = /\s*([ap])\.?m\.?/i,
        Hi = /,/g,
        xi = /\s+/g,
        Ni = /\u200e/g,
        zi = /UTC|GMT/,
        Ui = function () {
            function e(e) {
                var t = {},
                    n = {},
                    r = 0;
                for (var i in e) i in Oi ? (n[i] = e[i], r = Math.max(Oi[i], r)) : (t[i] = e[i], i in _i && (r = Math.max(_i[i], r)));
                this.standardDateProps = t, this.extendedSettings = n, this.severity = r, this.buildFormattingFunc = kt(_t)
            }

            return e.prototype.format = function (e, t) {
                return this.buildFormattingFunc(this.standardDateProps, this.extendedSettings, t)(e)
            }, e.prototype.formatRange = function (e, t, n) {
                var r = this,
                    i = r.standardDateProps,
                    o = r.extendedSettings,
                    a = Ut(e.marker, t.marker, n.calendarSystem);
                if (!a) return this.format(e, n);
                var s = a;
                !(s > 1) || "numeric" !== i.year && "2-digit" !== i.year || "numeric" !== i.month && "2-digit" !== i.month || "numeric" !== i.day && "2-digit" !== i.day || (s = 1);
                var u = this.format(e, n),
                    l = this.format(t, n);
                if (u === l) return u;
                var c = Lt(i, s),
                    d = _t(c, o, n),
                    f = d(e),
                    p = d(t),
                    h = At(u, f, l, p),
                    v = o.separator || "";
                return h ? h.before + f + v + p + h.after : u + v + l
            }, e.prototype.getLargestUnit = function () {
                switch (this.severity) {
                    case 7:
                    case 6:
                    case 5:
                        return "year";
                    case 4:
                        return "month";
                    case 3:
                        return "week";
                    default:
                        return "day"
                }
            }, e
        }(),
        Li = function () {
            function e(e, t) {
                this.cmdStr = e, this.separator = t
            }

            return e.prototype.format = function (e, t) {
                return t.cmdFormatter(this.cmdStr, Zt(e, null, t, this.separator))
            }, e.prototype.formatRange = function (e, t, n) {
                return n.cmdFormatter(this.cmdStr, Zt(e, t, n, this.separator))
            }, e
        }(),
        Ai = function () {
            function e(e) {
                this.func = e
            }

            return e.prototype.format = function (e, t) {
                return this.func(Zt(e, null, t))
            }, e.prototype.formatRange = function (e, t, n) {
                return this.func(Zt(e, t, n))
            }, e
        }(),
        Vi = function () {
            function e(e, t) {
                this.calendar = e, this.internalEventSource = t
            }

            return e.prototype.remove = function () {
                this.calendar.dispatch({
                    type: "REMOVE_EVENT_SOURCE",
                    sourceId: this.internalEventSource.sourceId
                })
            }, e.prototype.refetch = function () {
                this.calendar.dispatch({
                    type: "FETCH_EVENT_SOURCES",
                    sourceIds: [this.internalEventSource.sourceId]
                })
            }, Object.defineProperty(e.prototype, "id", {
                get: function () {
                    return this.internalEventSource.publicId
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "url", {
                get: function () {
                    return this.internalEventSource.meta.url
                },
                enumerable: !0,
                configurable: !0
            }), e
        }(),
        Bi = function () {
            function e(e, t, n) {
                this._calendar = e, this._def = t, this._instance = n || null
            }

            return e.prototype.setProp = function (e, t) {
                var n, r;
                if (e in ji) ;
                else if (e in Zi) "function" == typeof Zi[e] && (t = Zi[e](t)), this.mutate({
                    standardProps: (n = {}, n[e] = t, n)
                });
                else if (e in Fi) {
                    var i = void 0;
                    "function" == typeof Fi[e] && (t = Fi[e](t)), "color" === e ? i = {
                        backgroundColor: t,
                        borderColor: t
                    } : "editable" === e ? i = {
                        startEditable: t,
                        durationEditable: t
                    } : (r = {}, r[e] = t, i = r), this.mutate({
                        standardProps: {
                            ui: i
                        }
                    })
                }
            }, e.prototype.setExtendedProp = function (e, t) {
                var n;
                this.mutate({
                    extendedProps: (n = {}, n[e] = t, n)
                })
            }, e.prototype.setStart = function (e, t) {
                void 0 === t && (t = {});
                var n = this._calendar.dateEnv,
                    r = n.createMarker(e);
                if (r && this._instance) {
                    var i = this._instance.range,
                        o = $e(i.start, r, n, t.granularity),
                        a = null;
                    if (t.maintainDuration) {
                        a = ve($e(i.start, i.end, n, t.granularity), $e(r, i.end, n, t.granularity))
                    }
                    this.mutate({
                        startDelta: o,
                        endDelta: a
                    })
                }
            }, e.prototype.setEnd = function (e, t) {
                void 0 === t && (t = {});
                var n, r = this._calendar.dateEnv;
                if ((null == e || (n = r.createMarker(e))) && this._instance)
                    if (n) {
                        var i = $e(this._instance.range.end, n, r, t.granularity);
                        this.mutate({
                            endDelta: i
                        })
                    } else this.mutate({
                        standardProps: {
                            hasEnd: !1
                        }
                    })
            }, e.prototype.setDates = function (e, t, n) {
                void 0 === n && (n = {});
                var r, i = this._calendar.dateEnv,
                    o = {
                        allDay: n.allDay
                    },
                    a = i.createMarker(e);
                if (a && (null == t || (r = i.createMarker(t))) && this._instance) {
                    var s = this._instance.range;
                    !0 === n.allDay && (s = Je(s));
                    var u = $e(s.start, a, i, n.granularity);
                    if (r) {
                        var l = $e(s.end, r, i, n.granularity);
                        this.mutate({
                            startDelta: u,
                            endDelta: l,
                            standardProps: o
                        })
                    } else o.hasEnd = !1, this.mutate({
                        startDelta: u,
                        standardProps: o
                    })
                }
            }, e.prototype.moveStart = function (e) {
                var t = ue(e);
                t && this.mutate({
                    startDelta: t
                })
            }, e.prototype.moveEnd = function (e) {
                var t = ue(e);
                t && this.mutate({
                    endDelta: t
                })
            }, e.prototype.moveDates = function (e) {
                var t = ue(e);
                t && this.mutate({
                    startDelta: t,
                    endDelta: t
                })
            }, e.prototype.setAllDay = function (e, t) {
                void 0 === t && (t = {});
                var n = {
                        allDay: e
                    },
                    r = t.maintainDuration;
                null == r && (r = this._calendar.opt("allDayMaintainDuration")), this._def.allDay !== e && (n.hasEnd = r), this.mutate({
                    standardProps: n
                })
            }, e.prototype.formatRange = function (e) {
                var t = this._calendar.dateEnv,
                    n = this._instance,
                    r = Vt(e, this._calendar.opt("defaultRangeSeparator"));
                return this._def.hasEnd ? t.formatRange(n.range.start, n.range.end, r, {
                    forcedStartTzo: n.forcedStartTzo,
                    forcedEndTzo: n.forcedEndTzo
                }) : t.format(n.range.start, r, {
                    forcedTzo: n.forcedStartTzo
                })
            }, e.prototype.mutate = function (e) {
                var t = this._def,
                    n = this._instance;
                if (n) {
                    this._calendar.dispatch({
                        type: "MUTATE_EVENTS",
                        instanceId: n.instanceId,
                        mutation: e,
                        fromApi: !0
                    });
                    var r = this._calendar.state.eventStore;
                    this._def = r.defs[t.defId], this._instance = r.instances[n.instanceId]
                }
            }, e.prototype.remove = function () {
                this._calendar.dispatch({
                    type: "REMOVE_EVENT_DEF",
                    defId: this._def.defId
                })
            }, Object.defineProperty(e.prototype, "source", {
                get: function () {
                    var e = this._def.sourceId;
                    return e ? new Vi(this._calendar, this._calendar.state.eventSources[e]) : null
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "start", {
                get: function () {
                    return this._instance ? this._calendar.dateEnv.toDate(this._instance.range.start) : null
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "end", {
                get: function () {
                    return this._instance && this._def.hasEnd ? this._calendar.dateEnv.toDate(this._instance.range.end) : null
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "id", {
                get: function () {
                    return this._def.publicId
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "groupId", {
                get: function () {
                    return this._def.groupId
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "allDay", {
                get: function () {
                    return this._def.allDay
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "title", {
                get: function () {
                    return this._def.title
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "url", {
                get: function () {
                    return this._def.url
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "rendering", {
                get: function () {
                    return this._def.rendering
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "startEditable", {
                get: function () {
                    return this._def.ui.startEditable
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "durationEditable", {
                get: function () {
                    return this._def.ui.durationEditable
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "constraint", {
                get: function () {
                    return this._def.ui.constraints[0] || null
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "overlap", {
                get: function () {
                    return this._def.ui.overlap
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "allow", {
                get: function () {
                    return this._def.ui.allows[0] || null
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "backgroundColor", {
                get: function () {
                    return this._def.ui.backgroundColor
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "borderColor", {
                get: function () {
                    return this._def.ui.borderColor
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "textColor", {
                get: function () {
                    return this._def.ui.textColor
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "classNames", {
                get: function () {
                    return this._def.ui.classNames
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(e.prototype, "extendedProps", {
                get: function () {
                    return this._def.extendedProps
                },
                enumerable: !0,
                configurable: !0
            }), e
        }(),
        Fi = {
            editable: Boolean,
            startEditable: Boolean,
            durationEditable: Boolean,
            constraint: null,
            overlap: null,
            allow: null,
            className: Rn,
            classNames: Rn,
            color: String,
            backgroundColor: String,
            borderColor: String,
            textColor: String
        },
        Wi = {
            startEditable: null,
            durationEditable: null,
            constraints: [],
            overlap: null,
            allows: [],
            backgroundColor: "",
            borderColor: "",
            textColor: "",
            classNames: []
        },
        Zi = {
            id: String,
            groupId: String,
            title: String,
            url: String,
            rendering: String,
            extendedProps: null
        },
        ji = {
            start: null,
            date: null,
            end: null,
            allDay: null
        },
        Yi = 0,
        qi = {
            startTime: "09:00",
            endTime: "17:00",
            daysOfWeek: [1, 2, 3, 4, 5],
            rendering: "inverse-background",
            classNames: "fc-nonbusiness",
            groupId: "_businessHours"
        },
        Gi = vt(),
        Xi = function () {
            function e() {
                this.getKeysForEventDefs = kt(this._getKeysForEventDefs), this.splitDateSelection = kt(this._splitDateSpan), this.splitEventStore = kt(this._splitEventStore), this.splitIndividualUi = kt(this._splitIndividualUi), this.splitEventDrag = kt(this._splitInteraction), this.splitEventResize = kt(this._splitInteraction), this.eventUiBuilders = {}
            }

            return e.prototype.splitProps = function (e) {
                var t = this,
                    n = this.getKeyInfo(e),
                    r = this.getKeysForEventDefs(e.eventStore),
                    i = this.splitDateSelection(e.dateSelection),
                    o = this.splitIndividualUi(e.eventUiBases, r),
                    a = this.splitEventStore(e.eventStore, r),
                    s = this.splitEventDrag(e.eventDrag),
                    u = this.splitEventResize(e.eventResize),
                    l = {};
                this.eventUiBuilders = ot(n, function (e, n) {
                    return t.eventUiBuilders[n] || kt(jn)
                });
                for (var c in n) {
                    var d = n[c],
                        f = a[c] || Gi,
                        p = this.eventUiBuilders[c];
                    l[c] = {
                        businessHours: d.businessHours || e.businessHours,
                        dateSelection: i[c] || null,
                        eventStore: f,
                        eventUiBases: p(e.eventUiBases[""], d.ui, o[c]),
                        eventSelection: f.instances[e.eventSelection] ? e.eventSelection : "",
                        eventDrag: s[c] || null,
                        eventResize: u[c] || null
                    }
                }
                return l
            }, e.prototype._splitDateSpan = function (e) {
                var t = {};
                if (e)
                    for (var n = this.getKeysForDateSpan(e), r = 0, i = n; r < i.length; r++) {
                        var o = i[r];
                        t[o] = e
                    }
                return t
            }, e.prototype._getKeysForEventDefs = function (e) {
                var t = this;
                return ot(e.defs, function (e) {
                    return t.getKeysForEventDef(e)
                })
            }, e.prototype._splitEventStore = function (e, t) {
                var n = e.defs,
                    r = e.instances,
                    i = {};
                for (var o in n)
                    for (var a = 0, s = t[o]; a < s.length; a++) {
                        var u = s[a];
                        i[u] || (i[u] = vt()), i[u].defs[o] = n[o]
                    }
                for (var l in r)
                    for (var c = r[l], d = 0, f = t[c.defId]; d < f.length; d++) {
                        var u = f[d];
                        i[u] && (i[u].instances[l] = c)
                    }
                return i
            }, e.prototype._splitIndividualUi = function (e, t) {
                var n = {};
                for (var r in e)
                    if (r)
                        for (var i = 0, o = t[r]; i < o.length; i++) {
                            var a = o[i];
                            n[a] || (n[a] = {}), n[a][r] = e[r]
                        }
                return n
            }, e.prototype._splitInteraction = function (e) {
                var t = {};
                if (e) {
                    var n = this._splitEventStore(e.affectedEvents, this._getKeysForEventDefs(e.affectedEvents)),
                        r = this._getKeysForEventDefs(e.mutatedEvents),
                        i = this._splitEventStore(e.mutatedEvents, r),
                        o = function (r) {
                            t[r] || (t[r] = {
                                affectedEvents: n[r] || Gi,
                                mutatedEvents: i[r] || Gi,
                                isEvent: e.isEvent,
                                origSeg: e.origSeg
                            })
                        };
                    for (var a in n) o(a);
                    for (var a in i) o(a)
                }
                return t
            }, e
        }(),
        Ji = function () {
            function e() {
            }

            return e.mixInto = function (e) {
                this.mixIntoObj(e.prototype)
            }, e.mixIntoObj = function (e) {
                var t = this;
                Object.getOwnPropertyNames(this.prototype).forEach(function (n) {
                    e[n] || (e[n] = t.prototype[n])
                })
            }, e.mixOver = function (e) {
                var t = this;
                Object.getOwnPropertyNames(this.prototype).forEach(function (n) {
                    e.prototype[n] = t.prototype[n]
                })
            }, e
        }(),
        Ki = function (e) {
            function t() {
                return null !== e && e.apply(this, arguments) || this
            }

            return et(t, e), t.prototype.on = function (e, t) {
                return Jn(this._handlers || (this._handlers = {}), e, t), this
            }, t.prototype.one = function (e, t) {
                return Jn(this._oneHandlers || (this._oneHandlers = {}), e, t), this
            }, t.prototype.off = function (e, t) {
                return this._handlers && Kn(this._handlers, e, t), this._oneHandlers && Kn(this._oneHandlers, e, t), this
            }, t.prototype.trigger = function (e) {
                for (var t = [], n = 1; n < arguments.length; n++) t[n - 1] = arguments[n];
                return this.triggerWith(e, this, t), this
            }, t.prototype.triggerWith = function (e, t, n) {
                return this._handlers && je(this._handlers[e], t, n), this._oneHandlers && (je(this._oneHandlers[e], t, n), delete this._oneHandlers[e]), this
            }, t.prototype.hasHandlers = function (e) {
                return this._handlers && this._handlers[e] && this._handlers[e].length || this._oneHandlers && this._oneHandlers[e] && this._oneHandlers[e].length
            }, t
        }(Ji),
        Qi = function () {
            function e(e, t, n, r) {
                this.originEl = e, this.els = t, this.isHorizontal = n, this.isVertical = r
            }

            return e.prototype.build = function () {
                var e = this.originEl,
                    t = this.originClientRect = e.getBoundingClientRect();
                this.isHorizontal && this.buildElHorizontals(t.left), this.isVertical && this.buildElVerticals(t.top)
            }, e.prototype.buildElHorizontals = function (e) {
                for (var t = [], n = [], r = 0, i = this.els; r < i.length; r++) {
                    var o = i[r],
                        a = o.getBoundingClientRect();
                    t.push(a.left - e), n.push(a.right - e)
                }
                this.lefts = t, this.rights = n
            }, e.prototype.buildElVerticals = function (e) {
                for (var t = [], n = [], r = 0, i = this.els; r < i.length; r++) {
                    var o = i[r],
                        a = o.getBoundingClientRect();
                    t.push(a.top - e), n.push(a.bottom - e)
                }
                this.tops = t, this.bottoms = n
            }, e.prototype.leftToIndex = function (e) {
                var t, n = this.lefts,
                    r = this.rights,
                    i = n.length;
                for (t = 0; t < i; t++)
                    if (e >= n[t] && e < r[t]) return t
            }, e.prototype.topToIndex = function (e) {
                var t, n = this.tops,
                    r = this.bottoms,
                    i = n.length;
                for (t = 0; t < i; t++)
                    if (e >= n[t] && e < r[t]) return t
            }, e.prototype.getWidth = function (e) {
                return this.rights[e] - this.lefts[e]
            }, e.prototype.getHeight = function (e) {
                return this.bottoms[e] - this.tops[e]
            }, e
        }(),
        $i = function () {
            function e() {
            }

            return e.prototype.getMaxScrollTop = function () {
                return this.getScrollHeight() - this.getClientHeight()
            }, e.prototype.getMaxScrollLeft = function () {
                return this.getScrollWidth() - this.getClientWidth()
            }, e.prototype.canScrollVertically = function () {
                return this.getMaxScrollTop() > 0
            }, e.prototype.canScrollHorizontally = function () {
                return this.getMaxScrollLeft() > 0
            }, e.prototype.canScrollUp = function () {
                return this.getScrollTop() > 0
            }, e.prototype.canScrollDown = function () {
                return this.getScrollTop() < this.getMaxScrollTop()
            }, e.prototype.canScrollLeft = function () {
                return this.getScrollLeft() > 0
            }, e.prototype.canScrollRight = function () {
                return this.getScrollLeft() < this.getMaxScrollLeft()
            }, e
        }(),
        eo = function (e) {
            function t(t) {
                var n = e.call(this) || this;
                return n.el = t, n
            }

            return et(t, e), t.prototype.getScrollTop = function () {
                return this.el.scrollTop
            }, t.prototype.getScrollLeft = function () {
                return this.el.scrollLeft
            }, t.prototype.setScrollTop = function (e) {
                this.el.scrollTop = e
            }, t.prototype.setScrollLeft = function (e) {
                this.el.scrollLeft = e
            }, t.prototype.getScrollWidth = function () {
                return this.el.scrollWidth
            }, t.prototype.getScrollHeight = function () {
                return this.el.scrollHeight
            }, t.prototype.getClientHeight = function () {
                return this.el.clientHeight
            }, t.prototype.getClientWidth = function () {
                return this.el.clientWidth
            }, t
        }($i),
        to = function (e) {
            function t() {
                return null !== e && e.apply(this, arguments) || this
            }

            return et(t, e), t.prototype.getScrollTop = function () {
                return window.pageYOffset
            }, t.prototype.getScrollLeft = function () {
                return window.pageXOffset
            }, t.prototype.setScrollTop = function (e) {
                window.scroll(window.pageXOffset, e)
            }, t.prototype.setScrollLeft = function (e) {
                window.scroll(e, window.pageYOffset)
            }, t.prototype.getScrollWidth = function () {
                return document.documentElement.scrollWidth
            }, t.prototype.getScrollHeight = function () {
                return document.documentElement.scrollHeight
            }, t.prototype.getClientHeight = function () {
                return document.documentElement.clientHeight
            }, t.prototype.getClientWidth = function () {
                return document.documentElement.clientWidth
            }, t
        }($i),
        no = function (e) {
            function n(n, r) {
                var i = e.call(this, t("div", {
                    className: "fc-scroller"
                })) || this;
                return i.overflowX = n, i.overflowY = r, i.applyOverflow(), i
            }

            return et(n, e), n.prototype.clear = function () {
                this.setHeight("auto"), this.applyOverflow()
            }, n.prototype.destroy = function () {
                c(this.el)
            }, n.prototype.applyOverflow = function () {
                g(this.el, {
                    overflowX: this.overflowX,
                    overflowY: this.overflowY
                })
            }, n.prototype.lockOverflow = function (e) {
                var t = this.overflowX,
                    n = this.overflowY;
                e = e || this.getScrollbarWidths(), "auto" === t && (t = e.bottom || this.canScrollHorizontally() ? "scroll" : "hidden"), "auto" === n && (n = e.left || e.right || this.canScrollVertically() ? "scroll" : "hidden"), g(this.el, {
                    overflowX: t,
                    overflowY: n
                })
            }, n.prototype.setHeight = function (e) {
                y(this.el, "height", e)
            }, n.prototype.getScrollbarWidths = function () {
                var e = C(this.el);
                return {
                    left: e.scrollbarLeft,
                    right: e.scrollbarRight,
                    bottom: e.scrollbarBottom
                }
            }, n
        }(eo),
        ro = function () {
            function e(e) {
                this.calendarOptions = e, this.processIconOverride()
            }

            return e.prototype.processIconOverride = function () {
                this.iconOverrideOption && this.setIconOverride(this.calendarOptions[this.iconOverrideOption])
            }, e.prototype.setIconOverride = function (e) {
                var t, n;
                if ("object" == typeof e && e) {
                    t = ki({}, this.iconClasses);
                    for (n in e) t[n] = this.applyIconOverridePrefix(e[n]);
                    this.iconClasses = t
                } else !1 === e && (this.iconClasses = {})
            }, e.prototype.applyIconOverridePrefix = function (e) {
                var t = this.iconOverridePrefix;
                return t && 0 !== e.indexOf(t) && (e = t + e), e
            }, e.prototype.getClass = function (e) {
                return this.classes[e] || ""
            }, e.prototype.getIconClass = function (e) {
                var t = this.iconClasses[e];
                return t ? this.baseIconClass + " " + t : ""
            }, e.prototype.getCustomButtonIconClass = function (e) {
                var t;
                return this.iconOverrideCustomButtonOption && (t = e[this.iconOverrideCustomButtonOption]) ? this.baseIconClass + " " + this.applyIconOverridePrefix(t) : ""
            }, e
        }();
    ro.prototype.classes = {}, ro.prototype.iconClasses = {}, ro.prototype.baseIconClass = "", ro.prototype.iconOverridePrefix = "";
    var io = 0,
        oo = function () {
            function e(e, t) {
                t && (e.view = this), this.uid = String(io++), this.context = e, this.dateEnv = e.dateEnv, this.theme = e.theme, this.view = e.view, this.calendar = e.calendar, this.isRtl = "rtl" === this.opt("dir")
            }

            return e.addEqualityFuncs = function (e) {
                this.prototype.equalityFuncs = ki({}, this.prototype.equalityFuncs, e)
            }, e.prototype.opt = function (e) {
                return this.context.options[e]
            }, e.prototype.receiveProps = function (e) {
                var t = Qn(this.props || {}, e, this.equalityFuncs),
                    n = t.anyChanges,
                    r = t.comboProps;
                this.props = r, n && this.render(r)
            }, e.prototype.render = function (e) {
            }, e.prototype.destroy = function () {
            }, e
        }();
    oo.prototype.equalityFuncs = {};
    var ao = function (e) {
        function t(t, n, r) {
            var i = e.call(this, t, r) || this;
            return i.el = n, i
        }

        return et(t, e), t.prototype.destroy = function () {
            e.prototype.destroy.call(this), c(this.el)
        }, t.prototype.queryHit = function (e, t, n, r) {
            return null
        }, t.prototype.isInteractionValid = function (e) {
            var t = this.calendar,
                n = this.props.dateProfile,
                r = e.mutatedEvents.instances;
            if (n)
                for (var i in r)
                    if (!wt(n.validRange, r[i].range)) return !1;
            return dn(e, t)
        }, t.prototype.isDateSelectionValid = function (e) {
            var t = this.props.dateProfile;
            return !(t && !wt(t.validRange, e.range)) && fn(e, this.calendar)
        }, t.prototype.publiclyTrigger = function (e, t) {
            return this.calendar.publiclyTrigger(e, t)
        }, t.prototype.publiclyTriggerAfterSizing = function (e, t) {
            return this.calendar.publiclyTriggerAfterSizing(e, t)
        }, t.prototype.hasPublicHandlers = function (e) {
            return this.calendar.hasPublicHandlers(e)
        }, t.prototype.triggerRenderedSegs = function (e, t) {
            var n = this.calendar;
            if (this.hasPublicHandlers("eventPositioned"))
                for (var r = 0, i = e; r < i.length; r++) {
                    var o = i[r];
                    this.publiclyTriggerAfterSizing("eventPositioned", [{
                        event: new Bi(n, o.eventRange.def, o.eventRange.instance),
                        isMirror: t,
                        isStart: o.isStart,
                        isEnd: o.isEnd,
                        el: o.el,
                        view: this
                    }])
                }
            n.state.loadingLevel || (n.afterSizingTriggers._eventsPositioned = [null])
        }, t.prototype.triggerWillRemoveSegs = function (e, t) {
            for (var n = this.calendar, r = 0, i = e; r < i.length; r++) {
                var o = i[r];
                n.trigger("eventElRemove", o.el)
            }
            if (this.hasPublicHandlers("eventDestroy"))
                for (var a = 0, s = e; a < s.length; a++) {
                    var o = s[a];
                    this.publiclyTrigger("eventDestroy", [{
                        event: new Bi(n, o.eventRange.def, o.eventRange.instance),
                        isMirror: t,
                        el: o.el,
                        view: this
                    }])
                }
        }, t.prototype.isValidSegDownEl = function (e) {
            return !this.props.eventDrag && !this.props.eventResize && !d(e, ".fc-mirror") && (this.isPopover() || !this.isInPopover(e))
        }, t.prototype.isValidDateDownEl = function (e) {
            var t = d(e, this.fgSegSelector);
            return (!t || t.classList.contains("fc-mirror")) && !d(e, ".fc-more") && !d(e, "a[data-goto]") && !this.isInPopover(e)
        }, t.prototype.isPopover = function () {
            return this.el.classList.contains("fc-popover")
        }, t.prototype.isInPopover = function (e) {
            return Boolean(d(e, ".fc-popover"))
        }, t
    }(oo);
    ao.prototype.fgSegSelector = ".fc-event-container > *", ao.prototype.bgSegSelector = ".fc-bgevent:not(.fc-nonbusiness)";
    var so = 0,
        uo = function () {
            function e() {
                this.hooks = {
                    reducers: [],
                    eventDefParsers: [],
                    eventDragMutationMassagers: [],
                    eventDefMutationAppliers: [],
                    dateSelectionTransformers: [],
                    datePointTransforms: [],
                    dateSpanTransforms: [],
                    views: {},
                    viewPropsTransformers: [],
                    isPropsValid: null,
                    externalDefTransforms: [],
                    eventResizeJoinTransforms: [],
                    viewContainerModifiers: [],
                    eventDropTransformers: [],
                    componentInteractions: [],
                    calendarInteractions: [],
                    themeClasses: {},
                    eventSourceDefs: [],
                    cmdFormatter: null,
                    recurringTypes: [],
                    namedTimeZonedImpl: null,
                    defaultView: "",
                    elementDraggingImpl: null,
                    optionChangeHandlers: {}
                }, this.addedHash = {}
            }

            return e.prototype.add = function (e) {
                if (!this.addedHash[e.id]) {
                    this.addedHash[e.id] = !0;
                    for (var t = 0, n = e.deps; t < n.length; t++) {
                        var r = n[t];
                        this.add(r)
                    }
                    this.hooks = er(this.hooks, e)
                }
            }, e
        }(),
        lo = {
            ignoreRange: !0,
            parseMeta: function (e) {
                return Array.isArray(e) ? e : Array.isArray(e.events) ? e.events : null
            },
            fetch: function (e, t) {
                t({
                    rawEvents: e.eventSource.meta
                })
            }
        },
        co = $n({
            eventSourceDefs: [lo]
        }),
        fo = {
            parseMeta: function (e) {
                return "function" == typeof e ? e : "function" == typeof e.events ? e.events : null
            },
            fetch: function (e, t, n) {
                var r = e.calendar.dateEnv;
                Xn(e.eventSource.meta.bind(null, {
                    start: r.toDate(e.range.start),
                    end: r.toDate(e.range.end),
                    startStr: r.formatIso(e.range.start),
                    endStr: r.formatIso(e.range.end),
                    timeZone: r.timeZone
                }), function (e) {
                    t({
                        rawEvents: e
                    })
                }, n)
            }
        },
        po = $n({
            eventSourceDefs: [fo]
        }),
        ho = {
            parseMeta: function (e) {
                if ("string" == typeof e) e = {
                    url: e
                };
                else if (!e || "object" != typeof e || !e.url) return null;
                return {
                    url: e.url,
                    method: (e.method || "GET").toUpperCase(),
                    extraParams: e.extraParams,
                    startParam: e.startParam,
                    endParam: e.endParam,
                    timeZoneParam: e.timeZoneParam
                }
            },
            fetch: function (e, t, n) {
                var r = e.eventSource.meta,
                    i = ir(r, e.range, e.calendar);
                tr(r.method, r.url, i, function (e, n) {
                    t({
                        rawEvents: e,
                        xhr: n
                    })
                }, function (e, t) {
                    n({
                        message: e,
                        xhr: t
                    })
                })
            }
        },
        vo = $n({
            eventSourceDefs: [ho]
        }),
        go = {
            parse: function (e, t, n) {
                var r = n.createMarker.bind(n),
                    i = {
                        daysOfWeek: null,
                        startTime: ue,
                        endTime: ue,
                        startRecur: r,
                        endRecur: r
                    },
                    o = Ge(e, i, {}, t),
                    a = !1;
                for (var s in o)
                    if (null != o[s]) {
                        a = !0;
                        break
                    }
                return a ? {
                    allDayGuess: Boolean(!o.startTime && !o.endTime),
                    duration: o.startTime && o.endTime ? ve(o.endTime, o.startTime) : null,
                    typeData: o
                } : null
            },
            expand: function (e, t, n) {
                var r = Dt(t, {
                    start: e.startRecur,
                    end: e.endRecur
                });
                return r ? or(e.daysOfWeek, e.startTime, r, n) : []
            }
        },
        yo = $n({
            recurringTypes: [go]
        }),
        mo = $n({
            optionChangeHandlers: {
                events: function (e, t) {
                    ar([e], t)
                },
                eventSources: ar,
                plugins: sr
            }
        }),
        Eo = {},
        So = {
            defaultRangeSeparator: " - ",
            titleRangeSeparator: " – ",
            defaultTimedEventDuration: "01:00:00",
            defaultAllDayEventDuration: {
                day: 1
            },
            forceEventDuration: !1,
            nextDayThreshold: "00:00:00",
            columnHeader: !0,
            defaultView: "",
            aspectRatio: 1.35,
            header: {
                left: "title",
                center: "",
                right: "today prev,next"
            },
            weekends: !0,
            weekNumbers: !1,
            weekNumberCalculation: "local",
            editable: !1,
            scrollTime: "06:00:00",
            minTime: "00:00:00",
            maxTime: "24:00:00",
            showNonCurrentDates: !0,
            lazyFetching: !0,
            startParam: "start",
            endParam: "end",
            timeZoneParam: "timeZone",
            timeZone: "local",
            locales: [],
            locale: "",
            timeGridEventMinHeight: 0,
            themeSystem: "standard",
            dragRevertDuration: 500,
            dragScroll: !0,
            allDayMaintainDuration: !1,
            unselectAuto: !0,
            dropAccept: "*",
            eventOrder: "start,-duration,allDay,title",
            eventLimit: !1,
            eventLimitClick: "popover",
            dayPopoverFormat: {
                month: "long",
                day: "numeric",
                year: "numeric"
            },
            handleWindowResize: !0,
            windowResizeDelay: 100,
            longPressDelay: 1e3,
            eventDragMinDistance: 5
        },
        Do = {
            header: {
                left: "next,prev today",
                center: "",
                right: "title"
            },
            buttonIcons: {
                prev: "fc-icon-chevron-right",
                next: "fc-icon-chevron-left",
                prevYear: "fc-icon-chevrons-right",
                nextYear: "fc-icon-chevrons-left"
            }
        },
        bo = ["header", "footer", "buttonText", "buttonIcons"],
        To = [co, po, vo, yo, mo],
        wo = {
            code: "en",
            week: {
                dow: 0,
                doy: 4
            },
            dir: "ltr",
            buttonText: {
                prev: "prev",
                next: "next",
                prevYear: "prev year",
                nextYear: "next year",
                year: "year",
                today: "today",
                month: "month",
                week: "week",
                day: "day",
                list: "list"
            },
            weekLabel: "W",
            allDayText: "all-day",
            eventLimitText: "more",
            noEventsMessage: "No events to display"
        },
        Ro = function () {
            function e(e) {
                this.overrides = ki({}, e), this.dynamicOverrides = {}, this.compute()
            }

            return e.prototype.add = function (e) {
                ki(this.overrides, e), this.compute()
            }, e.prototype.addDynamic = function (e) {
                ki(this.dynamicOverrides, e), this.compute()
            }, e.prototype.reset = function (e) {
                this.overrides = e, this.compute()
            }, e.prototype.compute = function () {
                var e = Ye(this.dynamicOverrides.locales, this.overrides.locales, So.locales),
                    t = Ye(this.dynamicOverrides.locale, this.overrides.locale, So.locale),
                    n = cr(e),
                    r = dr(t || n.defaultCode, n.map).options,
                    i = Ye(this.dynamicOverrides.dir, this.overrides.dir, r.dir),
                    o = "rtl" === i ? Do : {};
                this.dirDefaults = o, this.localeDefaults = r, this.computed = ur([So, o, r, this.overrides, this.dynamicOverrides])
            }, e
        }(),
        Io = {},
        Co = function () {
            function e() {
            }

            return e.prototype.getMarkerYear = function (e) {
                return e.getUTCFullYear()
            }, e.prototype.getMarkerMonth = function (e) {
                return e.getUTCMonth()
            }, e.prototype.getMarkerDay = function (e) {
                return e.getUTCDate()
            }, e.prototype.arrayToMarker = function (e) {
                return oe(e)
            }, e.prototype.markerToArray = function (e) {
                return ie(e)
            }, e
        }();
    !function (e, t) {
        Io[e] = t
    }("gregory", Co);
    var Mo = /^\s*\d{4}-\d\d-\d\d([T ]\d)?/,
        ko = /(?:(Z)|([-+])(\d\d)(?::(\d\d))?)$/,
        Oo = function () {
            function e(e) {
                var t = this.timeZone = e.timeZone,
                    n = "local" !== t && "UTC" !== t;
                e.namedTimeZoneImpl && n && (this.namedTimeZoneImpl = new e.namedTimeZoneImpl(t)), this.canComputeOffset = Boolean(!n || this.namedTimeZoneImpl), this.calendarSystem = vr(e.calendarSystem), this.locale = e.locale, this.weekDow = e.locale.week.dow, this.weekDoy = e.locale.week.doy, "ISO" === e.weekNumberCalculation ? (this.weekDow = 1, this.weekDoy = 4) : "number" == typeof e.firstDay && (this.weekDow = e.firstDay), "function" == typeof e.weekNumberCalculation && (this.weekNumberFunc = e.weekNumberCalculation), this.weekLabel = null != e.weekLabel ? e.weekLabel : e.locale.options.weekLabel, this.cmdFormatter = e.cmdFormatter
            }

            return e.prototype.createMarker = function (e) {
                var t = this.createMarkerMeta(e);
                return null === t ? null : t.marker
            }, e.prototype.createNowMarker = function () {
                return this.canComputeOffset ? this.timestampToMarker((new Date).valueOf()) : oe(ne(new Date))
            }, e.prototype.createMarkerMeta = function (e) {
                if ("string" == typeof e) return this.parse(e);
                var t = null;
                return "number" == typeof e ? t = this.timestampToMarker(e) : e instanceof Date ? (e = e.valueOf(), isNaN(e) || (t = this.timestampToMarker(e))) : Array.isArray(e) && (t = oe(e)), null !== t && ae(t) ? {
                    marker: t,
                    isTimeUnspecified: !1,
                    forcedTzo: null
                } : null
            }, e.prototype.parse = function (e) {
                var t = gr(e);
                if (null === t) return null;
                var n = t.marker,
                    r = null;
                return null !== t.timeZoneOffset && (this.canComputeOffset ? n = this.timestampToMarker(n.valueOf() - 60 * t.timeZoneOffset * 1e3) : r = t.timeZoneOffset), {
                    marker: n,
                    isTimeUnspecified: t.isTimeUnspecified,
                    forcedTzo: r
                }
            }, e.prototype.getYear = function (e) {
                return this.calendarSystem.getMarkerYear(e)
            }, e.prototype.getMonth = function (e) {
                return this.calendarSystem.getMarkerMonth(e)
            }, e.prototype.add = function (e, t) {
                var n = this.calendarSystem.markerToArray(e);
                return n[0] += t.years, n[1] += t.months, n[2] += t.days, n[6] += t.milliseconds, this.calendarSystem.arrayToMarker(n)
            }, e.prototype.subtract = function (e, t) {
                var n = this.calendarSystem.markerToArray(e);
                return n[0] -= t.years, n[1] -= t.months, n[2] -= t.days, n[6] -= t.milliseconds, this.calendarSystem.arrayToMarker(n)
            }, e.prototype.addYears = function (e, t) {
                var n = this.calendarSystem.markerToArray(e);
                return n[0] += t, this.calendarSystem.arrayToMarker(n)
            }, e.prototype.addMonths = function (e, t) {
                var n = this.calendarSystem.markerToArray(e);
                return n[1] += t, this.calendarSystem.arrayToMarker(n)
            }, e.prototype.diffWholeYears = function (e, t) {
                var n = this.calendarSystem;
                return se(e) === se(t) && n.getMarkerDay(e) === n.getMarkerDay(t) && n.getMarkerMonth(e) === n.getMarkerMonth(t) ? n.getMarkerYear(t) - n.getMarkerYear(e) : null
            }, e.prototype.diffWholeMonths = function (e, t) {
                var n = this.calendarSystem;
                return se(e) === se(t) && n.getMarkerDay(e) === n.getMarkerDay(t) ? n.getMarkerMonth(t) - n.getMarkerMonth(e) + 12 * (n.getMarkerYear(t) - n.getMarkerYear(e)) : null
            }, e.prototype.greatestWholeUnit = function (e, t) {
                var n = this.diffWholeYears(e, t);
                return null !== n ? {
                    unit: "year",
                    value: n
                } : null !== (n = this.diffWholeMonths(e, t)) ? {
                    unit: "month",
                    value: n
                } : null !== (n = q(e, t)) ? {
                    unit: "week",
                    value: n
                } : null !== (n = G(e, t)) ? {
                    unit: "day",
                    value: n
                } : (n = W(e, t), Ze(n) ? {
                    unit: "hour",
                    value: n
                } : (n = Z(e, t), Ze(n) ? {
                    unit: "minute",
                    value: n
                } : (n = j(e, t), Ze(n) ? {
                    unit: "second",
                    value: n
                } : {
                    unit: "millisecond",
                    value: t.valueOf() - e.valueOf()
                })))
            }, e.prototype.countDurationsBetween = function (e, t, n) {
                var r;
                return n.years && null !== (r = this.diffWholeYears(e, t)) ? r / ye(n) : n.months && null !== (r = this.diffWholeMonths(e, t)) ? r / me(n) : n.days && null !== (r = G(e, t)) ? r / Ee(n) : (t.valueOf() - e.valueOf()) / be(n)
            }, e.prototype.startOf = function (e, t) {
                return "year" === t ? this.startOfYear(e) : "month" === t ? this.startOfMonth(e) : "week" === t ? this.startOfWeek(e) : "day" === t ? X(e) : "hour" === t ? J(e) : "minute" === t ? K(e) : "second" === t ? Q(e) : void 0
            }, e.prototype.startOfYear = function (e) {
                return this.calendarSystem.arrayToMarker([this.calendarSystem.getMarkerYear(e)])
            }, e.prototype.startOfMonth = function (e) {
                return this.calendarSystem.arrayToMarker([this.calendarSystem.getMarkerYear(e), this.calendarSystem.getMarkerMonth(e)])
            }, e.prototype.startOfWeek = function (e) {
                return this.calendarSystem.arrayToMarker([this.calendarSystem.getMarkerYear(e), this.calendarSystem.getMarkerMonth(e), e.getUTCDate() - (e.getUTCDay() - this.weekDow + 7) % 7])
            }, e.prototype.computeWeekNumber = function (e) {
                return this.weekNumberFunc ? this.weekNumberFunc(this.toDate(e)) : $(e, this.weekDow, this.weekDoy)
            }, e.prototype.format = function (e, t, n) {
                return void 0 === n && (n = {}), t.format({
                    marker: e,
                    timeZoneOffset: null != n.forcedTzo ? n.forcedTzo : this.offsetForMarker(e)
                }, this)
            }, e.prototype.formatRange = function (e, t, n, r) {
                return void 0 === r && (r = {}), r.isEndExclusive && (t = V(t, -1)), n.formatRange({
                    marker: e,
                    timeZoneOffset: null != r.forcedStartTzo ? r.forcedStartTzo : this.offsetForMarker(e)
                }, {
                    marker: t,
                    timeZoneOffset: null != r.forcedEndTzo ? r.forcedEndTzo : this.offsetForMarker(t)
                }, this)
            }, e.prototype.formatIso = function (e, t) {
                void 0 === t && (t = {});
                var n = null;
                return t.omitTimeZoneOffset || (n = null != t.forcedTzo ? t.forcedTzo : this.offsetForMarker(e)), Bt(e, n, t.omitTime)
            }, e.prototype.timestampToMarker = function (e) {
                return "local" === this.timeZone ? oe(ne(new Date(e))) : "UTC" !== this.timeZone && this.namedTimeZoneImpl ? oe(this.namedTimeZoneImpl.timestampToArray(e)) : new Date(e)
            }, e.prototype.offsetForMarker = function (e) {
                return "local" === this.timeZone ? -re(ie(e)).getTimezoneOffset() : "UTC" === this.timeZone ? 0 : this.namedTimeZoneImpl ? this.namedTimeZoneImpl.offsetForArray(ie(e)) : null
            }, e.prototype.toDate = function (e, t) {
                return "local" === this.timeZone ? re(ie(e)) : "UTC" === this.timeZone ? new Date(e.valueOf()) : this.namedTimeZoneImpl ? new Date(e.valueOf() - 1e3 * this.namedTimeZoneImpl.offsetForArray(ie(e)) * 60) : new Date(e.valueOf() - (t || 0))
            }, e
        }(),
        _o = {
            id: String,
            allDayDefault: Boolean,
            eventDataTransform: Function,
            success: Function,
            failure: Function
        },
        Po = 0,
        Ho = 0,
        xo = function () {
            function e(e, t) {
                this.viewSpec = e, this.options = e.options, this.dateEnv = t.dateEnv, this.calendar = t, this.initHiddenDays()
            }

            return e.prototype.buildPrev = function (e, t) {
                var n = this.dateEnv,
                    r = n.subtract(n.startOf(t, e.currentRangeUnit), e.dateIncrement);
                return this.build(r, -1)
            }, e.prototype.buildNext = function (e, t) {
                var n = this.dateEnv,
                    r = n.add(n.startOf(t, e.currentRangeUnit), e.dateIncrement);
                return this.build(r, 1)
            }, e.prototype.build = function (e, t, n) {
                void 0 === n && (n = !1);
                var r, i, o, a, s, u, l = null,
                    c = null;
                return r = this.buildValidRange(), r = this.trimHiddenDays(r), n && (e = It(e, r)), i = this.buildCurrentRangeInfo(e, t), o = /^(year|month|week|day)$/.test(i.unit), a = this.buildRenderRange(this.trimHiddenDays(i.range), i.unit, o), a = this.trimHiddenDays(a), s = a, this.options.showNonCurrentDates || (s = Dt(s, i.range)), l = ue(this.options.minTime), c = ue(this.options.maxTime), s = this.adjustActiveRange(s, l, c), s = Dt(s, r), u = Tt(i.range, r), {
                    validRange: r,
                    currentRange: i.range,
                    currentRangeUnit: i.unit,
                    isRangeAllDay: o,
                    activeRange: s,
                    renderRange: a,
                    minTime: l,
                    maxTime: c,
                    isValid: u,
                    dateIncrement: this.buildDateIncrement(i.duration)
                }
            }, e.prototype.buildValidRange = function () {
                return this.getRangeOption("validRange", this.calendar.getNow()) || {
                    start: null,
                    end: null
                }
            }, e.prototype.buildCurrentRangeInfo = function (e, t) {
                var n, r = this,
                    i = r.viewSpec,
                    o = r.dateEnv,
                    a = null,
                    s = null,
                    u = null;
                return i.duration ? (a = i.duration, s = i.durationUnit, u = this.buildRangeFromDuration(e, t, a, s)) : (n = this.options.dayCount) ? (s = "day", u = this.buildRangeFromDayCount(e, t, n)) : (u = this.buildCustomVisibleRange(e)) ? s = o.greatestWholeUnit(u.start, u.end).unit : (a = this.getFallbackDuration(), s = we(a).unit, u = this.buildRangeFromDuration(e, t, a, s)), {
                    duration: a,
                    unit: s,
                    range: u
                }
            }, e.prototype.getFallbackDuration = function () {
                return ue({
                    day: 1
                })
            }, e.prototype.adjustActiveRange = function (e, t, n) {
                var r = this.dateEnv,
                    i = e.start,
                    o = e.end;
                return this.viewSpec.class.prototype.usesMinMaxTime && (Ee(t) < 0 && (i = X(i), i = r.add(i, t)), Ee(n) > 1 && (o = X(o), o = A(o, -1), o = r.add(o, n))), {
                    start: i,
                    end: o
                }
            }, e.prototype.buildRangeFromDuration = function (e, t, n, r) {
                function i() {
                    s = c.startOf(e, d), u = c.add(s, n), l = {
                        start: s,
                        end: u
                    }
                }

                var o, a, s, u, l, c = this.dateEnv,
                    d = this.options.dateAlignment;
                return d || (o = this.options.dateIncrement, o ? (a = ue(o), d = be(a) < be(n) ? we(a, !de(o)).unit : r) : d = r), Ee(n) <= 1 && this.isHiddenDay(s) && (s = this.skipHiddenDays(s, t), s = X(s)), i(), this.trimHiddenDays(l) || (e = this.skipHiddenDays(e, t), i()), l
            }, e.prototype.buildRangeFromDayCount = function (e, t, n) {
                var r, i = this.dateEnv,
                    o = this.options.dateAlignment,
                    a = 0,
                    s = e;
                o && (s = i.startOf(s, o)), s = X(s), s = this.skipHiddenDays(s, t), r = s;
                do {
                    r = A(r, 1), this.isHiddenDay(r) || a++
                } while (a < n);
                return {
                    start: s,
                    end: r
                }
            }, e.prototype.buildCustomVisibleRange = function (e) {
                var t = this.dateEnv,
                    n = this.getRangeOption("visibleRange", t.toDate(e));
                return !n || null != n.start && null != n.end ? n : null
            }, e.prototype.buildRenderRange = function (e, t, n) {
                return e
            }, e.prototype.buildDateIncrement = function (e) {
                var t, n = this.options.dateIncrement;
                return n ? ue(n) : (t = this.options.dateAlignment) ? ue(1, t) : e || ue({
                    days: 1
                })
            }, e.prototype.getRangeOption = function (e) {
                for (var t = [], n = 1; n < arguments.length; n++) t[n - 1] = arguments[n];
                var r = this.options[e];
                return "function" == typeof r && (r = r.apply(null, t)), r && (r = mt(r, this.dateEnv)), r && (r = Ke(r)), r
            }, e.prototype.initHiddenDays = function () {
                var e, t = this.options.hiddenDays || [],
                    n = [],
                    r = 0;
                for (!1 === this.options.weekends && t.push(0, 6), e = 0; e < 7; e++) (n[e] = -1 !== t.indexOf(e)) || r++;
                if (!r) throw new Error("invalid hiddenDays");
                this.isHiddenDayHash = n
            }, e.prototype.trimHiddenDays = function (e) {
                var t = e.start,
                    n = e.end;
                return t && (t = this.skipHiddenDays(t)), n && (n = this.skipHiddenDays(n, -1, !0)), null == t || null == n || t < n ? {
                    start: t,
                    end: n
                } : null
            }, e.prototype.isHiddenDay = function (e) {
                return e instanceof Date && (e = e.getUTCDay()), this.isHiddenDayHash[e]
            }, e.prototype.skipHiddenDays = function (e, t, n) {
                for (void 0 === t && (t = 1), void 0 === n && (n = !1); this.isHiddenDayHash[(e.getUTCDay() + (n ? t : 0) + 7) % 7];) e = A(e, t);
                return e
            }, e
        }(),
        No = {
            start: null,
            end: null,
            allDay: Boolean
        },
        zo = {
            type: String,
            class: null
        },
        Uo = function (e) {
            function r(n, r) {
                var i = e.call(this, n) || this;
                return i._renderLayout = An(i.renderLayout, i.unrenderLayout), i._updateTitle = An(i.updateTitle, null, [i._renderLayout]), i._updateActiveButton = An(i.updateActiveButton, null, [i._renderLayout]), i._updateToday = An(i.updateToday, null, [i._renderLayout]), i._updatePrev = An(i.updatePrev, null, [i._renderLayout]), i._updateNext = An(i.updateNext, null, [i._renderLayout]), i.el = t("div", {
                    className: "fc-toolbar " + r
                }), i
            }

            return et(r, e), r.prototype.destroy = function () {
                e.prototype.destroy.call(this), this._renderLayout.unrender(), c(this.el)
            }, r.prototype.render = function (e) {
                this._renderLayout(e.layout), this._updateTitle(e.title), this._updateActiveButton(e.activeButton), this._updateToday(e.isTodayEnabled), this._updatePrev(e.isPrevEnabled), this._updateNext(e.isNextEnabled)
            }, r.prototype.renderLayout = function (e) {
                var t = this.el;
                this.viewsWithButtons = [], a(t, this.renderSection("left", e.left)), a(t, this.renderSection("center", e.center)), a(t, this.renderSection("right", e.right))
            }, r.prototype.unrenderLayout = function () {
                this.el.innerHTML = ""
            }, r.prototype.renderSection = function (e, r) {
                var i = this,
                    o = this,
                    s = o.theme,
                    u = o.calendar,
                    l = u.optionsManager,
                    c = u.viewSpecs,
                    d = t("div", {
                        className: "fc-" + e
                    }),
                    f = l.computed.customButtons || {},
                    p = l.overrides.buttonText || {},
                    h = l.computed.buttonText || {};
                return r && r.split(" ").forEach(function (e, t) {
                    var r, o = [],
                        l = !0;
                    if (e.split(",").forEach(function (e, t) {
                        var r, a, d, v, g, y, m, E, S;
                        "title" === e ? (o.push(n("<h2>&nbsp;</h2>")), l = !1) : ((r = f[e]) ? (d = function (e) {
                            r.click && r.click.call(E, e)
                        }, (v = s.getCustomButtonIconClass(r)) || (v = s.getIconClass(e)) || (g = r.text)) : (a = c[e]) ? (i.viewsWithButtons.push(e), d = function () {
                            u.changeView(e)
                        }, (g = a.buttonTextOverride) || (v = s.getIconClass(e)) || (g = a.buttonTextDefault)) : u[e] && (d = function () {
                            u[e]()
                        }, (g = p[e]) || (v = s.getIconClass(e)) || (g = h[e])), d && (m = ["fc-" + e + "-button", s.getClass("button")], g ? (y = bn(g), S = "") : v && (y = "<span class='" + v + "'></span>", S = ' aria-label="' + e + '"'), E = n('<button type="button" class="' + m.join(" ") + '"' + S + ">" + y + "</button>"), E.addEventListener("click", d), o.push(E)))
                    }), o.length > 1) {
                        r = document.createElement("div");
                        var v = s.getClass("buttonGroup");
                        l && v && r.classList.add(v), a(r, o), d.appendChild(r)
                    } else a(d, o)
                }), d
            }, r.prototype.updateToday = function (e) {
                this.toggleButtonEnabled("today", e)
            }, r.prototype.updatePrev = function (e) {
                this.toggleButtonEnabled("prev", e)
            }, r.prototype.updateNext = function (e) {
                this.toggleButtonEnabled("next", e)
            }, r.prototype.updateTitle = function (e) {
                p(this.el, "h2").forEach(function (t) {
                    t.innerText = e
                })
            }, r.prototype.updateActiveButton = function (e) {
                var t = this.theme.getClass("buttonActive");
                p(this.el, "button").forEach(function (n) {
                    e && n.classList.contains("fc-" + e + "-button") ? n.classList.add(t) : n.classList.remove(t)
                })
            }, r.prototype.toggleButtonEnabled = function (e, t) {
                p(this.el, ".fc-" + e + "-button").forEach(function (e) {
                    e.disabled = !t
                })
            }, r
        }(oo),
        Lo = function (e) {
            function n(n, r) {
                var i = e.call(this, n) || this;
                i._renderToolbars = An(i.renderToolbars), i.buildViewPropTransformers = kt(ni), i.el = r, s(r, i.contentEl = t("div", {
                    className: "fc-view-container"
                }));
                for (var o = i.calendar, a = 0, u = o.pluginSystem.hooks.viewContainerModifiers; a < u.length; a++) {
                    (0, u[a])(i.contentEl, o)
                }
                return i.toggleElClassNames(!0), i.computeTitle = kt(ei), i.parseBusinessHours = kt(function (e) {
                    return Un(e, i.calendar)
                }), i
            }

            return et(n, e), n.prototype.destroy = function () {
                this.header && this.header.destroy(), this.footer && this.footer.destroy(), this.view && this.view.destroy(), c(this.contentEl), this.toggleElClassNames(!1), e.prototype.destroy.call(this)
            }, n.prototype.toggleElClassNames = function (e) {
                var t = this.el.classList,
                    n = "fc-" + this.opt("dir"),
                    r = this.theme.getClass("widget");
                e ? (t.add("fc"), t.add(n), t.add(r)) : (t.remove("fc"), t.remove(n), t.remove(r))
            }, n.prototype.render = function (e) {
                this.freezeHeight();
                var t = this.computeTitle(e.dateProfile, e.viewSpec.options);
                this._renderToolbars(e.viewSpec, e.dateProfile, e.currentDate, e.dateProfileGenerator, t), this.renderView(e, t), this.updateSize(), this.thawHeight()
            }, n.prototype.renderToolbars = function (e, t, n, r, i) {
                var o = this.opt("header"),
                    u = this.opt("footer"),
                    l = this.calendar.getNow(),
                    c = r.build(l),
                    d = r.buildPrev(t, n),
                    f = r.buildNext(t, n),
                    p = {
                        title: i,
                        activeButton: e.type,
                        isTodayEnabled: c.isValid && !Rt(t.currentRange, l),
                        isPrevEnabled: d.isValid,
                        isNextEnabled: f.isValid
                    };
                o ? (this.header || (this.header = new Uo(this.context, "fc-header-toolbar"), s(this.el, this.header.el)), this.header.receiveProps(ki({
                    layout: o
                }, p))) : this.header && (this.header.destroy(), this.header = null), u ? (this.footer || (this.footer = new Uo(this.context, "fc-footer-toolbar"), a(this.el, this.footer.el)), this.footer.receiveProps(ki({
                    layout: u
                }, p))) : this.footer && (this.footer.destroy(), this.footer = null)
            }, n.prototype.renderView = function (e, t) {
                var n = this.view,
                    r = e.viewSpec,
                    i = e.dateProfileGenerator;
                n && n.viewSpec === r ? n.addScroll(n.queryScroll()) : (n && n.destroy(), n = this.view = new r.class({
                    calendar: this.calendar, view: null, dateEnv: this.dateEnv, theme: this.theme, options: r.options
                }, r, i, this.contentEl)), n.title = t;
                for (var o = {
                    dateProfile: e.dateProfile,
                    businessHours: this.parseBusinessHours(r.options.businessHours),
                    eventStore: e.eventStore,
                    eventUiBases: e.eventUiBases,
                    dateSelection: e.dateSelection,
                    eventSelection: e.eventSelection,
                    eventDrag: e.eventDrag,
                    eventResize: e.eventResize
                }, a = this.buildViewPropTransformers(this.calendar.pluginSystem.hooks.viewPropsTransformers), s = 0, u = a; s < u.length; s++) {
                    var l = u[s];
                    ki(o, l.transform(o, r, e, n))
                }
                n.receiveProps(o)
            }, n.prototype.updateSize = function (e) {
                void 0 === e && (e = !1);
                var t = this.view;
                e && t.addScroll(t.queryScroll()), (e || null == this.isHeightAuto) && this.computeHeightVars(), t.updateSize(e, this.viewHeight, this.isHeightAuto), t.updateNowIndicator(), t.popScroll(e)
            }, n.prototype.computeHeightVars = function () {
                var e = this.calendar,
                    t = e.opt("height"),
                    n = e.opt("contentHeight");
                this.isHeightAuto = "auto" === t || "auto" === n, this.viewHeight = "number" == typeof n ? n : "function" == typeof n ? n() : "number" == typeof t ? t - this.queryToolbarsHeight() : "function" == typeof t ? t() - this.queryToolbarsHeight() : "parent" === t ? this.el.parentNode.offsetHeight - this.queryToolbarsHeight() : Math.round(this.contentEl.offsetWidth / Math.max(e.opt("aspectRatio"), .5))
            }, n.prototype.queryToolbarsHeight = function () {
                var e = 0;
                return this.header && (e += _(this.header.el)), this.footer && (e += _(this.footer.el)), e
            }, n.prototype.freezeHeight = function () {
                g(this.el, {
                    height: this.el.offsetHeight,
                    overflow: "hidden"
                })
            }, n.prototype.thawHeight = function () {
                g(this.el, {
                    height: "",
                    overflow: ""
                })
            }, n
        }(oo),
        Ao = function () {
            function e(e) {
                this.component = e.component
            }

            return e.prototype.destroy = function () {
            }, e
        }(),
        Vo = {},
        Bo = function (e) {
            function t(t) {
                var n = e.call(this, t) || this;
                n.handleSegClick = function (e, t) {
                    var r = n.component,
                        i = Jt(t);
                    if (i && r.isValidSegDownEl(e.target)) {
                        var o = d(e.target, ".fc-has-url"),
                            a = o ? o.querySelector("a[href]").href : "";
                        r.publiclyTrigger("eventClick", [{
                            el: t,
                            event: new Bi(r.calendar, i.eventRange.def, i.eventRange.instance),
                            jsEvent: e,
                            view: r.view
                        }]), a && !e.defaultPrevented && (window.location.href = a)
                    }
                };
                var r = t.component;
                return n.destroy = N(r.el, "click", r.fgSegSelector + "," + r.bgSegSelector, n.handleSegClick), n
            }

            return et(t, e), t
        }(Ao),
        Fo = function (e) {
            function t(t) {
                var n = e.call(this, t) || this;
                n.handleEventElRemove = function (e) {
                    e === n.currentSegEl && n.handleSegLeave(null, n.currentSegEl)
                }, n.handleSegEnter = function (e, t) {
                    Jt(t) && (t.classList.add("fc-allow-mouse-resize"), n.currentSegEl = t, n.triggerEvent("eventMouseEnter", e, t))
                }, n.handleSegLeave = function (e, t) {
                    n.currentSegEl && (t.classList.remove("fc-allow-mouse-resize"), n.currentSegEl = null, n.triggerEvent("eventMouseLeave", e, t))
                };
                var r = t.component;
                return n.removeHoverListeners = z(r.el, r.fgSegSelector + "," + r.bgSegSelector, n.handleSegEnter, n.handleSegLeave), r.calendar.on("eventElRemove", n.handleEventElRemove), n
            }

            return et(t, e), t.prototype.destroy = function () {
                this.removeHoverListeners(), this.component.calendar.off("eventElRemove", this.handleEventElRemove)
            }, t.prototype.triggerEvent = function (e, t, n) {
                var r = this.component,
                    i = Jt(n);
                t && !r.isValidSegDownEl(t.target) || r.publiclyTrigger(e, [{
                    el: n,
                    event: new Bi(this.component.calendar, i.eventRange.def, i.eventRange.instance),
                    jsEvent: t,
                    view: r.view
                }])
            }, t
        }(Ao),
        Wo = function (e) {
            function t() {
                return null !== e && e.apply(this, arguments) || this
            }

            return et(t, e), t
        }(ro);
    Wo.prototype.classes = {
        widget: "fc-unthemed",
        widgetHeader: "fc-widget-header",
        widgetContent: "fc-widget-content",
        buttonGroup: "fc-button-group",
        button: "fc-button fc-button-primary",
        buttonActive: "fc-button-active",
        popoverHeader: "fc-widget-header",
        popoverContent: "fc-widget-content",
        headerRow: "fc-widget-header",
        dayRow: "fc-widget-content",
        listView: "fc-widget-content"
    }, Wo.prototype.baseIconClass = "fc-icon", Wo.prototype.iconClasses = {
        close: "fc-icon-x",
        prev: "fc-icon-chevron-left",
        next: "fc-icon-chevron-right",
        prevYear: "fc-icon-chevrons-left",
        nextYear: "fc-icon-chevrons-right"
    }, Wo.prototype.iconOverrideOption = "buttonIcons", Wo.prototype.iconOverrideCustomButtonOption = "icon", Wo.prototype.iconOverridePrefix = "fc-icon-";
    var Zo = function () {
        function e(e, t) {
            var n = this;
            this.parseRawLocales = kt(cr), this.buildLocale = kt(dr), this.buildDateEnv = kt(oi), this.buildTheme = kt(ai), this.buildEventUiSingleBase = kt(this._buildEventUiSingleBase), this.buildSelectionConfig = kt(this._buildSelectionConfig), this.buildEventUiBySource = Ot(ui, Fn), this.buildEventUiBases = kt(li), this.interactionsStore = {}, this.actionQueue = [], this.isReducing = !1, this.needsRerender = !1, this.needsFullRerender = !1, this.isRendering = !1, this.renderingPauseDepth = 0, this.buildDelayedRerender = kt(si), this.afterSizingTriggers = {}, this.isViewUpdated = !1, this.isDatesUpdated = !1, this.isEventsUpdated = !1, this.el = e, this.optionsManager = new Ro(t || {}), this.pluginSystem = new uo, this.addPluginInputs(this.optionsManager.computed.plugins || []), this.handleOptions(this.optionsManager.computed), this.publiclyTrigger("_init"), this.hydrate(), this.calendarInteractions = this.pluginSystem.hooks.calendarInteractions.map(function (e) {
                return new e(n)
            })
        }

        return e.prototype.addPluginInputs = function (e) {
            for (var t = lr(e), n = 0, r = t; n < r.length; n++) {
                var i = r[n];
                this.pluginSystem.add(i)
            }
        }, Object.defineProperty(e.prototype, "view", {
            get: function () {
                return this.component ? this.component.view : null
            },
            enumerable: !0,
            configurable: !0
        }), e.prototype.render = function () {
            this.component ? this.requestRerender(!0) : (this.renderableEventStore = vt(), this.bindHandlers(), this.executeRender())
        }, e.prototype.destroy = function () {
            if (this.component) {
                this.unbindHandlers(), this.component.destroy(), this.component = null;
                for (var e = 0, t = this.calendarInteractions; e < t.length; e++) {
                    t[e].destroy()
                }
                this.publiclyTrigger("_destroyed")
            }
        }, e.prototype.bindHandlers = function () {
            var e = this;
            this.removeNavLinkListener = N(this.el, "click", "a[data-goto]", function (t, n) {
                var r = n.getAttribute("data-goto");
                r = r ? JSON.parse(r) : {};
                var i = e.dateEnv,
                    o = i.createMarker(r.date),
                    a = r.type,
                    s = e.viewOpt("navLink" + Be(a) + "Click");
                "function" == typeof s ? s(i.toDate(o), t) : ("string" == typeof s && (a = s), e.zoomTo(o, a))
            }), this.opt("handleWindowResize") && window.addEventListener("resize", this.windowResizeProxy = qe(this.windowResize.bind(this), this.opt("windowResizeDelay")))
        }, e.prototype.unbindHandlers = function () {
            this.removeNavLinkListener(), this.windowResizeProxy && (window.removeEventListener("resize", this.windowResizeProxy), this.windowResizeProxy = null)
        }, e.prototype.hydrate = function () {
            var e = this;
            this.state = this.buildInitialState();
            var t = this.opt("eventSources") || [],
                n = this.opt("events"),
                r = [];
            n && t.unshift(n);
            for (var i = 0, o = t; i < o.length; i++) {
                var a = o[i],
                    s = mr(a, this);
                s && r.push(s)
            }
            this.batchRendering(function () {
                e.dispatch({
                    type: "INIT"
                }), e.dispatch({
                    type: "ADD_EVENT_SOURCES",
                    sources: r
                }), e.dispatch({
                    type: "SET_VIEW_TYPE",
                    viewType: e.opt("defaultView") || e.pluginSystem.hooks.defaultView
                })
            })
        }, e.prototype.buildInitialState = function () {
            return {
                viewType: null,
                loadingLevel: 0,
                eventSourceLoadingLevel: 0,
                currentDate: this.getInitialDate(),
                dateProfile: null,
                eventSources: {},
                eventStore: vt(),
                dateSelection: null,
                eventSelection: "",
                eventDrag: null,
                eventResize: null
            }
        }, e.prototype.dispatch = function (e) {
            if (this.actionQueue.push(e), !this.isReducing) {
                this.isReducing = !0;
                for (var t = this.state; this.actionQueue.length;) this.state = this.reduce(this.state, this.actionQueue.shift(), this);
                var n = this.state;
                this.isReducing = !1, !t.loadingLevel && n.loadingLevel ? this.publiclyTrigger("loading", [!0]) : t.loadingLevel && !n.loadingLevel && this.publiclyTrigger("loading", [!1]);
                var r = this.component && this.component.view;
                (t.eventStore !== n.eventStore || this.needsFullRerender) && t.eventStore && (this.isEventsUpdated = !0),
                (t.dateProfile !== n.dateProfile || this.needsFullRerender) && (t.dateProfile && r && this.publiclyTrigger("datesDestroy", [{
                    view: r,
                    el: r.el
                }]), this.isDatesUpdated = !0), (t.viewType !== n.viewType || this.needsFullRerender) && (t.viewType && r && this.publiclyTrigger("viewSkeletonDestroy", [{
                    view: r,
                    el: r.el
                }]), this.isViewUpdated = !0), this.requestRerender()
            }
        }, e.prototype.reduce = function (e, t, n) {
            return Or(e, t, n)
        }, e.prototype.requestRerender = function (e) {
            void 0 === e && (e = !1), this.needsRerender = !0, this.needsFullRerender = this.needsFullRerender || e, this.delayedRerender()
        }, e.prototype.tryRerender = function () {
            this.component && this.needsRerender && !this.renderingPauseDepth && !this.isRendering && this.executeRender()
        }, e.prototype.batchRendering = function (e) {
            this.renderingPauseDepth++, e(), this.renderingPauseDepth--, this.needsRerender && this.requestRerender()
        }, e.prototype.executeRender = function () {
            var e = this.needsFullRerender;
            this.needsRerender = !1, this.needsFullRerender = !1, this.isRendering = !0, this.renderComponent(e), this.isRendering = !1, this.needsRerender && this.delayedRerender()
        }, e.prototype.renderComponent = function (e) {
            var t = this,
                n = t.state,
                r = t.component,
                i = n.viewType,
                o = this.viewSpecs[i],
                a = e && r ? r.view.queryScroll() : null;
            if (!o) throw new Error('View type "' + i + '" is not valid');
            var s = this.renderableEventStore = n.eventSourceLoadingLevel && !this.opt("progressiveEventRendering") ? this.renderableEventStore : n.eventStore,
                u = this.buildEventUiSingleBase(o.options),
                l = this.buildEventUiBySource(n.eventSources),
                c = this.eventUiBases = this.buildEventUiBases(s.defs, u, l);
            !e && r || (r && (r.freezeHeight(), r.destroy()), r = this.component = new Lo({
                calendar: this,
                view: null,
                dateEnv: this.dateEnv,
                theme: this.theme,
                options: this.optionsManager.computed
            }, this.el)), r.receiveProps(ki({}, n, {
                viewSpec: o,
                dateProfile: n.dateProfile,
                dateProfileGenerator: this.dateProfileGenerators[i],
                eventStore: s,
                eventUiBases: c,
                dateSelection: n.dateSelection,
                eventSelection: n.eventSelection,
                eventDrag: n.eventDrag,
                eventResize: n.eventResize
            })), a && r.view.applyScroll(a, !1), this.isViewUpdated && (this.isViewUpdated = !1, this.publiclyTrigger("viewSkeletonRender", [{
                view: r.view,
                el: r.view.el
            }])), this.isDatesUpdated && (this.isDatesUpdated = !1, this.publiclyTrigger("datesRender", [{
                view: r.view,
                el: r.view.el
            }])), this.isEventsUpdated && (this.isEventsUpdated = !1), this.releaseAfterSizingTriggers()
        }, e.prototype.resetOptions = function (e) {
            var t = this,
                n = this.pluginSystem.hooks.optionChangeHandlers,
                r = this.optionsManager.overrides,
                i = {},
                o = {},
                a = {};
            for (var s in r) n[s] || (i[s] = r[s]);
            for (var u in e) n[u] ? a[u] = e[u] : o[u] = e[u];
            this.batchRendering(function () {
                Zn(i, o) ? t.processOptions(e, "reset") : t.processOptions(Wn(i, o));
                for (var r in a) n[r](a[r], t)
            })
        }, e.prototype.setOptions = function (e) {
            var t = this,
                n = this.pluginSystem.hooks.optionChangeHandlers,
                r = {},
                i = {};
            for (var o in e) n[o] ? i[o] = e[o] : r[o] = e[o];
            this.batchRendering(function () {
                t.processOptions(r);
                for (var e in i) n[e](i[e], t)
            })
        }, e.prototype.processOptions = function (e, t) {
            var n = this,
                r = this.dateEnv,
                i = !1,
                o = !1,
                a = !1;
            for (var s in e) /^(height|contentHeight|aspectRatio)$/.test(s) ? o = !0 : /^(defaultDate|defaultView)$/.test(s) || (a = !0, "timeZone" === s && (i = !0));
            "reset" === t ? (a = !0, this.optionsManager.reset(e)) : "dynamic" === t ? this.optionsManager.addDynamic(e) : this.optionsManager.add(e), a && (this.handleOptions(this.optionsManager.computed), this.needsFullRerender = !0, this.batchRendering(function () {
                i && n.dispatch({
                    type: "CHANGE_TIMEZONE",
                    oldDateEnv: r
                }), n.dispatch({
                    type: "SET_VIEW_TYPE",
                    viewType: n.state.viewType
                })
            })), o && this.updateSize()
        }, e.prototype.setOption = function (e, t) {
            var n;
            this.processOptions((n = {}, n[e] = t, n), "dynamic")
        }, e.prototype.getOption = function (e) {
            return this.optionsManager.computed[e]
        }, e.prototype.opt = function (e) {
            return this.optionsManager.computed[e]
        }, e.prototype.viewOpt = function (e) {
            return this.viewOpts()[e]
        }, e.prototype.viewOpts = function () {
            return this.viewSpecs[this.state.viewType].options
        }, e.prototype.handleOptions = function (e) {
            var t = this,
                n = this.pluginSystem.hooks;
            this.defaultAllDayEventDuration = ue(e.defaultAllDayEventDuration), this.defaultTimedEventDuration = ue(e.defaultTimedEventDuration), this.delayedRerender = this.buildDelayedRerender(e.rerenderDelay), this.theme = this.buildTheme(e);
            var r = this.parseRawLocales(e.locales);
            this.availableRawLocales = r.map;
            var i = this.buildLocale(e.locale || r.defaultCode, r.map);
            this.dateEnv = this.buildDateEnv(i, e.timeZone, n.namedTimeZonedImpl, e.firstDay, e.weekNumberCalculation, e.weekLabel, n.cmdFormatter), this.selectionConfig = this.buildSelectionConfig(e), this.viewSpecs = Qr(n.views, this.optionsManager), this.dateProfileGenerators = ot(this.viewSpecs, function (e) {
                return new e.class.prototype.dateProfileGeneratorClass(e, t)
            })
        }, e.prototype.getAvailableLocaleCodes = function () {
            return Object.keys(this.availableRawLocales)
        }, e.prototype._buildSelectionConfig = function (e) {
            return Cn("select", e, this)
        }, e.prototype._buildEventUiSingleBase = function (e) {
            return e.editable && (e = ki({}, e, {
                eventEditable: !0
            })), Cn("event", e, this)
        }, e.prototype.hasPublicHandlers = function (e) {
            return this.hasHandlers(e) || this.opt(e)
        }, e.prototype.publiclyTrigger = function (e, t) {
            var n = this.opt(e);
            if (this.triggerWith(e, this, t), n) return n.apply(this, t)
        }, e.prototype.publiclyTriggerAfterSizing = function (e, t) {
            var n = this.afterSizingTriggers;
            (n[e] || (n[e] = [])).push(t)
        }, e.prototype.releaseAfterSizingTriggers = function () {
            var e = this.afterSizingTriggers;
            for (var t in e)
                for (var n = 0, r = e[t]; n < r.length; n++) {
                    var i = r[n];
                    this.publiclyTrigger(t, i)
                }
            this.afterSizingTriggers = {}
        }, e.prototype.isValidViewType = function (e) {
            return Boolean(this.viewSpecs[e])
        }, e.prototype.changeView = function (e, t) {
            var n = null;
            t && (t.start && t.end ? (this.optionsManager.addDynamic({
                visibleRange: t
            }), this.handleOptions(this.optionsManager.computed)) : n = this.dateEnv.createMarker(t)), this.unselect(), this.dispatch({
                type: "SET_VIEW_TYPE",
                viewType: e,
                dateMarker: n
            })
        }, e.prototype.zoomTo = function (e, t) {
            var n;
            t = t || "day", n = this.viewSpecs[t] || this.getUnitViewSpec(t), this.unselect(), n ? this.dispatch({
                type: "SET_VIEW_TYPE",
                viewType: n.type,
                dateMarker: e
            }) : this.dispatch({
                type: "SET_DATE",
                dateMarker: e
            })
        }, e.prototype.getUnitViewSpec = function (e) {
            var t, n, r;
            t = this.component.header.viewsWithButtons;
            for (var i in this.viewSpecs) t.push(i);
            for (n = 0; n < t.length; n++)
                if ((r = this.viewSpecs[t[n]]) && r.singleUnit === e) return r
        }, e.prototype.getInitialDate = function () {
            var e = this.opt("defaultDate");
            return null != e ? this.dateEnv.createMarker(e) : this.getNow()
        }, e.prototype.prev = function () {
            this.unselect(), this.dispatch({
                type: "PREV"
            })
        }, e.prototype.next = function () {
            this.unselect(), this.dispatch({
                type: "NEXT"
            })
        }, e.prototype.prevYear = function () {
            this.unselect(), this.dispatch({
                type: "SET_DATE",
                dateMarker: this.dateEnv.addYears(this.state.currentDate, -1)
            })
        }, e.prototype.nextYear = function () {
            this.unselect(), this.dispatch({
                type: "SET_DATE",
                dateMarker: this.dateEnv.addYears(this.state.currentDate, 1)
            })
        }, e.prototype.today = function () {
            this.unselect(), this.dispatch({
                type: "SET_DATE",
                dateMarker: this.getNow()
            })
        }, e.prototype.gotoDate = function (e) {
            this.unselect(), this.dispatch({
                type: "SET_DATE",
                dateMarker: this.dateEnv.createMarker(e)
            })
        }, e.prototype.incrementDate = function (e) {
            var t = ue(e);
            t && (this.unselect(), this.dispatch({
                type: "SET_DATE",
                dateMarker: this.dateEnv.add(this.state.currentDate, t)
            }))
        }, e.prototype.getDate = function () {
            return this.dateEnv.toDate(this.state.currentDate)
        }, e.prototype.formatDate = function (e, t) {
            var n = this.dateEnv;
            return n.format(n.createMarker(e), Vt(t))
        }, e.prototype.formatRange = function (e, t, n) {
            var r = this.dateEnv;
            return r.formatRange(r.createMarker(e), r.createMarker(t), Vt(n, this.opt("defaultRangeSeparator")), n)
        }, e.prototype.formatIso = function (e, t) {
            var n = this.dateEnv;
            return n.formatIso(n.createMarker(e), {
                omitTime: t
            })
        }, e.prototype.windowResize = function (e) {
            !this.isHandlingWindowResize && this.component && e.target === window && (this.isHandlingWindowResize = !0, this.updateSize(), this.publiclyTrigger("windowResize", [this.view]), this.isHandlingWindowResize = !1)
        }, e.prototype.updateSize = function () {
            this.component && this.component.updateSize(!0)
        }, e.prototype.registerInteractiveComponent = function (e, t) {
            var n = ri(e, t),
                r = [Bo, Fo],
                i = r.concat(this.pluginSystem.hooks.componentInteractions),
                o = i.map(function (e) {
                    return new e(n)
                });
            this.interactionsStore[e.uid] = o, Vo[e.uid] = n
        }, e.prototype.unregisterInteractiveComponent = function (e) {
            for (var t = 0, n = this.interactionsStore[e.uid]; t < n.length; t++) {
                n[t].destroy()
            }
            delete this.interactionsStore[e.uid], delete Vo[e.uid]
        }, e.prototype.select = function (e, t) {
            var n;
            n = null == t ? null != e.start ? e : {
                start: e,
                end: null
            } : {
                start: e,
                end: t
            };
            var r = Ar(n, this.dateEnv, ue({
                days: 1
            }));
            r && (this.dispatch({
                type: "SELECT_DATES",
                selection: r
            }), this.triggerDateSelect(r))
        }, e.prototype.unselect = function (e) {
            this.state.dateSelection && (this.dispatch({
                type: "UNSELECT_DATES"
            }), this.triggerDateUnselect(e))
        }, e.prototype.triggerDateSelect = function (e, t) {
            var n = this.buildDateSpanApi(e);
            n.jsEvent = t ? t.origEvent : null, n.view = this.view, this.publiclyTrigger("select", [n])
        }, e.prototype.triggerDateUnselect = function (e) {
            this.publiclyTrigger("unselect", [{
                jsEvent: e ? e.origEvent : null,
                view: this.view
            }])
        }, e.prototype.triggerDateClick = function (e, t, n, r) {
            var i = this.buildDatePointApi(e);
            i.dayEl = t, i.jsEvent = r, i.view = n, this.publiclyTrigger("dateClick", [i])
        }, e.prototype.buildDatePointApi = function (e) {
            for (var t = {}, n = 0, r = this.pluginSystem.hooks.datePointTransforms; n < r.length; n++) {
                var i = r[n];
                ki(t, i(e, this))
            }
            return ki(t, Zr(e, this.dateEnv)), t
        }, e.prototype.buildDateSpanApi = function (e) {
            for (var t = {}, n = 0, r = this.pluginSystem.hooks.dateSpanTransforms; n < r.length; n++) {
                var i = r[n];
                ki(t, i(e, this))
            }
            return ki(t, Wr(e, this.dateEnv)), t
        }, e.prototype.getNow = function () {
            var e = this.opt("now");
            return "function" == typeof e && (e = e()), null == e ? this.dateEnv.createNowMarker() : this.dateEnv.createMarker(e)
        }, e.prototype.getDefaultEventEnd = function (e, t) {
            var n = t;
            return e ? (n = X(n), n = this.dateEnv.add(n, this.defaultAllDayEventDuration)) : n = this.dateEnv.add(n, this.defaultTimedEventDuration), n
        }, e.prototype.addEvent = function (e, t) {
            if (e instanceof Bi) {
                var n = e._def,
                    r = e._instance;
                return this.state.eventStore.defs[n.defId] || this.dispatch({
                    type: "ADD_EVENTS",
                    eventStore: lt({
                        def: n,
                        instance: r
                    })
                }), e
            }
            var i;
            if (t instanceof Vi) i = t.internalEventSource.sourceId;
            else if (null != t) {
                var o = this.getEventSourceById(t);
                if (!o) return console.warn('Could not find an event source with ID "' + t + '"'), null;
                i = o.internalEventSource.sourceId
            }
            var a = On(e, i, this);
            return a ? (this.dispatch({
                type: "ADD_EVENTS",
                eventStore: lt(a)
            }), new Bi(this, a.def, a.def.recurringDef ? null : a.instance)) : null
        }, e.prototype.getEventById = function (e) {
            var t = this.state.eventStore,
                n = t.defs,
                r = t.instances;
            e = String(e);
            for (var i in n) {
                var o = n[i];
                if (o.publicId === e) {
                    if (o.recurringDef) return new Bi(this, o, null);
                    for (var a in r) {
                        var s = r[a];
                        if (s.defId === o.defId) return new Bi(this, o, s)
                    }
                }
            }
            return null
        }, e.prototype.getEvents = function () {
            var e = this.state.eventStore,
                t = e.defs,
                n = e.instances,
                r = [];
            for (var i in n) {
                var o = n[i],
                    a = t[o.defId];
                r.push(new Bi(this, a, o))
            }
            return r
        }, e.prototype.removeAllEvents = function () {
            this.dispatch({
                type: "REMOVE_ALL_EVENTS"
            })
        }, e.prototype.rerenderEvents = function () {
            this.dispatch({
                type: "RESET_EVENTS"
            })
        }, e.prototype.getEventSources = function () {
            var e = this.state.eventSources,
                t = [];
            for (var n in e) t.push(new Vi(this, e[n]));
            return t
        }, e.prototype.getEventSourceById = function (e) {
            var t = this.state.eventSources;
            e = String(e);
            for (var n in t)
                if (t[n].publicId === e) return new Vi(this, t[n]);
            return null
        }, e.prototype.addEventSource = function (e) {
            if (e instanceof Vi) return this.state.eventSources[e.internalEventSource.sourceId] || this.dispatch({
                type: "ADD_EVENT_SOURCES",
                sources: [e.internalEventSource]
            }), e;
            var t = mr(e, this);
            return t ? (this.dispatch({
                type: "ADD_EVENT_SOURCES",
                sources: [t]
            }), new Vi(this, t)) : null
        }, e.prototype.removeAllEventSources = function () {
            this.dispatch({
                type: "REMOVE_ALL_EVENT_SOURCES"
            })
        }, e.prototype.refetchEvents = function () {
            this.dispatch({
                type: "FETCH_EVENT_SOURCES"
            })
        }, e
    }();
    Ki.mixInto(Zo);
    var jo = function (e) {
        function n(n, r, i, o) {
            var a = e.call(this, n, t("div", {
                className: "fc-view fc-" + r.type + "-view"
            }), !0) || this;
            return a.renderDatesMem = An(a.renderDatesWrap, a.unrenderDatesWrap), a.renderBusinessHoursMem = An(a.renderBusinessHours, a.unrenderBusinessHours, [a.renderDatesMem]), a.renderDateSelectionMem = An(a.renderDateSelectionWrap, a.unrenderDateSelectionWrap, [a.renderDatesMem]), a.renderEventsMem = An(a.renderEvents, a.unrenderEvents, [a.renderDatesMem]), a.renderEventSelectionMem = An(a.renderEventSelectionWrap, a.unrenderEventSelectionWrap, [a.renderEventsMem]), a.renderEventDragMem = An(a.renderEventDragWrap, a.unrenderEventDragWrap, [a.renderDatesMem]), a.renderEventResizeMem = An(a.renderEventResizeWrap, a.unrenderEventResizeWrap, [a.renderDatesMem]), a.viewSpec = r, a.dateProfileGenerator = i, a.type = r.type, a.eventOrderSpecs = Ue(a.opt("eventOrder")), a.nextDayThreshold = ue(a.opt("nextDayThreshold")), o.appendChild(a.el), a.initialize(), a
        }

        return et(n, e), n.prototype.initialize = function () {
        }, Object.defineProperty(n.prototype, "activeStart", {
            get: function () {
                return this.dateEnv.toDate(this.props.dateProfile.activeRange.start)
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(n.prototype, "activeEnd", {
            get: function () {
                return this.dateEnv.toDate(this.props.dateProfile.activeRange.end)
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(n.prototype, "currentStart", {
            get: function () {
                return this.dateEnv.toDate(this.props.dateProfile.currentRange.start)
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(n.prototype, "currentEnd", {
            get: function () {
                return this.dateEnv.toDate(this.props.dateProfile.currentRange.end)
            },
            enumerable: !0,
            configurable: !0
        }), n.prototype.render = function (e) {
            this.renderDatesMem(e.dateProfile), this.renderBusinessHoursMem(e.businessHours), this.renderDateSelectionMem(e.dateSelection), this.renderEventsMem(e.eventStore), this.renderEventSelectionMem(e.eventSelection), this.renderEventDragMem(e.eventDrag), this.renderEventResizeMem(e.eventResize)
        }, n.prototype.destroy = function () {
            e.prototype.destroy.call(this), this.renderDatesMem.unrender()
        }, n.prototype.updateSize = function (e, t, n) {
            var r = this.calendar;
            (e || r.isViewUpdated || r.isDatesUpdated || r.isEventsUpdated) && this.updateBaseSize(e, t, n)
        }, n.prototype.updateBaseSize = function (e, t, n) {
        }, n.prototype.renderDatesWrap = function (e) {
            this.renderDates(e), this.addScroll({
                isDateInit: !0
            }), this.startNowIndicator(e)
        }, n.prototype.unrenderDatesWrap = function () {
            this.stopNowIndicator(), this.unrenderDates()
        }, n.prototype.renderDates = function (e) {
        }, n.prototype.unrenderDates = function () {
        }, n.prototype.renderBusinessHours = function (e) {
        }, n.prototype.unrenderBusinessHours = function () {
        }, n.prototype.renderDateSelectionWrap = function (e) {
            e && this.renderDateSelection(e)
        }, n.prototype.unrenderDateSelectionWrap = function (e) {
            e && this.unrenderDateSelection(e)
        }, n.prototype.renderDateSelection = function (e) {
        }, n.prototype.unrenderDateSelection = function (e) {
        }, n.prototype.renderEvents = function (e) {
        }, n.prototype.unrenderEvents = function () {
        }, n.prototype.sliceEvents = function (e, t) {
            var n = this.props;
            return Yt(e, n.eventUiBases, n.dateProfile.activeRange, t ? this.nextDayThreshold : null).fg
        }, n.prototype.renderEventSelectionWrap = function (e) {
            e && this.renderEventSelection(e)
        }, n.prototype.unrenderEventSelectionWrap = function (e) {
            e && this.unrenderEventSelection(e)
        }, n.prototype.renderEventSelection = function (e) {
        }, n.prototype.unrenderEventSelection = function (e) {
        }, n.prototype.renderEventDragWrap = function (e) {
            e && this.renderEventDrag(e)
        }, n.prototype.unrenderEventDragWrap = function (e) {
            e && this.unrenderEventDrag(e)
        }, n.prototype.renderEventDrag = function (e) {
        }, n.prototype.unrenderEventDrag = function (e) {
        }, n.prototype.renderEventResizeWrap = function (e) {
            e && this.renderEventResize(e)
        }, n.prototype.unrenderEventResizeWrap = function (e) {
            e && this.unrenderEventResize(e)
        }, n.prototype.renderEventResize = function (e) {
        }, n.prototype.unrenderEventResize = function (e) {
        }, n.prototype.startNowIndicator = function (e) {
            var t, n, r, i = this,
                o = this.dateEnv;
            this.opt("nowIndicator") && (t = this.getNowIndicatorUnit(e)) && (n = this.updateNowIndicator.bind(this), this.initialNowDate = this.calendar.getNow(), this.initialNowQueriedMs = (new Date).valueOf(), r = o.add(o.startOf(this.initialNowDate, t), ue(1, t)).valueOf() - this.initialNowDate.valueOf(), this.nowIndicatorTimeoutID = setTimeout(function () {
                i.nowIndicatorTimeoutID = null, n(), r = "second" === t ? 1e3 : 6e4, i.nowIndicatorIntervalID = setInterval(n, r)
            }, r))
        }, n.prototype.updateNowIndicator = function () {
            this.props.dateProfile && this.initialNowDate && (this.unrenderNowIndicator(), this.renderNowIndicator(V(this.initialNowDate, (new Date).valueOf() - this.initialNowQueriedMs)), this.isNowIndicatorRendered = !0)
        }, n.prototype.stopNowIndicator = function () {
            this.isNowIndicatorRendered && (this.nowIndicatorTimeoutID && (clearTimeout(this.nowIndicatorTimeoutID), this.nowIndicatorTimeoutID = null), this.nowIndicatorIntervalID && (clearInterval(this.nowIndicatorIntervalID), this.nowIndicatorIntervalID = null), this.unrenderNowIndicator(), this.isNowIndicatorRendered = !1)
        }, n.prototype.getNowIndicatorUnit = function (e) {
        }, n.prototype.renderNowIndicator = function (e) {
        }, n.prototype.unrenderNowIndicator = function () {
        }, n.prototype.addScroll = function (e) {
            var t = this.queuedScroll || (this.queuedScroll = {});
            ki(t, e)
        }, n.prototype.popScroll = function (e) {
            this.applyQueuedScroll(e), this.queuedScroll = null
        }, n.prototype.applyQueuedScroll = function (e) {
            this.applyScroll(this.queuedScroll || {}, e)
        }, n.prototype.queryScroll = function () {
            var e = {};
            return this.props.dateProfile && ki(e, this.queryDateScroll()), e
        }, n.prototype.applyScroll = function (e, t) {
            e.isDateInit && (delete e.isDateInit, this.props.dateProfile && ki(e, this.computeInitialDateScroll())), this.props.dateProfile && this.applyDateScroll(e)
        }, n.prototype.computeInitialDateScroll = function () {
            return {}
        }, n.prototype.queryDateScroll = function () {
            return {}
        }, n.prototype.applyDateScroll = function (e) {
        }, n
    }(ao);
    Ki.mixInto(jo), jo.prototype.usesMinMaxTime = !1, jo.prototype.dateProfileGeneratorClass = xo;
    var Yo = function () {
            function e(e) {
                this.segs = [], this.isSizeDirty = !1, this.context = e
            }

            return e.prototype.renderSegs = function (e, t) {
                this.rangeUpdated(), e = this.renderSegEls(e, t), this.segs = e, this.attachSegs(e, t), this.isSizeDirty = !0, this.context.view.triggerRenderedSegs(this.segs, Boolean(t))
            }, e.prototype.unrender = function (e, t) {
                this.context.view.triggerWillRemoveSegs(this.segs, Boolean(t)), this.detachSegs(this.segs), this.segs = []
            }, e.prototype.rangeUpdated = function () {
                var e, t, n = this.context.options;
                this.eventTimeFormat = Vt(n.eventTimeFormat || this.computeEventTimeFormat(), n.defaultRangeSeparator), e = n.displayEventTime, null == e && (e = this.computeDisplayEventTime()), t = n.displayEventEnd, null == t && (t = this.computeDisplayEventEnd()), this.displayEventTime = e, this.displayEventEnd = t
            }, e.prototype.renderSegEls = function (e, t) {
                var n, i = "";
                if (e.length) {
                    for (n = 0; n < e.length; n++) i += this.renderSegHtml(e[n], t);
                    r(i).forEach(function (t, n) {
                        var r = e[n];
                        t && (r.el = t)
                    }), e = Gt(this.context.view, e, Boolean(t))
                }
                return e
            }, e.prototype.getSegClasses = function (e, t, n, r) {
                var i = ["fc-event", e.isStart ? "fc-start" : "fc-not-start", e.isEnd ? "fc-end" : "fc-not-end"].concat(e.eventRange.ui.classNames);
                return t && i.push("fc-draggable"), n && i.push("fc-resizable"), r && (i.push("fc-mirror"), r.isDragging && i.push("fc-dragging"), r.isResizing && i.push("fc-resizing")), i
            }, e.prototype.getTimeText = function (e, t, n) {
                var r = e.def,
                    i = e.instance;
                return this._getTimeText(i.range.start, r.hasEnd ? i.range.end : null, r.allDay, t, n, i.forcedStartTzo, i.forcedEndTzo)
            }, e.prototype._getTimeText = function (e, t, n, r, i, o, a) {
                var s = this.context.dateEnv;
                return null == r && (r = this.eventTimeFormat), null == i && (i = this.displayEventEnd), this.displayEventTime && !n ? i && t ? s.formatRange(e, t, r, {
                    forcedStartTzo: o,
                    forcedEndTzo: a
                }) : s.format(e, r, {
                    forcedTzo: o
                }) : ""
            }, e.prototype.computeEventTimeFormat = function () {
                return {
                    hour: "numeric",
                    minute: "2-digit",
                    omitZeroMinute: !0
                }
            }, e.prototype.computeDisplayEventTime = function () {
                return !0
            }, e.prototype.computeDisplayEventEnd = function () {
                return !0
            }, e.prototype.getSkinCss = function (e) {
                return {
                    "background-color": e.backgroundColor,
                    "border-color": e.borderColor,
                    color: e.textColor
                }
            }, e.prototype.sortEventSegs = function (e) {
                var t = this.context.view.eventOrderSpecs,
                    n = e.map(ci);
                return n.sort(function (e, n) {
                    return Le(e, n, t)
                }), n.map(function (e) {
                    return e._seg
                })
            }, e.prototype.computeSizes = function (e) {
                (e || this.isSizeDirty) && this.computeSegSizes(this.segs)
            }, e.prototype.assignSizes = function (e) {
                (e || this.isSizeDirty) && (this.assignSegSizes(this.segs), this.isSizeDirty = !1)
            }, e.prototype.computeSegSizes = function (e) {
            }, e.prototype.assignSegSizes = function (e) {
            }, e.prototype.hideByHash = function (e) {
                if (e)
                    for (var t = 0, n = this.segs; t < n.length; t++) {
                        var r = n[t];
                        e[r.eventRange.instance.instanceId] && (r.el.style.visibility = "hidden")
                    }
            }, e.prototype.showByHash = function (e) {
                if (e)
                    for (var t = 0, n = this.segs; t < n.length; t++) {
                        var r = n[t];
                        e[r.eventRange.instance.instanceId] && (r.el.style.visibility = "")
                    }
            }, e.prototype.selectByInstanceId = function (e) {
                if (e)
                    for (var t = 0, n = this.segs; t < n.length; t++) {
                        var r = n[t],
                            i = r.eventRange.instance;
                        i && i.instanceId === e && r.el && r.el.classList.add("fc-selected")
                    }
            }, e.prototype.unselectByInstanceId = function (e) {
                if (e)
                    for (var t = 0, n = this.segs; t < n.length; t++) {
                        var r = n[t];
                        r.el && r.el.classList.remove("fc-selected")
                    }
            }, e
        }(),
        qo = function () {
            function e(e) {
                this.fillSegTag = "div", this.dirtySizeFlags = {}, this.context = e, this.containerElsByType = {}, this.segsByType = {}
            }

            return e.prototype.getSegsByType = function (e) {
                return this.segsByType[e] || []
            }, e.prototype.renderSegs = function (e, t) {
                var n, r = this.renderSegEls(e, t),
                    i = this.attachSegs(e, r);
                i && (n = this.containerElsByType[e] || (this.containerElsByType[e] = [])).push.apply(n, i), this.segsByType[e] = r, "bgEvent" === e && this.context.view.triggerRenderedSegs(r, !1), this.dirtySizeFlags[e] = !0
            }, e.prototype.unrender = function (e) {
                var t = this.segsByType[e];
                t && ("bgEvent" === e && this.context.view.triggerWillRemoveSegs(t, !1), this.detachSegs(e, t))
            }, e.prototype.renderSegEls = function (e, t) {
                var n, i = this,
                    o = "";
                if (t.length) {
                    for (n = 0; n < t.length; n++) o += this.renderSegHtml(e, t[n]);
                    r(o).forEach(function (e, n) {
                        var r = t[n];
                        e && (r.el = e)
                    }), "bgEvent" === e && (t = Gt(this.context.view, t, !1)), t = t.filter(function (e) {
                        return f(e.el, i.fillSegTag)
                    })
                }
                return t
            }, e.prototype.renderSegHtml = function (e, t) {
                var n = null,
                    r = [];
                return "highlight" !== e && "businessHours" !== e && (n = {
                    "background-color": t.eventRange.ui.backgroundColor
                }), "highlight" !== e && (r = r.concat(t.eventRange.ui.classNames)), "businessHours" === e ? r.push("fc-bgevent") : r.push("fc-" + e.toLowerCase()), "<" + this.fillSegTag + (r.length ? ' class="' + r.join(" ") + '"' : "") + (n ? ' style="' + Tn(n) + '"' : "") + "></" + this.fillSegTag + ">"
            }, e.prototype.detachSegs = function (e, t) {
                var n = this.containerElsByType[e];
                n && (n.forEach(c), delete this.containerElsByType[e])
            }, e.prototype.computeSizes = function (e) {
                for (var t in this.segsByType) (e || this.dirtySizeFlags[t]) && this.computeSegSizes(this.segsByType[t])
            }, e.prototype.assignSizes = function (e) {
                for (var t in this.segsByType) (e || this.dirtySizeFlags[t]) && this.assignSegSizes(this.segsByType[t]);
                this.dirtySizeFlags = {}
            }, e.prototype.computeSegSizes = function (e) {
            }, e.prototype.assignSegSizes = function (e) {
            }, e
        }(),
        Go = function () {
            function e(e) {
                this.timeZoneName = e
            }

            return e
        }(),
        Xo = function () {
            function e(e) {
                this.emitter = new Ki
            }

            return e.prototype.destroy = function () {
            }, e.prototype.setMirrorIsVisible = function (e) {
            }, e.prototype.setMirrorNeedsRevert = function (e) {
            }, e.prototype.setAutoScrollEnabled = function (e) {
            }, e
        }(),
        Jo = {
            startTime: ue,
            duration: ue,
            create: Boolean,
            sourceId: String
        },
        Ko = {
            create: !0
        },
        Qo = function (e) {
            function t(t, r) {
                var i = e.call(this, t) || this;
                return r.innerHTML = "", r.appendChild(i.el = n('<div class="fc-row ' + i.theme.getClass("headerRow") + '"><table class="' + i.theme.getClass("tableGrid") + '"><thead></thead></table></div>')), i.thead = i.el.querySelector("thead"), i
            }

            return et(t, e), t.prototype.destroy = function () {
                c(this.el)
            }, t.prototype.render = function (e) {
                var t = e.dates,
                    n = e.datesRepDistinctDays,
                    r = [];
                e.renderIntroHtml && r.push(e.renderIntroHtml());
                for (var i = Vt(this.opt("columnHeaderFormat") || vi(n, t.length)), o = 0, a = t; o < a.length; o++) {
                    var s = a[o];
                    r.push(gi(s, e.dateProfile, n, t.length, i, this.context))
                }
                this.isRtl && r.reverse(), this.thead.innerHTML = "<tr>" + r.join("") + "</tr>"
            }, t
        }(oo),
        $o = function () {
            function e(e, t) {
                for (var n = e.start, r = e.end, i = [], o = [], a = -1; n < r;) t.isHiddenDay(n) ? i.push(a + .5) : (a++, i.push(a), o.push(n)), n = A(n, 1);
                this.dates = o, this.indices = i, this.cnt = o.length
            }

            return e.prototype.sliceRange = function (e) {
                var t = this.getDateDayIndex(e.start),
                    n = this.getDateDayIndex(A(e.end, -1)),
                    r = Math.max(0, t),
                    i = Math.min(this.cnt - 1, n);
                return r = Math.ceil(r), i = Math.floor(i), r <= i ? {
                    firstIndex: r,
                    lastIndex: i,
                    isStart: t === r,
                    isEnd: n === i
                } : null
            }, e.prototype.getDateDayIndex = function (e) {
                var t = this.indices,
                    n = Math.floor(F(this.dates[0], e));
                return n < 0 ? t[0] - 1 : n >= t.length ? t[t.length - 1] + 1 : t[n]
            }, e
        }(),
        ea = function () {
            function e(e, t) {
                var n, r, i, o = e.dates;
                if (t) {
                    for (r = o[0].getUTCDay(), n = 1; n < o.length && o[n].getUTCDay() !== r; n++) ;
                    i = Math.ceil(o.length / n)
                } else i = 1, n = o.length;
                this.rowCnt = i, this.colCnt = n, this.daySeries = e, this.cells = this.buildCells(), this.headerDates = this.buildHeaderDates()
            }

            return e.prototype.buildCells = function () {
                for (var e = [], t = 0; t < this.rowCnt; t++) {
                    for (var n = [], r = 0; r < this.colCnt; r++) n.push(this.buildCell(t, r));
                    e.push(n)
                }
                return e
            }, e.prototype.buildCell = function (e, t) {
                return {
                    date: this.daySeries.dates[e * this.colCnt + t]
                }
            }, e.prototype.buildHeaderDates = function () {
                for (var e = [], t = 0; t < this.colCnt; t++) e.push(this.cells[0][t].date);
                return e
            }, e.prototype.sliceRange = function (e) {
                var t = this.colCnt,
                    n = this.daySeries.sliceRange(e),
                    r = [];
                if (n)
                    for (var i = n.firstIndex, o = n.lastIndex, a = i; a <= o;) {
                        var s = Math.floor(a / t),
                            u = Math.min((s + 1) * t, o + 1);
                        r.push({
                            row: s,
                            firstCol: a % t,
                            lastCol: (u - 1) % t,
                            isStart: n.isStart && a === i,
                            isEnd: n.isEnd && u - 1 === o
                        }), a = u
                    }
                return r
            }, e
        }(),
        ta = function () {
            function e() {
                this.sliceBusinessHours = kt(this._sliceBusinessHours), this.sliceDateSelection = kt(this._sliceDateSpan), this.sliceEventStore = kt(this._sliceEventStore), this.sliceEventDrag = kt(this._sliceInteraction), this.sliceEventResize = kt(this._sliceInteraction)
            }

            return e.prototype.sliceProps = function (e, t, n, r) {
                for (var i = [], o = 4; o < arguments.length; o++) i[o - 4] = arguments[o];
                var a = e.eventUiBases,
                    s = this.sliceEventStore.apply(this, [e.eventStore, a, t, n, r].concat(i));
                return {
                    dateSelectionSegs: this.sliceDateSelection.apply(this, [e.dateSelection, a, r].concat(i)),
                    businessHourSegs: this.sliceBusinessHours.apply(this, [e.businessHours, t, n, r].concat(i)),
                    fgEventSegs: s.fg,
                    bgEventSegs: s.bg,
                    eventDrag: this.sliceEventDrag.apply(this, [e.eventDrag, a, t, n, r].concat(i)),
                    eventResize: this.sliceEventResize.apply(this, [e.eventResize, a, t, n, r].concat(i)),
                    eventSelection: e.eventSelection
                }
            }, e.prototype.sliceNowDate = function (e, t) {
                for (var n = [], r = 2; r < arguments.length; r++) n[r - 2] = arguments[r];
                return this._sliceDateSpan.apply(this, [{
                    range: {
                        start: e,
                        end: V(e, 1)
                    },
                    allDay: !1
                }, {}, t].concat(n))
            }, e.prototype._sliceBusinessHours = function (e, t, n, r) {
                for (var i = [], o = 4; o < arguments.length; o++) i[o - 4] = arguments[o];
                return e ? this._sliceEventStore.apply(this, [ct(e, yi(t, Boolean(n)), r.calendar), {}, t, n, r].concat(i)).bg : []
            }, e.prototype._sliceEventStore = function (e, t, n, r, i) {
                for (var o = [], a = 5; a < arguments.length; a++) o[a - 5] = arguments[a];
                if (e) {
                    var s = Yt(e, t, yi(n, Boolean(r)), r);
                    return {
                        bg: this.sliceEventRanges(s.bg, i, o),
                        fg: this.sliceEventRanges(s.fg, i, o)
                    }
                }
                return {
                    bg: [],
                    fg: []
                }
            }, e.prototype._sliceInteraction = function (e, t, n, r, i) {
                for (var o = [], a = 5; a < arguments.length; a++) o[a - 5] = arguments[a];
                if (!e) return null;
                var s = Yt(e.mutatedEvents, t, yi(n, Boolean(r)), r);
                return {
                    segs: this.sliceEventRanges(s.fg, i, o),
                    affectedInstances: e.affectedEvents.instances,
                    isEvent: e.isEvent,
                    sourceSeg: e.origSeg
                }
            }, e.prototype._sliceDateSpan = function (e, t, n) {
                for (var r = [], i = 3; i < arguments.length; i++) r[i - 3] = arguments[i];
                if (!e) return [];
                for (var o = jr(e, t, n.calendar), a = this.sliceRange.apply(this, [e.range].concat(r)), s = 0, u = a; s < u.length; s++) {
                    var l = u[s];
                    l.component = n, l.eventRange = o
                }
                return a
            }, e.prototype.sliceEventRanges = function (e, t, n) {
                for (var r = [], i = 0, o = e; i < o.length; i++) {
                    var a = o[i];
                    r.push.apply(r, this.sliceEventRange(a, t, n))
                }
                return r
            }, e.prototype.sliceEventRange = function (e, t, n) {
                for (var r = this.sliceRange.apply(this, [e.range].concat(n)), i = 0, o = r; i < o.length; i++) {
                    var a = o[i];
                    a.component = t, a.eventRange = e, a.isStart = e.isStart && a.isStart, a.isEnd = e.isEnd && a.isEnd
                }
                return r
            }, e
        }();
    e.Calendar = Zo, e.Component = oo, e.DateComponent = ao, e.DateEnv = Oo, e.DateProfileGenerator = xo, e.DayHeader = Qo, e.DaySeries = $o, e.DayTable = ea, e.ElementDragging = Xo, e.ElementScrollController = eo, e.EmitterMixin = Ki, e.EventApi = Bi, e.FgEventRenderer = Yo, e.FillRenderer = qo, e.Interaction = Ao, e.Mixin = Ji, e.NamedTimeZoneImpl = Go, e.PositionCache = Qi, e.ScrollComponent = no, e.ScrollController = $i, e.Slicer = ta, e.Splitter = Xi, e.Theme = ro, e.View = jo, e.WindowScrollController = to, e.addDays = A, e.addDurations = he, e.addMs = V, e.addWeeks = L, e.allowContextMenu = ze, e.allowSelection = xe, e.appendToElement = a, e.applyAll = je, e.applyMutationToEventStore = $t, e.applyStyle = g, e.applyStyleProp = y, e.asRoughMinutes = Se, e.asRoughMs = be, e.asRoughSeconds = De, e.buildGotoAnchorHtml = Yn, e.buildSegCompareObj = ci, e.capitaliseFirstLetter = Be, e.combineEventUis = Mn, e.compareByFieldSpec = Ae, e.compareByFieldSpecs = Le, e.compareNumbers = We, e.compensateScroll = Re, e.computeClippingRect = H, e.computeEdges = C, e.computeFallbackHeaderFormat = vi, e.computeHeightAndMargins = _, e.computeInnerRect = M, e.computeRect = k, e.computeVisibleDayRange = Ke, e.config = Eo, e.constrainPoint = D, e.createDuration = ue, e.createElement = t, e.createEmptyEventStore = vt, e.createEventInstance = Pn, e.createFormatter = Vt, e.createPlugin = $n, e.cssToStr = Tn, e.debounce = qe, e.diffDates = $e, e.diffDayAndTime = Y, e.diffDays = F, e.diffPoints = T, e.diffWeeks = B, e.diffWholeDays = G, e.diffWholeWeeks = q, e.disableCursor = Ce, e.distributeHeight = ke, e.elementClosest = d, e.elementMatches = f, e.enableCursor = Me, e.eventTupleToStore = lt, e.filterEventStoreDefs = yt, e.filterHash = it, e.findChildren = h, e.findElements = p, e.flexibleCompare = Ve, e.forceClassName = v, e.formatDate = di, e.formatIsoTimeString = Ft, e.formatRange = fi, e.freezeRaw = Xe, e.getAllDayHtml = qn, e.getClippingParents = P, e.getDayClasses = Gn, e.getElSeg = Jt, e.getRectCenter = b, e.getRelevantEvents = dt, e.globalDefaults = So, e.greatestDurationDenominator = we, e.hasBgRendering = qt, e.htmlEscape = bn, e.htmlToElement = n, e.insertAfterElement = u, e.interactionSettingsStore = Vo, e.interactionSettingsToStore = ii, e.intersectRanges = Dt, e.intersectRects = E, e.isArraysEqual = Mt, e.isDateSpansEqual = Br, e.isInt = Ze, e.isInteractionValid = dn, e.isMultiDayRange = Qe, e.isObjectsSimilar = Fn, e.isPropsValid = hn, e.isSingleDay = pe, e.isValidDate = ae, e.isValuesSimilar = Vn, e.listenBySelector = N, e.mapHash = ot, e.matchCellWidths = _e, e.memoize = kt, e.memoizeOutput = Ot, e.memoizeRendering = An, e.mergeEventStores = gt, e.multiplyDuration = ge, e.padStart = Fe, e.parseBusinessHours = Un, e.parseDragMeta = hi, e.parseEventDef = _n, e.parseFieldSpecs = Ue, e.parseMarker = gr, e.pointInsideRect = m, e.prependToElement = s, e.preventContextMenu = Ne, e.preventDefault = x, e.preventSelection = He, e.processScopedUiProps = Cn, e.rangeContainsMarker = Rt, e.rangeContainsRange = wt, e.rangesEqual = bt, e.rangesIntersect = Tt, e.refineProps = Ge, e.removeElement = c, e.removeExact = Ct, e.renderDateCell = gi, e.requestJson = tr, e.sliceEventStore = Yt, e.startOfDay = X, e.subtractInnerElHeight = Pe, e.translateRect = S, e.uncompensateScroll = Ie, e.undistributeHeight = Oe, e.unpromisify = Xn, e.version = "4.0.2", e.whenTransitionDone = U, e.wholeDivideDurations = Te, Object.defineProperty(e, "__esModule", {
        value: !0
    })
});

// locale
!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define(t) : (e = e || self, e.FullCalendarLocalesAll = t())
}(this, function () {
    "use strict";
    return [{
        code: "af",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Vorige",
            next: "Volgende",
            today: "Vandag",
            year: "Jaar",
            month: "Maand",
            week: "Week",
            day: "Dag",
            list: "Agenda"
        },
        allDayHtml: "Heeldag",
        eventLimitText: "Addisionele",
        noEventsMessage: "Daar is geen gebeurtenisse nie"
    }, {
        code: "ar-dz",
        week: {
            dow: 0,
            doy: 4
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar-kw",
        week: {
            dow: 0,
            doy: 12
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar-ly",
        week: {
            dow: 6,
            doy: 12
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar-ma",
        week: {
            dow: 6,
            doy: 12
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar-sa",
        week: {
            dow: 0,
            doy: 6
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar-tn",
        week: {
            dow: 1,
            doy: 4
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "ar",
        week: {
            dow: 6,
            doy: 12
        },
        dir: "rtl",
        buttonText: {
            prev: "السابق",
            next: "التالي",
            today: "اليوم",
            month: "شهر",
            week: "أسبوع",
            day: "يوم",
            list: "أجندة"
        },
        weekLabel: "أسبوع",
        allDayText: "اليوم كله",
        eventLimitText: "أخرى",
        noEventsMessage: "أي أحداث لعرض"
    }, {
        code: "bg",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "назад",
            next: "напред",
            today: "днес",
            month: "Месец",
            week: "Седмица",
            day: "Ден",
            list: "График"
        },
        allDayText: "Цял ден",
        eventLimitText: function (e) {
            return "+още " + e
        },
        noEventsMessage: "Няма събития за показване"
    }, {
        code: "bs",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Prošli",
            next: "Sljedeći",
            today: "Danas",
            month: "Mjesec",
            week: "Sedmica",
            day: "Dan",
            list: "Raspored"
        },
        weekLabel: "Sed",
        allDayText: "Cijeli dan",
        eventLimitText: function (e) {
            return "+ još " + e
        },
        noEventsMessage: "Nema događaja za prikazivanje"
    }, {
        code: "ca",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Anterior",
            next: "Següent",
            today: "Avui",
            month: "Mes",
            week: "Setmana",
            day: "Dia",
            list: "Agenda"
        },
        weekLabel: "Set",
        allDayText: "Tot el dia",
        eventLimitText: "més",
        noEventsMessage: "No hi ha esdeveniments per mostrar"
    }, {
        code: "cs",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Dříve",
            next: "Později",
            today: "Nyní",
            month: "Měsíc",
            week: "Týden",
            day: "Den",
            list: "Agenda"
        },
        weekLabel: "Týd",
        allDayText: "Celý den",
        eventLimitText: function (e) {
            return "+další: " + e
        },
        noEventsMessage: "Žádné akce k zobrazení"
    }, {
        code: "da",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Forrige",
            next: "Næste",
            today: "Idag",
            month: "Måned",
            week: "Uge",
            day: "Dag",
            list: "Agenda"
        },
        weekLabel: "Uge",
        allDayText: "Hele dagen",
        eventLimitText: "flere",
        noEventsMessage: "Ingen arrangementer at vise"
    }, {
        code: "de",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Zurück",
            next: "Vor",
            today: "Heute",
            year: "Jahr",
            month: "Monat",
            week: "Woche",
            day: "Tag",
            list: "Terminübersicht"
        },
        weekLabel: "KW",
        allDayText: "Ganztägig",
        eventLimitText: function (e) {
            return "+ weitere " + e
        },
        noEventsMessage: "Keine Ereignisse anzuzeigen"
    }, {
        code: "el",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Προηγούμενος",
            next: "Επόμενος",
            today: "Σήμερα",
            month: "Μήνας",
            week: "Εβδομάδα",
            day: "Ημέρα",
            list: "Ατζέντα"
        },
        weekLabel: "Εβδ",
        allDayText: "Ολοήμερο",
        eventLimitText: "περισσότερα",
        noEventsMessage: "Δεν υπάρχουν γεγονότα για να εμφανιστεί"
    }, {
        code: "en-au",
        week: {
            dow: 1,
            doy: 4
        }
    }, {
        code: "en-gb",
        week: {
            dow: 1,
            doy: 4
        }
    }, {
        code: "en-nz",
        week: {
            dow: 1,
            doy: 4
        }
    }, {
        code: "es",
        week: {
            dow: 0,
            doy: 6
        },
        buttonText: {
            prev: "Ant",
            next: "Sig",
            today: "Hoy",
            month: "Mes",
            week: "Semana",
            day: "Día",
            list: "Agenda"
        },
        weekLabel: "Sm",
        allDayHtml: "Todo<br/>el día",
        eventLimitText: "más",
        noEventsMessage: "No hay eventos para mostrar"
    }, {
        code: "es",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Ant",
            next: "Sig",
            today: "Hoy",
            month: "Mes",
            week: "Semana",
            day: "Día",
            list: "Agenda"
        },
        weekLabel: "Sm",
        allDayHtml: "Todo<br/>el día",
        eventLimitText: "más",
        noEventsMessage: "No hay eventos para mostrar"
    }, {
        code: "et",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Eelnev",
            next: "Järgnev",
            today: "Täna",
            month: "Kuu",
            week: "Nädal",
            day: "Päev",
            list: "Päevakord"
        },
        weekLabel: "näd",
        allDayText: "Kogu päev",
        eventLimitText: function (e) {
            return "+ veel " + e
        },
        noEventsMessage: "Kuvamiseks puuduvad sündmused"
    }, {
        code: "eu",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Aur",
            next: "Hur",
            today: "Gaur",
            month: "Hilabetea",
            week: "Astea",
            day: "Eguna",
            list: "Agenda"
        },
        weekLabel: "As",
        allDayHtml: "Egun<br/>osoa",
        eventLimitText: "gehiago",
        noEventsMessage: "Ez dago ekitaldirik erakusteko"
    }, {
        code: "fa",
        week: {
            dow: 6,
            doy: 12
        },
        dir: "rtl",
        buttonText: {
            prev: "قبلی",
            next: "بعدی",
            today: "امروز",
            month: "ماه",
            week: "هفته",
            day: "روز",
            list: "برنامه"
        },
        weekLabel: "هف",
        allDayText: "تمام روز",
        eventLimitText: function (e) {
            return "بیش از " + e
        },
        noEventsMessage: "هیچ رویدادی به نمایش"
    }, {
        code: "fi",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Edellinen",
            next: "Seuraava",
            today: "Tänään",
            month: "Kuukausi",
            week: "Viikko",
            day: "Päivä",
            list: "Tapahtumat"
        },
        weekLabel: "Vk",
        allDayText: "Koko päivä",
        eventLimitText: "lisää",
        noEventsMessage: "Ei näytettäviä tapahtumia"
    }, {
        code: "fr",
        buttonText: {
            prev: "Précédent",
            next: "Suivant",
            today: "Aujourd'hui",
            year: "Année",
            month: "Mois",
            week: "Semaine",
            day: "Jour",
            list: "Mon planning"
        },
        weekLabel: "Sem.",
        allDayHtml: "Toute la<br/>journée",
        eventLimitText: "en plus",
        noEventsMessage: "Aucun événement à afficher"
    }, {
        code: "fr-ch",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Précédent",
            next: "Suivant",
            today: "Courant",
            year: "Année",
            month: "Mois",
            week: "Semaine",
            day: "Jour",
            list: "Mon planning"
        },
        weekLabel: "Sm",
        allDayHtml: "Toute la<br/>journée",
        eventLimitText: "en plus",
        noEventsMessage: "Aucun événement à afficher"
    }, {
        code: "fr",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Précédent",
            next: "Suivant",
            today: "Aujourd'hui",
            year: "Année",
            month: "Mois",
            week: "Semaine",
            day: "Jour",
            list: "Mon planning"
        },
        weekLabel: "Sem.",
        allDayHtml: "Toute la<br/>journée",
        eventLimitText: "en plus",
        noEventsMessage: "Aucun événement à afficher"
    }, {
        code: "gl",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Ant",
            next: "Seg",
            today: "Hoxe",
            month: "Mes",
            week: "Semana",
            day: "Día",
            list: "Axenda"
        },
        weekLabel: "Sm",
        allDayHtml: "Todo<br/>o día",
        eventLimitText: "máis",
        noEventsMessage: "Non hai eventos para amosar"
    }, {
        code: "he",
        dir: "rtl",
        buttonText: {
            prev: "הקודם",
            next: "הבא",
            today: "היום",
            month: "חודש",
            week: "שבוע",
            day: "יום",
            list: "סדר יום"
        },
        allDayText: "כל היום",
        eventLimitText: "אחר",
        noEventsMessage: "אין אירועים להצגה",
        weekLabel: "שבוע"
    }, {
        code: "hi",
        week: {
            dow: 0,
            doy: 6
        },
        buttonText: {
            prev: "पिछला",
            next: "अगला",
            today: "आज",
            month: "महीना",
            week: "सप्ताह",
            day: "दिन",
            list: "कार्यसूची"
        },
        weekLabel: "हफ्ता",
        allDayText: "सभी दिन",
        eventLimitText: function (e) {
            return "+अधिक " + e
        },
        noEventsMessage: "कोई घटनाओं को प्रदर्शित करने के लिए"
    }, {
        code: "hr",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Prijašnji",
            next: "Sljedeći",
            today: "Danas",
            month: "Mjesec",
            week: "Tjedan",
            day: "Dan",
            list: "Raspored"
        },
        weekLabel: "Tje",
        allDayText: "Cijeli dan",
        eventLimitText: function (e) {
            return "+ još " + e
        },
        noEventsMessage: "Nema događaja za prikaz"
    }, {
        code: "hu",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "vissza",
            next: "előre",
            today: "ma",
            month: "Hónap",
            week: "Hét",
            day: "Nap",
            list: "Napló"
        },
        weekLabel: "Hét",
        allDayText: "Egész nap",
        eventLimitText: "további",
        noEventsMessage: "Nincs megjeleníthető esemény"
    }, {
        code: "id",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "mundur",
            next: "maju",
            today: "hari ini",
            month: "Bulan",
            week: "Minggu",
            day: "Hari",
            list: "Agenda"
        },
        weekLabel: "Mg",
        allDayHtml: "Sehari<br/>penuh",
        eventLimitText: "lebih",
        noEventsMessage: "Tidak ada acara untuk ditampilkan"
    }, {
        code: "is",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Fyrri",
            next: "Næsti",
            today: "Í dag",
            month: "Mánuður",
            week: "Vika",
            day: "Dagur",
            list: "Dagskrá"
        },
        weekLabel: "Vika",
        allDayHtml: "Allan<br/>daginn",
        eventLimitText: "meira",
        noEventsMessage: "Engir viðburðir til að sýna"
    }, {
        code: "it",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Prec",
            next: "Succ",
            today: "Oggi",
            month: "Mese",
            week: "Settimana",
            day: "Giorno",
            list: "Agenda"
        },
        weekLabel: "Sm",
        allDayHtml: "Tutto il<br/>giorno",
        eventLimitText: function (e) {
            return "+altri " + e
        },
        noEventsMessage: "Non ci sono eventi da visualizzare"
    }, {
        code: "ja",
        buttonText: {
            prev: "前",
            next: "次",
            today: "今日",
            month: "月",
            week: "週",
            day: "日",
            list: "予定リスト"
        },
        weekLabel: "週",
        allDayText: "終日",
        eventLimitText: function (e) {
            return "他 " + e + " 件"
        },
        noEventsMessage: "表示する予定はありません"
    }, {
        code: "ka",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "წინა",
            next: "შემდეგი",
            today: "დღეს",
            month: "თვე",
            week: "კვირა",
            day: "დღე",
            list: "დღის წესრიგი"
        },
        weekLabel: "კვ",
        allDayText: "მთელი დღე",
        eventLimitText: function (e) {
            return "+ კიდევ " + e
        },
        noEventsMessage: "ღონისძიებები არ არის"
    }, {
        code: "kk",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Алдыңғы",
            next: "Келесі",
            today: "Бүгін",
            month: "Ай",
            week: "Апта",
            day: "Күн",
            list: "Күн тәртібі"
        },
        weekLabel: "Не",
        allDayText: "Күні бойы",
        eventLimitText: function (e) {
            return "+ тағы " + e
        },
        noEventsMessage: "Көрсету үшін оқиғалар жоқ"
    }, {
        code: "ko",
        buttonText: {
            prev: "이전달",
            next: "다음달",
            today: "오늘",
            month: "월",
            week: "주",
            day: "일",
            list: "일정목록"
        },
        weekLabel: "주",
        allDayText: "종일",
        eventLimitText: "개",
        noEventsMessage: "일정이 없습니다"
    }, {
        code: "lb",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Zréck",
            next: "Weider",
            today: "Haut",
            month: "Mount",
            week: "Woch",
            day: "Dag",
            list: "Terminiwwersiicht"
        },
        weekLabel: "W",
        allDayText: "Ganzen Dag",
        eventLimitText: "méi",
        noEventsMessage: "Nee Evenementer ze affichéieren"
    }, {
        code: "lt",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Atgal",
            next: "Pirmyn",
            today: "Šiandien",
            month: "Mėnuo",
            week: "Savaitė",
            day: "Diena",
            list: "Darbotvarkė"
        },
        weekLabel: "SAV",
        allDayText: "Visą dieną",
        eventLimitText: "daugiau",
        noEventsMessage: "Nėra įvykių rodyti"
    }, {
        code: "lv",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Iepr.",
            next: "Nāk.",
            today: "Šodien",
            month: "Mēnesis",
            week: "Nedēļa",
            day: "Diena",
            list: "Dienas kārtība"
        },
        weekLabel: "Ned.",
        allDayText: "Visu dienu",
        eventLimitText: function (e) {
            return "+vēl " + e
        },
        noEventsMessage: "Nav notikumu"
    }, {
        code: "mk",
        buttonText: {
            prev: "претходно",
            next: "следно",
            today: "Денес",
            month: "Месец",
            week: "Недела",
            day: "Ден",
            list: "График"
        },
        weekLabel: "Сед",
        allDayText: "Цел ден",
        eventLimitText: function (e) {
            return "+повеќе " + e
        },
        noEventsMessage: "Нема настани за прикажување"
    }, {
        code: "ms",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Sebelum",
            next: "Selepas",
            today: "hari ini",
            month: "Bulan",
            week: "Minggu",
            day: "Hari",
            list: "Agenda"
        },
        weekLabel: "Mg",
        allDayText: "Sepanjang hari",
        eventLimitText: function (e) {
            return "masih ada " + e + " acara"
        },
        noEventsMessage: "Tiada peristiwa untuk dipaparkan"
    }, {
        code: "nb",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Forrige",
            next: "Neste",
            today: "I dag",
            month: "Måned",
            week: "Uke",
            day: "Dag",
            list: "Agenda"
        },
        weekLabel: "Uke",
        allDayText: "Hele dagen",
        eventLimitText: "til",
        noEventsMessage: "Ingen hendelser å vise"
    }, {
        code: "nl",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Voorgaand",
            next: "Volgende",
            today: "Vandaag",
            year: "Jaar",
            month: "Maand",
            week: "Week",
            day: "Dag",
            list: "Agenda"
        },
        allDayText: "Hele dag",
        eventLimitText: "extra",
        noEventsMessage: "Geen evenementen om te laten zien"
    }, {
        code: "nn",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Førre",
            next: "Neste",
            today: "I dag",
            month: "Månad",
            week: "Veke",
            day: "Dag",
            list: "Agenda"
        },
        weekLabel: "Veke",
        allDayText: "Heile dagen",
        eventLimitText: "til",
        noEventsMessage: "Ingen hendelser å vise"
    }, {
        code: "pl",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Poprzedni",
            next: "Następny",
            today: "Dziś",
            month: "Miesiąc",
            week: "Tydzień",
            day: "Dzień",
            list: "Plan dnia"
        },
        weekLabel: "Tydz",
        allDayText: "Cały dzień",
        eventLimitText: "więcej",
        noEventsMessage: "Brak wydarzeń do wyświetlenia"
    }, {
        code: "pt-br",
        buttonText: {
            prev: "Anterior",
            next: "Próximo",
            today: "Hoje",
            month: "Mês",
            week: "Semana",
            day: "Dia",
            list: "Compromissos"
        },
        weekLabel: "Sm",
        allDayText: "dia inteiro",
        eventLimitText: function (e) {
            return "mais +" + e
        },
        noEventsMessage: "Não há eventos para mostrar"
    }, {
        code: "pt",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Anterior",
            next: "Seguinte",
            today: "Hoje",
            month: "Mês",
            week: "Semana",
            day: "Dia",
            list: "Agenda"
        },
        weekLabel: "Sem",
        allDayText: "Todo o dia",
        eventLimitText: "mais",
        noEventsMessage: "Não há eventos para mostrar"
    }, {
        code: "ro",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "precedentă",
            next: "următoare",
            today: "Azi",
            month: "Lună",
            week: "Săptămână",
            day: "Zi",
            list: "Agendă"
        },
        weekLabel: "Săpt",
        allDayText: "Toată ziua",
        eventLimitText: function (e) {
            return "+alte " + e
        },
        noEventsMessage: "Nu există evenimente de afișat"
    }, {
        code: "ru",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Пред",
            next: "След",
            today: "Сегодня",
            month: "Месяц",
            week: "Неделя",
            day: "День",
            list: "Повестка дня"
        },
        weekLabel: "Нед",
        allDayText: "Весь день",
        eventLimitText: function (e) {
            return "+ ещё " + e
        },
        noEventsMessage: "Нет событий для отображения"
    }, {
        code: "sk",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Predchádzajúci",
            next: "Nasledujúci",
            today: "Dnes",
            month: "Mesiac",
            week: "Týždeň",
            day: "Deň",
            list: "Rozvrh"
        },
        weekLabel: "Ty",
        allDayText: "Celý deň",
        eventLimitText: function (e) {
            return "+ďalšie: " + e
        },
        noEventsMessage: "Žiadne akcie na zobrazenie"
    }, {
        code: "sl",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Prejšnji",
            next: "Naslednji",
            today: "Trenutni",
            month: "Mesec",
            week: "Teden",
            day: "Dan",
            list: "Dnevni red"
        },
        weekLabel: "Teden",
        allDayText: "Ves dan",
        eventLimitText: "več",
        noEventsMessage: "Ni dogodkov za prikaz"
    }, {
        code: "sq",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "mbrapa",
            next: "Përpara",
            today: "sot",
            month: "Muaj",
            week: "Javë",
            day: "Ditë",
            list: "Listë"
        },
        weekLabel: "Ja",
        allDayHtml: "Gjithë<br/>ditën",
        eventLimitText: function (e) {
            return "+më tepër " + e
        },
        noEventsMessage: "Nuk ka evente për të shfaqur"
    }, {
        code: "sr-cyrl",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Претходна",
            next: "следећи",
            today: "Данас",
            month: "Месец",
            week: "Недеља",
            day: "Дан",
            list: "Планер"
        },
        weekLabel: "Сед",
        allDayText: "Цео дан",
        eventLimitText: function (e) {
            return "+ још " + e
        },
        noEventsMessage: "Нема догађаја за приказ"
    }, {
        code: "sr",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Prethodna",
            next: "Sledeći",
            today: "Danas",
            month: "Mеsеc",
            week: "Nеdеlja",
            day: "Dan",
            list: "Planеr"
        },
        weekLabel: "Sed",
        allDayText: "Cеo dan",
        eventLimitText: function (e) {
            return "+ još " + e
        },
        noEventsMessage: "Nеma događaja za prikaz"
    }, {
        code: "sv",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Förra",
            next: "Nästa",
            today: "Idag",
            month: "Månad",
            week: "Vecka",
            day: "Dag",
            list: "Program"
        },
        weekLabel: "v.",
        allDayText: "Heldag",
        eventLimitText: "till",
        noEventsMessage: "Inga händelser att visa"
    }, {
        code: "th",
        buttonText: {
            prev: "ย้อน",
            next: "ถัดไป",
            today: "วันนี้",
            month: "เดือน",
            week: "สัปดาห์",
            day: "วัน",
            list: "แผนงาน"
        },
        allDayText: "ตลอดวัน",
        eventLimitText: "เพิ่มเติม",
        noEventsMessage: "ไม่มีกิจกรรมที่จะแสดง"
    }, {
        code: "tr",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "geri",
            next: "ileri",
            today: "bugün",
            month: "Ay",
            week: "Hafta",
            day: "Gün",
            list: "Ajanda"
        },
        weekLabel: "Hf",
        allDayText: "Tüm gün",
        eventLimitText: "daha fazla",
        noEventsMessage: "Gösterilecek etkinlik yok"
    }, {
        code: "uk",
        week: {
            dow: 1,
            doy: 7
        },
        buttonText: {
            prev: "Попередній",
            next: "далі",
            today: "Сьогодні",
            month: "Місяць",
            week: "Тиждень",
            day: "День",
            list: "Порядок денний"
        },
        weekLabel: "Тиж",
        allDayText: "Увесь день",
        eventLimitText: function (e) {
            return "+ще " + e + "..."
        },
        noEventsMessage: "Немає подій для відображення"
    }, {
        code: "vi",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "Trước",
            next: "Tiếp",
            today: "Hôm nay",
            month: "Tháng",
            week: "Tuần",
            day: "Ngày",
            list: "Lịch biểu"
        },
        weekLabel: "Tu",
        allDayText: "Cả ngày",
        eventLimitText: function (e) {
            return "+ thêm " + e
        },
        noEventsMessage: "Không có sự kiện để hiển thị"
    }, {
        code: "zh-cn",
        week: {
            dow: 1,
            doy: 4
        },
        buttonText: {
            prev: "上月",
            next: "下月",
            today: "今天",
            month: "月",
            week: "周",
            day: "日",
            list: "日程"
        },
        weekLabel: "周",
        allDayText: "全天",
        eventLimitText: function (e) {
            return "另外 " + e + " 个"
        },
        noEventsMessage: "没有事件显示"
    }, {
        code: "zh-tw",
        buttonText: {
            prev: "上月",
            next: "下月",
            today: "今天",
            month: "月",
            week: "週",
            day: "天",
            list: "活動列表"
        },
        weekLabel: "周",
        allDayText: "整天",
        eventLimitText: "顯示更多",
        noEventsMessage: "没有任何活動"
    }]
});

// interactio

!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports, require("@fullcalendar/core")) : "function" == typeof define && define.amd ? define(["exports", "@fullcalendar/core"], t) : (e = e || self, t(e.FullCalendarInteraction = {}, e.FullCalendar))
}(this, function (e, t) {
    "use strict";

    function n(e, t) {
        function n() {
            this.constructor = e
        }

        m(e, t), e.prototype = null === t ? Object.create(t) : (n.prototype = t.prototype, new n)
    }

    function r(e) {
        return 0 === e.button && !e.ctrlKey
    }

    function i() {
        y++, setTimeout(function () {
            y--
        }, t.config.touchMouseIgnoreWait)
    }

    function o() {
        D++ || window.addEventListener("touchmove", l, {
            passive: !1
        })
    }

    function a() {
        --D || window.removeEventListener("touchmove", l, {
            passive: !1
        })
    }

    function l(e) {
        w && e.preventDefault()
    }

    function s(e) {
        var t = e.tagName;
        return "HTML" === t || "BODY" === t
    }

    function c(e, n) {
        return !e && !n || Boolean(e) === Boolean(n) && t.isDateSpansEqual(e.dateSpan, n.dateSpan)
    }

    function d(e) {
        var t = e.opt("selectLongPressDelay");
        return null == t && (t = e.opt("longPressDelay")), t
    }

    function u(e, n, r) {
        var i = e.dateSpan,
            o = n.dateSpan,
            a = [i.range.start, i.range.end, o.range.start, o.range.end];
        a.sort(t.compareNumbers);
        for (var l = {}, s = 0, c = r; s < c.length; s++) {
            var d = c[s],
                u = d(e, n);
            if (!1 === u) return null;
            u && S(l, u)
        }
        return l.range = {
            start: a[0],
            end: a[3]
        }, l.allDay = i.allDay, l
    }

    function g(e, n, r) {
        var i = e.dateSpan,
            o = n.dateSpan,
            a = i.range.start,
            l = o.range.start,
            s = {};
        i.allDay !== o.allDay && (s.allDay = o.allDay, s.hasEnd = n.component.opt("allDayMaintainDuration"), o.allDay && (a = t.startOfDay(a)));
        var c = t.diffDates(a, l, e.component.dateEnv, e.component === n.component ? e.component.largeUnit : null);
        c.milliseconds && (s.allDay = !1);
        for (var d = {
            startDelta: c,
            endDelta: c,
            standardProps: s
        }, u = 0, g = r; u < g.length; u++) {
            (0, g[u])(d, e, n)
        }
        return d
    }

    function h(e) {
        var t = e.opt("eventLongPressDelay");
        return null == t && (t = e.opt("longPressDelay")), t
    }

    function p(e, n, r, i, o) {
        for (var a = e.component.dateEnv, l = e.dateSpan.range.start, s = n.dateSpan.range.start, c = t.diffDates(l, s, a, e.component.largeUnit), d = {}, u = 0, g = o; u < g.length; u++) {
            var h = g[u],
                p = h(e, n);
            if (!1 === p) return null;
            p && S(d, p)
        }
        if (r) {
            if (a.add(i.start, c) < i.end) return d.startDelta = c, d
        } else if (a.add(i.end, c) > i.start) return d.endDelta = c, d;
        return null
    }

    function v(e, n, r) {
        for (var i = S({}, n.leftoverProps), o = 0, a = r.pluginSystem.hooks.externalDefTransforms; o < a.length; o++) {
            var l = a[o];
            S(i, l(e, n))
        }
        var s = t.parseEventDef(i, n.sourceId, e.allDay, r.opt("forceEventDuration") || Boolean(n.duration), r),
            c = e.range.start;
        e.allDay && n.startTime && (c = r.dateEnv.add(c, n.startTime));
        var d = n.duration ? r.dateEnv.add(c, n.duration) : r.getDefaultEventEnd(e.allDay, c);
        return {
            def: s,
            instance: t.createEventInstance(s.defId, {
                start: c,
                end: d
            })
        }
    }

    function f(e) {
        var n = E(e, "event"),
            r = n ? JSON.parse(n) : {
                create: !1
            };
        return t.parseDragMeta(r)
    }

    function E(e, n) {
        var r = t.config.dataAttrPrefix,
            i = (r ? r + "-" : "") + n;
        return e.getAttribute("data-" + i) || ""
    }

    /*! *****************************************************************************
        Copyright (c) Microsoft Corporation. All rights reserved.
        Licensed under the Apache License, Version 2.0 (the "License"); you may not use
        this file except in compliance with the License. You may obtain a copy of the
        License at http://www.apache.org/licenses/LICENSE-2.0

        THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
        KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
        WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
        MERCHANTABLITY OR NON-INFRINGEMENT.

        See the Apache Version 2.0 License for specific language governing permissions
        and limitations under the License.
        ***************************************************************************** */
    var m = function (e, t) {
            return (m = Object.setPrototypeOf || {
                    __proto__: []
                }
                instanceof Array && function (e, t) {
                    e.__proto__ = t
                } || function (e, t) {
                    for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n])
                })(e, t)
        },
        S = function () {
            return S = Object.assign || function (e) {
                for (var t, n = 1, r = arguments.length; n < r; n++) {
                    t = arguments[n];
                    for (var i in t) Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i])
                }
                return e
            }, S.apply(this, arguments)
        };
    t.config.touchMouseIgnoreWait = 500;
    var y = 0,
        D = 0,
        w = !1,
        T = function () {
            function e(e) {
                var n = this;
                this.subjectEl = null, this.downEl = null, this.selector = "", this.handleSelector = "", this.shouldIgnoreMove = !1, this.shouldWatchScroll = !0, this.isDragging = !1, this.isTouchDragging = !1, this.wasTouchScroll = !1, this.handleMouseDown = function (e) {
                    if (!n.shouldIgnoreMouse() && r(e) && n.tryStart(e)) {
                        var t = n.createEventFromMouse(e, !0);
                        n.emitter.trigger("pointerdown", t), n.initScrollWatch(t), n.shouldIgnoreMove || document.addEventListener("mousemove", n.handleMouseMove), document.addEventListener("mouseup", n.handleMouseUp)
                    }
                }, this.handleMouseMove = function (e) {
                    var t = n.createEventFromMouse(e);
                    n.recordCoords(t), n.emitter.trigger("pointermove", t)
                }, this.handleMouseUp = function (e) {
                    document.removeEventListener("mousemove", n.handleMouseMove), document.removeEventListener("mouseup", n.handleMouseUp), n.emitter.trigger("pointerup", n.createEventFromMouse(e)), n.cleanup()
                }, this.handleTouchStart = function (e) {
                    if (n.tryStart(e)) {
                        n.isTouchDragging = !0;
                        var t = n.createEventFromTouch(e, !0);
                        n.emitter.trigger("pointerdown", t), n.initScrollWatch(t);
                        var r = e.target;
                        n.shouldIgnoreMove || r.addEventListener("touchmove", n.handleTouchMove), r.addEventListener("touchend", n.handleTouchEnd), r.addEventListener("touchcancel", n.handleTouchEnd), window.addEventListener("scroll", n.handleTouchScroll, !0)
                    }
                }, this.handleTouchMove = function (e) {
                    var t = n.createEventFromTouch(e);
                    n.recordCoords(t), n.emitter.trigger("pointermove", t)
                }, this.handleTouchEnd = function (e) {
                    if (n.isDragging) {
                        var t = e.target;
                        t.removeEventListener("touchmove", n.handleTouchMove), t.removeEventListener("touchend", n.handleTouchEnd), t.removeEventListener("touchcancel", n.handleTouchEnd), window.removeEventListener("scroll", n.handleTouchScroll, !0), n.emitter.trigger("pointerup", n.createEventFromTouch(e)), n.cleanup(), n.isTouchDragging = !1, i()
                    }
                }, this.handleTouchScroll = function () {
                    n.wasTouchScroll = !0
                }, this.handleScroll = function (e) {
                    if (!n.shouldIgnoreMove) {
                        var t = window.pageXOffset - n.prevScrollX + n.prevPageX,
                            r = window.pageYOffset - n.prevScrollY + n.prevPageY;
                        n.emitter.trigger("pointermove", {
                            origEvent: e,
                            isTouch: n.isTouchDragging,
                            subjectEl: n.subjectEl,
                            pageX: t,
                            pageY: r,
                            deltaX: t - n.origPageX,
                            deltaY: r - n.origPageY
                        })
                    }
                }, this.containerEl = e, this.emitter = new t.EmitterMixin, e.addEventListener("mousedown", this.handleMouseDown), e.addEventListener("touchstart", this.handleTouchStart, {
                    passive: !0
                }), o()
            }

            return e.prototype.destroy = function () {
                this.containerEl.removeEventListener("mousedown", this.handleMouseDown), this.containerEl.removeEventListener("touchstart", this.handleTouchStart, {
                    passive: !0
                }), a()
            }, e.prototype.tryStart = function (e) {
                var n = this.querySubjectEl(e),
                    r = e.target;
                return !(!n || this.handleSelector && !t.elementClosest(r, this.handleSelector)) && (this.subjectEl = n, this.downEl = r, this.isDragging = !0, this.wasTouchScroll = !1, !0)
            }, e.prototype.cleanup = function () {
                w = !1, this.isDragging = !1, this.subjectEl = null, this.downEl = null, this.destroyScrollWatch()
            }, e.prototype.querySubjectEl = function (e) {
                return this.selector ? t.elementClosest(e.target, this.selector) : this.containerEl
            }, e.prototype.shouldIgnoreMouse = function () {
                return y || this.isTouchDragging
            }, e.prototype.cancelTouchScroll = function () {
                this.isDragging && (w = !0)
            }, e.prototype.initScrollWatch = function (e) {
                this.shouldWatchScroll && (this.recordCoords(e), window.addEventListener("scroll", this.handleScroll, !0))
            }, e.prototype.recordCoords = function (e) {
                this.shouldWatchScroll && (this.prevPageX = e.pageX, this.prevPageY = e.pageY, this.prevScrollX = window.pageXOffset, this.prevScrollY = window.pageYOffset)
            }, e.prototype.destroyScrollWatch = function () {
                this.shouldWatchScroll && window.removeEventListener("scroll", this.handleScroll, !0)
            }, e.prototype.createEventFromMouse = function (e, t) {
                var n = 0,
                    r = 0;
                return t ? (this.origPageX = e.pageX, this.origPageY = e.pageY) : (n = e.pageX - this.origPageX, r = e.pageY - this.origPageY), {
                    origEvent: e,
                    isTouch: !1,
                    subjectEl: this.subjectEl,
                    pageX: e.pageX,
                    pageY: e.pageY,
                    deltaX: n,
                    deltaY: r
                }
            }, e.prototype.createEventFromTouch = function (e, t) {
                var n, r, i = e.touches,
                    o = 0,
                    a = 0;
                return i && i.length ? (n = i[0].pageX, r = i[0].pageY) : (n = e.pageX, r = e.pageY), t ? (this.origPageX = n, this.origPageY = r) : (o = n - this.origPageX, a = r - this.origPageY), {
                    origEvent: e,
                    isTouch: !0,
                    subjectEl: this.subjectEl,
                    pageX: n,
                    pageY: r,
                    deltaX: o,
                    deltaY: a
                }
            }, e
        }(),
        M = function () {
            function e() {
                this.isVisible = !1, this.sourceEl = null, this.mirrorEl = null, this.sourceElRect = null, this.parentNode = document.body, this.zIndex = 9999, this.revertDuration = 0
            }

            return e.prototype.start = function (e, t, n) {
                this.sourceEl = e, this.sourceElRect = this.sourceEl.getBoundingClientRect(), this.origScreenX = t - window.pageXOffset, this.origScreenY = n - window.pageYOffset, this.deltaX = 0, this.deltaY = 0, this.updateElPosition()
            }, e.prototype.handleMove = function (e, t) {
                this.deltaX = e - window.pageXOffset - this.origScreenX, this.deltaY = t - window.pageYOffset - this.origScreenY, this.updateElPosition()
            }, e.prototype.setIsVisible = function (e) {
                e ? this.isVisible || (this.mirrorEl && (this.mirrorEl.style.display = ""), this.isVisible = e, this.updateElPosition()) : this.isVisible && (this.mirrorEl && (this.mirrorEl.style.display = "none"), this.isVisible = e)
            }, e.prototype.stop = function (e, t) {
                var n = this,
                    r = function () {
                        n.cleanup(), t()
                    };
                e && this.mirrorEl && this.isVisible && this.revertDuration && (this.deltaX || this.deltaY) ? this.doRevertAnimation(r, this.revertDuration) : setTimeout(r, 0)
            }, e.prototype.doRevertAnimation = function (e, n) {
                var r = this.mirrorEl,
                    i = this.sourceEl.getBoundingClientRect();
                r.style.transition = "top " + n + "ms,left " + n + "ms", t.applyStyle(r, {
                    left: i.left,
                    top: i.top
                }), t.whenTransitionDone(r, function () {
                    r.style.transition = "", e()
                })
            }, e.prototype.cleanup = function () {
                this.mirrorEl && (t.removeElement(this.mirrorEl), this.mirrorEl = null), this.sourceEl = null
            }, e.prototype.updateElPosition = function () {
                this.sourceEl && this.isVisible && t.applyStyle(this.getMirrorEl(), {
                    left: this.sourceElRect.left + this.deltaX,
                    top: this.sourceElRect.top + this.deltaY
                })
            }, e.prototype.getMirrorEl = function () {
                var e = this.sourceElRect,
                    n = this.mirrorEl;
                return n || (n = this.mirrorEl = this.sourceEl.cloneNode(!0), n.classList.add("fc-unselectable"), n.classList.add("fc-dragging"), t.applyStyle(n, {
                    position: "fixed",
                    zIndex: this.zIndex,
                    visibility: "",
                    boxSizing: "border-box",
                    width: e.right - e.left,
                    height: e.bottom - e.top,
                    right: "auto",
                    bottom: "auto",
                    margin: 0
                }), this.parentNode.appendChild(n)), n
            }, e
        }(),
        b = function (e) {
            function t(t, n) {
                var r = e.call(this) || this;
                return r.handleScroll = function () {
                    r.scrollTop = r.scrollController.getScrollTop(), r.scrollLeft = r.scrollController.getScrollLeft(), r.handleScrollChange()
                }, r.scrollController = t, r.doesListening = n, r.scrollTop = r.origScrollTop = t.getScrollTop(), r.scrollLeft = r.origScrollLeft = t.getScrollLeft(), r.scrollWidth = t.getScrollWidth(), r.scrollHeight = t.getScrollHeight(), r.clientWidth = t.getClientWidth(), r.clientHeight = t.getClientHeight(), r.clientRect = r.computeClientRect(), r.doesListening && r.getEventTarget().addEventListener("scroll", r.handleScroll), r
            }

            return n(t, e), t.prototype.destroy = function () {
                this.doesListening && this.getEventTarget().removeEventListener("scroll", this.handleScroll)
            }, t.prototype.getScrollTop = function () {
                return this.scrollTop
            }, t.prototype.getScrollLeft = function () {
                return this.scrollLeft
            }, t.prototype.setScrollTop = function (e) {
                this.scrollController.setScrollTop(e), this.doesListening || (this.scrollTop = Math.max(Math.min(e, this.getMaxScrollTop()), 0), this.handleScrollChange())
            }, t.prototype.setScrollLeft = function (e) {
                this.scrollController.setScrollLeft(e), this.doesListening || (this.scrollLeft = Math.max(Math.min(e, this.getMaxScrollLeft()), 0), this.handleScrollChange())
            }, t.prototype.getClientWidth = function () {
                return this.clientWidth
            }, t.prototype.getClientHeight = function () {
                return this.clientHeight
            }, t.prototype.getScrollWidth = function () {
                return this.scrollWidth
            }, t.prototype.getScrollHeight = function () {
                return this.scrollHeight
            }, t.prototype.handleScrollChange = function () {
            }, t
        }(t.ScrollController),
        C = function (e) {
            function r(n, r) {
                return e.call(this, new t.ElementScrollController(n), r) || this
            }

            return n(r, e), r.prototype.getEventTarget = function () {
                return this.scrollController.el
            }, r.prototype.computeClientRect = function () {
                return t.computeInnerRect(this.scrollController.el)
            }, r
        }(b),
        R = function (e) {
            function r(n) {
                return e.call(this, new t.WindowScrollController, n) || this
            }

            return n(r, e), r.prototype.getEventTarget = function () {
                return window
            }, r.prototype.computeClientRect = function () {
                return {
                    left: this.scrollLeft,
                    right: this.scrollLeft + this.clientWidth,
                    top: this.scrollTop,
                    bottom: this.scrollTop + this.clientHeight
                }
            }, r.prototype.handleScrollChange = function () {
                this.clientRect = this.computeClientRect()
            }, r
        }(b),
        I = "function" == typeof performance ? performance.now : Date.now,
        P = function () {
            function e() {
                var e = this;
                this.isEnabled = !0, this.scrollQuery = [window, ".fc-scroller"], this.edgeThreshold = 50, this.maxVelocity = 300, this.pointerScreenX = null, this.pointerScreenY = null, this.isAnimating = !1, this.scrollCaches = null, this.everMovedUp = !1, this.everMovedDown = !1, this.everMovedLeft = !1, this.everMovedRight = !1, this.animate = function () {
                    if (e.isAnimating) {
                        var t = e.computeBestEdge(e.pointerScreenX + window.pageXOffset, e.pointerScreenY + window.pageYOffset);
                        if (t) {
                            var n = I();
                            e.handleSide(t, (n - e.msSinceRequest) / 1e3), e.requestAnimation(n)
                        } else e.isAnimating = !1
                    }
                }
            }

            return e.prototype.start = function (e, t) {
                this.isEnabled && (this.scrollCaches = this.buildCaches(), this.pointerScreenX = null, this.pointerScreenY = null, this.everMovedUp = !1, this.everMovedDown = !1, this.everMovedLeft = !1, this.everMovedRight = !1, this.handleMove(e, t))
            }, e.prototype.handleMove = function (e, t) {
                if (this.isEnabled) {
                    var n = e - window.pageXOffset,
                        r = t - window.pageYOffset,
                        i = null === this.pointerScreenY ? 0 : r - this.pointerScreenY,
                        o = null === this.pointerScreenX ? 0 : n - this.pointerScreenX;
                    i < 0 ? this.everMovedUp = !0 : i > 0 && (this.everMovedDown = !0), o < 0 ? this.everMovedLeft = !0 : o > 0 && (this.everMovedRight = !0), this.pointerScreenX = n, this.pointerScreenY = r, this.isAnimating || (this.isAnimating = !0, this.requestAnimation(I()))
                }
            }, e.prototype.stop = function () {
                if (this.isEnabled) {
                    this.isAnimating = !1;
                    for (var e = 0, t = this.scrollCaches; e < t.length; e++) {
                        t[e].destroy()
                    }
                    this.scrollCaches = null
                }
            }, e.prototype.requestAnimation = function (e) {
                this.msSinceRequest = e, requestAnimationFrame(this.animate)
            }, e.prototype.handleSide = function (e, t) {
                var n = e.scrollCache,
                    r = this.edgeThreshold,
                    i = r - e.distance,
                    o = i * i / (r * r) * this.maxVelocity * t,
                    a = 1;
                switch (e.name) {
                    case "left":
                        a = -1;
                    case "right":
                        n.setScrollLeft(n.getScrollLeft() + o * a);
                        break;
                    case "top":
                        a = -1;
                    case "bottom":
                        n.setScrollTop(n.getScrollTop() + o * a)
                }
            }, e.prototype.computeBestEdge = function (e, t) {
                for (var n = this.edgeThreshold, r = null, i = 0, o = this.scrollCaches; i < o.length; i++) {
                    var a = o[i],
                        l = a.clientRect,
                        s = e - l.left,
                        c = l.right - e,
                        d = t - l.top,
                        u = l.bottom - t;
                    s >= 0 && c >= 0 && d >= 0 && u >= 0 && (d <= n && this.everMovedUp && a.canScrollUp() && (!r || r.distance > d) && (r = {
                        scrollCache: a,
                        name: "top",
                        distance: d
                    }), u <= n && this.everMovedDown && a.canScrollDown() && (!r || r.distance > u) && (r = {
                        scrollCache: a,
                        name: "bottom",
                        distance: u
                    }), s <= n && this.everMovedLeft && a.canScrollLeft() && (!r || r.distance > s) && (r = {
                        scrollCache: a,
                        name: "left",
                        distance: s
                    }), c <= n && this.everMovedRight && a.canScrollRight() && (!r || r.distance > c) && (r = {
                        scrollCache: a,
                        name: "right",
                        distance: c
                    }))
                }
                return r
            }, e.prototype.buildCaches = function () {
                return this.queryScrollEls().map(function (e) {
                    return e === window ? new R(!1) : new C(e, !1)
                })
            }, e.prototype.queryScrollEls = function () {
                for (var e = [], t = 0, n = this.scrollQuery; t < n.length; t++) {
                    var r = n[t];
                    "object" == typeof r ? e.push(r) : e.push.apply(e, Array.prototype.slice.call(document.querySelectorAll(r)))
                }
                return e
            }, e
        }(),
        L = function (e) {
            function r(n) {
                var r = e.call(this, n) || this;
                r.delay = null, r.minDistance = 0, r.touchScrollAllowed = !0, r.mirrorNeedsRevert = !1, r.isInteracting = !1, r.isDragging = !1, r.isDelayEnded = !1, r.isDistanceSurpassed = !1, r.delayTimeoutId = null, r.onPointerDown = function (e) {
                    r.isDragging || (r.isInteracting = !0, r.isDelayEnded = !1, r.isDistanceSurpassed = !1, t.preventSelection(document.body), t.preventContextMenu(document.body), e.isTouch || e.origEvent.preventDefault(), r.emitter.trigger("pointerdown", e), r.pointer.shouldIgnoreMove || (r.mirror.setIsVisible(!1), r.mirror.start(e.subjectEl, e.pageX, e.pageY), r.startDelay(e), r.minDistance || r.handleDistanceSurpassed(e)))
                }, r.onPointerMove = function (e) {
                    if (r.isInteracting) {
                        if (r.emitter.trigger("pointermove", e), !r.isDistanceSurpassed) {
                            var t = r.minDistance,
                                n = void 0,
                                i = e.deltaX,
                                o = e.deltaY;
                            n = i * i + o * o, n >= t * t && r.handleDistanceSurpassed(e)
                        }
                        r.isDragging && ("scroll" !== e.origEvent.type && (r.mirror.handleMove(e.pageX, e.pageY), r.autoScroller.handleMove(e.pageX, e.pageY)), r.emitter.trigger("dragmove", e))
                    }
                }, r.onPointerUp = function (e) {
                    r.isInteracting && (r.isInteracting = !1, t.allowSelection(document.body), t.allowContextMenu(document.body), r.emitter.trigger("pointerup", e), r.isDragging && (r.autoScroller.stop(), r.tryStopDrag(e)), r.delayTimeoutId && (clearTimeout(r.delayTimeoutId), r.delayTimeoutId = null))
                };
                var i = r.pointer = new T(n);
                return i.emitter.on("pointerdown", r.onPointerDown), i.emitter.on("pointermove", r.onPointerMove), i.emitter.on("pointerup", r.onPointerUp), r.mirror = new M, r.autoScroller = new P, r
            }

            return n(r, e), r.prototype.destroy = function () {
                this.pointer.destroy()
            }, r.prototype.startDelay = function (e) {
                var t = this;
                "number" == typeof this.delay ? this.delayTimeoutId = setTimeout(function () {
                    t.delayTimeoutId = null, t.handleDelayEnd(e)
                }, this.delay) : this.handleDelayEnd(e)
            }, r.prototype.handleDelayEnd = function (e) {
                this.isDelayEnded = !0, this.tryStartDrag(e)
            }, r.prototype.handleDistanceSurpassed = function (e) {
                this.isDistanceSurpassed = !0, this.tryStartDrag(e)
            }, r.prototype.tryStartDrag = function (e) {
                this.isDelayEnded && this.isDistanceSurpassed && (this.pointer.wasTouchScroll && !this.touchScrollAllowed || (this.isDragging = !0, this.mirrorNeedsRevert = !1, this.autoScroller.start(e.pageX, e.pageY), this.emitter.trigger("dragstart", e), !1 === this.touchScrollAllowed && this.pointer.cancelTouchScroll()))
            }, r.prototype.tryStopDrag = function (e) {
                this.mirror.stop(this.mirrorNeedsRevert, this.stopDrag.bind(this, e))
            }, r.prototype.stopDrag = function (e) {
                this.isDragging = !1, this.emitter.trigger("dragend", e)
            }, r.prototype.setIgnoreMove = function (e) {
                this.pointer.shouldIgnoreMove = e
            }, r.prototype.setMirrorIsVisible = function (e) {
                this.mirror.setIsVisible(e)
            }, r.prototype.setMirrorNeedsRevert = function (e) {
                this.mirrorNeedsRevert = e
            }, r.prototype.setAutoScrollEnabled = function (e) {
                this.autoScroller.isEnabled = e
            }, r
        }(t.ElementDragging),
        j = function () {
            function e(e) {
                this.origRect = t.computeRect(e), this.scrollCaches = t.getClippingParents(e).map(function (e) {
                    return new C(e, !0)
                })
            }

            return e.prototype.destroy = function () {
                for (var e = 0, t = this.scrollCaches; e < t.length; e++) {
                    t[e].destroy()
                }
            }, e.prototype.computeLeft = function () {
                for (var e = this.origRect.left, t = 0, n = this.scrollCaches; t < n.length; t++) {
                    var r = n[t];
                    e += r.origScrollLeft - r.getScrollLeft()
                }
                return e
            }, e.prototype.computeTop = function () {
                for (var e = this.origRect.top, t = 0, n = this.scrollCaches; t < n.length; t++) {
                    var r = n[t];
                    e += r.origScrollTop - r.getScrollTop()
                }
                return e
            }, e.prototype.isWithinClipping = function (e, n) {
                for (var r = {
                    left: e,
                    top: n
                }, i = 0, o = this.scrollCaches; i < o.length; i++) {
                    var a = o[i];
                    if (!s(a.getEventTarget()) && !t.pointInsideRect(r, a.clientRect)) return !1
                }
                return !0
            }, e
        }(),
        A = function () {
            function e(e, n) {
                var r = this;
                this.useSubjectCenter = !1, this.requireInitial = !0, this.initialHit = null, this.movingHit = null, this.finalHit = null, this.handlePointerDown = function (e) {
                    var t = r.dragging;
                    r.initialHit = null, r.movingHit = null, r.finalHit = null, r.prepareHits(), r.processFirstCoord(e), r.initialHit || !r.requireInitial ? (t.setIgnoreMove(!1), r.emitter.trigger("pointerdown", e)) : t.setIgnoreMove(!0)
                }, this.handleDragStart = function (e) {
                    r.emitter.trigger("dragstart", e), r.handleMove(e, !0)
                }, this.handleDragMove = function (e) {
                    r.emitter.trigger("dragmove", e), r.handleMove(e)
                }, this.handlePointerUp = function (e) {
                    r.releaseHits(), r.emitter.trigger("pointerup", e)
                }, this.handleDragEnd = function (e) {
                    r.movingHit && r.emitter.trigger("hitupdate", null, !0, e), r.finalHit = r.movingHit, r.movingHit = null, r.emitter.trigger("dragend", e)
                }, this.droppableStore = n, e.emitter.on("pointerdown", this.handlePointerDown), e.emitter.on("dragstart", this.handleDragStart), e.emitter.on("dragmove", this.handleDragMove), e.emitter.on("pointerup", this.handlePointerUp), e.emitter.on("dragend", this.handleDragEnd), this.dragging = e, this.emitter = new t.EmitterMixin
            }

            return e.prototype.processFirstCoord = function (e) {
                var n, r = {
                        left: e.pageX,
                        top: e.pageY
                    },
                    i = r,
                    o = e.subjectEl;
                o !== document && (n = t.computeRect(o), i = t.constrainPoint(i, n));
                var a = this.initialHit = this.queryHitForOffset(i.left, i.top);
                if (a) {
                    if (this.useSubjectCenter && n) {
                        var l = t.intersectRects(n, a.rect);
                        l && (i = t.getRectCenter(l))
                    }
                    this.coordAdjust = t.diffPoints(i, r)
                } else this.coordAdjust = {
                    left: 0,
                    top: 0
                }
            }, e.prototype.handleMove = function (e, t) {
                var n = this.queryHitForOffset(e.pageX + this.coordAdjust.left, e.pageY + this.coordAdjust.top);
                !t && c(this.movingHit, n) || (this.movingHit = n, this.emitter.trigger("hitupdate", n, !1, e))
            }, e.prototype.prepareHits = function () {
                this.offsetTrackers = t.mapHash(this.droppableStore, function (e) {
                    return new j(e.el)
                })
            }, e.prototype.releaseHits = function () {
                var e = this.offsetTrackers;
                for (var t in e) e[t].destroy();
                this.offsetTrackers = {}
            }, e.prototype.queryHitForOffset = function (e, n) {
                var r = this,
                    i = r.droppableStore,
                    o = r.offsetTrackers,
                    a = null;
                for (var l in i) {
                    var s = i[l].component,
                        c = o[l];
                    if (c.isWithinClipping(e, n)) {
                        var d = c.computeLeft(),
                            u = c.computeTop(),
                            g = e - d,
                            h = n - u,
                            p = c.origRect,
                            v = p.right - p.left,
                            f = p.bottom - p.top;
                        if (g >= 0 && g < v && h >= 0 && h < f) {
                            var E = s.queryHit(g, h, v, f);
                            !E || s.props.dateProfile && !t.rangeContainsRange(s.props.dateProfile.activeRange, E.dateSpan.range) || a && !(E.layer > a.layer) || (E.rect.left += d, E.rect.right += d, E.rect.top += u, E.rect.bottom += u, a = E)
                        }
                    }
                }
                return a
            }, e
        }(),
        H = function (e) {
            function r(n) {
                var r = e.call(this, n) || this;
                r.handlePointerDown = function (e) {
                    var t = r.dragging;
                    t.setIgnoreMove(!r.component.isValidDateDownEl(t.pointer.downEl))
                }, r.handleDragEnd = function (e) {
                    var t = r.component;
                    if (!r.dragging.pointer.wasTouchScroll) {
                        var n = r.hitDragging,
                            i = n.initialHit,
                            o = n.finalHit;
                        i && o && c(i, o) && t.calendar.triggerDateClick(i.dateSpan, i.dayEl, t.view, e.origEvent)
                    }
                };
                var i = n.component;
                r.dragging = new L(i.el), r.dragging.autoScroller.isEnabled = !1;
                var o = r.hitDragging = new A(r.dragging, t.interactionSettingsToStore(n));
                return o.emitter.on("pointerdown", r.handlePointerDown), o.emitter.on("dragend", r.handleDragEnd), r
            }

            return n(r, e), r.prototype.destroy = function () {
                this.dragging.destroy()
            }, r
        }(t.Interaction),
        N = function (e) {
            function r(n) {
                var r = e.call(this, n) || this;
                r.dragSelection = null, r.handlePointerDown = function (e) {
                    var t = r,
                        n = t.component,
                        i = t.dragging,
                        o = n.opt("selectable") && n.isValidDateDownEl(e.origEvent.target);
                    i.setIgnoreMove(!o), i.delay = e.isTouch ? d(n) : null
                }, r.handleDragStart = function (e) {
                    r.component.calendar.unselect(e)
                }, r.handleHitUpdate = function (e, n) {
                    var i = r.component.calendar,
                        o = null,
                        a = !1;
                    e && ((o = u(r.hitDragging.initialHit, e, i.pluginSystem.hooks.dateSelectionTransformers)) && r.component.isDateSelectionValid(o) || (a = !0, o = null)), o ? i.dispatch({
                        type: "SELECT_DATES",
                        selection: o
                    }) : n || i.dispatch({
                        type: "UNSELECT_DATES"
                    }), a ? t.disableCursor() : t.enableCursor(), n || (r.dragSelection = o)
                }, r.handlePointerUp = function (e) {
                    r.dragSelection && (r.component.calendar.triggerDateSelect(r.dragSelection, e), r.dragSelection = null)
                };
                var i = n.component,
                    o = r.dragging = new L(i.el);
                o.touchScrollAllowed = !1, o.minDistance = i.opt("selectMinDistance") || 0, o.autoScroller.isEnabled = i.opt("dragScroll");
                var a = r.hitDragging = new A(r.dragging, t.interactionSettingsToStore(n));
                return a.emitter.on("pointerdown", r.handlePointerDown), a.emitter.on("dragstart", r.handleDragStart), a.emitter.on("hitupdate", r.handleHitUpdate), a.emitter.on("pointerup", r.handlePointerUp), r
            }

            return n(r, e), r.prototype.destroy = function () {
                this.dragging.destroy()
            }, r
        }(t.Interaction),
        V = function (e) {
            function r(n) {
                var i = e.call(this, n) || this;
                i.subjectSeg = null, i.isDragging = !1, i.eventRange = null, i.relevantEvents = null, i.receivingCalendar = null, i.validMutation = null, i.mutatedRelevantEvents = null, i.handlePointerDown = function (e) {
                    var n = e.origEvent.target,
                        r = i,
                        o = r.component,
                        a = r.dragging,
                        l = a.mirror,
                        s = o.calendar,
                        c = i.subjectSeg = t.getElSeg(e.subjectEl),
                        d = i.eventRange = c.eventRange,
                        u = d.instance.instanceId;
                    i.relevantEvents = t.getRelevantEvents(s.state.eventStore, u), a.minDistance = e.isTouch ? 0 : o.opt("eventDragMinDistance"), a.delay = e.isTouch && u !== o.props.eventSelection ? h(o) : null, l.parentNode = s.el, l.revertDuration = o.opt("dragRevertDuration");
                    var g = o.isValidSegDownEl(n) && !t.elementClosest(n, ".fc-resizer");
                    a.setIgnoreMove(!g), i.isDragging = g && e.subjectEl.classList.contains("fc-draggable")
                }, i.handleDragStart = function (e) {
                    var n = i.component.calendar,
                        r = i.eventRange,
                        o = r.instance.instanceId;
                    e.isTouch ? o !== i.component.props.eventSelection && n.dispatch({
                        type: "SELECT_EVENT",
                        eventInstanceId: o
                    }) : n.dispatch({
                        type: "UNSELECT_EVENT"
                    }), i.isDragging && (n.unselect(e), n.publiclyTrigger("eventDragStart", [{
                        el: i.subjectSeg.el,
                        event: new t.EventApi(n, r.def, r.instance),
                        jsEvent: e.origEvent,
                        view: i.component.view
                    }]))
                }, i.handleHitUpdate = function (e, n) {
                    if (i.isDragging) {
                        var r = i.relevantEvents,
                            o = i.hitDragging.initialHit,
                            a = i.component.calendar,
                            l = null,
                            s = null,
                            d = null,
                            u = !1,
                            h = {
                                affectedEvents: r,
                                mutatedEvents: t.createEmptyEventStore(),
                                isEvent: !0,
                                origSeg: i.subjectSeg
                            };
                        if (e) {
                            var p = e.component;
                            l = p.calendar, a === l || p.opt("editable") && p.opt("droppable") ? (s = g(o, e, l.pluginSystem.hooks.eventDragMutationMassagers)) && (d = t.applyMutationToEventStore(r, l.eventUiBases, s, l), h.mutatedEvents = d, p.isInteractionValid(h) || (u = !0, s = null, d = null, h.mutatedEvents = t.createEmptyEventStore())) : l = null
                        }
                        i.displayDrag(l, h), u ? t.disableCursor() : t.enableCursor(), n || (a === l && c(o, e) && (s = null), i.dragging.setMirrorNeedsRevert(!s), i.dragging.setMirrorIsVisible(!e || !document.querySelector(".fc-mirror")), i.receivingCalendar = l, i.validMutation = s, i.mutatedRelevantEvents = d)
                    }
                }, i.handlePointerUp = function () {
                    i.isDragging || i.cleanup()
                }, i.handleDragEnd = function (e) {
                    if (i.isDragging) {
                        var n = i.component.calendar,
                            r = i.component.view,
                            o = i.receivingCalendar,
                            a = i.eventRange.def,
                            l = i.eventRange.instance,
                            s = new t.EventApi(n, a, l),
                            c = i.relevantEvents,
                            d = i.mutatedRelevantEvents,
                            u = i.hitDragging.finalHit;
                        if (i.clearDrag(), n.publiclyTrigger("eventDragStop", [{
                            el: i.subjectSeg.el,
                            event: s,
                            jsEvent: e.origEvent,
                            view: r
                        }]), i.validMutation) {
                            if (o === n) {
                                n.dispatch({
                                    type: "MERGE_EVENTS",
                                    eventStore: d
                                });
                                for (var g = {}, h = 0, p = n.pluginSystem.hooks.eventDropTransformers; h < p.length; h++) {
                                    var v = p[h];
                                    S(g, v(i.validMutation, n))
                                }
                                S(g, {
                                    el: e.subjectEl,
                                    delta: i.validMutation.startDelta,
                                    oldEvent: s,
                                    event: new t.EventApi(n, d.defs[a.defId], l ? d.instances[l.instanceId] : null),
                                    revert: function () {
                                        n.dispatch({
                                            type: "MERGE_EVENTS",
                                            eventStore: c
                                        })
                                    },
                                    jsEvent: e.origEvent,
                                    view: r
                                }), n.publiclyTrigger("eventDrop", [g])
                            } else if (o) {
                                n.publiclyTrigger("eventLeave", [{
                                    draggedEl: e.subjectEl,
                                    event: s,
                                    view: r
                                }]), n.dispatch({
                                    type: "REMOVE_EVENT_INSTANCES",
                                    instances: i.mutatedRelevantEvents.instances
                                }), o.dispatch({
                                    type: "MERGE_EVENTS",
                                    eventStore: i.mutatedRelevantEvents
                                }), e.isTouch && o.dispatch({
                                    type: "SELECT_EVENT",
                                    eventInstanceId: l.instanceId
                                });
                                var f = o.buildDatePointApi(u.dateSpan);
                                f.draggedEl = e.subjectEl, f.jsEvent = e.origEvent, f.view = u.component, o.publiclyTrigger("drop", [f]), o.publiclyTrigger("eventReceive", [{
                                    draggedEl: e.subjectEl,
                                    event: new t.EventApi(o, d.defs[a.defId], d.instances[l.instanceId]),
                                    view: u.component
                                }])
                            }
                        } else n.publiclyTrigger("_noEventDrop")
                    }
                    i.cleanup()
                };
                var o = i.component,
                    a = i.dragging = new L(o.el);
                a.pointer.selector = r.SELECTOR, a.touchScrollAllowed = !1, a.autoScroller.isEnabled = o.opt("dragScroll");
                var l = i.hitDragging = new A(i.dragging, t.interactionSettingsStore);
                return l.useSubjectCenter = n.useEventCenter, l.emitter.on("pointerdown", i.handlePointerDown), l.emitter.on("dragstart", i.handleDragStart), l.emitter.on("hitupdate", i.handleHitUpdate), l.emitter.on("pointerup", i.handlePointerUp), l.emitter.on("dragend", i.handleDragEnd), i
            }

            return n(r, e), r.prototype.destroy = function () {
                this.dragging.destroy()
            }, r.prototype.displayDrag = function (e, n) {
                var r = this.component.calendar,
                    i = this.receivingCalendar;
                i && i !== e && (i === r ? i.dispatch({
                    type: "SET_EVENT_DRAG",
                    state: {
                        affectedEvents: n.affectedEvents,
                        mutatedEvents: t.createEmptyEventStore(),
                        isEvent: !0,
                        origSeg: n.origSeg
                    }
                }) : i.dispatch({
                    type: "UNSET_EVENT_DRAG"
                })), e && e.dispatch({
                    type: "SET_EVENT_DRAG",
                    state: n
                })
            }, r.prototype.clearDrag = function () {
                var e = this.component.calendar,
                    t = this.receivingCalendar;
                t && t.dispatch({
                    type: "UNSET_EVENT_DRAG"
                }), e !== t && e.dispatch({
                    type: "UNSET_EVENT_DRAG"
                })
            }, r.prototype.cleanup = function () {
                this.subjectSeg = null, this.isDragging = !1, this.eventRange = null, this.relevantEvents = null, this.receivingCalendar = null, this.validMutation = null, this.mutatedRelevantEvents = null
            }, r.SELECTOR = ".fc-draggable, .fc-resizable", r
        }(t.Interaction),
        Y = function (e) {
            function r(n) {
                var r = e.call(this, n) || this;
                r.draggingSeg = null, r.eventRange = null, r.relevantEvents = null, r.validMutation = null, r.mutatedRelevantEvents = null, r.handlePointerDown = function (e) {
                    var t = r.component,
                        n = r.querySeg(e),
                        i = r.eventRange = n.eventRange;
                    r.dragging.minDistance = t.opt("eventDragMinDistance"), r.dragging.setIgnoreMove(!r.component.isValidSegDownEl(e.origEvent.target) || e.isTouch && r.component.props.eventSelection !== i.instance.instanceId)
                }, r.handleDragStart = function (e) {
                    var n = r.component.calendar,
                        i = r.eventRange;
                    r.relevantEvents = t.getRelevantEvents(n.state.eventStore, r.eventRange.instance.instanceId), r.draggingSeg = r.querySeg(e), n.unselect(), n.publiclyTrigger("eventResizeStart", [{
                        el: r.draggingSeg.el,
                        event: new t.EventApi(n, i.def, i.instance),
                        jsEvent: e.origEvent,
                        view: r.component.view
                    }])
                }, r.handleHitUpdate = function (e, n, i) {
                    var o = r.component.calendar,
                        a = r.relevantEvents,
                        l = r.hitDragging.initialHit,
                        s = r.eventRange.instance,
                        d = null,
                        u = null,
                        g = !1,
                        h = {
                            affectedEvents: a,
                            mutatedEvents: t.createEmptyEventStore(),
                            isEvent: !0,
                            origSeg: r.draggingSeg
                        };
                    e && (d = p(l, e, i.subjectEl.classList.contains("fc-start-resizer"), s.range, o.pluginSystem.hooks.eventResizeJoinTransforms)), d && (u = t.applyMutationToEventStore(a, o.eventUiBases, d, o), h.mutatedEvents = u, r.component.isInteractionValid(h) || (g = !0, d = null, u = null, h.mutatedEvents = null)), u ? o.dispatch({
                        type: "SET_EVENT_RESIZE",
                        state: h
                    }) : o.dispatch({
                        type: "UNSET_EVENT_RESIZE"
                    }), g ? t.disableCursor() : t.enableCursor(), n || (d && c(l, e) && (d = null), r.validMutation = d, r.mutatedRelevantEvents = u)
                }, r.handleDragEnd = function (e) {
                    var n = r.component.calendar,
                        i = r.component.view,
                        o = r.eventRange.def,
                        a = r.eventRange.instance,
                        l = new t.EventApi(n, o, a),
                        s = r.relevantEvents,
                        c = r.mutatedRelevantEvents;
                    n.publiclyTrigger("eventResizeStop", [{
                        el: r.draggingSeg.el,
                        event: l,
                        jsEvent: e.origEvent,
                        view: i
                    }]), r.validMutation ? (n.dispatch({
                        type: "MERGE_EVENTS",
                        eventStore: c
                    }), n.publiclyTrigger("eventResize", [{
                        el: r.draggingSeg.el,
                        startDelta: r.validMutation.startDelta || t.createDuration(0),
                        endDelta: r.validMutation.endDelta || t.createDuration(0),
                        prevEvent: l,
                        event: new t.EventApi(n, c.defs[o.defId], a ? c.instances[a.instanceId] : null),
                        revert: function () {
                            n.dispatch({
                                type: "MERGE_EVENTS",
                                eventStore: s
                            })
                        },
                        jsEvent: e.origEvent,
                        view: i
                    }])) : n.publiclyTrigger("_noEventResize"), r.draggingSeg = null, r.relevantEvents = null, r.validMutation = null
                };
                var i = n.component,
                    o = r.dragging = new L(i.el);
                o.pointer.selector = ".fc-resizer", o.touchScrollAllowed = !1, o.autoScroller.isEnabled = i.opt("dragScroll");
                var a = r.hitDragging = new A(r.dragging, t.interactionSettingsToStore(n));
                return a.emitter.on("pointerdown", r.handlePointerDown), a.emitter.on("dragstart", r.handleDragStart), a.emitter.on("hitupdate", r.handleHitUpdate), a.emitter.on("dragend", r.handleDragEnd), r
            }

            return n(r, e), r.prototype.destroy = function () {
                this.dragging.destroy()
            }, r.prototype.querySeg = function (e) {
                return t.getElSeg(t.elementClosest(e.subjectEl, this.component.fgSegSelector))
            }, r
        }(t.Interaction),
        _ = function () {
            function e(e) {
                var n = this;
                this.isRecentPointerDateSelect = !1, this.onSelect = function (e) {
                    e.jsEvent && (n.isRecentPointerDateSelect = !0)
                }, this.onDocumentPointerUp = function (e) {
                    var r = n,
                        i = r.calendar,
                        o = r.documentPointer,
                        a = i.state;
                    if (!o.wasTouchScroll) {
                        if (a.dateSelection && !n.isRecentPointerDateSelect) {
                            var l = i.viewOpt("unselectAuto"),
                                s = i.viewOpt("unselectCancel");
                            !l || l && t.elementClosest(o.downEl, s) || i.unselect(e)
                        }
                        a.eventSelection && !t.elementClosest(o.downEl, V.SELECTOR) && i.dispatch({
                            type: "UNSELECT_EVENT"
                        })
                    }
                    n.isRecentPointerDateSelect = !1
                }, this.calendar = e;
                var r = this.documentPointer = new T(document);
                r.shouldIgnoreMove = !0, r.shouldWatchScroll = !1, r.emitter.on("pointerup", this.onDocumentPointerUp), e.on("select", this.onSelect)
            }

            return e.prototype.destroy = function () {
                this.calendar.off("select", this.onSelect), this.documentPointer.destroy()
            }, e
        }(),
        X = function () {
            function e(e, n) {
                var r = this;
                this.receivingCalendar = null, this.droppableEvent = null, this.suppliedDragMeta = null, this.dragMeta = null, this.handleDragStart = function (e) {
                    r.dragMeta = r.buildDragMeta(e.subjectEl)
                }, this.handleHitUpdate = function (e, n, i) {
                    var o = r.hitDragging.dragging,
                        a = null,
                        l = null,
                        s = !1,
                        c = {
                            affectedEvents: t.createEmptyEventStore(),
                            mutatedEvents: t.createEmptyEventStore(),
                            isEvent: r.dragMeta.create,
                            origSeg: null
                        };
                    e && (a = e.component.calendar, r.canDropElOnCalendar(i.subjectEl, a) && (l = v(e.dateSpan, r.dragMeta, a), c.mutatedEvents = t.eventTupleToStore(l), (s = !t.isInteractionValid(c, a)) && (c.mutatedEvents = t.createEmptyEventStore(), l = null))), r.displayDrag(a, c), o.setMirrorIsVisible(n || !l || !document.querySelector(".fc-mirror")), s ? t.disableCursor() : t.enableCursor(), n || (o.setMirrorNeedsRevert(!l), r.receivingCalendar = a, r.droppableEvent = l)
                }, this.handleDragEnd = function (e) {
                    var n = r,
                        i = n.receivingCalendar,
                        o = n.droppableEvent;
                    if (r.clearDrag(), i && o) {
                        var a = r.hitDragging.finalHit,
                            l = a.component.view,
                            s = r.dragMeta,
                            c = i.buildDatePointApi(a.dateSpan);
                        c.draggedEl = e.subjectEl, c.jsEvent = e.origEvent, c.view = l, i.publiclyTrigger("drop", [c]), s.create && (i.dispatch({
                            type: "MERGE_EVENTS",
                            eventStore: t.eventTupleToStore(o)
                        }), e.isTouch && i.dispatch({
                            type: "SELECT_EVENT",
                            eventInstanceId: o.instance.instanceId
                        }), i.publiclyTrigger("eventReceive", [{
                            draggedEl: e.subjectEl,
                            event: new t.EventApi(i, o.def, o.instance),
                            view: l
                        }]))
                    }
                    r.receivingCalendar = null, r.droppableEvent = null
                };
                var i = this.hitDragging = new A(e, t.interactionSettingsStore);
                i.requireInitial = !1, i.emitter.on("dragstart", this.handleDragStart), i.emitter.on("hitupdate", this.handleHitUpdate), i.emitter.on("dragend", this.handleDragEnd), this.suppliedDragMeta = n
            }

            return e.prototype.buildDragMeta = function (e) {
                return "object" == typeof this.suppliedDragMeta ? t.parseDragMeta(this.suppliedDragMeta) : "function" == typeof this.suppliedDragMeta ? t.parseDragMeta(this.suppliedDragMeta(e)) : f(e)
            }, e.prototype.displayDrag = function (e, t) {
                var n = this.receivingCalendar;
                n && n !== e && n.dispatch({
                    type: "UNSET_EVENT_DRAG"
                }), e && e.dispatch({
                    type: "SET_EVENT_DRAG",
                    state: t
                })
            }, e.prototype.clearDrag = function () {
                this.receivingCalendar && this.receivingCalendar.dispatch({
                    type: "UNSET_EVENT_DRAG"
                })
            }, e.prototype.canDropElOnCalendar = function (e, n) {
                var r = n.opt("dropAccept");
                return "function" == typeof r ? r(e) : "string" != typeof r || !r || Boolean(t.elementMatches(e, r))
            }, e
        }();
    t.config.dataAttrPrefix = "";
    var U = function () {
            function e(e, n) {
                var r = this;
                void 0 === n && (n = {}), this.handlePointerDown = function (e) {
                    var n = r.dragging,
                        i = r.settings,
                        o = i.minDistance,
                        a = i.longPressDelay;
                    n.minDistance = null != o ? o : e.isTouch ? 0 : t.globalDefaults.eventDragMinDistance, n.delay = e.isTouch ? null != a ? a : t.globalDefaults.longPressDelay : 0
                }, this.handleDragStart = function (e) {
                    e.isTouch && r.dragging.delay && e.subjectEl.classList.contains("fc-event") && r.dragging.mirror.getMirrorEl().classList.add("fc-selected")
                }, this.settings = n;
                var i = this.dragging = new L(e);
                i.touchScrollAllowed = !1, null != n.itemSelector && (i.pointer.selector = n.itemSelector), null != n.appendTo && (i.mirror.parentNode = n.appendTo), i.emitter.on("pointerdown", this.handlePointerDown), i.emitter.on("dragstart", this.handleDragStart), new X(i, n.eventData)
            }

            return e.prototype.destroy = function () {
                this.dragging.destroy()
            }, e
        }(),
        O = function (e) {
            function t(t) {
                var n = e.call(this, t) || this;
                n.shouldIgnoreMove = !1, n.mirrorSelector = "", n.currentMirrorEl = null, n.handlePointerDown = function (e) {
                    n.emitter.trigger("pointerdown", e), n.shouldIgnoreMove || n.emitter.trigger("dragstart", e)
                }, n.handlePointerMove = function (e) {
                    n.shouldIgnoreMove || n.emitter.trigger("dragmove", e)
                }, n.handlePointerUp = function (e) {
                    n.emitter.trigger("pointerup", e), n.shouldIgnoreMove || n.emitter.trigger("dragend", e)
                };
                var r = n.pointer = new T(t);
                return r.emitter.on("pointerdown", n.handlePointerDown), r.emitter.on("pointermove", n.handlePointerMove), r.emitter.on("pointerup", n.handlePointerUp), n
            }

            return n(t, e), t.prototype.destroy = function () {
                this.pointer.destroy()
            }, t.prototype.setIgnoreMove = function (e) {
                this.shouldIgnoreMove = e
            }, t.prototype.setMirrorIsVisible = function (e) {
                if (e) this.currentMirrorEl && (this.currentMirrorEl.style.visibility = "", this.currentMirrorEl = null);
                else {
                    var t = this.mirrorSelector ? document.querySelector(this.mirrorSelector) : null;
                    t && (this.currentMirrorEl = t, t.style.visibility = "hidden")
                }
            }, t
        }(t.ElementDragging),
        q = function () {
            function e(e, t) {
                var n = document;
                e === document || e instanceof Element ? (n = e, t = t || {}) : t = e || {};
                var r = this.dragging = new O(n);
                "string" == typeof t.itemSelector ? r.pointer.selector = t.itemSelector : n === document && (r.pointer.selector = "[data-event]"), "string" == typeof t.mirrorSelector && (r.mirrorSelector = t.mirrorSelector), new X(r, t.eventData)
            }

            return e.prototype.destroy = function () {
                this.dragging.destroy()
            }, e
        }(),
        W = t.createPlugin({
            componentInteractions: [H, N, V, Y],
            calendarInteractions: [_],
            elementDraggingImpl: L
        });
    e.Draggable = U, e.FeaturefulElementDragging = L, e.PointerDragging = T, e.ThirdPartyDraggable = q, e.default = W, Object.defineProperty(e, "__esModule", {
        value: !0
    })
});


// daygrid
!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports, require("@fullcalendar/core")) : "function" == typeof define && define.amd ? define(["exports", "@fullcalendar/core"], t) : (e = e || self, t(e.FullCalendarDayGrid = {}, e.FullCalendar))
}(this, function (e, t) {
    "use strict";

    function r(e, t) {
        function r() {
            this.constructor = e
        }

        l(e, t), e.prototype = null === t ? Object.create(t) : (r.prototype = t.prototype, new r)
    }

    function n(e, t) {
        var r, n;
        for (r = 0; r < t.length; r++)
            if (n = t[r], n.firstCol <= e.lastCol && n.lastCol >= e.firstCol) return !0;
        return !1
    }

    function i(e, t) {
        return e.leftCol - t.leftCol
    }

    function o(e, r, n, i) {
        var o = n.dateEnv,
            s = n.theme,
            l = t.rangeContainsMarker(r.activeRange, e),
            a = t.getDayClasses(e, r, n);
        return a.unshift("fc-day", s.getClass("widgetContent")), '<td class="' + a.join(" ") + '"' + (l ? ' data-date="' + o.formatIso(e, {
            omitTime: !0
        }) + '"' : "") + (i ? " " + i : "") + "></td>"
    }

    function s(e, r) {
        var n = new t.DaySeries(e.renderRange, r);
        return new t.DayTable(n, /year|month|week/.test(e.currentRangeUnit))
    }

    /*! *****************************************************************************
        Copyright (c) Microsoft Corporation. All rights reserved.
        Licensed under the Apache License, Version 2.0 (the "License"); you may not use
        this file except in compliance with the License. You may obtain a copy of the
        License at http://www.apache.org/licenses/LICENSE-2.0

        THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
        KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
        WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
        MERCHANTABLITY OR NON-INFRINGEMENT.

        See the Apache Version 2.0 License for specific language governing permissions
        and limitations under the License.
        ***************************************************************************** */
    var l = function (e, t) {
            return (l = Object.setPrototypeOf || {
                    __proto__: []
                }
                instanceof Array && function (e, t) {
                    e.__proto__ = t
                } || function (e, t) {
                    for (var r in t) t.hasOwnProperty(r) && (e[r] = t[r])
                })(e, t)
        },
        a = function () {
            return a = Object.assign || function (e) {
                for (var t, r = 1, n = arguments.length; r < n; r++) {
                    t = arguments[r];
                    for (var i in t) Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i])
                }
                return e
            }, a.apply(this, arguments)
        },
        d = function (e) {
            function n() {
                return null !== e && e.apply(this, arguments) || this
            }

            return r(n, e), n.prototype.buildRenderRange = function (r, n, i) {
                var o, s = this.dateEnv,
                    l = e.prototype.buildRenderRange.call(this, r, n, i),
                    a = l.start,
                    d = l.end;
                if (/^(year|month)$/.test(n) && (a = s.startOfWeek(a), o = s.startOfWeek(d), o.valueOf() !== d.valueOf() && (d = t.addWeeks(o, 1))), this.options.monthMode && this.options.fixedWeekCount) {
                    var c = Math.ceil(t.diffWeeks(a, d));
                    d = t.addWeeks(d, 6 - c)
                }
                return {
                    start: a,
                    end: d
                }
            }, n
        }(t.DateProfileGenerator),
        c = function () {
            function e(e) {
                var t = this;
                this.isHidden = !0, this.margin = 10, this.documentMousedown = function (e) {
                    t.el && !t.el.contains(e.target) && t.hide()
                }, this.options = e
            }

            return e.prototype.show = function () {
                this.isHidden && (this.el || this.render(), this.el.style.display = "", this.position(), this.isHidden = !1, this.trigger("show"))
            }, e.prototype.hide = function () {
                this.isHidden || (this.el.style.display = "none", this.isHidden = !0, this.trigger("hide"))
            }, e.prototype.render = function () {
                var e = this,
                    r = this.options,
                    n = this.el = t.createElement("div", {
                        className: "fc-popover " + (r.className || ""),
                        style: {
                            top: "0",
                            left: "0"
                        }
                    });
                "function" == typeof r.content && r.content(n), r.parentEl.appendChild(n), t.listenBySelector(n, "click", ".fc-close", function (t) {
                    e.hide()
                }), r.autoHide && document.addEventListener("mousedown", this.documentMousedown)
            }, e.prototype.destroy = function () {
                this.hide(), this.el && (t.removeElement(this.el), this.el = null), document.removeEventListener("mousedown", this.documentMousedown)
            }, e.prototype.position = function () {
                var e, r, n = this.options,
                    i = this.el,
                    o = i.getBoundingClientRect(),
                    s = t.computeRect(i.offsetParent),
                    l = t.computeClippingRect(n.parentEl);
                e = n.top || 0, r = void 0 !== n.left ? n.left : void 0 !== n.right ? n.right - o.width : 0, e = Math.min(e, l.bottom - o.height - this.margin), e = Math.max(e, l.top + this.margin), r = Math.min(r, l.right - o.width - this.margin), r = Math.max(r, l.left + this.margin), t.applyStyle(i, {
                    top: e - s.top,
                    left: r - s.left
                })
            }, e.prototype.trigger = function (e) {
                this.options[e] && this.options[e].apply(this, Array.prototype.slice.call(arguments, 1))
            }, e
        }(),
        h = function (e) {
            function n() {
                return null !== e && e.apply(this, arguments) || this
            }

            return r(n, e), n.prototype.renderSegHtml = function (e, r) {
                var n, i, o = this.context.options,
                    s = e.eventRange,
                    l = s.def,
                    a = s.ui,
                    d = l.allDay,
                    c = a.startEditable,
                    h = d && e.isStart && a.durationEditable && o.eventResizableFromStart,
                    p = d && e.isEnd && a.durationEditable,
                    u = this.getSegClasses(e, c, h || p, r),
                    f = t.cssToStr(this.getSkinCss(a)),
                    g = "";
                return u.unshift("fc-day-grid-event", "fc-h-event"), e.isStart && (n = this.getTimeText(s)) && (g = '<span class="fc-time">' + t.htmlEscape(n) + "</span>"), i = '<span class="fc-title">' + (t.htmlEscape(l.title || "") || "&nbsp;") + "</span>", '<a class="' + u.join(" ") + '"' + (l.url ? ' href="' + t.htmlEscape(l.url) + '"' : "") + (f ? ' style="' + f + '"' : "") + '><div class="fc-content">' + ("rtl" === o.dir ? i + " " + g : g + " " + i) + "</div>" + (h ? '<div class="fc-resizer fc-start-resizer"></div>' : "") + (p ? '<div class="fc-resizer fc-end-resizer"></div>' : "") + "</a>"
            }, n.prototype.computeEventTimeFormat = function () {
                return {
                    hour: "numeric",
                    minute: "2-digit",
                    omitZeroMinute: !0,
                    meridiem: "narrow"
                }
            }, n.prototype.computeDisplayEventEnd = function () {
                return !1
            }, n
        }(t.FgEventRenderer),
        p = function (e) {
            function o(t) {
                var r = e.call(this, t.context) || this;
                return r.dayGrid = t, r
            }

            return r(o, e), o.prototype.attachSegs = function (e, t) {
                var r = this.rowStructs = this.renderSegRows(e);
                this.dayGrid.rowEls.forEach(function (e, t) {
                    e.querySelector(".fc-content-skeleton > table").appendChild(r[t].tbodyEl)
                }), t || this.dayGrid.removeSegPopover()
            }, o.prototype.detachSegs = function () {
                for (var e, r = this.rowStructs || []; e = r.pop();) t.removeElement(e.tbodyEl);
                this.rowStructs = null
            }, o.prototype.renderSegRows = function (e) {
                var t, r, n = [];
                for (t = this.groupSegRows(e), r = 0; r < t.length; r++) n.push(this.renderSegRow(r, t[r]));
                return n
            }, o.prototype.renderSegRow = function (e, r) {
                function n(e) {
                    for (; s < e;) c = (b[i - 1] || [])[s], c ? c.rowSpan = (c.rowSpan || 1) + 1 : (c = document.createElement("td"), l.appendChild(c)), v[i][s] = c, b[i][s] = c, s++
                }

                var i, o, s, l, a, d, c, h = this.dayGrid,
                    p = h.colCnt,
                    u = h.isRtl,
                    f = this.buildSegLevels(r),
                    g = Math.max(1, f.length),
                    m = document.createElement("tbody"),
                    y = [],
                    v = [],
                    b = [];
                for (i = 0; i < g; i++) {
                    if (o = f[i], s = 0, l = document.createElement("tr"), y.push([]), v.push([]), b.push([]), o)
                        for (a = 0; a < o.length; a++) {
                            d = o[a];
                            var w = u ? p - 1 - d.lastCol : d.firstCol,
                                S = u ? p - 1 - d.firstCol : d.lastCol;
                            for (n(w), c = t.createElement("td", {
                                className: "fc-event-container"
                            }, d.el), w !== S ? c.colSpan = S - w + 1 : b[i][s] = c; s <= S;) v[i][s] = c, y[i][s] = d, s++;
                            l.appendChild(c)
                        }
                    n(p);
                    var C = h.renderProps.renderIntroHtml();
                    C && (h.isRtl ? t.appendToElement(l, C) : t.prependToElement(l, C)), m.appendChild(l)
                }
                return {
                    row: e,
                    tbodyEl: m,
                    cellMatrix: v,
                    segMatrix: y,
                    segLevels: f,
                    segs: r
                }
            }, o.prototype.buildSegLevels = function (e) {
                var t, r, o, s = this.dayGrid,
                    l = s.isRtl,
                    a = s.colCnt,
                    d = [];
                for (e = this.sortEventSegs(e), t = 0; t < e.length; t++) {
                    for (r = e[t], o = 0; o < d.length && n(r, d[o]); o++) ;
                    r.level = o, r.leftCol = l ? a - 1 - r.lastCol : r.firstCol, r.rightCol = l ? a - 1 - r.firstCol : r.lastCol, (d[o] || (d[o] = [])).push(r)
                }
                for (o = 0; o < d.length; o++) d[o].sort(i);
                return d
            }, o.prototype.groupSegRows = function (e) {
                var t, r = [];
                for (t = 0; t < this.dayGrid.rowCnt; t++) r.push([]);
                for (t = 0; t < e.length; t++) r[e[t].row].push(e[t]);
                return r
            }, o.prototype.computeDisplayEventEnd = function () {
                return 1 === this.dayGrid.colCnt
            }, o
        }(h),
        u = function (e) {
            function n() {
                return null !== e && e.apply(this, arguments) || this
            }

            return r(n, e), n.prototype.attachSegs = function (e, r) {
                var n = r.sourceSeg,
                    i = this.rowStructs = this.renderSegRows(e);
                this.dayGrid.rowEls.forEach(function (e, r) {
                    var o, s, l = t.htmlToElement('<div class="fc-mirror-skeleton"><table></table></div>');
                    n && n.row === r ? o = n.el : (o = e.querySelector(".fc-content-skeleton tbody")) || (o = e.querySelector(".fc-content-skeleton table")), s = o.getBoundingClientRect().top - e.getBoundingClientRect().top, l.style.top = s + "px", l.querySelector("table").appendChild(i[r].tbodyEl), e.appendChild(l)
                })
            }, n
        }(p),
        f = function (e) {
            function n(t) {
                var r = e.call(this, t.context) || this;
                return r.fillSegTag = "td", r.dayGrid = t, r
            }

            return r(n, e), n.prototype.renderSegs = function (t, r) {
                "bgEvent" === t && (r = r.filter(function (e) {
                    return e.eventRange.def.allDay
                })), e.prototype.renderSegs.call(this, t, r)
            }, n.prototype.attachSegs = function (e, t) {
                var r, n, i, o = [];
                for (r = 0; r < t.length; r++) n = t[r], i = this.renderFillRow(e, n), this.dayGrid.rowEls[n.row].appendChild(i), o.push(i);
                return o
            }, n.prototype.renderFillRow = function (e, r) {
                var n, i, o, s = this.dayGrid,
                    l = s.colCnt,
                    a = s.isRtl,
                    d = a ? l - 1 - r.lastCol : r.firstCol,
                    c = a ? l - 1 - r.firstCol : r.lastCol,
                    h = d,
                    p = c + 1;
                n = "businessHours" === e ? "bgevent" : e.toLowerCase(), i = t.htmlToElement('<div class="fc-' + n + '-skeleton"><table><tr></tr></table></div>'), o = i.getElementsByTagName("tr")[0], h > 0 && t.appendToElement(o, new Array(h + 1).join("<td></td>")), r.el.colSpan = p - h, o.appendChild(r.el), p < l && t.appendToElement(o, new Array(l - p + 1).join("<td></td>"));
                var u = s.renderProps.renderIntroHtml();
                return u && (s.isRtl ? t.appendToElement(o, u) : t.prependToElement(o, u)), i
            }, n
        }(t.FillRenderer),
        g = function (e) {
            function n(r, n) {
                var i = e.call(this, r, n) || this,
                    o = i.eventRenderer = new m(i),
                    s = i.renderFrame = t.memoizeRendering(i._renderFrame);
                return i.renderFgEvents = t.memoizeRendering(o.renderSegs.bind(o), o.unrender.bind(o), [s]), i.renderEventSelection = t.memoizeRendering(o.selectByInstanceId.bind(o), o.unselectByInstanceId.bind(o), [i.renderFgEvents]), i.renderEventDrag = t.memoizeRendering(o.hideByHash.bind(o), o.showByHash.bind(o), [s]), i.renderEventResize = t.memoizeRendering(o.hideByHash.bind(o), o.showByHash.bind(o), [s]), r.calendar.registerInteractiveComponent(i, {
                    el: i.el,
                    useEventCenter: !1
                }), i
            }

            return r(n, e), n.prototype.render = function (e) {
                this.renderFrame(e.date), this.renderFgEvents(e.fgSegs), this.renderEventSelection(e.eventSelection), this.renderEventDrag(e.eventDragInstances), this.renderEventResize(e.eventResizeInstances)
            }, n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.renderFrame.unrender(), this.calendar.unregisterInteractiveComponent(this)
            }, n.prototype._renderFrame = function (e) {
                var r = this,
                    n = r.theme,
                    i = r.dateEnv,
                    o = i.format(e, t.createFormatter(this.opt("dayPopoverFormat")));
                this.el.innerHTML = '<div class="fc-header ' + n.getClass("popoverHeader") + '"><span class="fc-title">' + t.htmlEscape(o) + '</span><span class="fc-close ' + n.getIconClass("close") + '"></span></div><div class="fc-body ' + n.getClass("popoverContent") + '"><div class="fc-event-container"></div></div>', this.segContainerEl = this.el.querySelector(".fc-event-container")
            }, n.prototype.queryHit = function (e, r, n, i) {
                var o = this.props.date;
                if (e < n && r < i) return {
                    component: this,
                    dateSpan: {
                        allDay: !0,
                        range: {
                            start: o,
                            end: t.addDays(o, 1)
                        }
                    },
                    dayEl: this.el,
                    rect: {
                        left: 0,
                        top: 0,
                        right: n,
                        bottom: i
                    },
                    layer: 1
                }
            }, n
        }(t.DateComponent),
        m = function (e) {
            function n(t) {
                var r = e.call(this, t.context) || this;
                return r.dayTile = t, r
            }

            return r(n, e), n.prototype.attachSegs = function (e) {
                for (var t = 0, r = e; t < r.length; t++) {
                    var n = r[t];
                    this.dayTile.segContainerEl.appendChild(n.el)
                }
            }, n.prototype.detachSegs = function (e) {
                for (var r = 0, n = e; r < n.length; r++) {
                    var i = n[r];
                    t.removeElement(i.el)
                }
            }, n
        }(h),
        y = function () {
            function e(e) {
                this.context = e
            }

            return e.prototype.renderHtml = function (e) {
                var t = [];
                e.renderIntroHtml && t.push(e.renderIntroHtml());
                for (var r = 0, n = e.cells; r < n.length; r++) {
                    var i = n[r];
                    t.push(o(i.date, e.dateProfile, this.context, i.htmlAttrs))
                }
                return e.cells.length || t.push('<td class="fc-day ' + this.context.theme.getClass("widgetContent") + '"></td>'), "rtl" === this.context.options.dir && t.reverse(), "<tr>" + t.join("") + "</tr>"
            }, e
        }(),
        v = t.createFormatter({
            day: "numeric"
        }),
        b = t.createFormatter({
            week: "numeric"
        }),
        w = function (e) {
            function n(r, n, i) {
                var o = e.call(this, r, n) || this;
                o.bottomCoordPadding = 0, o.isCellSizesDirty = !1;
                var s = o.eventRenderer = new p(o),
                    l = o.fillRenderer = new f(o);
                o.mirrorRenderer = new u(o);
                var a = o.renderCells = t.memoizeRendering(o._renderCells, o._unrenderCells);
                return o.renderBusinessHours = t.memoizeRendering(l.renderSegs.bind(l, "businessHours"), l.unrender.bind(l, "businessHours"), [a]), o.renderDateSelection = t.memoizeRendering(l.renderSegs.bind(l, "highlight"), l.unrender.bind(l, "highlight"), [a]), o.renderBgEvents = t.memoizeRendering(l.renderSegs.bind(l, "bgEvent"), l.unrender.bind(l, "bgEvent"), [a]), o.renderFgEvents = t.memoizeRendering(s.renderSegs.bind(s), s.unrender.bind(s), [a]), o.renderEventSelection = t.memoizeRendering(s.selectByInstanceId.bind(s), s.unselectByInstanceId.bind(s), [o.renderFgEvents]), o.renderEventDrag = t.memoizeRendering(o._renderEventDrag, o._unrenderEventDrag, [a]), o.renderEventResize = t.memoizeRendering(o._renderEventResize, o._unrenderEventResize, [a]), o.renderProps = i, o
            }

            return r(n, e), n.prototype.render = function (e) {
                var t = e.cells;
                this.rowCnt = t.length, this.colCnt = t[0].length, this.renderCells(t, e.isRigid), this.renderBusinessHours(e.businessHourSegs), this.renderDateSelection(e.dateSelectionSegs), this.renderBgEvents(e.bgEventSegs), this.renderFgEvents(e.fgEventSegs), this.renderEventSelection(e.eventSelection), this.renderEventDrag(e.eventDrag), this.renderEventResize(e.eventResize), this.segPopoverTile && this.updateSegPopoverTile()
            }, n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.renderCells.unrender()
            }, n.prototype.getCellRange = function (e, r) {
                var n = this.props.cells[e][r].date;
                return {
                    start: n,
                    end: t.addDays(n, 1)
                }
            }, n.prototype.updateSegPopoverTile = function (e, t) {
                var r = this.props;
                this.segPopoverTile.receiveProps({
                    date: e || this.segPopoverTile.props.date,
                    fgSegs: t || this.segPopoverTile.props.fgSegs,
                    eventSelection: r.eventSelection,
                    eventDragInstances: r.eventDrag ? r.eventDrag.affectedInstances : null,
                    eventResizeInstances: r.eventResize ? r.eventResize.affectedInstances : null
                })
            }, n.prototype._renderCells = function (e, r) {
                var n, i, o = this,
                    s = o.view,
                    l = o.dateEnv,
                    a = this,
                    d = a.rowCnt,
                    c = a.colCnt,
                    h = "";
                for (n = 0; n < d; n++) h += this.renderDayRowHtml(n, r);
                for (this.el.innerHTML = h, this.rowEls = t.findElements(this.el, ".fc-row"), this.cellEls = t.findElements(this.el, ".fc-day, .fc-disabled-day"), this.isRtl && this.cellEls.reverse(), this.rowPositions = new t.PositionCache(this.el, this.rowEls, !1, !0), this.colPositions = new t.PositionCache(this.el, this.cellEls.slice(0, c), !0, !1), n = 0; n < d; n++)
                    for (i = 0; i < c; i++) this.publiclyTrigger("dayRender", [{
                        date: l.toDate(e[n][i].date),
                        el: this.getCellEl(n, i),
                        view: s
                    }]);
                this.isCellSizesDirty = !0
            }, n.prototype._unrenderCells = function () {
                this.removeSegPopover()
            }, n.prototype.renderDayRowHtml = function (e, t) {
                var r = this.theme,
                    n = ["fc-row", "fc-week", r.getClass("dayRow")];
                t && n.push("fc-rigid");
                var i = new y(this.context);
                return '<div class="' + n.join(" ") + '"><div class="fc-bg"><table class="' + r.getClass("tableGrid") + '">' + i.renderHtml({
                    cells: this.props.cells[e],
                    dateProfile: this.props.dateProfile,
                    renderIntroHtml: this.renderProps.renderBgIntroHtml
                }) + '</table></div><div class="fc-content-skeleton"><table>' + (this.getIsNumbersVisible() ? "<thead>" + this.renderNumberTrHtml(e) + "</thead>" : "") + "</table></div></div>"
            }, n.prototype.getIsNumbersVisible = function () {
                return this.getIsDayNumbersVisible() || this.renderProps.cellWeekNumbersVisible || this.renderProps.colWeekNumbersVisible
            }, n.prototype.getIsDayNumbersVisible = function () {
                return this.rowCnt > 1
            }, n.prototype.renderNumberTrHtml = function (e) {
                var t = this.renderProps.renderNumberIntroHtml(e, this);
                return "<tr>" + (this.isRtl ? "" : t) + this.renderNumberCellsHtml(e) + (this.isRtl ? t : "") + "</tr>"
            }, n.prototype.renderNumberCellsHtml = function (e) {
                var t, r, n = [];
                for (t = 0; t < this.colCnt; t++) r = this.props.cells[e][t].date, n.push(this.renderNumberCellHtml(r));
                return this.isRtl && n.reverse(), n.join("")
            }, n.prototype.renderNumberCellHtml = function (e) {
                var r, n, i = this,
                    o = i.view,
                    s = i.dateEnv,
                    l = "",
                    a = t.rangeContainsMarker(this.props.dateProfile.activeRange, e),
                    d = this.getIsDayNumbersVisible() && a;
                return d || this.renderProps.cellWeekNumbersVisible ? (r = t.getDayClasses(e, this.props.dateProfile, this.context), r.unshift("fc-day-top"), this.renderProps.cellWeekNumbersVisible && (n = s.weekDow), l += '<td class="' + r.join(" ") + '"' + (a ? ' data-date="' + s.formatIso(e, {
                    omitTime: !0
                }) + '"' : "") + ">", this.renderProps.cellWeekNumbersVisible && e.getUTCDay() === n && (l += t.buildGotoAnchorHtml(o, {
                    date: e,
                    type: "week"
                }, {
                    class: "fc-week-number"
                }, s.format(e, b))), d && (l += t.buildGotoAnchorHtml(o, e, {
                    class: "fc-day-number"
                }, s.format(e, v))), l += "</td>") : "<td></td>"
            }, n.prototype.updateSize = function (e) {
                var t = this,
                    r = t.fillRenderer,
                    n = t.eventRenderer,
                    i = t.mirrorRenderer;
                (e || this.isCellSizesDirty) && (this.buildColPositions(), this.buildRowPositions(), this.isCellSizesDirty = !1), r.computeSizes(e), n.computeSizes(e), i.computeSizes(e), r.assignSizes(e), n.assignSizes(e), i.assignSizes(e)
            }, n.prototype.buildColPositions = function () {
                this.colPositions.build()
            }, n.prototype.buildRowPositions = function () {
                this.rowPositions.build(), this.rowPositions.bottoms[this.rowCnt - 1] += this.bottomCoordPadding
            }, n.prototype.positionToHit = function (e, t) {
                var r = this,
                    n = r.colPositions,
                    i = r.rowPositions,
                    o = n.leftToIndex(e),
                    s = i.topToIndex(t);
                if (null != s && null != o) return {
                    row: s,
                    col: o,
                    dateSpan: {
                        range: this.getCellRange(s, o),
                        allDay: !0
                    },
                    dayEl: this.getCellEl(s, o),
                    relativeRect: {
                        left: n.lefts[o],
                        right: n.rights[o],
                        top: i.tops[s],
                        bottom: i.bottoms[s]
                    }
                }
            }, n.prototype.getCellEl = function (e, t) {
                return this.cellEls[e * this.colCnt + t]
            }, n.prototype._renderEventDrag = function (e) {
                e && (this.eventRenderer.hideByHash(e.affectedInstances), this.fillRenderer.renderSegs("highlight", e.segs))
            }, n.prototype._unrenderEventDrag = function (e) {
                e && (this.eventRenderer.showByHash(e.affectedInstances), this.fillRenderer.unrender("highlight"))
            }, n.prototype._renderEventResize = function (e) {
                e && (this.eventRenderer.hideByHash(e.affectedInstances), this.fillRenderer.renderSegs("highlight", e.segs), this.mirrorRenderer.renderSegs(e.segs, {
                    isResizing: !0,
                    sourceSeg: e.sourceSeg
                }))
            }, n.prototype._unrenderEventResize = function (e) {
                e && (this.eventRenderer.showByHash(e.affectedInstances), this.fillRenderer.unrender("highlight"), this.mirrorRenderer.unrender(e.segs, {
                    isResizing: !0,
                    sourceSeg: e.sourceSeg
                }))
            }, n.prototype.removeSegPopover = function () {
                this.segPopover && this.segPopover.hide()
            }, n.prototype.limitRows = function (e) {
                var t, r, n = this.eventRenderer.rowStructs || [];
                for (t = 0; t < n.length; t++) this.unlimitRow(t), !1 !== (r = !!e && ("number" == typeof e ? e : this.computeRowLevelLimit(t))) && this.limitRow(t, r)
            }, n.prototype.computeRowLevelLimit = function (e) {
                var r, n, i = this.rowEls[e],
                    o = i.getBoundingClientRect().bottom,
                    s = t.findChildren(this.eventRenderer.rowStructs[e].tbodyEl);
                for (r = 0; r < s.length; r++)
                    if (n = s[r], n.classList.remove("fc-limited"), n.getBoundingClientRect().bottom > o) return r;
                return !1
            }, n.prototype.limitRow = function (e, r) {
                var n, i, o, s, l, a, d, c, h, p, u, f, g, m, y, v = this,
                    b = this,
                    w = b.colCnt,
                    S = b.isRtl,
                    C = this.eventRenderer.rowStructs[e],
                    E = [],
                    R = 0,
                    H = function (n) {
                        for (; R < n;) a = v.getCellSegs(e, R, r), a.length && (h = i[r - 1][R], y = v.renderMoreLink(e, R, a), m = t.createElement("div", null, y), h.appendChild(m), E.push(m[0])), R++
                    };
                if (r && r < C.segLevels.length) {
                    for (n = C.segLevels[r - 1], i = C.cellMatrix, o = t.findChildren(C.tbodyEl).slice(r), o.forEach(function (e) {
                        e.classList.add("fc-limited")
                    }), s = 0; s < n.length; s++) {
                        l = n[s];
                        var D = S ? w - 1 - l.lastCol : l.firstCol,
                            P = S ? w - 1 - l.firstCol : l.lastCol;
                        for (H(D), c = [], d = 0; R <= P;) a = this.getCellSegs(e, R, r), c.push(a), d += a.length, R++;
                        if (d) {
                            for (h = i[r - 1][D], p = h.rowSpan || 1, u = [], f = 0; f < c.length; f++) g = t.createElement("td", {
                                className: "fc-more-cell",
                                rowSpan: p
                            }), a = c[f], y = this.renderMoreLink(e, D + f, [l].concat(a)), m = t.createElement("div", null, y), g.appendChild(m), u.push(g), E.push(g);
                            h.classList.add("fc-limited"), t.insertAfterElement(h, u), o.push(h)
                        }
                    }
                    H(this.colCnt), C.moreEls = E, C.limitedEls = o
                }
            }, n.prototype.unlimitRow = function (e) {
                var r = this.eventRenderer.rowStructs[e];
                r.moreEls && (r.moreEls.forEach(t.removeElement), r.moreEls = null), r.limitedEls && (r.limitedEls.forEach(function (e) {
                    e.classList.remove("fc-limited")
                }), r.limitedEls = null)
            }, n.prototype.renderMoreLink = function (e, r, n) {
                var i = this,
                    o = this,
                    s = o.view,
                    l = o.dateEnv,
                    a = t.createElement("a", {
                        className: "fc-more"
                    });
                return a.innerText = this.getMoreLinkText(n.length), a.addEventListener("click", function (t) {
                    var o = i.opt("eventLimitClick"),
                        a = i.isRtl ? i.colCnt - r - 1 : r,
                        d = i.props.cells[e][a].date,
                        c = t.currentTarget,
                        h = i.getCellEl(e, r),
                        p = i.getCellSegs(e, r),
                        u = i.resliceDaySegs(p, d),
                        f = i.resliceDaySegs(n, d);
                    "function" == typeof o && (o = i.publiclyTrigger("eventLimitClick", [{
                        date: l.toDate(d),
                        allDay: !0,
                        dayEl: h,
                        moreEl: c,
                        segs: u,
                        hiddenSegs: f,
                        jsEvent: t,
                        view: s
                    }])), "popover" === o ? i.showSegPopover(e, r, c, u) : "string" == typeof o && s.calendar.zoomTo(d, o)
                }), a
            }, n.prototype.showSegPopover = function (e, r, n, i) {
                var o, s, l = this,
                    a = this,
                    d = a.calendar,
                    h = a.view,
                    p = a.theme,
                    u = this.isRtl ? this.colCnt - r - 1 : r,
                    f = n.parentNode;
                o = 1 === this.rowCnt ? h.el : this.rowEls[e], s = {
                    className: "fc-more-popover " + p.getClass("popover"),
                    parentEl: h.el,
                    top: t.computeRect(o).top,
                    autoHide: !0,
                    content: function (t) {
                        l.segPopoverTile = new g(l.context, t), l.updateSegPopoverTile(l.props.cells[e][u].date, i)
                    },
                    hide: function () {
                        l.segPopoverTile.destroy(), l.segPopoverTile = null, l.segPopover.destroy(), l.segPopover = null
                    }
                }, this.isRtl ? s.right = t.computeRect(f).right + 1 : s.left = t.computeRect(f).left - 1, this.segPopover = new c(s), this.segPopover.show(), d.releaseAfterSizingTriggers()
            }, n.prototype.resliceDaySegs = function (e, r) {
                for (var n = r, i = t.addDays(n, 1), o = {
                    start: n,
                    end: i
                }, s = [], l = 0, d = e; l < d.length; l++) {
                    var c = d[l],
                        h = c.eventRange,
                        p = h.range,
                        u = t.intersectRanges(p, o);
                    u && s.push(a({}, c, {
                        eventRange: {
                            def: h.def,
                            ui: a({}, h.ui, {
                                durationEditable: !1
                            }),
                            instance: h.instance,
                            range: u
                        },
                        isStart: c.isStart && u.start.valueOf() === p.start.valueOf(),
                        isEnd: c.isEnd && u.end.valueOf() === p.end.valueOf()
                    }))
                }
                return s
            }, n.prototype.getMoreLinkText = function (e) {
                var t = this.opt("eventLimitText");
                return "function" == typeof t ? t(e) : "+" + e + " " + t
            }, n.prototype.getCellSegs = function (e, t, r) {
                for (var n, i = this.eventRenderer.rowStructs[e].segMatrix, o = r || 0, s = []; o < i.length;) n = i[o][t], n && s.push(n), o++;
                return s
            }, n
        }(t.DateComponent),
        S = t.createFormatter({
            week: "numeric"
        }),
        C = function (e) {
            function n(r, n, i, o) {
                var s = e.call(this, r, n, i, o) || this;
                s.renderHeadIntroHtml = function () {
                    var e = s.theme;
                    return s.colWeekNumbersVisible ? '<th class="fc-week-number ' + e.getClass("widgetHeader") + '" ' + s.weekNumberStyleAttr() + "><span>" + t.htmlEscape(s.opt("weekLabel")) + "</span></th>" : ""
                }, s.renderDayGridNumberIntroHtml = function (e, r) {
                    var n = s.dateEnv,
                        i = r.props.cells[e][0].date;
                    return s.colWeekNumbersVisible ? '<td class="fc-week-number" ' + s.weekNumberStyleAttr() + ">" + t.buildGotoAnchorHtml(s, {
                        date: i,
                        type: "week",
                        forceOff: 1 === r.colCnt
                    }, n.format(i, S)) + "</td>" : ""
                }, s.renderDayGridBgIntroHtml = function () {
                    var e = s.theme;
                    return s.colWeekNumbersVisible ? '<td class="fc-week-number ' + e.getClass("widgetContent") + '" ' + s.weekNumberStyleAttr() + "></td>" : ""
                }, s.renderDayGridIntroHtml = function () {
                    return s.colWeekNumbersVisible ? '<td class="fc-week-number" ' + s.weekNumberStyleAttr() + "></td>" : ""
                }, s.el.classList.add("fc-dayGrid-view"), s.el.innerHTML = s.renderSkeletonHtml(), s.scroller = new t.ScrollComponent("hidden", "auto");
                var l = s.scroller.el;
                s.el.querySelector(".fc-body > tr > td").appendChild(l), l.classList.add("fc-day-grid-container");
                var a = t.createElement("div", {
                    className: "fc-day-grid"
                });
                l.appendChild(a);
                var d;
                return s.opt("weekNumbers") ? s.opt("weekNumbersWithinDays") ? (d = !0, s.colWeekNumbersVisible = !1) : (d = !1, s.colWeekNumbersVisible = !0) : (s.colWeekNumbersVisible = !1, d = !1), s.dayGrid = new w(s.context, a, {
                    renderNumberIntroHtml: s.renderDayGridNumberIntroHtml,
                    renderBgIntroHtml: s.renderDayGridBgIntroHtml,
                    renderIntroHtml: s.renderDayGridIntroHtml,
                    colWeekNumbersVisible: s.colWeekNumbersVisible,
                    cellWeekNumbersVisible: d
                }), s
            }

            return r(n, e), n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.dayGrid.destroy(), this.scroller.destroy()
            }, n.prototype.renderSkeletonHtml = function () {
                var e = this.theme;
                return '<table class="' + e.getClass("tableGrid") + '">' + (this.opt("columnHeader") ? '<thead class="fc-head"><tr><td class="fc-head-container ' + e.getClass("widgetHeader") + '">&nbsp;</td></tr></thead>' : "") + '<tbody class="fc-body"><tr><td class="' + e.getClass("widgetContent") + '"></td></tr></tbody></table>'
            }, n.prototype.weekNumberStyleAttr = function () {
                return null != this.weekNumberWidth ? 'style="width:' + this.weekNumberWidth + 'px"' : ""
            }, n.prototype.hasRigidRows = function () {
                var e = this.opt("eventLimit");
                return e && "number" != typeof e
            }, n.prototype.updateSize = function (t, r, n) {
                e.prototype.updateSize.call(this, t, r, n), this.dayGrid.updateSize(t)
            }, n.prototype.updateBaseSize = function (e, r, n) {
                var i, o, s = this.dayGrid,
                    l = this.opt("eventLimit"),
                    a = this.header ? this.header.el : null;
                if (!s.rowEls) return void (n || (i = this.computeScrollerHeight(r), this.scroller.setHeight(i)));
                this.colWeekNumbersVisible && (this.weekNumberWidth = t.matchCellWidths(t.findElements(this.el, ".fc-week-number"))), this.scroller.clear(), a && t.uncompensateScroll(a), s.removeSegPopover(), l && "number" == typeof l && s.limitRows(l), i = this.computeScrollerHeight(r), this.setGridHeight(i, n), l && "number" != typeof l && s.limitRows(l), n || (this.scroller.setHeight(i), o = this.scroller.getScrollbarWidths(), (o.left || o.right) && (a && t.compensateScroll(a, o), i = this.computeScrollerHeight(r), this.scroller.setHeight(i)), this.scroller.lockOverflow(o))
            }, n.prototype.computeScrollerHeight = function (e) {
                return e - t.subtractInnerElHeight(this.el, this.scroller.el)
            }, n.prototype.setGridHeight = function (e, r) {
                this.opt("monthMode") ? (r && (e *= this.dayGrid.rowCnt / 6), t.distributeHeight(this.dayGrid.rowEls, e, !r)) : r ? t.undistributeHeight(this.dayGrid.rowEls) : t.distributeHeight(this.dayGrid.rowEls, e, !0)
            }, n.prototype.computeInitialDateScroll = function () {
                return {
                    top: 0
                }
            }, n.prototype.queryDateScroll = function () {
                return {
                    top: this.scroller.getScrollTop()
                }
            }, n.prototype.applyDateScroll = function (e) {
                void 0 !== e.top && this.scroller.setScrollTop(e.top)
            }, n
        }(t.View);
    C.prototype.dateProfileGeneratorClass = d;
    var E = function (e) {
            function t(t, r) {
                var n = e.call(this, t, r.el) || this;
                return n.slicer = new R, n.dayGrid = r, t.calendar.registerInteractiveComponent(n, {
                    el: n.dayGrid.el
                }), n
            }

            return r(t, e), t.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.calendar.unregisterInteractiveComponent(this)
            }, t.prototype.render = function (e) {
                var t = this.dayGrid,
                    r = e.dateProfile,
                    n = e.dayTable;
                t.receiveProps(a({}, this.slicer.sliceProps(e, r, e.nextDayThreshold, t, n), {
                    dateProfile: r,
                    cells: n.cells,
                    isRigid: e.isRigid
                }))
            }, t.prototype.queryHit = function (e, t) {
                var r = this.dayGrid.positionToHit(e, t);
                if (r) return {
                    component: this.dayGrid,
                    dateSpan: r.dateSpan,
                    dayEl: r.dayEl,
                    rect: {
                        left: r.relativeRect.left,
                        right: r.relativeRect.right,
                        top: r.relativeRect.top,
                        bottom: r.relativeRect.bottom
                    },
                    layer: 0
                }
            }, t
        }(t.DateComponent),
        R = function (e) {
            function t() {
                return null !== e && e.apply(this, arguments) || this
            }

            return r(t, e), t.prototype.sliceRange = function (e, t) {
                return t.sliceRange(e)
            }, t
        }(t.Slicer),
        H = function (e) {
            function n(r, n, i, o) {
                var l = e.call(this, r, n, i, o) || this;
                return l.buildDayTable = t.memoize(s), l.opt("columnHeader") && (l.header = new t.DayHeader(l.context, l.el.querySelector(".fc-head-container"))), l.simpleDayGrid = new E(l.context, l.dayGrid), l
            }

            return r(n, e), n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.header && this.header.destroy(), this.simpleDayGrid.destroy()
            }, n.prototype.render = function (t) {
                e.prototype.render.call(this, t);
                var r = this.props.dateProfile,
                    n = this.dayTable = this.buildDayTable(r, this.dateProfileGenerator);
                this.header && this.header.receiveProps({
                    dateProfile: r,
                    dates: n.headerDates,
                    datesRepDistinctDays: 1 === n.rowCnt,
                    renderIntroHtml: this.renderHeadIntroHtml
                }), this.simpleDayGrid.receiveProps({
                    dateProfile: r,
                    dayTable: n,
                    businessHours: t.businessHours,
                    dateSelection: t.dateSelection,
                    eventStore: t.eventStore,
                    eventUiBases: t.eventUiBases,
                    eventSelection: t.eventSelection,
                    eventDrag: t.eventDrag,
                    eventResize: t.eventResize,
                    isRigid: this.hasRigidRows(),
                    nextDayThreshold: this.nextDayThreshold
                })
            }, n
        }(C),
        D = t.createPlugin({
            defaultView: "dayGridMonth",
            views: {
                dayGrid: H,
                dayGridDay: {
                    type: "dayGrid",
                    duration: {
                        days: 1
                    }
                },
                dayGridWeek: {
                    type: "dayGrid",
                    duration: {
                        weeks: 1
                    }
                },
                dayGridMonth: {
                    type: "dayGrid",
                    duration: {
                        months: 1
                    },
                    monthMode: !0,
                    fixedWeekCount: !0
                }
            }
        });
    e.AbstractDayGridView = C, e.DayBgRow = y, e.DayGrid = w, e.DayGridSlicer = R, e.DayGridView = H, e.SimpleDayGrid = E, e.buildBasicDayTable = s, e.default = D, Object.defineProperty(e, "__esModule", {
        value: !0
    })
});

// timegrid
!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports, require("@fullcalendar/core"), require("@fullcalendar/daygrid")) : "function" == typeof define && define.amd ? define(["exports", "@fullcalendar/core", "@fullcalendar/daygrid"], t) : (e = e || self, t(e.FullCalendarTimeGrid = {}, e.FullCalendar, e.FullCalendarDayGrid))
}(this, function (e, t, r) {
    "use strict";

    function i(e, t) {
        function r() {
            this.constructor = e
        }

        u(e, t), e.prototype = null === t ? Object.create(t) : (r.prototype = t.prototype, new r)
    }

    function n(e) {
        var t, r, i, n = [];
        for (t = 0; t < e.length; t++) {
            for (r = e[t], i = 0; i < n.length && a(r, n[i]).length; i++) ;
            r.level = i, (n[i] || (n[i] = [])).push(r)
        }
        return n
    }

    function o(e) {
        var t, r, i, n, o;
        for (t = 0; t < e.length; t++)
            for (r = e[t], i = 0; i < r.length; i++)
                for (n = r[i], n.forwardSegs = [], o = t + 1; o < e.length; o++) a(n, e[o], n.forwardSegs)
    }

    function s(e) {
        var t, r, i = e.forwardSegs,
            n = 0;
        if (void 0 === e.forwardPressure) {
            for (t = 0; t < i.length; t++) r = i[t], s(r), n = Math.max(n, 1 + r.forwardPressure);
            e.forwardPressure = n
        }
    }

    function a(e, t, r) {
        void 0 === r && (r = []);
        for (var i = 0; i < t.length; i++) l(e, t[i]) && r.push(t[i]);
        return r
    }

    function l(e, t) {
        return e.bottom > t.top && e.top < t.bottom
    }

    function d(e) {
        var r = t.buildSegCompareObj(e);
        return r.forwardPressure = e.forwardPressure, r.backwardCoord = e.backwardCoord, r
    }

    function c(e, t, r) {
        for (var i = [], n = 0, o = e.headerDates; n < o.length; n++) {
            var s = o[n];
            i.push({
                start: r.add(s, t.minTime),
                end: r.add(s, t.maxTime)
            })
        }
        return i
    }

    function h(e, r) {
        var i = new t.DaySeries(e.renderRange, r);
        return new t.DayTable(i, !1)
    }

    /*! *****************************************************************************
        Copyright (c) Microsoft Corporation. All rights reserved.
        Licensed under the Apache License, Version 2.0 (the "License"); you may not use
        this file except in compliance with the License. You may obtain a copy of the
        License at http://www.apache.org/licenses/LICENSE-2.0

        THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
        KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
        WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
        MERCHANTABLITY OR NON-INFRINGEMENT.

        See the Apache Version 2.0 License for specific language governing permissions
        and limitations under the License.
        ***************************************************************************** */
    var u = function (e, t) {
            return (u = Object.setPrototypeOf || {
                    __proto__: []
                }
                instanceof Array && function (e, t) {
                    e.__proto__ = t
                } || function (e, t) {
                    for (var r in t) t.hasOwnProperty(r) && (e[r] = t[r])
                })(e, t)
        },
        p = function () {
            return p = Object.assign || function (e) {
                for (var t, r = 1, i = arguments.length; r < i; r++) {
                    t = arguments[r];
                    for (var n in t) Object.prototype.hasOwnProperty.call(t, n) && (e[n] = t[n])
                }
                return e
            }, p.apply(this, arguments)
        },
        f = function (e) {
            function r(r) {
                var i = e.call(this, r.context) || this;
                return i.timeGrid = r, i.fullTimeFormat = t.createFormatter({
                    hour: "numeric",
                    minute: "2-digit",
                    separator: i.context.options.defaultRangeSeparator
                }), i
            }

            return i(r, e), r.prototype.attachSegs = function (e, t) {
                for (var r = this.timeGrid.groupSegsByCol(e), i = 0; i < r.length; i++) r[i] = this.sortEventSegs(r[i]);
                this.segsByCol = r, this.timeGrid.attachSegsByCol(r, this.timeGrid.fgContainerEls)
            }, r.prototype.detachSegs = function (e) {
                e.forEach(function (e) {
                    t.removeElement(e.el)
                }), this.segsByCol = null
            }, r.prototype.computeSegSizes = function (e) {
                var t = this,
                    r = t.timeGrid,
                    i = t.segsByCol,
                    n = r.colCnt;
                if (r.computeSegVerticals(e), i)
                    for (var o = 0; o < n; o++) this.computeSegHorizontals(i[o])
            }, r.prototype.assignSegSizes = function (e) {
                var t = this,
                    r = t.timeGrid,
                    i = t.segsByCol,
                    n = r.colCnt;
                if (r.assignSegVerticals(e), i)
                    for (var o = 0; o < n; o++) this.assignSegCss(i[o])
            }, r.prototype.computeEventTimeFormat = function () {
                return {
                    hour: "numeric",
                    minute: "2-digit",
                    meridiem: !1
                }
            }, r.prototype.computeDisplayEventEnd = function () {
                return !0
            }, r.prototype.renderSegHtml = function (e, r) {
                var i, n, o, s = e.eventRange,
                    a = s.def,
                    l = s.ui,
                    d = a.allDay,
                    c = l.startEditable,
                    h = e.isStart && l.durationEditable && this.context.options.eventResizableFromStart,
                    u = e.isEnd && l.durationEditable,
                    p = this.getSegClasses(e, c, h || u, r),
                    f = t.cssToStr(this.getSkinCss(l));
                if (p.unshift("fc-time-grid-event"), t.isMultiDayRange(s.range)) {
                    if (e.isStart || e.isEnd) {
                        var m = e.start,
                            g = e.end;
                        i = this._getTimeText(m, g, d), n = this._getTimeText(m, g, d, this.fullTimeFormat), o = this._getTimeText(m, g, d, null, !1)
                    }
                } else i = this.getTimeText(s), n = this.getTimeText(s, this.fullTimeFormat), o = this.getTimeText(s, null, !1);
                return '<a class="' + p.join(" ") + '"' + (a.url ? ' href="' + t.htmlEscape(a.url) + '"' : "") + (f ? ' style="' + f + '"' : "") + '><div class="fc-content">' + (i ? '<div class="fc-time" data-start="' + t.htmlEscape(o) + '" data-full="' + t.htmlEscape(n) + '"><span>' + t.htmlEscape(i) + "</span></div>" : "") + (a.title ? '<div class="fc-title">' + t.htmlEscape(a.title) + "</div>" : "") + "</div>" + (u ? '<div class="fc-resizer fc-end-resizer"></div>' : "") + "</a>"
            }, r.prototype.computeSegHorizontals = function (e) {
                var t, r, i;
                if (t = n(e), o(t), r = t[0]) {
                    for (i = 0; i < r.length; i++) s(r[i]);
                    for (i = 0; i < r.length; i++) this.computeSegForwardBack(r[i], 0, 0)
                }
            }, r.prototype.computeSegForwardBack = function (e, t, r) {
                var i, n = e.forwardSegs;
                if (void 0 === e.forwardCoord)
                    for (n.length ? (this.sortForwardSegs(n), this.computeSegForwardBack(n[0], t + 1, r), e.forwardCoord = n[0].backwardCoord) : e.forwardCoord = 1, e.backwardCoord = e.forwardCoord - (e.forwardCoord - r) / (t + 1), i = 0; i < n.length; i++) this.computeSegForwardBack(n[i], 0, e.forwardCoord)
            }, r.prototype.sortForwardSegs = function (e) {
                var r = e.map(d),
                    i = [{
                        field: "forwardPressure",
                        order: -1
                    }, {
                        field: "backwardCoord",
                        order: 1
                    }].concat(this.context.view.eventOrderSpecs);
                return r.sort(function (e, r) {
                    return t.compareByFieldSpecs(e, r, i)
                }), r.map(function (e) {
                    return e._seg
                })
            }, r.prototype.assignSegCss = function (e) {
                for (var r = 0, i = e; r < i.length; r++) {
                    var n = i[r];
                    t.applyStyle(n.el, this.generateSegCss(n)), n.level > 0 && n.el.classList.add("fc-time-grid-event-inset"), n.eventRange.def.title && n.bottom - n.top < 30 && n.el.classList.add("fc-short")
                }
            }, r.prototype.generateSegCss = function (e) {
                var t, r, i = this.context.options.slotEventOverlap,
                    n = e.backwardCoord,
                    o = e.forwardCoord,
                    s = this.timeGrid.generateSegVerticalCss(e),
                    a = this.timeGrid.isRtl;
                return i && (o = Math.min(1, n + 2 * (o - n))), a ? (t = 1 - o, r = n) : (t = n, r = 1 - o), s.zIndex = e.level + 1, s.left = 100 * t + "%", s.right = 100 * r + "%", i && e.forwardPressure && (s[a ? "marginLeft" : "marginRight"] = 20), s
            }, r
        }(t.FgEventRenderer),
        m = function (e) {
            function t() {
                return null !== e && e.apply(this, arguments) || this
            }

            return i(t, e), t.prototype.attachSegs = function (e, t) {
                this.segsByCol = this.timeGrid.groupSegsByCol(e), this.timeGrid.attachSegsByCol(this.segsByCol, this.timeGrid.mirrorContainerEls), this.sourceSeg = t.sourceSeg
            }, t.prototype.generateSegCss = function (t) {
                var r = e.prototype.generateSegCss.call(this, t),
                    i = this.sourceSeg;
                if (i && i.col === t.col) {
                    var n = e.prototype.generateSegCss.call(this, i);
                    r.left = n.left, r.right = n.right, r.marginLeft = n.marginLeft, r.marginRight = n.marginRight
                }
                return r
            }, t
        }(f),
        g = function (e) {
            function t(t) {
                var r = e.call(this, t.context) || this;
                return r.timeGrid = t, r
            }

            return i(t, e), t.prototype.attachSegs = function (e, t) {
                var r, i = this.timeGrid;
                return "bgEvent" === e ? r = i.bgContainerEls : "businessHours" === e ? r = i.businessContainerEls : "highlight" === e && (r = i.highlightContainerEls), i.attachSegsByCol(i.groupSegsByCol(t), r), t.map(function (e) {
                    return e.el
                })
            }, t.prototype.computeSegSizes = function (e) {
                this.timeGrid.computeSegVerticals(e)
            }, t.prototype.assignSegSizes = function (e) {
                this.timeGrid.assignSegVerticals(e)
            }, t
        }(t.FillRenderer),
        y = [{
            hours: 1
        }, {
            minutes: 30
        }, {
            minutes: 15
        }, {
            seconds: 30
        }, {
            seconds: 15
        }],
        v = function (e) {
            function n(r, i, n) {
                var o = e.call(this, r, i) || this;
                o.isSlatSizesDirty = !1, o.isColSizesDirty = !1, o.renderSlats = t.memoizeRendering(o._renderSlats);
                var s = o.eventRenderer = new f(o),
                    a = o.fillRenderer = new g(o);
                o.mirrorRenderer = new m(o);
                var l = o.renderColumns = t.memoizeRendering(o._renderColumns, o._unrenderColumns);
                return o.renderBusinessHours = t.memoizeRendering(a.renderSegs.bind(a, "businessHours"), a.unrender.bind(a, "businessHours"), [l]), o.renderDateSelection = t.memoizeRendering(o._renderDateSelection, o._unrenderDateSelection, [l]), o.renderFgEvents = t.memoizeRendering(s.renderSegs.bind(s), s.unrender.bind(s), [l]), o.renderBgEvents = t.memoizeRendering(a.renderSegs.bind(a, "bgEvent"), a.unrender.bind(a, "bgEvent"), [l]), o.renderEventSelection = t.memoizeRendering(s.selectByInstanceId.bind(s), s.unselectByInstanceId.bind(s), [o.renderFgEvents]), o.renderEventDrag = t.memoizeRendering(o._renderEventDrag, o._unrenderEventDrag, [l]), o.renderEventResize = t.memoizeRendering(o._renderEventResize, o._unrenderEventResize, [l]), o.processOptions(), i.innerHTML = '<div class="fc-bg"></div><div class="fc-slats"></div><hr class="fc-divider ' + o.theme.getClass("widgetHeader") + '" style="display:none" />', o.rootBgContainerEl = i.querySelector(".fc-bg"), o.slatContainerEl = i.querySelector(".fc-slats"), o.bottomRuleEl = i.querySelector(".fc-divider"), o.renderProps = n, o
            }

            return i(n, e), n.prototype.processOptions = function () {
                var e, r, i = this.opt("slotDuration"),
                    n = this.opt("snapDuration");
                i = t.createDuration(i), n = n ? t.createDuration(n) : i, e = t.wholeDivideDurations(i, n), null === e && (n = i, e = 1), this.slotDuration = i, this.snapDuration = n, this.snapsPerSlot = e, r = this.opt("slotLabelFormat"), Array.isArray(r) && (r = r[r.length - 1]), this.labelFormat = t.createFormatter(r || {
                    hour: "numeric",
                    minute: "2-digit",
                    omitZeroMinute: !0,
                    meridiem: "short"
                }), r = this.opt("slotLabelInterval"), this.labelInterval = r ? t.createDuration(r) : this.computeLabelInterval(i)
            }, n.prototype.computeLabelInterval = function (e) {
                var r, i, n;
                for (r = y.length - 1; r >= 0; r--)
                    if (i = t.createDuration(y[r]), null !== (n = t.wholeDivideDurations(i, e)) && n > 1) return i;
                return e
            }, n.prototype.render = function (e) {
                var t = e.cells;
                this.colCnt = t.length, this.renderSlats(e.dateProfile), this.renderColumns(e.cells, e.dateProfile), this.renderBusinessHours(e.businessHourSegs), this.renderDateSelection(e.dateSelectionSegs), this.renderFgEvents(e.fgEventSegs), this.renderBgEvents(e.bgEventSegs), this.renderEventSelection(e.eventSelection), this.renderEventDrag(e.eventDrag), this.renderEventResize(e.eventResize)
            }, n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.renderSlats.unrender(), this.renderColumns.unrender()
            }, n.prototype.updateSize = function (e) {
                var t = this,
                    r = t.fillRenderer,
                    i = t.eventRenderer,
                    n = t.mirrorRenderer;
                (e || this.isSlatSizesDirty) && (this.buildSlatPositions(), this.isSlatSizesDirty = !1), (e || this.isColSizesDirty) && (this.buildColPositions(), this.isColSizesDirty = !1), r.computeSizes(e), i.computeSizes(e), n.computeSizes(e), r.assignSizes(e), i.assignSizes(e), n.assignSizes(e)
            }, n.prototype._renderSlats = function (e) {
                var r = this.theme;
                this.slatContainerEl.innerHTML = '<table class="' + r.getClass("tableGrid") + '">' + this.renderSlatRowHtml(e) + "</table>", this.slatEls = t.findElements(this.slatContainerEl, "tr"), this.slatPositions = new t.PositionCache(this.el, this.slatEls, !1, !0), this.isSlatSizesDirty = !0
            }, n.prototype.renderSlatRowHtml = function (e) {
                for (var r, i, n, o = this, s = o.dateEnv, a = o.theme, l = o.isRtl, d = "", c = t.startOfDay(e.renderRange.start), h = e.minTime, u = t.createDuration(0); t.asRoughMs(h) < t.asRoughMs(e.maxTime);) r = s.add(c, h), i = null !== t.wholeDivideDurations(u, this.labelInterval), n = '<td class="fc-axis fc-time ' + a.getClass("widgetContent") + '">' + (i ? "<span>" + t.htmlEscape(s.format(r, this.labelFormat)) + "</span>" : "") + "</td>", d += '<tr data-time="' + t.formatIsoTimeString(r) + '"' + (i ? "" : ' class="fc-minor"') + ">" + (l ? "" : n) + '<td class="' + a.getClass("widgetContent") + '"></td>' + (l ? n : "") + "</tr>", h = t.addDurations(h, this.slotDuration), u = t.addDurations(u, this.slotDuration);
                return d
            }, n.prototype._renderColumns = function (e, i) {
                var n = this.theme,
                    o = new r.DayBgRow(this.context);
                this.rootBgContainerEl.innerHTML = '<table class="' + n.getClass("tableGrid") + '">' + o.renderHtml({
                    cells: e,
                    dateProfile: i,
                    renderIntroHtml: this.renderProps.renderBgIntroHtml
                }) + "</table>", this.colEls = t.findElements(this.el, ".fc-day, .fc-disabled-day"), this.isRtl && this.colEls.reverse(), this.colPositions = new t.PositionCache(this.el, this.colEls, !0, !1), this.renderContentSkeleton(), this.isColSizesDirty = !0
            }, n.prototype._unrenderColumns = function () {
                this.unrenderContentSkeleton()
            }, n.prototype.renderContentSkeleton = function () {
                var e, r = [];
                r.push(this.renderProps.renderIntroHtml());
                for (var i = 0; i < this.colCnt; i++) r.push('<td><div class="fc-content-col"><div class="fc-event-container fc-mirror-container"></div><div class="fc-event-container"></div><div class="fc-highlight-container"></div><div class="fc-bgevent-container"></div><div class="fc-business-container"></div></div></td>');
                this.isRtl && r.reverse(), e = this.contentSkeletonEl = t.htmlToElement('<div class="fc-content-skeleton"><table><tr>' + r.join("") + "</tr></table></div>"), this.colContainerEls = t.findElements(e, ".fc-content-col"), this.mirrorContainerEls = t.findElements(e, ".fc-mirror-container"), this.fgContainerEls = t.findElements(e, ".fc-event-container:not(.fc-mirror-container)"), this.bgContainerEls = t.findElements(e, ".fc-bgevent-container"), this.highlightContainerEls = t.findElements(e, ".fc-highlight-container"), this.businessContainerEls = t.findElements(e, ".fc-business-container"), this.isRtl && (this.colContainerEls.reverse(), this.mirrorContainerEls.reverse(), this.fgContainerEls.reverse(), this.bgContainerEls.reverse(), this.highlightContainerEls.reverse(), this.businessContainerEls.reverse()), this.el.appendChild(e)
            }, n.prototype.unrenderContentSkeleton = function () {
                t.removeElement(this.contentSkeletonEl)
            }, n.prototype.groupSegsByCol = function (e) {
                var t, r = [];
                for (t = 0; t < this.colCnt; t++) r.push([]);
                for (t = 0; t < e.length; t++) r[e[t].col].push(e[t]);
                return r
            }, n.prototype.attachSegsByCol = function (e, t) {
                var r, i, n;
                for (r = 0; r < this.colCnt; r++)
                    for (i = e[r], n = 0; n < i.length; n++) t[r].appendChild(i[n].el)
            }, n.prototype.getNowIndicatorUnit = function () {
                return "minute"
            }, n.prototype.renderNowIndicator = function (e, r) {
                if (this.colContainerEls) {
                    var i, n = this.computeDateTop(r),
                        o = [];
                    for (i = 0; i < e.length; i++) {
                        var s = t.createElement("div", {
                            className: "fc-now-indicator fc-now-indicator-line"
                        });
                        s.style.top = n + "px", this.colContainerEls[e[i].col].appendChild(s), o.push(s)
                    }
                    if (e.length > 0) {
                        var a = t.createElement("div", {
                            className: "fc-now-indicator fc-now-indicator-arrow"
                        });
                        a.style.top = n + "px", this.contentSkeletonEl.appendChild(a), o.push(a)
                    }
                    this.nowIndicatorEls = o
                }
            }, n.prototype.unrenderNowIndicator = function () {
                this.nowIndicatorEls && (this.nowIndicatorEls.forEach(t.removeElement), this.nowIndicatorEls = null)
            }, n.prototype.getTotalSlatHeight = function () {
                return this.slatContainerEl.offsetHeight
            }, n.prototype.computeDateTop = function (e, r) {
                return r || (r = t.startOfDay(e)), this.computeTimeTop(e.valueOf() - r.valueOf())
            }, n.prototype.computeTimeTop = function (e) {
                var r, i, n = this.slatEls.length,
                    o = this.props.dateProfile,
                    s = (e - t.asRoughMs(o.minTime)) / t.asRoughMs(this.slotDuration);
                return s = Math.max(0, s), s = Math.min(n, s), r = Math.floor(s), r = Math.min(r, n - 1), i = s - r, this.slatPositions.tops[r] + this.slatPositions.getHeight(r) * i
            }, n.prototype.computeSegVerticals = function (e) {
                var t, r, i, n = this.opt("timeGridEventMinHeight");
                for (t = 0; t < e.length; t++) r = e[t], i = this.props.cells[r.col].date, r.top = this.computeDateTop(r.start, i), r.bottom = Math.max(r.top + n, this.computeDateTop(r.end, i))
            }, n.prototype.assignSegVerticals = function (e) {
                var r, i;
                for (r = 0; r < e.length; r++) i = e[r], t.applyStyle(i.el, this.generateSegVerticalCss(i))
            }, n.prototype.generateSegVerticalCss = function (e) {
                return {
                    top: e.top,
                    bottom: -e.bottom
                }
            }, n.prototype.buildColPositions = function () {
                this.colPositions.build()
            }, n.prototype.buildSlatPositions = function () {
                this.slatPositions.build()
            }, n.prototype.positionToHit = function (e, r) {
                var i = this,
                    n = i.dateEnv,
                    o = i.snapsPerSlot,
                    s = i.slatPositions,
                    a = i.colPositions,
                    l = a.leftToIndex(e),
                    d = s.topToIndex(r);
                if (null != l && null != d) {
                    var c = s.tops[d],
                        h = s.getHeight(d),
                        u = (r - c) / h,
                        p = Math.floor(u * o),
                        f = d * o + p,
                        m = this.props.cells[l].date,
                        g = t.addDurations(this.props.dateProfile.minTime, t.multiplyDuration(this.snapDuration, f)),
                        y = n.add(m, g);
                    return {
                        col: l,
                        dateSpan: {
                            range: {
                                start: y,
                                end: n.add(y, this.snapDuration)
                            },
                            allDay: !1
                        },
                        dayEl: this.colEls[l],
                        relativeRect: {
                            left: a.lefts[l],
                            right: a.rights[l],
                            top: c,
                            bottom: c + h
                        }
                    }
                }
            }, n.prototype._renderEventDrag = function (e) {
                e && (this.eventRenderer.hideByHash(e.affectedInstances), e.isEvent ? this.mirrorRenderer.renderSegs(e.segs, {
                    isDragging: !0,
                    sourceSeg: e.sourceSeg
                }) : this.fillRenderer.renderSegs("highlight", e.segs))
            }, n.prototype._unrenderEventDrag = function (e) {
                e && (this.eventRenderer.showByHash(e.affectedInstances), this.mirrorRenderer.unrender(e.segs, {
                    isDragging: !0,
                    sourceSeg: e.sourceSeg
                }), this.fillRenderer.unrender("highlight"))
            }, n.prototype._renderEventResize = function (e) {
                e && (this.eventRenderer.hideByHash(e.affectedInstances), this.mirrorRenderer.renderSegs(e.segs, {
                    isResizing: !0,
                    sourceSeg: e.sourceSeg
                }))
            }, n.prototype._unrenderEventResize = function (e) {
                e && (this.eventRenderer.showByHash(e.affectedInstances), this.mirrorRenderer.unrender(e.segs, {
                    isResizing: !0,
                    sourceSeg: e.sourceSeg
                }))
            }, n.prototype._renderDateSelection = function (e) {
                e && (this.opt("selectMirror") ? this.mirrorRenderer.renderSegs(e, {
                    isSelecting: !0
                }) : this.fillRenderer.renderSegs("highlight", e))
            }, n.prototype._unrenderDateSelection = function (e) {
                this.mirrorRenderer.unrender(e, {
                    isSelecting: !0
                }), this.fillRenderer.unrender("highlight")
            }, n
        }(t.DateComponent),
        S = function (e) {
            function r() {
                return null !== e && e.apply(this, arguments) || this
            }

            return i(r, e), r.prototype.getKeyInfo = function () {
                return {
                    allDay: {},
                    timed: {}
                }
            }, r.prototype.getKeysForDateSpan = function (e) {
                return e.allDay ? ["allDay"] : ["timed"]
            }, r.prototype.getKeysForEventDef = function (e) {
                return e.allDay ? t.hasBgRendering(e) ? ["timed", "allDay"] : ["allDay"] : ["timed"]
            }, r
        }(t.Splitter),
        C = t.createFormatter({
            week: "short"
        }),
        E = function (e) {
            function n(i, n, o, s) {
                var a = e.call(this, i, n, o, s) || this;
                a.splitter = new S, a.renderHeadIntroHtml = function () {
                    var e, r = a,
                        i = r.theme,
                        n = r.dateEnv,
                        o = a.props.dateProfile.renderRange,
                        s = t.diffDays(o.start, o.end);
                    return a.opt("weekNumbers") ? (e = n.format(o.start, C), '<th class="fc-axis fc-week-number ' + i.getClass("widgetHeader") + '" ' + a.axisStyleAttr() + ">" + t.buildGotoAnchorHtml(a, {
                        date: o.start,
                        type: "week",
                        forceOff: s > 1
                    }, t.htmlEscape(e)) + "</th>") : '<th class="fc-axis ' + i.getClass("widgetHeader") + '" ' + a.axisStyleAttr() + "></th>"
                }, a.renderTimeGridBgIntroHtml = function () {
                    return '<td class="fc-axis ' + a.theme.getClass("widgetContent") + '" ' + a.axisStyleAttr() + "></td>"
                }, a.renderTimeGridIntroHtml = function () {
                    return '<td class="fc-axis" ' + a.axisStyleAttr() + "></td>"
                }, a.renderDayGridBgIntroHtml = function () {
                    return '<td class="fc-axis ' + a.theme.getClass("widgetContent") + '" ' + a.axisStyleAttr() + "><span>" + t.getAllDayHtml(a) + "</span></td>"
                }, a.renderDayGridIntroHtml = function () {
                    return '<td class="fc-axis" ' + a.axisStyleAttr() + "></td>"
                }, a.el.classList.add("fc-timeGrid-view"), a.el.innerHTML = a.renderSkeletonHtml(), a.scroller = new t.ScrollComponent("hidden", "auto");
                var l = a.scroller.el;
                a.el.querySelector(".fc-body > tr > td").appendChild(l), l.classList.add("fc-time-grid-container");
                var d = t.createElement("div", {
                    className: "fc-time-grid"
                });
                return l.appendChild(d), a.timeGrid = new v(a.context, d, {
                    renderBgIntroHtml: a.renderTimeGridBgIntroHtml,
                    renderIntroHtml: a.renderTimeGridIntroHtml
                }), a.opt("allDaySlot") && (a.dayGrid = new r.DayGrid(a.context, a.el.querySelector(".fc-day-grid"), {
                    renderNumberIntroHtml: a.renderDayGridIntroHtml,
                    renderBgIntroHtml: a.renderDayGridBgIntroHtml,
                    renderIntroHtml: a.renderDayGridIntroHtml,
                    colWeekNumbersVisible: !1,
                    cellWeekNumbersVisible: !1
                }), a.dayGrid.bottomCoordPadding = a.el.querySelector(".fc-divider").offsetHeight), a
            }

            return i(n, e), n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.timeGrid.destroy(), this.dayGrid && this.dayGrid.destroy(), this.scroller.destroy()
            }, n.prototype.renderSkeletonHtml = function () {
                var e = this.theme;
                return '<table class="' + e.getClass("tableGrid") + '">' + (this.opt("columnHeader") ? '<thead class="fc-head"><tr><td class="fc-head-container ' + e.getClass("widgetHeader") + '">&nbsp;</td></tr></thead>' : "") + '<tbody class="fc-body"><tr><td class="' + e.getClass("widgetContent") + '">' + (this.opt("allDaySlot") ? '<div class="fc-day-grid"></div><hr class="fc-divider ' + e.getClass("widgetHeader") + '" />' : "") + "</td></tr></tbody></table>"
            }, n.prototype.getNowIndicatorUnit = function () {
                return this.timeGrid.getNowIndicatorUnit()
            }, n.prototype.unrenderNowIndicator = function () {
                this.timeGrid.unrenderNowIndicator()
            }, n.prototype.updateSize = function (t, r, i) {
                e.prototype.updateSize.call(this, t, r, i), this.timeGrid.updateSize(t), this.dayGrid && this.dayGrid.updateSize(t)
            }, n.prototype.updateBaseSize = function (e, r, i) {
                var n, o, s, a = this;
                if (this.axisWidth = t.matchCellWidths(t.findElements(this.el, ".fc-axis")), !this.timeGrid.colEls) return void (i || (o = this.computeScrollerHeight(r), this.scroller.setHeight(o)));
                var l = t.findElements(this.el, ".fc-row").filter(function (e) {
                    return !a.scroller.el.contains(e)
                });
                this.timeGrid.bottomRuleEl.style.display = "none", this.scroller.clear(), l.forEach(t.uncompensateScroll), this.dayGrid && (this.dayGrid.removeSegPopover(), n = this.opt("eventLimit"), n && "number" != typeof n && (n = 5), n && this.dayGrid.limitRows(n)), i || (o = this.computeScrollerHeight(r), this.scroller.setHeight(o), s = this.scroller.getScrollbarWidths(), (s.left || s.right) && (l.forEach(function (e) {
                    t.compensateScroll(e, s)
                }), o = this.computeScrollerHeight(r), this.scroller.setHeight(o)), this.scroller.lockOverflow(s), this.timeGrid.getTotalSlatHeight() < o && (this.timeGrid.bottomRuleEl.style.display = ""))
            }, n.prototype.computeScrollerHeight = function (e) {
                return e - t.subtractInnerElHeight(this.el, this.scroller.el)
            }, n.prototype.computeInitialDateScroll = function () {
                var e = t.createDuration(this.opt("scrollTime")),
                    r = this.timeGrid.computeTimeTop(e.milliseconds);
                return r = Math.ceil(r), r && r++, {
                    top: r
                }
            }, n.prototype.queryDateScroll = function () {
                return {
                    top: this.scroller.getScrollTop()
                }
            }, n.prototype.applyDateScroll = function (e) {
                void 0 !== e.top && this.scroller.setScrollTop(e.top)
            }, n.prototype.axisStyleAttr = function () {
                return null != this.axisWidth ? 'style="width:' + this.axisWidth + 'px"' : ""
            }, n
        }(t.View);
    E.prototype.usesMinMaxTime = !0;
    var b = function (e) {
            function r(r, i) {
                var n = e.call(this, r, i.el) || this;
                return n.buildDayRanges = t.memoize(c), n.slicer = new D, n.timeGrid = i, r.calendar.registerInteractiveComponent(n, {
                    el: n.timeGrid.el
                }), n
            }

            return i(r, e), r.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.calendar.unregisterInteractiveComponent(this)
            }, r.prototype.render = function (e) {
                var t = e.dateProfile,
                    r = e.dayTable,
                    i = this.dayRanges = this.buildDayRanges(r, t, this.dateEnv);
                this.timeGrid.receiveProps(p({}, this.slicer.sliceProps(e, t, null, this.timeGrid, i), {
                    dateProfile: t,
                    cells: r.cells[0]
                }))
            }, r.prototype.renderNowIndicator = function (e) {
                this.timeGrid.renderNowIndicator(this.slicer.sliceNowDate(e, this.timeGrid, this.dayRanges), e)
            }, r.prototype.queryHit = function (e, t) {
                var r = this.timeGrid.positionToHit(e, t);
                if (r) return {
                    component: this.timeGrid,
                    dateSpan: r.dateSpan,
                    dayEl: r.dayEl,
                    rect: {
                        left: r.relativeRect.left,
                        right: r.relativeRect.right,
                        top: r.relativeRect.top,
                        bottom: r.relativeRect.bottom
                    },
                    layer: 0
                }
            }, r
        }(t.DateComponent),
        D = function (e) {
            function r() {
                return null !== e && e.apply(this, arguments) || this
            }

            return i(r, e), r.prototype.sliceRange = function (e, r) {
                for (var i = [], n = 0; n < r.length; n++) {
                    var o = t.intersectRanges(e, r[n]);
                    o && i.push({
                        start: o.start,
                        end: o.end,
                        isStart: o.start.valueOf() === e.start.valueOf(),
                        isEnd: o.end.valueOf() === e.end.valueOf(),
                        col: n
                    })
                }
                return i
            }, r
        }(t.Slicer),
        w = function (e) {
            function n(i, n, o, s) {
                var a = e.call(this, i, n, o, s) || this;
                return a.buildDayTable = t.memoize(h), a.opt("columnHeader") && (a.header = new t.DayHeader(a.context, a.el.querySelector(".fc-head-container"))), a.simpleTimeGrid = new b(a.context, a.timeGrid), a.dayGrid && (a.simpleDayGrid = new r.SimpleDayGrid(a.context, a.dayGrid)), a
            }

            return i(n, e), n.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.header && this.header.destroy(), this.simpleTimeGrid.destroy(), this.simpleDayGrid && this.simpleDayGrid.destroy()
            }, n.prototype.render = function (t) {
                e.prototype.render.call(this, t);
                var r = this.props.dateProfile,
                    i = this.buildDayTable(r, this.dateProfileGenerator),
                    n = this.splitter.splitProps(t);
                this.header && this.header.receiveProps({
                    dateProfile: r,
                    dates: i.headerDates,
                    datesRepDistinctDays: !0,
                    renderIntroHtml: this.renderHeadIntroHtml
                }), this.simpleTimeGrid.receiveProps(p({}, n.timed, {
                    dateProfile: r,
                    dayTable: i
                })), this.simpleDayGrid && this.simpleDayGrid.receiveProps(p({}, n.allDay, {
                    dateProfile: r,
                    dayTable: i,
                    nextDayThreshold: this.nextDayThreshold,
                    isRigid: !1
                }))
            }, n.prototype.renderNowIndicator = function (e) {
                this.simpleTimeGrid.renderNowIndicator(e)
            }, n
        }(E),
        G = t.createPlugin({
            defaultView: "timeGridWeek",
            views: {
                timeGrid: {
                    class: w,
                    allDaySlot: !0,
                    slotDuration: "00:30:00",
                    slotEventOverlap: !0
                },
                timeGridDay: {
                    type: "timeGrid",
                    duration: {
                        days: 1
                    }
                },
                timeGridWeek: {
                    type: "timeGrid",
                    duration: {
                        weeks: 1
                    }
                }
            }
        });
    e.AbstractTimeGridView = E, e.TimeGrid = v, e.TimeGridSlicer = D, e.TimeGridView = w, e.buildDayRanges = c, e.buildDayTable = h, e.default = G, Object.defineProperty(e, "__esModule", {
        value: !0
    })
});

// list

!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports, require("@fullcalendar/core")) : "function" == typeof define && define.amd ? define(["exports", "@fullcalendar/core"], t) : (e = e || self, t(e.FullCalendarList = {}, e.FullCalendar))
}(this, function (e, t) {
    "use strict";

    function n(e, t) {
        function n() {
            this.constructor = e
        }

        s(e, t), e.prototype = null === t ? Object.create(t) : (n.prototype = t.prototype, new n)
    }

    function r(e) {
        for (var n = t.startOfDay(e.renderRange.start), r = e.renderRange.end, s = [], a = []; n < r;) s.push(n), a.push({
            start: n,
            end: t.addDays(n, 1)
        }), n = t.addDays(n, 1);
        return {
            dayDates: s,
            dayRanges: a
        }
    }

    /*! *****************************************************************************
        Copyright (c) Microsoft Corporation. All rights reserved.
        Licensed under the Apache License, Version 2.0 (the "License"); you may not use
        this file except in compliance with the License. You may obtain a copy of the
        License at http://www.apache.org/licenses/LICENSE-2.0

        THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
        KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
        WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
        MERCHANTABLITY OR NON-INFRINGEMENT.

        See the Apache Version 2.0 License for specific language governing permissions
        and limitations under the License.
        ***************************************************************************** */
    var s = function (e, t) {
            return (s = Object.setPrototypeOf || {
                    __proto__: []
                }
                instanceof Array && function (e, t) {
                    e.__proto__ = t
                } || function (e, t) {
                    for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n])
                })(e, t)
        },
        a = function (e) {
            function r(t) {
                var n = e.call(this, t.context) || this;
                return n.listView = t, n
            }

            return n(r, e), r.prototype.attachSegs = function (e) {
                e.length ? this.listView.renderSegList(e) : this.listView.renderEmptyMessage()
            }, r.prototype.detachSegs = function () {
            }, r.prototype.renderSegHtml = function (e) {
                var n, r = this.context,
                    s = r.view,
                    a = r.theme,
                    i = e.eventRange,
                    o = i.def,
                    l = i.instance,
                    d = i.ui,
                    c = o.url,
                    p = ["fc-list-item"].concat(d.classNames),
                    h = d.backgroundColor;
                return n = o.allDay ? t.getAllDayHtml(s) : t.isMultiDayRange(i.range) ? e.isStart ? t.htmlEscape(this._getTimeText(l.range.start, e.end, !1)) : e.isEnd ? t.htmlEscape(this._getTimeText(e.start, l.range.end, !1)) : t.getAllDayHtml(s) : t.htmlEscape(this.getTimeText(i)), c && p.push("fc-has-url"), '<tr class="' + p.join(" ") + '">' + (this.displayEventTime ? '<td class="fc-list-item-time ' + a.getClass("widgetContent") + '">' + (n || "") + "</td>" : "") + '<td class="fc-list-item-marker ' + a.getClass("widgetContent") + '"><span class="fc-event-dot"' + (h ? ' style="background-color:' + h + '"' : "") + '></span></td><td class="fc-list-item-title ' + a.getClass("widgetContent") + '"><a' + (c ? ' href="' + t.htmlEscape(c) + '"' : "") + ">" + t.htmlEscape(o.title || "") + "</a></td></tr>"
            }, r.prototype.computeEventTimeFormat = function () {
                return {
                    hour: "numeric",
                    minute: "2-digit",
                    meridiem: "short"
                }
            }, r
        }(t.FgEventRenderer),
        i = function (e) {
            function s(n, s, i, o) {
                var l = e.call(this, n, s, i, o) || this;
                l.computeDateVars = t.memoize(r), l.eventStoreToSegs = t.memoize(l._eventStoreToSegs);
                var d = l.eventRenderer = new a(l);
                l.renderContent = t.memoizeRendering(d.renderSegs.bind(d), d.unrender.bind(d)), l.el.classList.add("fc-list-view");
                for (var c = (l.theme.getClass("listView") || "").split(" "), p = 0, h = c; p < h.length; p++) {
                    var u = h[p];
                    u && l.el.classList.add(u)
                }
                return l.scroller = new t.ScrollComponent("hidden", "auto"), l.el.appendChild(l.scroller.el), l.contentEl = l.scroller.el, n.calendar.registerInteractiveComponent(l, {
                    el: l.el
                }), l
            }

            return n(s, e), s.prototype.render = function (e) {
                var t = this.computeDateVars(e.dateProfile),
                    n = t.dayDates,
                    r = t.dayRanges;
                this.dayDates = n, this.renderContent(this.eventStoreToSegs(e.eventStore, e.eventUiBases, r))
            }, s.prototype.destroy = function () {
                e.prototype.destroy.call(this), this.scroller.destroy(), this.calendar.unregisterInteractiveComponent(this)
            }, s.prototype.updateSize = function (t, n, r) {
                e.prototype.updateSize.call(this, t, n, r), this.eventRenderer.computeSizes(t), this.eventRenderer.assignSizes(t), this.scroller.clear(), r || this.scroller.setHeight(this.computeScrollerHeight(n))
            }, s.prototype.computeScrollerHeight = function (e) {
                return e - t.subtractInnerElHeight(this.el, this.scroller.el)
            }, s.prototype._eventStoreToSegs = function (e, n, r) {
                return this.eventRangesToSegs(t.sliceEventStore(e, n, this.props.dateProfile.activeRange, this.nextDayThreshold).fg, r)
            }, s.prototype.eventRangesToSegs = function (e, t) {
                for (var n = [], r = 0, s = e; r < s.length; r++) {
                    var a = s[r];
                    n.push.apply(n, this.eventRangeToSegs(a, t))
                }
                return n
            }, s.prototype.eventRangeToSegs = function (e, n) {
                var r, s, a, i = this,
                    o = i.dateEnv,
                    l = i.nextDayThreshold,
                    d = e.range,
                    c = e.def.allDay,
                    p = [];
                for (r = 0; r < n.length; r++)
                    if ((s = t.intersectRanges(d, n[r])) && (a = {
                        component: this,
                        eventRange: e,
                        start: s.start,
                        end: s.end,
                        isStart: e.isStart && s.start.valueOf() === d.start.valueOf(),
                        isEnd: e.isEnd && s.end.valueOf() === d.end.valueOf(),
                        dayIndex: r
                    }, p.push(a), !a.isEnd && !c && r + 1 < n.length && d.end < o.add(n[r + 1].start, l))) {
                        a.end = d.end, a.isEnd = !0;
                        break
                    }
                return p
            }, s.prototype.renderEmptyMessage = function () {
                this.contentEl.innerHTML = '<div class="fc-list-empty-wrap2"><div class="fc-list-empty-wrap1"><div class="fc-list-empty">' + t.htmlEscape(this.opt("noEventsMessage")) + "</div></div></div>"
            }, s.prototype.renderSegList = function (e) {
                var n, r, s, a = this.groupSegsByDay(e),
                    i = t.htmlToElement('<table class="fc-list-table ' + this.calendar.theme.getClass("tableList") + '"><tbody></tbody></table>'),
                    o = i.querySelector("tbody");
                for (n = 0; n < a.length; n++)
                    if (r = a[n])
                        for (o.appendChild(this.buildDayHeaderRow(this.dayDates[n])), r = this.eventRenderer.sortEventSegs(r), s = 0; s < r.length; s++) o.appendChild(r[s].el);
                this.contentEl.innerHTML = "", this.contentEl.appendChild(i)
            }, s.prototype.groupSegsByDay = function (e) {
                var t, n, r = [];
                for (t = 0; t < e.length; t++) n = e[t], (r[n.dayIndex] || (r[n.dayIndex] = [])).push(n);
                return r
            }, s.prototype.buildDayHeaderRow = function (e) {
                var n = this.dateEnv,
                    r = t.createFormatter(this.opt("listDayFormat")),
                    s = t.createFormatter(this.opt("listDayAltFormat"));
                return t.createElement("tr", {
                    className: "fc-list-heading",
                    "data-date": n.formatIso(e, {
                        omitTime: !0
                    })
                }, '<td class="' + (this.calendar.theme.getClass("tableListHeading") || this.calendar.theme.getClass("widgetHeader")) + '" colspan="3">' + (r ? t.buildGotoAnchorHtml(this, e, {
                    class: "fc-list-heading-main"
                }, t.htmlEscape(n.format(e, r))) : "") + (s ? t.buildGotoAnchorHtml(this, e, {
                    class: "fc-list-heading-alt"
                }, t.htmlEscape(n.format(e, s))) : "") + "</td>")
            }, s
        }(t.View);
    i.prototype.fgSegSelector = ".fc-list-item";
    var o = t.createPlugin({
        views: {
            list: {
                class: i,
                buttonTextKey: "list",
                listDayFormat: {
                    month: "long",
                    day: "numeric",
                    year: "numeric"
                }
            },
            listDay: {
                type: "list",
                duration: {
                    days: 1
                },
                listDayFormat: {
                    weekday: "long"
                }
            },
            listWeek: {
                type: "list",
                duration: {
                    weeks: 1
                },
                listDayFormat: {
                    weekday: "long"
                },
                listDayAltFormat: {
                    month: "long",
                    day: "numeric",
                    year: "numeric"
                }
            },
            listMonth: {
                type: "list",
                duration: {
                    month: 1
                },
                listDayAltFormat: {
                    weekday: "long"
                }
            },
            listYear: {
                type: "list",
                duration: {
                    year: 1
                },
                listDayAltFormat: {
                    weekday: "long"
                }
            }
        }
    });
    e.ListView = i, e.default = o, Object.defineProperty(e, "__esModule", {
        value: !0
    })
});