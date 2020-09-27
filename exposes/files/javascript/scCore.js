const SCDEBUG = scGlobals.system.localhost;
let SCAJAXTYPE = "GET";

class ScDebug {
    constructor() {
    }

    static out() {
        if (SCDEBUG) {
            console.log("%cLine: " + this.getCallerLine(2), "background: #ffffff; color: #2b8d95");
            for (let t in arguments) console.log(arguments[t]);
            console.log("%c------------------------------------------------------------------------------", "background: #ffffff; color: #808080")
        }
    }

    static error() {
        if (SCDEBUG) {
            console.log("%cLine: " + this.getCallerLine(2), "background: #ffffff; color: #ff0000");
            for (let t in arguments) console.error("%c" + arguments[t], "background: #ffffff; color: #ff0000");
            console.log("%c------------------------------------------------------------------------------", "background: #ffffff; color: #808080")
        }
    }

    static getCallerLine(t) {
        let e = (new Error).stack.split("\n");
        return e[t].split("/").pop() + " <- " + e[t + 1].split("/").pop()
    }
}

class ScCore {
    constructor() {
    }

    static isset(t) {
        return void 0 !== t && null != t
    }

    static issetMinLength(t, e) {
        return null != t && (e = e || 1, !!this.isset(t) && t.length >= e)
    }

    static alert(t, e) {
        if (this.isset(t)) {
            if ("undefined" == typeof scApp) return void alert(t);
            let n = "";
            n = this.isset(t.text) ? t.text : t, $.isArray(n) && (n = n.join("<br><br>")), scGlobals.device.type, scApp.f7.dialog.alert("<div class='scScrollableAlert'>" + n + "</div>", scGlobals.system.modalTitle, e)
        }
    }

    static confirm() {
        scApp.f7.dialog.confirm(arguments[0], arguments[1], arguments[2], arguments[3])
    }

    static pad(t, e, n) {
        n || (n = "0");
        for (var i = String(t); i.length < (e || 2);) i = n + i;
        return i
    }

    static ajax(t) {
        let e = $.extend({
            error: function (t, e) {
                let n = "";
                n = 0 === t.status ? "Not connect.\n Verify Network." : 404 == t.status ? "Requested page not found. [404]" : 500 == t.status ? "Internal Server Error [500]." : "parsererror" === e ? "Requested JSON parse failed." : "timeout" === e ? "Time out error." : "abort" === e ? "Ajax request aborted." : "Uncaught Error.\n" + t.responseText, ScDebug.error(n + t.responseText)
            },
            showIndicator: !0,
            indicatorTitle: ""
        }, t);
        e.showIndicator, $.ajax(e)
    }

    static icons2Unicode() {
        if (navigator.userAgent.toLowerCase().includes("javafx")) {
            var t = {
                bars: "&#9776;",
                home: "&#127968;",
                menu: "&#9776;",
                person: "&#128100;"
            };
            $(".icon").css("font-style", "normal"), $(".icon").each(function () {
                $(this).html(t[$(this).html()])
            }), $(".icon").removeClass("icon f7-icons")
        }
    }

    static afterOut() {
        ScCore.isset(ScCore.callbackAfterOut) && ScCore.callbackAfterOut(), ScCore.callbackAfterOut = function () {
        }, scApp.flags.transitionRunning = !1
    }

    static routerBack(t, e) {
        scApp.flags.transitionRunning = !0, ScCore.isset(e) ? scApp.f7.views.main.router.back(t, e) : ScCore.isset(t) ? scApp.f7.views.main.router.back(t) : scApp.f7.views.main.router.back()
    }

    static goHome(t) {
        ScCore.callbackAfterOut = t || function () {
        }, t = ScCore.callbackAfterOut;
        let e = Object.size(scApp.dialogs.dialogs);
        e > 0 ? "phone" == scGlobals.device.type ? (scApp.f7.popup.close(), 1 == e ? ScCore.routerBack() : ScCore.routerBack("/", {
            force: !0
        }), scApp.dialogs.removeAll()) : (scApp.dialogs.closeAll(), t(), ScCore.callbackAfterOut = function () {
        }) : (ScCore.callbackAfterOut(), ScCore.callbackAfterOut = function () {
        })
    }

    static composeUrl(t, e) {
        return e = e || "query.php", scGlobals.connection.path2PHP + e + "?sc_version=" + scGlobals.system.version + "&" + scGlobals.connection.authString + "&" + t + "&_=" + (new Date).getTime()
    }

    static getAuthParams() {
        let t = {},
            e = scGlobals.connection.authString.split("&");
        for (let n in e) {
            let i = e[n].split("=");
            t[i[0]] = i[1]
        }
        return t
    }

    static performQuery(t, e, n, i) {
        scGlobals.system.localhost || (SCAJAXTYPE = "POST");
        let s = $.extend({
                autologin: !0,
                forceCallback: !1,
                type: SCAJAXTYPE,
                dataType: "json"
            }, i),
            o = this.composeUrl("", n),
            r = this,
            a = o.split("?");
        this.ajax({
            url: a[0],
            data: a[1] + "&" + t,
            type: s.type,
            success: function (t) {
                ScDebug.out(t), r.setUserData(t), r.noError(t) && t.header.logType > 89 ? (s.autologin && (ScCore.exHasApp() ? r.exAutoLogin() : ScCore.login()), s.forceCallback && e(t)) : e(t)
            }
        })
    }

    static noError(t) {
        return !(t.header.state > 0) || (ScCore.isset(scStr[t.header.textT]) > 0 && this.alert(scStr[t.header.textT]), !0)
    }

    static setUserData(t) {
        ScCore.isset(t.header.log) && (scGlobals.user = $.extend(scGlobals.user, t.header.log))
    }

    static serializeForm(t) {
        let e = {};
        return $.each(t.find("[name]"), function () {
            e[$(this).attr("name")] = $(this).val()
        }), e
    }

    static uniqid() {
        return scGlobals.system.idCounter++, "scid_" + scGlobals.system.idCounter
    }

    static showDialogs(t) {
        let e = $.extend({
            modules: [],
            dialogs: []
        }, t);
        scApp.f7.panel.close(), scApp.dialogs.addDialogs(e.dialogs)
    }

    static template(t, e) {
        let n = (0, scApp.templates[t])(e);
        return n = n.replace(/(##)([a-zA-Z0-9]+)(##)/g, function (t, e, n, i) {
            return scStr[n]
        }), $(n)
    }

    static loadMenu() {
        scGlobals.layout.showMenu && ScCore.performQuery("cmd=1&subcmd=1", function (t) {
            this.isset(t.item.menu) ? (this.translate(t.item.menu), this.setMenuTitle(this.getPerson().fullname), $("#scMainMenuContent").html(this.template("corMainMenu", t.item)), this.addMenuEvents(), this.prepareExternalLinks()) : this.login()
        }.bind(this))
    }

    static login() {
        scGlobals.layout.loginRunning || ScCore.moduleFunc({
            module: "ScPrivate",
            func: "login"
        })
    }

    static openDefaultDialogs() {
        90 == scGlobals.user.type ? this.exHasApp() && this.login() : "vplan" == scGlobals.user.username.substr(0, 5) ? ScCore.moduleFunc({
            module: "ScTimeTable",
            func: "showChanges",
            params: {},
            callback: function () {
            }
        }) : (10 == scGlobals.client.number && ScCore.moduleFunc({
            module: "ScTimeTable",
            func: "showCalendar",
            params: {}
        }), 2 == scGlobals.client.number && ScCore.moduleFunc({
            module: "ScPersonlists",
            func: "showAllMembers",
            params: {}
        }), 224 == scGlobals.client.number && (ScCore.moduleFunc({
            module: "ScTimeTable",
            func: "showCalendar",
            params: {}
        }), 2e3 == scGlobals.user.type && setTimeout(function () {
            ScCore.moduleFunc({
                module: "ScCore",
                func: "checkGlobalMessage"
            })
        }, 2e3)))
    }

    static addMenuEvents() {
        $(".scMenuItem").unbind();
        let t = this;
        $(".scMenuItem").click(function () {
            let e = {};
            $(this).attr("scParams").length > 0 && (e = $.parseJSON($(this).attr("scParams")));
            let n = {
                module: $(this).attr("scModule"),
                func: $(this).attr("scFunc"),
                params: e
            };
            t.moduleFunc(n)
        })
    }

    static setMenuTitle(t) {
        $("#scMainMenuPage").find(".title").html(t)
    }

    static prepareExternalLinks() {
        this.exHasApp() && ($("[scTypeExternalLink]").removeClass("link"), $("[scTypeExternalLink]").removeClass("external"), $("[scTypeExternalLink]").click(function () {
            ScCore.exOpenUrl($(this).attr("href"))
        }))
    }

    static moduleFunc(t) {
        let e = $.extend({
            module: "",
            func: "",
            params: {},
            callback: function () {
            }
        }, t);
        "ScCore" == e.module ? ScCore[e.func](e.params) : scApp.modules.addModules({
            modules: [{
                name: e.module
            }],
            callback: function () {
                ScCore.isset(scApp.modules.modules[e.module][e.func]) && scApp.modules.modules[e.module][e.func](e.params), e.callback()
            }
        })
    }

    static translate(t, e, n) {
        ScCore.isset(e) || (e = "textT"), ScCore.isset(n) || (n = "text");
        for (let i in t) "object" == typeof t[i] ? this.translate(t[i], e) : i == e && (t[n] = scStr[t[i]] || t[i])
    }

    static getDateFromString(t, e) {
        t = t.substring(0, 10), e = $.extend({
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        }, e);
        new Date(new Date(t).getDate());
        return new Date(t).toLocaleDateString(scGlobals.user.langExt, e)
    }

    static getShortDateFromString(t, e) {
        return t.substring(8, 10) + "." + t.substring(5, 7) + "."
    }

    static getTimeFromString(t, e) {
        return t.length > 8 && (t = t.substring(11, 16)), t
    }

    static validateEmail(t) {
        return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(t)
    }

    static dateDiffInDays(t, e) {
        const n = Date.UTC(t.getFullYear(), t.getMonth(), t.getDate()),
            i = Date.UTC(e.getFullYear(), e.getMonth(), e.getDate());
        return Math.floor((i - n) / 864e5)
    }

    static autoPanelHeight() {
        return $("#scHomePageContent").height() - 18
    }

    static getPageWidth() {
        return parseInt($("#scHomePageContent").width())
    }

    static maxFractionWidth(t, e) {
        e = e || scGlobals.layout.panelWidth;
        let n = $("#scHomePageContent").width() * t;
        return n > e ? e : n
    }

    static dialogsColorPickerAttach(t, e) {
        let n = scApp.f7.colorPicker.create({
            inputEl: "",
            targetEl: "#" + t,
            targetElSetBackgroundColor: !0,
            modules: ["initial-current-colors", "sb-spectrum", "hsb-sliders", "rgb-sliders", "alpha-slider", "hex", "palette"],
            openIn: "auto",
            sliderValue: !0,
            sliderValueEditable: !0,
            sliderLabel: !0,
            hexLabel: !0,
            hexValueEditable: !0,
            groupedModules: !0,
            palette: [
                ["#FFEBEE", "#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "#F44336", "#E53935", "#D32F2F", "#C62828", "#B71C1C"],
                ["#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC", "#9C27B0", "#8E24AA", "#7B1FA2", "#6A1B9A", "#4A148C"],
                ["#E8EAF6", "#C5CAE9", "#9FA8DA", "#7986CB", "#5C6BC0", "#3F51B5", "#3949AB", "#303F9F", "#283593", "#1A237E"],
                ["#E1F5FE", "#B3E5FC", "#81D4FA", "#4FC3F7", "#29B6F6", "#03A9F4", "#039BE5", "#0288D1", "#0277BD", "#01579B"],
                ["#E0F2F1", "#B2DFDB", "#80CBC4", "#4DB6AC", "#26A69A", "#009688", "#00897B", "#00796B", "#00695C", "#004D40"],
                ["#F1F8E9", "#DCEDC8", "#C5E1A5", "#AED581", "#9CCC65", "#8BC34A", "#7CB342", "#689F38", "#558B2F", "#33691E"],
                ["#FFFDE7", "#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58", "#FFEB3B", "#FDD835", "#FBC02D", "#F9A825", "#F57F17"],
                ["#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D", "#FFA726", "#FF9800", "#FB8C00", "#F57C00", "#EF6C00", "#E65100"]
            ],
            formatValue: function (t) {
                return "rgba(" + t.rgba.join(", ") + ")"
            },
            value: {
                hex: "#00ffff"
            },
            navbarCloseText: scStr.corDone,
            navbarTitleText: scStr.corColorSelect,
            toolbarCloseText: scStr.corDone,
            toolbarPopover: !0
        });
        return n.setValue({
            hex: e
        }), n
    }

    static dialogsColorPickerInsert(t) {
        return '<i class="icon color-icon" id="' + t + '"></i>'
    }

    static dialogsDatePickerAttach(t) {
        let e = $.extend({
            id: this.uniqid(),
            value: [],
            closeOnSelect: !0
        }, t);
        return scApp.f7.calendar.create({
            inputEl: "#" + e.id,
            monthNames: scStr.corMonthNames,
            monthNamesShort: scStr.corMonthShortNames,
            dayNames: scStr.corWeekdaysLong,
            dayNamesShort: scStr.corWeekdaysShort,
            dateFormat: scGlobals.localization.dateFormat,
            value: e.value,
            closeOnSelect: e.closeOnSelect
        })
    }

    static dialogsDatePickerInsert(t) {
        let e = $.extend({
            id: this.uniqid(),
            placeholder: ""
        }, t);
        return '<input type="text" style="cursor:pointer;" value="' + e.value + '" placeholder="' + e.placeholder + '" readonly="readonly" id="' + e.id + '"/>'
    }

    static dialogsTimePickerAttach(t) {
        let e = $.extend({
            id: this.uniqid(),
            value: []
        }, t);
        return scApp.f7.picker.create({
            inputEl: "#" + e.id,
            formatValue: function (t, e) {
                return e[0] + ":" + e[1]
            },
            value: e.value,
            cols: [{
                values: function () {
                    for (var t = [], e = 0; e <= 23; e++) t.push(e);
                    return t
                }()
            }, {
                divider: !0,
                content: ":"
            }, {
                values: function () {
                    for (var t = [], e = 0; e <= 59; e += 5) t.push(e < 10 ? "0" + e : e);
                    return t
                }()
            }]
        })
    }

    static dialogsTimePickerInsert(t) {
        let e = $.extend({
            id: this.uniqid(),
            placeholder: ""
        }, t);
        return '<input type="text" style="cursor:pointer;" placeholder="' + e.placeholder + '" id="' + e.id + '"/>'
    }

    static elementToggleInsert(t) {
        let e = $.extend({
            id: this.uniqid(),
            placeholder: ""
        }, t);
        return '<input type="text" placeholder="' + e.placeholder + '" id="' + e.id + '"/>'
    }

    static afterLogin(t, e) {
        if (scGlobals.connection.authString = e, ScCore.loadMenu(), scApp.dialogs.dialogOrder.length > 0 ? (ScCore.loadNameFile(), scApp.dialogs.updateData()) : ScCore.openDefaultDialogs(), this.exHasApp()) this.exSendDeviceToken();
        else if (t.client != scGlobals.client.name) return void (window.location.href = window.location.href.split("?")[0] + "?" + e);
        scGlobals.client.name = t.client, scGlobals.externApp.loginProcedureRunning = !1, scApp.dialogs.updateData()
    }

    static exHasApp() {
        return ScDebug.out(this.isset(ScCore.exGetAppSettings().support)), this.isset(ScCore.exGetAppSettings().support)
    }

    static exSendDeviceToken() {
        if ($("#scDeviceToken").text().length > 0) {
            let t = "&deviceToken=" + $("#scDeviceToken").text();
            t += "&mobileAppId=" + this.exGetAppSettings().mobileAppId, t += "&app_version=" + this.exGetAppSettings().appVersion, t += "&dev_systemversion=" + this.exGetAppSettings().osVersion, t += "&dev_model=" + this.exGetAppSettings().modelName, this.isset(this.exGetAppSettings().platform) && (t += "&platform=" + this.exGetAppSettings().platform), ScCore.performQuery(t, function (t) {
            }.bind(this))
        }
    }

    static exGoBack() {
        Object.size(scApp.dialogs.dialogs) > 0 && "phone" == scGlobals.device.type && (scApp.flags.transitionRunning || ScCore.routerBack())
    }

    static exMessageReceived(t) {
        let e = JSON.parse(atob(t));
        for (let t in e) 1 == parseInt(ScCore.exGetAppSettings().platform) && ScCore.alert("<b>" + e[t].aps.alert.title + "</b><br>" + e[t].scooso.messageHTML), 2 == parseInt(ScCore.exGetAppSettings().platform) && ScCore.alert("<b>" + e[t].title + "</b><br>" + e[t].messageHTML)
    }

    static exSetAppCommand(t) {
        let e = $("#scSetAppCommand").html();
        e.length < 1 && (e = "[]");
        let n = jQuery.parseJSON(e);
        n.push(t), $("#scSetAppCommand").html(JSON.stringify(n))
    }

    static exResetApp() {
        ScCore.exSetAppCommand({
            command: "reset",
            params: {
                dummy: ""
            }
        })
    }

    static exGetAppSettings() {
        return jQuery.parseJSON($("#scAppSettings").html())
    }

    static exIsSupported(t) {
        return !(!ScCore.isset(ScCore.exGetAppSettings().support) || !ScCore.isset(ScCore.exGetAppSettings().support[t]))
    }

    static exAutoLogin(t) {
        let e = $.extend({
            fail: function () {
            },
            success: function () {
            }
        }, t);
        ScCore.isset(ScCore.exGetAppSettings().authString) && ScCore.exGetAppSettings().authString.length > 2 && !scGlobals.externApp.loginProcedureRunning ? (scGlobals.externApp.loginProcedureRunning = !0, scGlobals.connection.authString = ScCore.exGetAppSettings().authString.replaceAll("&amp;", "&"), ScCore.performQuery("cmd=2&subcmd=1000", function (t) {
            if (0 == t.header.state) ScCore.afterLogin({
                client: t.header.client,
                type: t.header.logType
            }, scGlobals.connection.authString), scGlobals.externApp.loginProcedureRunning = !1, e.success();
            else if (ScCore.exIsSupported("authentication")) {
                if ("android" == ScCore.exGetAppSettings().system) try {
                    scAndroidCMD.authentication("1")
                } catch (t) {
                } else ScCore.exSetAppCommand({
                    command: "authentication",
                    params: {
                        withPwd: !0
                    }
                });
                ScCore.exWaitForPwd()
            }
        }, "", {
            forceCallback: !0
        })) : e.fail()
    }

    static exWaitForPwd() {
        var t = $("#scCommandFromApp").text();
        if (t.length > 0) {
            var e = jQuery.parseJSON(t);
            "login" == e.command ? ($("#scCommandFromApp").html(""), e.params.password.length > 0 ? ScCore.performQuery("fInstitution=" + e.params.client + "&fUsername=" + e.params.username + "&fPassword=" + e.params.password, function (t) {
                4 == t.header.state ? (ScCore.exSaveLogin(e.params.client, e.params.username, e.params.password, t.header.authString), ScCore.afterLogin(t.header.log, t.header.authString)) : ScCore.moduleFunc({
                    module: "ScPrivate",
                    func: "login"
                })
            }.bind(this), "../m_index.php") : ScCore.moduleFunc({
                module: "ScPrivate",
                func: "login"
            })) : ScCore.moduleFunc({
                module: "ScPrivate",
                func: "login"
            })
        } else setTimeout(ScCore.exWaitForPwd, 200)
    }

    static exSaveLogin(t, e, n, i) {
        ScCore.exIsSupported("saveLogin") && (ScDebug.out("save login on App"), 2 == parseInt(ScCore.exGetAppSettings().platform) ? scAndroidCMD.saveLogin(t, e, n, i) : ScCore.exSetAppCommand({
            command: "saveLogin",
            params: {
                client: t,
                username: e,
                password: n,
                authString: i
            }
        }))
    }

    static exCallNumber(t) {
        if (t = t.toPhoneNumber(), 1 == parseInt(ScCore.exGetAppSettings().platform)) {
            let e = {
                command: "callNumber",
                params: {
                    number: t
                }
            };
            this.exSetAppCommand(e)
        }
        2 == parseInt(ScCore.exGetAppSettings().platform) && scAndroidCMD.callNumber(t)
    }

    static exOpenUrl(t) {
        if (".." == t.substring(0, 2) && (t = scGlobals.system.localhost ? "http://192.168.178.52/own/scssl/scooso_4_0/server/bin/php/query.php?" + t.split("?")[1] : "https://scooso.org/scooso/bin/php/query.php?" + t.split("?")[1]), 1 == parseInt(ScCore.exGetAppSettings().platform)) {
            let e = {
                command: "openUrl",
                params: {
                    url: t
                }
            };
            this.exSetAppCommand(e)
        }
        2 == parseInt(ScCore.exGetAppSettings().platform) && scAndroidCMD.openUrl(t)
    }

    static exOpenMail(t) {
        if (1 == parseInt(ScCore.exGetAppSettings().platform)) {
            let e = {
                command: "openMail",
                params: {
                    mail: t
                }
            };
            this.exSetAppCommand(e)
        }
        2 == parseInt(ScCore.exGetAppSettings().platform) && scAndroidCMD.openMail(t)
    }

    static exShowCoords(t, e, n, i) {
        if (n = n || 1e3, i = i || "", 1 == parseInt(ScCore.exGetAppSettings().platform)) {
            let s = {
                command: "showCoords",
                params: {
                    lat: t,
                    lon: e,
                    name: i,
                    radius: n
                }
            };
            this.exSetAppCommand(s)
        }
        2 == parseInt(ScCore.exGetAppSettings().platform) && scAndroidCMD.showCoords(t, e)
    }

    static exUpdateApp(t) {
        if (t = t || !1, 1 == parseInt(ScCore.exGetAppSettings().platform)) {
            let e = {};
            e = t ? {
                command: "updateAppComplete",
                params: {}
            } : {
                command: "updateApp",
                params: {}
            }, this.exSetAppCommand(e)
        }
        2 == parseInt(ScCore.exGetAppSettings().platform) && (t ? scAndroidCMD.updateAppComplete() : scAndroidCMD.updateApp())
    }

    static exScoosoIsRunning() {
        2 == parseInt(ScCore.exGetAppSettings().platform) && scAndroidCMD.scoosoIsRunning()
    }

    static copy2Clipboard(t) {
        (t = $(t)[0]).select(), t.setSelectionRange(0, 99999), document.execCommand("copy"), ScCore.alert(scStr.corCopied2Clipboard)
    }

    static checkGlobalMessage() {
        ScCore.performQuery("cmd=3000&subcmd=5000", function (t) {
            t.item.OK < 1 && ScCore.showGlobalMessage()
        })
    }

    static showGlobalMessage() {
        if (20 == scGlobals.user.type || "KNB" == scGlobals.user.username) {
            let t = ScCore.uniqid(),
                e = "\n\t\t\t\t\t\t<div class='scScrollableAlert' style=\"text-align:left;\"> Damit du auch weiterhin an Videokonferenzen teilnehmen kannst, ist deine schriftliche Zustimmung erforderlich.\n\t\t\t\t\t\t\t<br>\n\t\t\t\t\t\t\tIn <a href='#' id=" + t + "info>diesem Verzeichnis</a> findest Du die Einwilligung und weitere Informationen zur Videokonferenz. Drucke die Einwilligung aus und unterschreibe sie.\n\t\t\t\t\t\t\tWenn Du jünger als 16 Jahre bist, ist weiterhin die Unterschrift einer/eines Sorgeberechtigten erforderlich.\n\t\t\t\t\t\t\tLade anschließend ein Foto der Einwilligung auf die übliche Art und Weise in <a href='#' id=" + t + 'confirmation>dieses Verzeichnis</a>.\n\t\t\x3c!--\t\t\t\t\t<a class="link external" href=\'https://www.rwg-neuwied.de/hp/images/downloads/Elternbriefe/Schuljahr_2019_2020/webex/VorlageEinwilligungSuS_scooso.pdf\' target=_blank>Einwilligung</a>--\x3e\n\t\t\t\t\t\t\t<br><br>\n\t\t\x3c!--\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t<label class="item-checkbox item-content">\n\t\t\t\t\t\t\t\t<input name={{inputName}} type="checkbox" {{checked}}>\n\t\t\t\t\t\t\t\t<i class="icon icon-checkbox"></i>Diesen Hinweis nicht mehr anzeigen.\n\t\t\t\t\t\t\t</label>\t\n\t\t--\x3e\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</div>\n\t\t\t\t\t',
                n = scApp.f7.dialog.alert(e, "Videokonferenzen", function () {
                });
            $("#" + t + "info").click(function () {
                ScCore.moduleFunc({
                    module: "ScCloud",
                    func: "showDir",
                    params: {
                        id: 310,
                        destId: 26520,
                        destType: 10030,
                        parDate: "2020-04-20 08:00:00"
                    },
                    callback: function () {
                    }
                }), n.close()
            }), $("#" + t + "confirmation").click(function () {
                ScCore.moduleFunc({
                    module: "ScCloud",
                    func: "showDir",
                    params: {
                        id: 320,
                        destId: 26520,
                        destType: 10030,
                        parDate: "2020-04-20 08:00:00"
                    },
                    callback: function () {
                    }
                }), n.close()
            })
        }
    }

    static message2Group(t) {
        ScCore.moduleFunc({
            module: "ScMessages",
            func: "sendMessage",
            params: {
                plid: t
            },
            callback: function () {
            }
        })
    }

    static select4Mail(t) {
        ScCore.moduleFunc({
            module: "ScMessages",
            func: "select4Mail",
            params: t,
            callback: function () {
            }
        })
    }

    static mail2Group(t, e) {
        e = e || !1, this.mail2Object(2, t, e)
    }

    static mail2Object(t, e, n) {
        n = n ? 1 : 0, this.performQuery("cmd=3&subcmd=20&subsubcmd=" + t + "&id=" + e + "&videoconfirm=" + n, function (t) {
            if (0 == t.header.state)
                if (t.tables.mails.length > 0) {
                    let e = "mailto:?bcc=";
                    for (let n in t.tables.mails) e += t.tables.mails[n].value + ", ";
                    if (parseInt(ScCore.exGetAppSettings().platform) > 0) ScCore.exOpenUrl(e);
                    else {
                        let t = "<button class='button button-large'><a class='link external' href='" + e + "'>Mailprogramm öffnen</a></button>";
                        1 == n && (t = "Schülerinnen und Schüler, die die Einwilligung zu Videokonferenzen gegeben haben.<br>" + t);
                        let i = scApp.f7.dialog.create({
                            text: t,
                            closeByBackdropClick: "true",
                            on: {
                                opened: function () {
                                }
                            }
                        });
                        i.open(), $(i.el).find("a").click(function () {
                            i.close(!0)
                        })
                    }
                } else ScCore.alert("Diese Abfrage enthält keine Daten.")
        })
    }

    static loadNameFile() {
        ScDebug.out("Load Namefile...")
    }

    static decryptNameFile(t) {
        ScCore.performQuery("cmd=1000&subcmd=1150", function (e) {
            let n = e.item.encryptKey,
                i = Aes.Ctr.decrypt(t.substring(10), n, 256),
                s = Object.keys(scGlobals.anonymous.personMemory).length;
            ScDebug.out("Person Memory before: " + s), scGlobals.anonymous.personMemory = $.extend(scGlobals.anonymous.personMemory, jQuery.parseJSON(i));
            let o = Object.keys(scGlobals.anonymous.personMemory).length;
            ScDebug.out("Person Memory after: " + o);
            let r = o - s;
            ScDebug.out(r + " read"), r > 0 && (scGlobals.anonymous.personMemorySet = !0, $("#scWebAppName").css("color", "#" + scGlobals.layout.colors.main))
        }.bind(this))
    }

    static getPerson(t, e) {
        e = $.extend({}, e);
        let n = scGlobals.user;
        return this.isset(t) && (n = {
            id: 0,
            title: "",
            name: "",
            prename: "",
            username: "",
            fullname: "",
            fullnameRev: ""
        }, scGlobals.anonymous.personMemorySet && ((n = scGlobals.anonymous.personMemory[t]).id = n[0], n.title = n[1], n.name = n[2], n.prename = n[3])), (n.prename + n.name).length > 0 ? (n.fullname = n.prename + " " + n.name, n.fullnameRev = n.name + ", " + n.prename) : (n.fullname = n.username, n.fullnameRev = n.username), n
    }

    static sorter(t, e) {
    }

    static downloadFile(t) {
        if ((t = $.extend({
            fid: 0,
            onFinished: function () {
            }
        }, t)).fid > 0) {
            let e = ScCore.composeUrl("cmd=3000&subcmd=20&varname=file&file[" + t.fid + "]=on");
            this.ajax({
                url: e,
                dataType: "",
                success: function (e) {
                    t.onFinished({
                        content: e
                    })
                }
            })
        } else t.onFinished({
            content: ""
        })
    }

    static uploadFile(t) {
        (t = $.extend({
            fid: 0,
            dir: 0,
            base64: !1,
            name: "text.txt",
            destType: 0,
            destId: 0,
            parDate: "",
            content: "",
            published: !1,
            type: 10,
            onFinished: function () {
            }
        }, t)).base64 && (t.content = btoa(t.content)), scApp.f7.preloader.show(), ScCore.performQuery("cmd=3000&subcmd=9&dir=" + t.dir + "&fid=" + t.fid + "&name=" + t.name + "&destType=" + t.destType + "&destId=" + t.destId + "&sourceType=" + t.sourceType + "&sourceId=" + t.sourceId + "&parDate=" + t.parDate + "&base64=" + (t.base64 ? 1 : 0) + "&type=" + t.type + "&published=" + (t.published ? 1 : 0) + "&content=" + t.content, function (e) {
            scApp.f7.preloader.hide(), 0 == e.header.state && (scApp.dialogs.updateData("ScTimeTable_showCalendar"), scApp.dialogs.updateData("ScCloud_showDir"), t.onFinished(e), scApp.dialogs.updateData("ScCloud_showDir"))
        }, "", {
            type: "post"
        })
    }

    static showCloudDirectory(t) {
        scApp.modules.addModules({
            modules: scGlobals.externScripts.dropzone,
            callback: function () {
                ScCore.prepareCloudDirectory(t)
            }
        })
    }

    static prepareCloudDirectory(t) {
        t = $.extend({
            div: $("<div>"),
            dir: 0,
            showFileList: !0,
            showDropZone: !0,
            fieldParams: {
                destType: 0,
                destId: 0,
                parDate: ""
            },
            onOneFile: function () {
            },
            onAllFiles: function () {
            },
            onDirUpdate: function () {
            }
        }, t);
        let e = ScCore.uniqid();
        t.showFileList ? (t.div.append("<table class='scCloudDirectoryTable'><tr><td id='" + e + "_f' class=scCloudFileList scType=scCloudFileList scId=" + t.dir + " scDestType=" + t.fieldParams.destType + " scDestId=" + t.fieldParams.destId + " scParDate=" + t.fieldParams.parDate + "></td></tr><tr><td id='" + e + "_t'></td></tr></table>"), $("#" + e + "_t").append("<div id=" + e + " class='dropzone dropzone-previews'></div>")) : t.div.append("<div id=" + e + " class='dropzone dropzone-previews'></div>"), t.div_f = $("#" + e + "_f");
        let n = $.extend({
                cmd: 3e3,
                subcmd: 10,
                dir: t.dir,
                destType: t.fieldParams.destType,
                destId: t.fieldParams.destId,
                parDate: t.fieldParams.parDate
            }, ScCore.getAuthParams()),
            i = parseInt(scGlobals.connection.postMaxSize / 1024 / 1024),
            s = scGlobals.connection.postMaxSize,
            o = {
                url: scGlobals.connection.path2PHP + "query.php",
                maxFilesize: i,
                resizeWidth: scGlobals.connection.maxImgWidth,
                accept: function (t, e) {
                    ScDebug.out(t);
                    let n = t.name.fileExtension();
                    ["pdf", "txt", "doc", "docx", "xlsx", "xls", "ppt", "pptx", "jpg", "jpeg", "png", "mp3", "wma", "zip"].includes(n.toLowerCase()) || 21 == scGlobals.user.type ? t.size > s ? (e(sprintf(scStr.corFileTooBig, i)), ScCore.alert(sprintf(scStr.corFileTooBig, i))) : e() : (e(scStr.corNoValidFileType), ScCore.alert(scStr.corNoValidFileType))
                },
                init: function () {
                    this.on("complete", function (e) {
                        0 === this.getUploadingFiles().length && 0 === this.getQueuedFiles().length ? 310 == t.dir || 320 == t.dir ? (scApp.dialogs.updateData("ScTimeTable_showCalendar"), ScCore.performQuery("cmd=3000&subcmd=13&dir=" + t.dir + "&destType=" + n.destType + "&destId=" + n.destId + "&parDate=" + n.parDate, function (e) {
                            0 == e.header.state && (ScDebug.out("All uploaded"), t.showFileList && ScCore.getFilesOfCloudDirectory(t), scApp.dialogs.updateData("ScTimeTable_showCalendar"), scApp.dialogs.updateData("ScCloud_showDir"), scApp.dialogs.updateData("ScTimeTable_showTodoList"), scApp.dialogs.updateData("ScTimeTable_showMyEvents"), t.onAllFiles())
                        })) : (ScDebug.out("All uploaded"), t.showFileList && ScCore.getFilesOfCloudDirectory(t), scApp.dialogs.updateData("ScTimeTable_showCalendar"), scApp.dialogs.updateData("ScCloud_showDir"), scApp.dialogs.updateData("ScTimeTable_showTodoList"), scApp.dialogs.updateData("ScTimeTable_showMyEvents"), t.onAllFiles()) : (ScDebug.out("One file uploaded:", e), t.onOneFile(e))
                    }), this.on("sending", function (t, e, n) {
                    })
                },
                queuecomplete: function (t, e) {
                    ScDebug.out(t, e)
                },
                params: n
            };
        o = $.extend(scStr.corDropzone, o), t.div.find("#" + e).dropzone(o), 310 == t.dir && 21 != scGlobals.user.type && t.div.find("#" + e).hide(), t.showDropZone || t.div.find("#" + e).hide(), t.div.find(".dropzone").addClass("no-fastclick"), t.showFileList && ScCore.getFilesOfCloudDirectory(t)
    }

    static getFilesOfCloudDirectory(t) {
        (t = $.extend({
            div_f: $("<div>"),
            dir: 0
        }, t)).dir > 0 ? this.loadCloudFileLists({
            div_f: t.div_f,
            dir: t.dir,
            fieldParams: t.fieldParams,
            callback: function (e) {
                t.div_f.unbind(), t.div_f.click(function () {
                    ScCore.moduleFunc({
                        module: "ScCloud",
                        func: "showDir",
                        params: {
                            id: t.dir,
                            destId: t.fieldParams.destId,
                            destType: t.fieldParams.destType,
                            parDate: t.fieldParams.parDate
                        },
                        callback: function () {
                        }
                    })
                }), t.onDirUpdate(e)
            }
        }) : t.onDirUpdate([])
    }

    static loadCloudFileLists(t) {
        let e = "&destid=" + (t = $.extend({
            div_f: $("<div>"),
            dir: 0,
            callback: function () {
            }
        }, t)).fieldParams.destId + "&desttype=" + t.fieldParams.destType + "&pardate=" + t.fieldParams.parDate;
        ScCore.performQuery("cmd=4000&subcmd=5&subsubcmd=2&prop=" + t.dir + e, function (e) {
            if (0 == e.header.state) {
                let n = [];
                t.div_f.empty();
                for (let i in e.tables.items) {
                    let s = e.tables.items[i].name;
                    t.div_f.append(s.shorten(30) + "<br>"), n.push({
                        name: s
                    })
                }
                t.callback(n)
            }
        }.bind(this))
    }

    static updateCloudFileLists(t) {
        t = $.extend({
            div_f: $("<div>"),
            dir: 0,
            noBind: !1,
            onDirUpdate: function () {
            }
        }, t), $("[scType=scCloudFileList]").each(function (t) {
            ScCore.loadCloudFileLists({
                div_f: $(this),
                dir: $(this).attr("scId"),
                fieldParams: {
                    destType: $(this).attr("scDestType"),
                    destId: $(this).attr("scDestId"),
                    parDate: $(this).attr("scParDate")
                }
            })
        })
    }

    static attachLinks(t) {
        t.find("[scLinkToPerson]").click(function () {
            let t = $(this).attr("scLinkToPerson");
            ScCore.moduleFunc({
                module: "ScPersons",
                func: "show",
                params: {
                    id: t
                }
            })
        }), t.find("[scLinkToPersonImage]").click(function () {
            let t = $(this).attr("scLinkToPersonImage");
            ScCore.moduleFunc({
                module: "ScPersons",
                func: "showImage",
                params: {
                    id: t
                }
            })
        }), t.find("[scLinkToUrl]").click(function () {
            let t = $(this).attr("scLinkToUrl");
            "http" != t.substring(0, 4) && (t = "http://" + t), ScCore.exGetAppSettings().platform > 0 ? ScCore.exOpenUrl(t) : window.open(t, "_blank")
        }), t.find("[scLinkToEmail]").click(function () {
            let t = $(this).attr("scLinkToEmail");
            ScCore.exGetAppSettings().platform > 0 ? ScCore.exOpenMail(t) : window.open("mailto:" + t, "_blank")
        }), t.find("[scLinkToPhone]").click(function () {
            let t = $(this).attr("scLinkToPhone").toPhoneNumber();
            ScCore.exGetAppSettings().platform > 0 ? ScCore.exCallNumber(t) : window.open("tel:" + t, "_blank")
        }), t.find("[scLinkToLocation]").click(function () {
            let t = $(this).attr("scLinkToLocation"),
                e = "https://www.google.de/maps/place/" + t;
            t.length > 0 && (ScCore.exGetAppSettings().platform > 0 ? ScCore.exOpenUrl(e) : window.open(e, "_blank"))
        })
    }

    static loadScript(t, e, n) {
        if (e = e || function () {
        }, n = n || function () {
        }, ScCore.isset(scApp.modules.externScripts[t])) e(), n();
        else if (ScCore.isset(scGlobals.externScripts[t])) {
            let i = scGlobals.connection.path2ExternJS + scGlobals.externScripts[t].file;
            $.getScript(i, function () {
                if (ScDebug.out("Extern script " + t + " loaded: " + i), scApp.modules.externScripts[t] = !0, ScCore.isset(scGlobals.externScripts[t].css)) {
                    let e = scGlobals.connection.path2ExternJS + scGlobals.externScripts[t].css;
                    ScDebug.out("Extern css " + t + " loaded: " + e), e += "?_=" + Math.random(), $("head").append('<link rel="stylesheet" href="' + e + '" type="text/css" />')
                }
                e(), n()
            }).fail(function () {
                arguments[0].readyState
            })
        }
    }

    static bitTest(t, e) {
        return 1 == (t >> e & 1)
    }

    static s2ab(t) {
        for (var e = new ArrayBuffer(t.length), n = new Uint8Array(e), i = 0; i != t.length; ++i) n[i] = 255 & t.charCodeAt(i);
        return e
    }
}

class ScProgressor {
    constructor(t, e, n, i) {
        this.callback = t, this.start = e, this.end = n, this.step = i, this.runProgress(this.start)
    }

    runProgress(t) {
        let e = t + this.step;
        if (e > this.end && (e = this.end), this.callback(t, e), e < this.end) {
            let t = this;
            setTimeout(function () {
                t.runProgress(e)
            }, 5)
        }
    }
}

class ScCanvasBox {
    static roundRect(t, e, n, i, s, o, r, a) {
        if (void 0 === a && (a = !0), void 0 === o && (o = 5), "number" == typeof o) o = {
            tl: o,
            tr: o,
            br: o,
            bl: o
        };
        else {
            var c = {
                tl: 0,
                tr: 0,
                br: 0,
                bl: 0
            };
            for (var l in c) o[l] = o[l] || c[l]
        }
        t.beginPath(), t.moveTo(e + o.tl, n), t.lineTo(e + i - o.tr, n), t.quadraticCurveTo(e + i, n, e + i, n + o.tr), t.lineTo(e + i, n + s - o.br), t.quadraticCurveTo(e + i, n + s, e + i - o.br, n + s), t.lineTo(e + o.bl, n + s), t.quadraticCurveTo(e, n + s, e, n + s - o.bl), t.lineTo(e, n + o.tl), t.quadraticCurveTo(e, n, e + o.tl, n), t.closePath(), r && t.fill(), a && t.stroke()
    }
}

class ScModules {
    constructor() {
        this.modules = {}, this.externScripts = {}
    }

    addModule(params1) {
        let params = $.extend({}, {
                name: "",
                lang: scGlobals.user.lang,
                extern: !1,
                callback: function () {
                },
                _callback: function () {
                }
            }, params1),
            thiz = this;
        if (params.extern) ScCore.loadScript(params.name, params.callback, params._callback);
        else {
            let moduleDir = scGlobals.connection.path2Modules + params.name.toUpperCase() + "/",
                langURL = moduleDir + "lang/" + params.lang + ".js",
                scriptURL = moduleDir + params.name + ".js";
            ScCore.isset(this.modules[params.name]) ? (params.callback(), params._callback()) : (ScDebug.out("load module: " + params.name), $.getScript(langURL, function () {
                ScDebug.out("Module " + params.name + " loaded: " + langURL), $.getScript(scriptURL, function () {
                    ScDebug.out("Module " + params.name + " loaded: " + scriptURL), thiz.modules[params.name] = eval("new " + params.name + "()"), thiz.modules[params.name]._loadDependencies(function () {
                        thiz.modules[params.name].initialize({
                            callback: function () {
                                params.callback(), params._callback()
                            }
                        })
                    })
                })
            }))
        }
    }

    addModules(t) {
        let e = $.extend({}, {
            modules: [],
            callback: function () {
            }
        }, t);
        if (e.modules.length > 0) {
            let t = e.modules.shift(),
                n = this;
            t._callback = function () {
                n.addModules(e)
            }, this.addModule(t)
        } else e.callback()
    }
}

class ScModule {
    constructor() {
        this.dependencies = []
    }

    _loadDependencies(t) {
        scApp.modules.addModules({
            modules: this.dependencies,
            callback: t
        })
    }

    initialize(t) {
        this.params = $.extend({
            callback: {}
        }, t), ScDebug.out("Module " + this.constructor.name + " initialized."), t.callback()
    }
}

class ScContent {
    constructor() {
        this.params, this.templates = [], this.div, this.module = scApp.modules.modules[this.constructor.name.split("_")[0]], this.dependencies = [], ScDebug.out("Content " + this.constructor.name + " created")
    }

    getDialog() {
        return this.params.dialog
    }

    closeDialog() {
        scApp.dialogs.close(this.params.dialogId)
    }

    getHeight() {
        return this.params.dialog.getHeight()
    }

    setParams(t) {
        this.params = $.extend({
            call: {},
            contentDiv: void 0
        }, t), this.div = $("#" + this.params.contentDiv)
    }

    update() {
        this.getContexts(function (t) {
            if (this.templates.length > 0) {
                let e = $("<div>");
                for (let n in this.templates) {
                    let i = ScCore.template(this.templates[n], t[n]);
                    e.append(i)
                }
                this.setContent(e)
            }
            this.prepare(), this.detachEvents(), this.attachEvents(), this.div.find("[scTemplateCheckboxSelectAll]").change(function () {
                $(this).prop("checked") ? $(this).closest("ul").find("input:checkbox").prop("checked", "checked") : $(this).closest("ul").find("input:checkbox").prop("checked", "")
            })
        }.bind(this))
    }

    setContent(t) {
        this.div.html(t), this.div.find("input[type!=hidden]:first").focus()
    }

    setTitle(t) {
        this.params.dialog.setTitle(t)
    }

    detachEvents() {
        this.div.off()
    }

    getTitle() {
        return this.title || ""
    }

    getContexts(t) {
        t([])
    }

    initialize() {
    }

    prepare() {
    }

    attachEvents() {
    }

    updateData() {
        this.update()
    }
}

class ScDialogs {
    constructor(t) {
        this.params = $.extend({
            div: $("#" + scGlobals.layout.mainContentDiv)
        }, t), this.dialogs = {}, this.dialogOrder = [], this.dialogs2Add = [], this.phone = "phone" == scGlobals.device.type
    }

    addDialogs(t) {
        if (this.phone) {
            ScCore.isset(t) && (this.dialogs2Add = t);
            let e = this.dialogs2Add.shift();
            ScCore.isset(e) && scApp.dialogs.addDialog(e)
        } else
            for (let e in t) scApp.dialogs.addDialog(t[e])
    }

    addDialog(t) {
        let e = new ScDialog(t);
        this.dialogs[e.id] = e, this.dialogOrder.push(e), scGlobals.layout.showMenu || 1 != Object.size(this.dialogs) || e.contentDiv.parents().find(".navbar").find(".left").css("visibility", "hidden"), ScDebug.out("Dialog added", this.dialogs, this.dialogOrder), this.arrange()
    }

    closeLast() {
        let t = this.dialogOrder[this.dialogOrder.length - 1].id;
        this.close(t)
    }

    close(t) {
        this.phone ? ScCore.routerBack() : this.dialogs[t].panel.close(), this.remove(t)
    }

    closeAll() {
        for (let t in this.dialogs) this.close(t)
    }

    id2Number(t) {
        for (let e in this.dialogOrder)
            if (t == this.dialogOrder[e].id) return e
    }

    remove(t) {
        if (ScCore.isset(t) && (t.search("contextMenu") < 0 && (delete this.dialogs[t], this.dialogOrder.splice(this.id2Number(t), 1), ScDebug.out("Dialog removed with id: " + t, this.dialogs, this.dialogOrder), this.arrange()), !this.phone))
            for (let e in this.dialogs) {
                ScDebug.out("parent", this.dialogs[e]), this.dialogs[e].parentId == t && this.close(this.dialogs[e].id)
            }
    }

    removeAll() {
        for (let t in this.dialogs) this.remove(t)
    }

    arrange() {
        if (!this.phone) {
            let t = $(".navbar").height() || 0,
                e = t > 0 ? scGlobals.layout.panelMargin : 0;
            t = t > 0 ? scGlobals.layout.panelMargin + t : 0;
            let n = scGlobals.layout.panelMargin,
                i = e,
                s = t;
            for (let t in this.dialogs)
                if ("maximized" != this.dialogs[t].panel.status && !this.dialogs[t].panelConfig.position) {
                    let e = parseInt(this.dialogs[t].panelConfig.panelSize.width),
                        o = ScCore.getPageWidth();
                    e = e > o ? o : e, this.dialogs[t].panel.resize({
                        width: e - 2 * n
                    }), i + this.dialogs[t].panel.clientWidth > this.params.div.width() && (i = this.params.div.width() - this.dialogs[t].panel.clientWidth - n), i < 0 && (i = 0), this.dialogs[t].panel.reposition("left-top " + i + " " + s), i += this.dialogs[t].panel.clientWidth + n
                }
        }
    }

    updateData(t) {
        for (let e in this.dialogs) this.dialogs[e].updateData(t)
    }

    getActiveUpdateTypes() {
        let t = {};
        for (let e in this.dialogs) {
            let n = this.dialogs[e];
            for (let e in n.contents) {
                let i = n.contents[e].updateType;
                ScCore.isset(t[i]) ? t[i]++ : t[i] = 1
            }
        }
        return ScDebug.out(t), t
    }
}

class ScDialog {
    constructor(t) {
        this.params = $.extend({
            title: "",
            config: {},
            contents: []
        }, t), this.id = ScCore.uniqid(), this.contentId = ScCore.uniqid(), this.panel, this.panelConfig, this.setPanelConfig(this.params.config), this.phone = "phone" == scGlobals.device.type, this.contentDiv, this.title = this.title || this.params.title, this.contents = {}, this.contentsCreated = !1, this.create()
    }

    create() {
        this.phone ? (0 == this.params.title.length && (this.params.title = " "), scApp.f7.views.main.router.navigate("/query/" + this.id + "/" + this.contentId + "/" + this.params.title, {}), this.contentDiv = $("#" + this.contentId)) : (this.panelConfig.id = this.id, this.panel = jsPanel.create(this.panelConfig), this.contentDiv = $(this.panel.content), this.createPanelMenu(), this.addContents(), this.setTitle(this.title), this.panelConfig.maximize && this.maximizePanel()), scApp.f7.panel.close()
    }

    createPanelMenu() {
        let t = this;
        if (ScCore.isset(this.params.config.menu) && this.params.config.menu.length > 0) {
            this.panel.setHeaderLogo("<i class='icon f7-icons scContextMenuIcon' >bars</i>");
            let e = this.params.config.menu;
            $(this.panel.headerlogo).click(function (n) {
                let i = (n.pageX || n.touches[0].pageX) + "px",
                    s = (n.pageY || n.touches[0].pageY) + "px",
                    o = '<div class="scListGroup scContextMenu">',
                    r = 0;
                for (let t in e) {
                    let n = t > 0 ? "scContextMenuNewGroup" : "";
                    for (let i in e[t]) {
                        let s = e[t][i].color || "";
                        s.length > 0 && (s = 'style="color:' + s + '"'), o += '<a class="scListGroupItem ' + n + '" href="#" cmi="' + r + '" ' + s + '><i class="icon f7-icons scContextMenuIcon">' + e[t][i].icon + "</i> " + e[t][i].title + "</a>", r++
                    }
                }
                o += "</div>", jsPanel.create($.extend({}, scConstants.contextMenuConfig, {
                    content: o
                }), function (n) {
                    jsPanel.setStyle(n, {
                        position: "absolute",
                        left: i,
                        top: s
                    }), n.addEventListener("mouseleave", function () {
                        n.close()
                    }, !1), n.addEventListener("touchend", function () {
                        n.close()
                    }, !1), $(n).find(".icon").css("font-size", scGlobals.layout.contextMenuIconSize + "px"), t.attachMenuActions(n, e)
                })
            })
        }
    }

    createPhoneMenu() {
        let t = this;
        if (ScCore.isset(this.params.config.menu)) {
            if (this.params.config.menu.length > 0) {
                let e = this.params.config.menu;
                $("#" + this.id + "_cmenu").unbind().click(function () {
                    let n = [];
                    for (let i in e) {
                        let s = [];
                        for (let n in e[i]) s.push({
                            text: '<i class="icon f7-icons scContextMenuIcon">' + e[i][n].icon + "</i> " + e[i][n].title,
                            onClick: function () {
                                e[i][n].action(t)
                            },
                            color: e[i][n].color || ""
                        });
                        n.push(s)
                    }
                    scApp.f7.actions.create({
                        buttons: n
                    }).open()
                }).css("display", "initial")
            }
        } else $("#" + this.id).parent().find(".scContextMenuPhone").css("display", "none")
    }

    attachMenuActions(t, e) {
        let n = this,
            i = 0;
        for (let s in e)
            for (let o in e[s]) $(t).find("[cmi=" + i + "]").click(function () {
                e[s][o].action(n)
            }), i++
    }

    addContents() {
        if (this.phone && this.createPhoneMenu(), !this.contentsCreated) {
            let t = this.params.contents.slice();
            this.addContent(t);
            let e = this.contents[Object.keys(this.contents)[0]].getTitle();
            e.length > 0 && this.setTitle(e), this.contentsCreated = !0
        }
    }

    addContent(cs) {
        let content = cs.shift(),
            contentDiv = ScCore.uniqid();
        this.append("<div id='" + contentDiv + "'><br><br><div class='text-align-center'><div class='preloader'  style='width: 44px; height: 44px'></div></div></div>");
        let cname = content.module + "_" + content.func,
            contentId = ScCore.uniqid();
        this.contents[contentId] = eval("new " + cname + "()"), this.contents[contentId].updateType = this.contents[contentId].updateType || this.contents[contentId].constructor.name;
        let thiz = this;
        scApp.modules.addModules({
            modules: thiz.contents[contentId].dependencies,
            callback: function () {
                let t = $.extend({}, thiz.params.contents.params, {
                    call: content,
                    contentDiv: contentDiv,
                    dialogId: thiz.id,
                    dialog: thiz
                });
                thiz.contents[contentId].setParams(t), thiz.contents[contentId].initialize(), thiz.contents[contentId].update(), thiz.contents[contentId].dialog = thiz, ScCore.isset(t.call.params) && ScCore.isset(t.call.params.parent) && (thiz.parentId = t.call.params.parent), cs.length > 0 && thiz.addContent(cs)
            }
        })
    }

    updateData(t) {
        t = t || "";
        for (let e in this.contents) {
            (this.contents[e].updateType || "") != t && 0 != t.length || this.contents[e].updateData()
        }
    }

    append(t) {
        this.contentDiv.append(t)
    }

    setContent(t) {
        this.contentDiv.html(t)
    }

    setTitle(t) {
        ScCore.isset(t) && (this.phone ? this.contentDiv.parent().parent().find(".navbar-current").find(".title").html(t) : this.panel.setHeaderTitle(t))
    }

    maximizePanel() {
        this.panelConfig.header || $("#scHomePageContent").css("overflow", "hidden"), this.panel.maximize()
    }

    hidePreloader() {
        this.phone ? scApp.f7.preloader.hide() : this.panel.setHeaderLogo("")
    }

    showPreloader() {
        this.phone ? scApp.f7.preloader.show() : this.panel.setHeaderLogo('<div class="preloader color-white" style="margin-left:4px"></div>')
    }

    showListIndex() {
        $("#" + this.id + "_listIndex").css("display", "inline")
    }

    showSearchBar(t) {
        let e = $.extend({
            el: "#" + this.id + "_searchbar",
            searchContainer: ".list",
            searchIn: ".item-title",
            on: {
                search(t, e, n) {
                    console.log(e, n)
                }
            }
        }, t);
        return ScDebug.out($("#" + this.id + "_searchbar")), scApp.f7.searchbar.create(e)
    }

    setPanelConfig(t) {
        let e = $(".navbar").height() || 0;
        e > 0 && scGlobals.layout.panelMargin;
        e = e > 0 ? scGlobals.layout.panelMargin + e : 0;
        let n = $(".toolbar").height() || 0;
        n = n > 0 ? scGlobals.layout.panelMargin + n : 0, this.panelConfig = $.extend({
            dragit: {
                opacity: .8
            },
            theme: "#" + scGlobals.layout.colors.main,
            headerControls: {
                minimize: "remove"
            },
            boxShadow: 1,
            container: "#scHomePageContent",
            panelSize: {
                width: scGlobals.layout.panelWidth,
                height: ScCore.autoPanelHeight()
            },
            content: "",
            contentOverflow: "auto",
            maximizedMargin: [e, 0, n, 0],
            syncMargins: !0,
            callback: function (t) {
            },
            onbeforeclose: function () {
                return !0
            }
        }, t)
    }

    getContentByNumber(t) {
        for (let e in this.contents)
            if (this.contents[e].params.call.number == t) return this.contents[e]
    }

    getHeight() {
        return this.contentDiv.height()
    }

    getWidth() {
        return this.contentDiv.width()
    }
}

class ScIO {
    constructor() {
    }

    static onDrag(t) {
        return void 0 !== t && null != t
    }
}

const scConstants = {
    panelOnlyClose: {
        maximize: "remove",
        minimize: "remove",
        smallify: "remove",
        smallifyrev: "remove",
        normalize: "remove"
    },
    panelModalConfig: {
        dragit: !1,
        theme: "#" + scGlobals.layout.colors.main,
        closeOnEscape: !0,
        headerControls: {
            maximize: "remove",
            minimize: "remove",
            smallify: "remove",
            smallifyrev: "remove",
            normalize: "remove"
        },
        headerTitle: scGlobals.system.dialogTitle,
        boxShadow: 1,
        container: "#scHomePageContent",
        position: "center",
        panelSize: "450 350",
        contentOverflow: "auto",
        syncMargins: !0,
        callback: function (t) {
        },
        onbeforeclose: function () {
            return !0
        }
    },
    contextMenuConfig: {
        id: "contextMenu" + ScCore.uniqid(),
        dragit: !1,
        theme: "#" + scGlobals.layout.colors.main,
        closeOnEscape: !0,
        headerControls: "none",
        header: !1,
        boxShadow: 1,
        container: "#scHomePageContent",
        panelSize: {
            width: "auto",
            height: "auto"
        },
        content: "",
        contentOverflow: "auto",
        syncMargins: !0,
        callback: function (t) {
        },
        onbeforeclose: function () {
            return !0
        }
    }
};
Number.prototype.pad = function (t, e) {
    return ScCore.pad(this, t, e)
}, Number.prototype.checksum = function () {
    return this < 10 ? this : this % 9
}, String.prototype.pad = function (t, e) {
    return ScCore.pad(this, t, e)
}, String.prototype.replaceAll = function (t, e) {
    return this.replace(new RegExp(t, "g"), e)
}, String.prototype.toPhoneNumber = function () {
    return this.replace(/[^\d\+]/g, "")
}, String.prototype.mySql2Iso1 = function () {
    return this.replace(" ", "T")
}, String.prototype.mySql2Iso2 = function () {
    return this.replace(" ", "T") + ".000Z"
}, String.prototype.mySql2Local = function () {
    let t = "";
    if (19 != this.length && 10 != this.length || (t = this.substring(8, 10) + "." + this.substring(5, 7) + "." + this.substring(0, 4)), 10 == this.length) return t;
    return 8 == this.length ? this.substring(0, 5) : 19 == this.length ? t + ", " + this.substring(11, 16) : ""
}, String.prototype.mySql2LocalDate = function () {
    return this.mySql2Local().substr(0, 10)
}, String.prototype.iso2Local = function () {
    return this.substring(0, 19).replace("T", " ").mySql2Local()
}, String.prototype.mySql2Date = function () {
    let t = this.split(/[- :]/);
    return t[1]--, new Date(...t)
}, String.prototype.shorten = function (t) {
    return this.length > t - 3 ? this.substr(0, t - 3) + "..." : this.substr(0, t)
}, String.prototype.checkExtension = function (t) {
    return this.length > 0 ? this.replace("." + t, "") + "." + t : ""
}, String.prototype.fileExtension = function (t) {
    return this.split(".").pop()
}, String.prototype.humanFileSize = function () {
    let t = parseInt(this),
        e = 0 == t ? 0 : Math.floor(Math.log(t) / Math.log(1024));
    return 1 * (t / Math.pow(1024, e)).toFixed(2) + " " + ["B", "kB", "MB", "GB", "TB"][e]
}, String.prototype.toHTML = function () {
    return this.replace(/\n/g, "<br />")
}, String.prototype.random = function (t) {
    let e = "",
        n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        i = n.length;
    for (let s = 0; s < t; s++) e += n.charAt(Math.floor(Math.random() * i));
    return e
}, Object.size = function (t) {
    var e, n = 0;
    for (e in t) t.hasOwnProperty(e) && n++;
    return n
}, Date.prototype.getWeekNumber = function () {
    var t = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate())),
        e = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - e);
    var n = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil(((t - n) / 864e5 + 1) / 7)
}, Date.prototype.toMySql = function () {
    return this.toISOString().slice(0, 19).replace("T", " ")
}, Date.prototype.ddmmyyyy = function () {
    var t = this.getFullYear().toString(),
        e = (this.getMonth() + 1).toString(),
        n = this.getDate().toString();
    return (n[1] ? n : "0" + n[0]) + "." + (e[1] ? e : "0" + e[0]) + "." + t
}, Date.prototype.yyyymmdd = function () {
    var t = this.getFullYear().toString(),
        e = (this.getMonth() + 1).toString(),
        n = this.getDate().toString();
    return t + "-" + (e[1] ? e : "0" + e[0]) + "-" + (n[1] ? n : "0" + n[0])
}, Date.prototype.addDays = function (t) {
    return new Date(this.valueOf() + 864e5 * t)
}, jQuery.download = function (t, e, n) {
    if (t && e) {
        e = "string" == typeof e ? e : jQuery.param(e);
        var i = "";
        jQuery.each(e.split("&"), function () {
            var t = this.split("=");
            i += '<input type="hidden" name="' + t[0] + '" value="' + t[1] + '" />'
        }), jQuery('<form action="' + t + '" method="' + (n || "post") + '">' + i + "</form>").appendTo("body").submit().remove()
    }
}, $.fn.extend({
    disableSelection: function () {
        this.each(function () {
            this.onselectstart = function () {
                return !1
            }, this.unselectable = "on", $(this).css("-moz-user-select", "none"), $(this).css("-webkit-user-select", "none")
        })
    }
}), $.fn.extend({
    scEnter: function (t) {
        this.each(function () {
            $(this).keypress(function (e) {
                if (13 == e.which) return t(), !1
            })
        })
    }
}), $.fn.extend({
    toggleButton: function () {
        this.each(function () {
            $(this).hasClass("scButton-active") ? $(this).removeClass("scButton-active") : $(this).addClass("scButton-active")
        })
    }
}), $.fn.extend({
    setButtonStatus: function (t) {
        this.each(function () {
            t ? $(this).addClass("scButton-active") : $(this).removeClass("scButton-active")
        })
    }
}), $.fn.extend({
    scVal: function (t) {
        if ("checkbox" == $(this).attr("type")) {
            if (!ScCore.isset(t)) return $(this).is(":checked") ? 1 : 0;
            t > 0 ? $(this).prop("checked", !0) : $(this).prop("checked", !1)
        } else {
            if (!ScCore.isset(t)) return $(this).val();
            $(this).val(t)
        }
    }
}),
    function (t) {
        t.fn.pop = function () {
            var t = this.get(-1);
            return this.splice(this.length - 1, 1), t
        }, t.fn.shift = function () {
            var t = this.get(0);
            return this.splice(0, 1), t
        }
    }(jQuery);

class ScClock {
    constructor(t) {
        this.div = t, this.started = !1, this.timer, this.startTime
    }

    start() {
        this.started = !0, this.div.html("0.0"), this.startTime = (new Date).getTime(), this.timer = setInterval(function () {
            let t = (((new Date).getTime() - this.startTime) / 1e3).toFixed(1);
            "INPUT" == this.div.prop("tagName") ? this.div.val(t) : this.div.text(t)
        }.bind(this), 10)
    }

    stop() {
        clearInterval(this.timer)
    }
}

function KolorWheel(t) {
    this.resultList = [this], this.elm = null, void 0 === t && (t = "#000000"), "function" == typeof t.validateHsl ? this.setHsl([t.h, t.s, t.l]) : this.setColor(t)
}

KolorWheel.prototype.setColor = function (t) {
    void 0 !== t && ("object" == typeof t ? this.setHsl(t) : this.setHex(t))
}, KolorWheel.prototype.setHsl = function (t) {
    return this.h = t[0], this.s = t[1], this.l = t[2], this.validateHsl(), this
}, KolorWheel.prototype.validateHsl = function () {
    this.h = this.h % 360, this.h < 0 && (this.h += 360), this.s < 0 && (this.s = 0), this.s > 100 && (this.s = 100), this.l < 0 && (this.l = 0), this.l > 100 && (this.l = 100)
}, KolorWheel.prototype.setHex = function (t) {
    "#" == t.substring(0, 1) && (t = t.substring(1));
    var e = parseInt(t.substring(0, 2), 16),
        n = parseInt(t.substring(2, 4), 16),
        i = parseInt(t.substring(4, 6), 16);
    return this.setRgb([e, n, i]), this
}, KolorWheel.prototype.setRgb = function (t) {
    var e = t[0] / 255,
        n = t[1] / 255,
        i = t[2] / 255,
        s = Math.max(e, n, i),
        o = Math.min(e, n, i);
    if (this.h = (s + o) / 2, this.s = this.h, this.l = this.h, s == o) this.h = 0, this.s = 0;
    else {
        var r = s - o;
        switch (this.s = this.l > .5 ? r / (2 - s - o) : r / (s + o), s) {
            case e:
                this.h = (n - i) / r + (n < i ? 6 : 0);
                break;
            case n:
                this.h = (i - e) / r + 2;
                break;
            case i:
                this.h = (e - n) / r + 4
        }
        this.h = this.h / 6
    }
    return this.h = 360 * this.h, this.s = 100 * this.s, this.l = 100 * this.l, this
}, KolorWheel.prototype.hue2rgb = function (t, e, n) {
    return n < 0 && (n += 1), n > 1 && (n -= 1), n < 1 / 6 ? t + 6 * (e - t) * n : n < .5 ? e : n < 2 / 3 ? t + (e - t) * (2 / 3 - n) * 6 : t
}, KolorWheel.prototype.getRgb = function () {
    this.validateHsl();
    var t = this.h / 360,
        e = this.s / 100,
        n = this.l / 100,
        i = n,
        s = n,
        o = n;
    if (0 != e) {
        var r = n < .5 ? n * (1 + e) : n + e - n * e,
            a = 2 * n - r;
        i = this.hue2rgb(a, r, t + 1 / 3), s = this.hue2rgb(a, r, t), o = this.hue2rgb(a, r, t - 1 / 3)
    }
    return [Math.round(255 * i), Math.round(255 * s), Math.round(255 * o)]
}, KolorWheel.prototype.getHex = function () {
    var t = this.getRgb(),
        e = this.toHexByte(t[0]);
    return e += this.toHexByte(t[1]), "#" + (e += this.toHexByte(t[2])).toUpperCase()
}, KolorWheel.prototype.toHexByte = function (t) {
    var e = t.toString(16);
    return e.length < 2 && (e = "0" + e), e
}, KolorWheel.prototype.getHsl = function () {
    return this.validateHsl(), [this.h, this.s, this.l]
}, KolorWheel.prototype.multi = function (t, e, n, i, s, o, r, a, c, l) {
    var u = [].concat(this.resultList);
    for (var p in this.resultList = [], u) {
        var h = u[p];
        h.workList = [], "rel" == t && KolorWheel.prototype.spinSingle.call(h, "rel", e, n, i, s, o, r, a, c, l), "abs" == t && KolorWheel.prototype.spinSingle.call(h, "abs", e, n, i, s, o, r, a, c, l), this.resultList = this.resultList.concat(h.workList)
    }
    if (0 == this.resultList.length) return this;
    var d = this.resultList[this.resultList.length - 1];
    return this.h = d.h, this.s = d.s, this.l = d.l, this
}, KolorWheel.prototype.rel = function (t, e, n, i, s) {
    return this.multi("rel", t, e, n, i, s)
}, KolorWheel.prototype.abs = function (t, e, n, i, s) {
    var o = !1;
    if ("object" == typeof t ? "function" == typeof t.validateHsl && (o = !0) : ("#" == ("" + t).substring(0, 1) && (o = !0), ("" + t).length > 4 && (o = !0)), o) {
        var r = new KolorWheel(t);
        return this.multi("abs", r.h, r.s, r.l, e, n)
    }
    return this.multi("abs", t, e, n, i, s)
}, KolorWheel.prototype.spinSingle = function (t, e, n, i, s, o) {
    var r = "abs" == t ? -1 : 0;
    void 0 === e && (e = r), void 0 === n && (n = r), void 0 === i && (i = r), void 0 === e && (s = 12);
    var a = 0,
        c = 0,
        l = 0;
    "object" == typeof e && (a = e.length), "object" == typeof n && (c = n.length), "object" == typeof i && (l = i.length), void 0 === s && (a > (s = 1) && (s = a), c > s && (s = c), l > s && (s = l)), void 0 === o && (o = 0);
    var u = null;
    for ("object" == typeof s && (s = (u = s).length), step = o; step < s; step++) {
        var p, h, d, f = new KolorWheel(this),
            m = 1 == s ? 1 : step / (s - 1);
        p = a > 0 ? e[step % a] : e * m, h = c > 0 ? n[step % c] : n * m, d = l > 0 ? i[step % l] : i * m, "rel" == t ? (f.h += p, f.s += h, f.l += d) : (f.h = e == r ? this.h : 0 == a ? this.calcLinearGradientStep(step, s, this.h, e) : p, f.s = n == r ? this.s : 0 == c ? this.calcLinearGradientStep(step, s, this.s, n) : h, f.l = i == r ? this.l : 0 == l ? this.calcLinearGradientStep(step, s, this.l, i) : d), f.step = step, u && (f.elm = u.eq(step)), this.workList[step] = f
    }
}, KolorWheel.prototype.calcLinearGradientStep = function (t, e, n, i) {
    return n + t / (e - 1) * (i - n)
}, KolorWheel.prototype.each = function (t) {
    for (var e in this.resultList) t.call(this.resultList[e], this.resultList[e].elm)
}, KolorWheel.prototype.get = function (t) {
    return void 0 === t && (t = 0), this.resultList[t]
}, KolorWheel.prototype.isDark = function () {
    return !this.isLight()
}, KolorWheel.prototype.isLight = function () {
    var t = this.getRgb();
    return .299 * t[0] + .587 * t[1] + .114 * t[2] > 127
},
    function () {
        "use strict";
        var t = {
            not_string: /[^s]/,
            not_bool: /[^t]/,
            not_type: /[^T]/,
            not_primitive: /[^v]/,
            number: /[diefg]/,
            numeric_arg: /[bcdiefguxX]/,
            json: /[j]/,
            not_json: /[^j]/,
            text: /^[^\x25]+/,
            modulo: /^\x25{2}/,
            placeholder: /^\x25(?:([1-9]\d*)\$|\(([^)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-gijostTuvxX])/,
            key: /^([a-z_][a-z_\d]*)/i,
            key_access: /^\.([a-z_][a-z_\d]*)/i,
            index_access: /^\[(\d+)\]/,
            sign: /^[+-]/
        };

        function e(n) {
            return function (n, i) {
                var s, o, r, a, c, l, u, p, h, d = 1,
                    f = n.length,
                    m = "";
                for (o = 0; o < f; o++)
                    if ("string" == typeof n[o]) m += n[o];
                    else if ("object" == typeof n[o]) {
                        if ((a = n[o]).keys)
                            for (s = i[d], r = 0; r < a.keys.length; r++) {
                                if (null == s) throw new Error(e('[sprintf] Cannot access property "%s" of undefined value "%s"', a.keys[r], a.keys[r - 1]));
                                s = s[a.keys[r]]
                            } else s = a.param_no ? i[a.param_no] : i[d++];
                        if (t.not_type.test(a.type) && t.not_primitive.test(a.type) && s instanceof Function && (s = s()), t.numeric_arg.test(a.type) && "number" != typeof s && isNaN(s)) throw new TypeError(e("[sprintf] expecting number but found %T", s));
                        switch (t.number.test(a.type) && (p = 0 <= s), a.type) {
                            case "b":
                                s = parseInt(s, 10).toString(2);
                                break;
                            case "c":
                                s = String.fromCharCode(parseInt(s, 10));
                                break;
                            case "d":
                            case "i":
                                s = parseInt(s, 10);
                                break;
                            case "j":
                                s = JSON.stringify(s, null, a.width ? parseInt(a.width) : 0);
                                break;
                            case "e":
                                s = a.precision ? parseFloat(s).toExponential(a.precision) : parseFloat(s).toExponential();
                                break;
                            case "f":
                                s = a.precision ? parseFloat(s).toFixed(a.precision) : parseFloat(s);
                                break;
                            case "g":
                                s = a.precision ? String(Number(s.toPrecision(a.precision))) : parseFloat(s);
                                break;
                            case "o":
                                s = (parseInt(s, 10) >>> 0).toString(8);
                                break;
                            case "s":
                                s = String(s), s = a.precision ? s.substring(0, a.precision) : s;
                                break;
                            case "t":
                                s = String(!!s), s = a.precision ? s.substring(0, a.precision) : s;
                                break;
                            case "T":
                                s = Object.prototype.toString.call(s).slice(8, -1).toLowerCase(), s = a.precision ? s.substring(0, a.precision) : s;
                                break;
                            case "u":
                                s = parseInt(s, 10) >>> 0;
                                break;
                            case "v":
                                s = s.valueOf(), s = a.precision ? s.substring(0, a.precision) : s;
                                break;
                            case "x":
                                s = (parseInt(s, 10) >>> 0).toString(16);
                                break;
                            case "X":
                                s = (parseInt(s, 10) >>> 0).toString(16).toUpperCase()
                        }
                        t.json.test(a.type) ? m += s : (!t.number.test(a.type) || p && !a.sign ? h = "" : (h = p ? "+" : "-", s = s.toString().replace(t.sign, "")), l = a.pad_char ? "0" === a.pad_char ? "0" : a.pad_char.charAt(1) : " ", u = a.width - (h + s).length, c = a.width && 0 < u ? l.repeat(u) : "", m += a.align ? h + s + c : "0" === l ? h + c + s : c + h + s)
                    }
                return m
            }(function (e) {
                if (i[e]) return i[e];
                for (var n, s = e, o = [], r = 0; s;) {
                    if (null !== (n = t.text.exec(s))) o.push(n[0]);
                    else if (null !== (n = t.modulo.exec(s))) o.push("%");
                    else {
                        if (null === (n = t.placeholder.exec(s))) throw new SyntaxError("[sprintf] unexpected placeholder");
                        if (n[2]) {
                            r |= 1;
                            var a = [],
                                c = n[2],
                                l = [];
                            if (null === (l = t.key.exec(c))) throw new SyntaxError("[sprintf] failed to parse named argument key");
                            for (a.push(l[1]);
                                 "" !== (c = c.substring(l[0].length));)
                                if (null !== (l = t.key_access.exec(c))) a.push(l[1]);
                                else {
                                    if (null === (l = t.index_access.exec(c))) throw new SyntaxError("[sprintf] failed to parse named argument key");
                                    a.push(l[1])
                                }
                            n[2] = a
                        } else r |= 2;
                        if (3 === r) throw new Error("[sprintf] mixing positional and named placeholders is not (yet) supported");
                        o.push({
                            placeholder: n[0],
                            param_no: n[1],
                            keys: n[2],
                            sign: n[3],
                            pad_char: n[4],
                            align: n[5],
                            width: n[6],
                            precision: n[7],
                            type: n[8]
                        })
                    }
                    s = s.substring(n[0].length)
                }
                return i[e] = o
            }(n), arguments)
        }

        function n(t, n) {
            return e.apply(null, [t].concat(n || []))
        }

        var i = Object.create(null);
        "undefined" != typeof exports && (exports.sprintf = e, exports.vsprintf = n), "undefined" != typeof window && (window.sprintf = e, window.vsprintf = n, "function" == typeof define && define.amd && define(function () {
            return {
                sprintf: e,
                vsprintf: n
            }
        }))
    }();
var yall = function () {
    "use strict";
    return function (t) {
        var e = (t = t || {}).lazyClass || "lazy",
            n = t.lazyBackgroundClass || "lazy-bg",
            i = "idleLoadTimeout" in t ? t.idleLoadTimeout : 200,
            s = t.observeChanges || !1,
            o = t.events || {},
            r = t.noPolyfill || !1,
            a = window,
            c = "requestIdleCallback",
            l = "IntersectionObserver",
            u = l in a && l + "Entry" in a,
            p = /baidu|(?:google|bing|yandex|duckduck)bot/i.test(navigator.userAgent),
            h = ["srcset", "src", "poster"],
            d = [],
            f = function (t, i) {
                return d.slice.call((i || document).querySelectorAll(t || "img." + e + ",video." + e + ",iframe." + e + ",." + n))
            },
            m = function (e) {
                var i = e.parentNode;
                "PICTURE" == i.nodeName && v(f("source", i), b), "VIDEO" == e.nodeName && v(f("source", e), b), b(e);
                var s = e.classList;
                s.contains(n) && (s.remove(n), s.add(t.lazyBackgroundLoaded || "lazy-bg-loaded"))
            },
            g = function (t) {
                for (var e in o) t.addEventListener(e, o[e].listener || o[e], o[e].options || void 0)
            },
            b = function (t) {
                for (var n in h)
                    if (h[n] in t.dataset) {
                        t.setAttribute(h[n], t.dataset[h[n]]);
                        var i = t.parentNode;
                        "SOURCE" === t.nodeName && i.autoplay && (i.load(), /Trident/.test(navigator.userAgent) && i.play(), i.classList.remove(e)), t.classList.remove(e)
                    }
            },
            v = function (t, e) {
                for (var n = 0; n < t.length; n++) a[l] && e instanceof a[l] ? e.observe(t[n]) : e(t[n])
            },
            y = f();
        if (v(y, g), u && !p) {
            var S = new a[l](function (t) {
                v(t, function (t) {
                    if (t.isIntersecting || t.intersectionRatio) {
                        var e = t.target;
                        c in a && i ? a[c](function () {
                            m(e)
                        }, {
                            timeout: i
                        }) : m(e), S.unobserve(e), (y = y.filter(function (t) {
                            return t != e
                        })).length || s || S.disconnect()
                    }
                })
            }, {
                rootMargin: ("threshold" in t ? t.threshold : 200) + "px 0%"
            });
            v(y, S), s && v(f(t.observeRootSelector || "body"), function (e) {
                new MutationObserver(function () {
                    v(f(), function (t) {
                        y.indexOf(t) < 0 && (y.push(t), g(t), u && !p ? S.observe(t) : (r || p) && v(y, m))
                    })
                }).observe(e, t.mutationObserverOptions || {
                    childList: !0,
                    subtree: !0
                })
            })
        } else (r || p) && v(y, m)
    }
}();
!function (t, e) {
    "use strict";
    var n = null;

    function i() {
        n.setAttribute("data-orientation", t.innerHeight > t.innerWidth ? "portrait" : "landscape")
    }

    "function" != typeof t.CustomEvent && (t.CustomEvent = function (t, n) {
        n = n || {
            bubbles: !1,
            cancelable: !1,
            detail: void 0
        };
        var i = e.createEvent("CustomEvent");
        return i.initCustomEvent(t, n.bubbles, n.cancelable, n.detail), i
    }, t.CustomEvent.prototype = t.Event.prototype), t.addEventListener("load", function () {
        (n = e.documentElement).style.setProperty("--notch-top", "env(safe-area-inset-top)"), n.style.setProperty("--notch-right", "env(safe-area-inset-right)"), n.style.setProperty("--notch-bottom", "env(safe-area-inset-bottom)"), n.style.setProperty("--notch-left", "env(safe-area-inset-left)");
        var s = t.getComputedStyle(n);
        [parseInt(s.getPropertyValue("--notch-top") || "-1", 10), parseInt(s.getPropertyValue("--notch-right") || "-1", 10), parseInt(s.getPropertyValue("--notch-bottom") || "-1", 10), parseInt(s.getPropertyValue("--notch-left") || "-1", 10)].some(function (t) {
            return t > 0
        }) && (n.setAttribute("data-notch", "true"), t.dispatchEvent(new CustomEvent("notch-detected", {
            bubbles: !0,
            cancelable: !0
        })), t.addEventListener("resize", i), i())
    })
}(this, document),
    function (t, e, n, i) {
        "use strict";

        function s(t, e, n) {
            return setTimeout(l(t, n), e)
        }

        function o(t, e, n) {
            return !!Array.isArray(t) && (r(t, n[e], n), !0)
        }

        function r(t, e, n) {
            var s;
            if (t)
                if (t.forEach) t.forEach(e, n);
                else if (t.length !== i)
                    for (s = 0; s < t.length;) e.call(n, t[s], s, t), s++;
                else
                    for (s in t) t.hasOwnProperty(s) && e.call(n, t[s], s, t)
        }

        function a(e, n, i) {
            var s = "DEPRECATED METHOD: " + n + "\n" + i + " AT \n";
            return function () {
                var n = new Error("get-stack-trace"),
                    i = n && n.stack ? n.stack.replace(/^[^\(]+?[\n$]/gm, "").replace(/^\s+at\s+/gm, "").replace(/^Object.<anonymous>\s*\(/gm, "{anonymous}()@") : "Unknown Stack Trace",
                    o = t.console && (t.console.warn || t.console.log);
                return o && o.call(t.console, s, i), e.apply(this, arguments)
            }
        }

        function c(t, e, n) {
            var i, s = e.prototype;
            (i = t.prototype = Object.create(s)).constructor = t, i._super = s, n && Z(i, n)
        }

        function l(t, e) {
            return function () {
                return t.apply(e, arguments)
            }
        }

        function u(t, e) {
            return typeof t == nt ? t.apply(e && e[0] || i, e) : t
        }

        function p(t, e) {
            return t === i ? e : t
        }

        function h(t, e, n) {
            r(g(e), function (e) {
                t.addEventListener(e, n, !1)
            })
        }

        function d(t, e, n) {
            r(g(e), function (e) {
                t.removeEventListener(e, n, !1)
            })
        }

        function f(t, e) {
            for (; t;) {
                if (t == e) return !0;
                t = t.parentNode
            }
            return !1
        }

        function m(t, e) {
            return t.indexOf(e) > -1
        }

        function g(t) {
            return t.trim().split(/\s+/g)
        }

        function b(t, e, n) {
            if (t.indexOf && !n) return t.indexOf(e);
            for (var i = 0; i < t.length;) {
                if (n && t[i][n] == e || !n && t[i] === e) return i;
                i++
            }
            return -1
        }

        function v(t) {
            return Array.prototype.slice.call(t, 0)
        }

        function y(t, e, n) {
            for (var i = [], s = [], o = 0; o < t.length;) {
                var r = e ? t[o][e] : t[o];
                b(s, r) < 0 && i.push(t[o]), s[o] = r, o++
            }
            return n && (i = e ? i.sort(function (t, n) {
                return t[e] > n[e]
            }) : i.sort()), i
        }

        function S(t, e) {
            for (var n, s, o = e[0].toUpperCase() + e.slice(1), r = 0; r < tt.length;) {
                if ((s = (n = tt[r]) ? n + o : e) in t) return s;
                r++
            }
            return i
        }

        function C(e) {
            var n = e.ownerDocument || e;
            return n.defaultView || n.parentWindow || t
        }

        function x(t, e) {
            var n = this;
            this.manager = t, this.callback = e, this.element = t.element, this.target = t.options.inputTarget, this.domHandler = function (e) {
                u(t.options.enable, [t]) && n.handler(e)
            }, this.init()
        }

        function A(t, e, n) {
            var i = n.pointers.length,
                s = n.changedPointers.length,
                o = e & mt && i - s == 0,
                r = e & (bt | vt) && i - s == 0;
            n.isFirst = !!o, n.isFinal = !!r, o && (t.session = {}), n.eventType = e,
                function (t, e) {
                    var n = t.session,
                        i = e.pointers,
                        s = i.length;
                    n.firstInput || (n.firstInput = D(e)), s > 1 && !n.firstMultiple ? n.firstMultiple = D(e) : 1 === s && (n.firstMultiple = !1);
                    var o = n.firstInput,
                        r = n.firstMultiple,
                        a = r ? r.center : o.center,
                        c = e.center = w(i);
                    e.timeStamp = ot(), e.deltaTime = e.timeStamp - o.timeStamp, e.angle = I(a, c), e.distance = F(a, c),
                        function (t, e) {
                            var n = e.center,
                                i = t.offsetDelta || {},
                                s = t.prevDelta || {},
                                o = t.prevInput || {};
                            e.eventType !== mt && o.eventType !== bt || (s = t.prevDelta = {
                                x: o.deltaX || 0,
                                y: o.deltaY || 0
                            }, i = t.offsetDelta = {
                                x: n.x,
                                y: n.y
                            }), e.deltaX = s.x + (n.x - i.x), e.deltaY = s.y + (n.y - i.y)
                        }(n, e), e.offsetDirection = E(e.deltaX, e.deltaY);
                    var l = k(e.deltaTime, e.deltaX, e.deltaY);
                    e.overallVelocityX = l.x, e.overallVelocityY = l.y, e.overallVelocity = st(l.x) > st(l.y) ? l.x : l.y, e.scale = r ? function (t, e) {
                        return F(e[0], e[1], Et) / F(t[0], t[1], Et)
                    }(r.pointers, i) : 1, e.rotation = r ? function (t, e) {
                        return I(e[1], e[0], Et) + I(t[1], t[0], Et)
                    }(r.pointers, i) : 0, e.maxPointers = n.prevInput ? e.pointers.length > n.prevInput.maxPointers ? e.pointers.length : n.prevInput.maxPointers : e.pointers.length, T(n, e);
                    var u = t.element;
                    f(e.srcEvent.target, u) && (u = e.srcEvent.target), e.target = u
                }(t, n), t.emit("hammer.input", n), t.recognize(n), t.session.prevInput = n
        }

        function T(t, e) {
            var n, s, o, r, a = t.lastInterval || e,
                c = e.timeStamp - a.timeStamp;
            if (e.eventType != vt && (c > ft || a.velocity === i)) {
                var l = e.deltaX - a.deltaX,
                    u = e.deltaY - a.deltaY,
                    p = k(c, l, u);
                s = p.x, o = p.y, n = st(p.x) > st(p.y) ? p.x : p.y, r = E(l, u), t.lastInterval = e
            } else n = a.velocity, s = a.velocityX, o = a.velocityY, r = a.direction;
            e.velocity = n, e.velocityX = s, e.velocityY = o, e.direction = r
        }

        function D(t) {
            for (var e = [], n = 0; n < t.pointers.length;) e[n] = {
                clientX: it(t.pointers[n].clientX),
                clientY: it(t.pointers[n].clientY)
            }, n++;
            return {
                timeStamp: ot(),
                pointers: e,
                center: w(e),
                deltaX: t.deltaX,
                deltaY: t.deltaY
            }
        }

        function w(t) {
            var e = t.length;
            if (1 === e) return {
                x: it(t[0].clientX),
                y: it(t[0].clientY)
            };
            for (var n = 0, i = 0, s = 0; e > s;) n += t[s].clientX, i += t[s].clientY, s++;
            return {
                x: it(n / e),
                y: it(i / e)
            }
        }

        function k(t, e, n) {
            return {
                x: e / t || 0,
                y: n / t || 0
            }
        }

        function E(t, e) {
            return t === e ? yt : st(t) >= st(e) ? 0 > t ? St : Ct : 0 > e ? xt : At
        }

        function F(t, e, n) {
            n || (n = kt);
            var i = e[n[0]] - t[n[0]],
                s = e[n[1]] - t[n[1]];
            return Math.sqrt(i * i + s * s)
        }

        function I(t, e, n) {
            n || (n = kt);
            var i = e[n[0]] - t[n[0]],
                s = e[n[1]] - t[n[1]];
            return 180 * Math.atan2(s, i) / Math.PI
        }

        function M() {
            this.evEl = It, this.evWin = Mt, this.pressed = !1, x.apply(this, arguments)
        }

        function P() {
            this.evEl = Gt, this.evWin = $t, x.apply(this, arguments), this.store = this.manager.session.pointerEvents = []
        }

        function _() {
            this.evTarget = zt, this.evWin = Ot, this.started = !1, x.apply(this, arguments)
        }

        function G() {
            this.evTarget = Nt, this.targetIds = {}, x.apply(this, arguments)
        }

        function $() {
            x.apply(this, arguments);
            var t = l(this.handler, this);
            this.touch = new G(this.manager, t), this.mouse = new M(this.manager, t), this.primaryTouch = null, this.lastTouches = []
        }

        function L(t) {
            var e = t.changedPointers[0];
            if (e.identifier === this.primaryTouch) {
                var n = {
                    x: e.clientX,
                    y: e.clientY
                };
                this.lastTouches.push(n);
                var i = this.lastTouches;
                setTimeout(function () {
                    var t = i.indexOf(n);
                    t > -1 && i.splice(t, 1)
                }, jt)
            }
        }

        function z(t, e) {
            this.manager = t, this.set(e)
        }

        function O(t) {
            this.options = Z({}, this.defaults, t || {}), this.id = ct++, this.manager = null, this.options.enable = p(this.options.enable, !0), this.state = Jt, this.simultaneous = {}, this.requireFail = []
        }

        function B(t) {
            return t & ie ? "cancel" : t & ee ? "end" : t & te ? "move" : t & Zt ? "start" : ""
        }

        function N(t) {
            return t == At ? "down" : t == xt ? "up" : t == St ? "left" : t == Ct ? "right" : ""
        }

        function j(t, e) {
            var n = e.manager;
            return n ? n.get(t) : t
        }

        function R() {
            O.apply(this, arguments)
        }

        function U() {
            R.apply(this, arguments), this.pX = null, this.pY = null
        }

        function W() {
            R.apply(this, arguments)
        }

        function H() {
            O.apply(this, arguments), this._timer = null, this._input = null
        }

        function q() {
            R.apply(this, arguments)
        }

        function Y() {
            R.apply(this, arguments)
        }

        function V() {
            O.apply(this, arguments), this.pTime = !1, this.pCenter = !1, this._timer = null, this._input = null, this.count = 0
        }

        function X(t, e) {
            return (e = e || {}).recognizers = p(e.recognizers, X.defaults.preset), new K(t, e)
        }

        function K(t, e) {
            this.options = Z({}, X.defaults, e || {}), this.options.inputTarget = this.options.inputTarget || t, this.handlers = {}, this.session = {}, this.recognizers = [], this.oldCssProps = {}, this.element = t, this.input = function (t) {
                var e = t.options.inputClass;
                return new (e || (ut ? P : pt ? G : lt ? $ : M))(t, A)
            }(this), this.touchAction = new z(this, this.options.touchAction), Q(this, !0), r(this.options.recognizers, function (t) {
                var e = this.add(new t[0](t[1]));
                t[2] && e.recognizeWith(t[2]), t[3] && e.requireFailure(t[3])
            }, this)
        }

        function Q(t, e) {
            var n, i = t.element;
            i.style && (r(t.options.cssProps, function (s, o) {
                n = S(i.style, o), e ? (t.oldCssProps[n] = i.style[n], i.style[n] = s) : i.style[n] = t.oldCssProps[n] || ""
            }), e || (t.oldCssProps = {}))
        }

        function J(t, n) {
            var i = e.createEvent("Event");
            i.initEvent(t, !0, !0), i.gesture = n, n.target.dispatchEvent(i)
        }

        var Z, tt = ["", "webkit", "Moz", "MS", "ms", "o"],
            et = e.createElement("div"),
            nt = "function",
            it = Math.round,
            st = Math.abs,
            ot = Date.now;
        Z = "function" != typeof Object.assign ? function (t) {
            if (t === i || null === t) throw new TypeError("Cannot convert undefined or null to object");
            for (var e = Object(t), n = 1; n < arguments.length; n++) {
                var s = arguments[n];
                if (s !== i && null !== s)
                    for (var o in s) s.hasOwnProperty(o) && (e[o] = s[o])
            }
            return e
        } : Object.assign;
        var rt = a(function (t, e, n) {
                for (var s = Object.keys(e), o = 0; o < s.length;) (!n || n && t[s[o]] === i) && (t[s[o]] = e[s[o]]), o++;
                return t
            }, "extend", "Use `assign`."),
            at = a(function (t, e) {
                return rt(t, e, !0)
            }, "merge", "Use `assign`."),
            ct = 1,
            lt = "ontouchstart" in t,
            ut = S(t, "PointerEvent") !== i,
            pt = lt && /mobile|tablet|ip(ad|hone|od)|android/i.test(navigator.userAgent),
            ht = "touch",
            dt = "mouse",
            ft = 25,
            mt = 1,
            gt = 2,
            bt = 4,
            vt = 8,
            yt = 1,
            St = 2,
            Ct = 4,
            xt = 8,
            At = 16,
            Tt = St | Ct,
            Dt = xt | At,
            wt = Tt | Dt,
            kt = ["x", "y"],
            Et = ["clientX", "clientY"];
        x.prototype = {
            handler: function () {
            },
            init: function () {
                this.evEl && h(this.element, this.evEl, this.domHandler), this.evTarget && h(this.target, this.evTarget, this.domHandler), this.evWin && h(C(this.element), this.evWin, this.domHandler)
            },
            destroy: function () {
                this.evEl && d(this.element, this.evEl, this.domHandler), this.evTarget && d(this.target, this.evTarget, this.domHandler), this.evWin && d(C(this.element), this.evWin, this.domHandler)
            }
        };
        var Ft = {
                mousedown: mt,
                mousemove: gt,
                mouseup: bt
            },
            It = "mousedown",
            Mt = "mousemove mouseup";
        c(M, x, {
            handler: function (t) {
                var e = Ft[t.type];
                e & mt && 0 === t.button && (this.pressed = !0), e & gt && 1 !== t.which && (e = bt), this.pressed && (e & bt && (this.pressed = !1), this.callback(this.manager, e, {
                    pointers: [t],
                    changedPointers: [t],
                    pointerType: dt,
                    srcEvent: t
                }))
            }
        });
        var Pt = {
                pointerdown: mt,
                pointermove: gt,
                pointerup: bt,
                pointercancel: vt,
                pointerout: vt
            },
            _t = {
                2: ht,
                3: "pen",
                4: dt,
                5: "kinect"
            },
            Gt = "pointerdown",
            $t = "pointermove pointerup pointercancel";
        t.MSPointerEvent && !t.PointerEvent && (Gt = "MSPointerDown", $t = "MSPointerMove MSPointerUp MSPointerCancel"), c(P, x, {
            handler: function (t) {
                var e = this.store,
                    n = !1,
                    i = t.type.toLowerCase().replace("ms", ""),
                    s = Pt[i],
                    o = _t[t.pointerType] || t.pointerType,
                    r = o == ht,
                    a = b(e, t.pointerId, "pointerId");
                s & mt && (0 === t.button || r) ? 0 > a && (e.push(t), a = e.length - 1) : s & (bt | vt) && (n = !0), 0 > a || (e[a] = t, this.callback(this.manager, s, {
                    pointers: e,
                    changedPointers: [t],
                    pointerType: o,
                    srcEvent: t
                }), n && e.splice(a, 1))
            }
        });
        var Lt = {
                touchstart: mt,
                touchmove: gt,
                touchend: bt,
                touchcancel: vt
            },
            zt = "touchstart",
            Ot = "touchstart touchmove touchend touchcancel";
        c(_, x, {
            handler: function (t) {
                var e = Lt[t.type];
                if (e === mt && (this.started = !0), this.started) {
                    var n = function (t, e) {
                        var n = v(t.touches),
                            i = v(t.changedTouches);
                        return e & (bt | vt) && (n = y(n.concat(i), "identifier", !0)), [n, i]
                    }.call(this, t, e);
                    e & (bt | vt) && n[0].length - n[1].length == 0 && (this.started = !1), this.callback(this.manager, e, {
                        pointers: n[0],
                        changedPointers: n[1],
                        pointerType: ht,
                        srcEvent: t
                    })
                }
            }
        });
        var Bt = {
                touchstart: mt,
                touchmove: gt,
                touchend: bt,
                touchcancel: vt
            },
            Nt = "touchstart touchmove touchend touchcancel";
        c(G, x, {
            handler: function (t) {
                var e = Bt[t.type],
                    n = function (t, e) {
                        var n = v(t.touches),
                            i = this.targetIds;
                        if (e & (mt | gt) && 1 === n.length) return i[n[0].identifier] = !0, [n, n];
                        var s, o, r = v(t.changedTouches),
                            a = [],
                            c = this.target;
                        if (o = n.filter(function (t) {
                            return f(t.target, c)
                        }), e === mt)
                            for (s = 0; s < o.length;) i[o[s].identifier] = !0, s++;
                        for (s = 0; s < r.length;) i[r[s].identifier] && a.push(r[s]), e & (bt | vt) && delete i[r[s].identifier], s++;
                        return a.length ? [y(o.concat(a), "identifier", !0), a] : void 0
                    }.call(this, t, e);
                n && this.callback(this.manager, e, {
                    pointers: n[0],
                    changedPointers: n[1],
                    pointerType: ht,
                    srcEvent: t
                })
            }
        });
        var jt = 2500,
            Rt = 25;
        c($, x, {
            handler: function (t, e, n) {
                var i = n.pointerType == ht,
                    s = n.pointerType == dt;
                if (!(s && n.sourceCapabilities && n.sourceCapabilities.firesTouchEvents)) {
                    if (i) (function (t, e) {
                        t & mt ? (this.primaryTouch = e.changedPointers[0].identifier, L.call(this, e)) : t & (bt | vt) && L.call(this, e)
                    }).call(this, e, n);
                    else if (s && function (t) {
                        for (var e = t.srcEvent.clientX, n = t.srcEvent.clientY, i = 0; i < this.lastTouches.length; i++) {
                            var s = this.lastTouches[i],
                                o = Math.abs(e - s.x),
                                r = Math.abs(n - s.y);
                            if (Rt >= o && Rt >= r) return !0
                        }
                        return !1
                    }.call(this, n)) return;
                    this.callback(t, e, n)
                }
            },
            destroy: function () {
                this.touch.destroy(), this.mouse.destroy()
            }
        });
        var Ut = S(et.style, "touchAction"),
            Wt = Ut !== i,
            Ht = "compute",
            qt = "auto",
            Yt = "manipulation",
            Vt = "none",
            Xt = "pan-x",
            Kt = "pan-y",
            Qt = function () {
                if (!Wt) return !1;
                var e = {},
                    n = t.CSS && t.CSS.supports;
                return ["auto", "manipulation", "pan-y", "pan-x", "pan-x pan-y", "none"].forEach(function (i) {
                    e[i] = !n || t.CSS.supports("touch-action", i)
                }), e
            }();
        z.prototype = {
            set: function (t) {
                t == Ht && (t = this.compute()), Wt && this.manager.element.style && Qt[t] && (this.manager.element.style[Ut] = t), this.actions = t.toLowerCase().trim()
            },
            update: function () {
                this.set(this.manager.options.touchAction)
            },
            compute: function () {
                var t = [];
                return r(this.manager.recognizers, function (e) {
                    u(e.options.enable, [e]) && (t = t.concat(e.getTouchAction()))
                }),
                    function (t) {
                        if (m(t, Vt)) return Vt;
                        var e = m(t, Xt),
                            n = m(t, Kt);
                        return e && n ? Vt : e || n ? e ? Xt : Kt : m(t, Yt) ? Yt : qt
                    }(t.join(" "))
            },
            preventDefaults: function (t) {
                var e = t.srcEvent,
                    n = t.offsetDirection;
                if (!this.manager.session.prevented) {
                    var i = this.actions,
                        s = m(i, Vt) && !Qt[Vt],
                        o = m(i, Kt) && !Qt[Kt],
                        r = m(i, Xt) && !Qt[Xt];
                    if (s) {
                        var a = 1 === t.pointers.length,
                            c = t.distance < 2,
                            l = t.deltaTime < 250;
                        if (a && c && l) return
                    }
                    return r && o ? void 0 : s || o && n & Tt || r && n & Dt ? this.preventSrc(e) : void 0
                }
                e.preventDefault()
            },
            preventSrc: function (t) {
                this.manager.session.prevented = !0, t.preventDefault()
            }
        };
        var Jt = 1,
            Zt = 2,
            te = 4,
            ee = 8,
            ne = ee,
            ie = 16;
        O.prototype = {
            defaults: {},
            set: function (t) {
                return Z(this.options, t), this.manager && this.manager.touchAction.update(), this
            },
            recognizeWith: function (t) {
                if (o(t, "recognizeWith", this)) return this;
                var e = this.simultaneous;
                return e[(t = j(t, this)).id] || (e[t.id] = t, t.recognizeWith(this)), this
            },
            dropRecognizeWith: function (t) {
                return o(t, "dropRecognizeWith", this) ? this : (t = j(t, this), delete this.simultaneous[t.id], this)
            },
            requireFailure: function (t) {
                if (o(t, "requireFailure", this)) return this;
                var e = this.requireFail;
                return -1 === b(e, t = j(t, this)) && (e.push(t), t.requireFailure(this)), this
            },
            dropRequireFailure: function (t) {
                if (o(t, "dropRequireFailure", this)) return this;
                t = j(t, this);
                var e = b(this.requireFail, t);
                return e > -1 && this.requireFail.splice(e, 1), this
            },
            hasRequireFailures: function () {
                return this.requireFail.length > 0
            },
            canRecognizeWith: function (t) {
                return !!this.simultaneous[t.id]
            },
            emit: function (t) {
                function e(e) {
                    n.manager.emit(e, t)
                }

                var n = this,
                    i = this.state;
                ee > i && e(n.options.event + B(i)), e(n.options.event), t.additionalEvent && e(t.additionalEvent), i >= ee && e(n.options.event + B(i))
            },
            tryEmit: function (t) {
                return this.canEmit() ? this.emit(t) : void (this.state = 32)
            },
            canEmit: function () {
                for (var t = 0; t < this.requireFail.length;) {
                    if (!(this.requireFail[t].state & (32 | Jt))) return !1;
                    t++
                }
                return !0
            },
            recognize: function (t) {
                var e = Z({}, t);
                return u(this.options.enable, [this, e]) ? (this.state & (ne | ie | 32) && (this.state = Jt), this.state = this.process(e), void (this.state & (Zt | te | ee | ie) && this.tryEmit(e))) : (this.reset(), void (this.state = 32))
            },
            process: function (t) {
            },
            getTouchAction: function () {
            },
            reset: function () {
            }
        }, c(R, O, {
            defaults: {
                pointers: 1
            },
            attrTest: function (t) {
                var e = this.options.pointers;
                return 0 === e || t.pointers.length === e
            },
            process: function (t) {
                var e = this.state,
                    n = t.eventType,
                    i = e & (Zt | te),
                    s = this.attrTest(t);
                return i && (n & vt || !s) ? e | ie : i || s ? n & bt ? e | ee : e & Zt ? e | te : Zt : 32
            }
        }), c(U, R, {
            defaults: {
                event: "pan",
                threshold: 10,
                pointers: 1,
                direction: wt
            },
            getTouchAction: function () {
                var t = this.options.direction,
                    e = [];
                return t & Tt && e.push(Kt), t & Dt && e.push(Xt), e
            },
            directionTest: function (t) {
                var e = this.options,
                    n = !0,
                    i = t.distance,
                    s = t.direction,
                    o = t.deltaX,
                    r = t.deltaY;
                return s & e.direction || (e.direction & Tt ? (s = 0 === o ? yt : 0 > o ? St : Ct, n = o != this.pX, i = Math.abs(t.deltaX)) : (s = 0 === r ? yt : 0 > r ? xt : At, n = r != this.pY, i = Math.abs(t.deltaY))), t.direction = s, n && i > e.threshold && s & e.direction
            },
            attrTest: function (t) {
                return R.prototype.attrTest.call(this, t) && (this.state & Zt || !(this.state & Zt) && this.directionTest(t))
            },
            emit: function (t) {
                this.pX = t.deltaX, this.pY = t.deltaY;
                var e = N(t.direction);
                e && (t.additionalEvent = this.options.event + e), this._super.emit.call(this, t)
            }
        }), c(W, R, {
            defaults: {
                event: "pinch",
                threshold: 0,
                pointers: 2
            },
            getTouchAction: function () {
                return [Vt]
            },
            attrTest: function (t) {
                return this._super.attrTest.call(this, t) && (Math.abs(t.scale - 1) > this.options.threshold || this.state & Zt)
            },
            emit: function (t) {
                if (1 !== t.scale) {
                    var e = t.scale < 1 ? "in" : "out";
                    t.additionalEvent = this.options.event + e
                }
                this._super.emit.call(this, t)
            }
        }), c(H, O, {
            defaults: {
                event: "press",
                pointers: 1,
                time: 251,
                threshold: 9
            },
            getTouchAction: function () {
                return [qt]
            },
            process: function (t) {
                var e = this.options,
                    n = t.pointers.length === e.pointers,
                    i = t.distance < e.threshold,
                    o = t.deltaTime > e.time;
                if (this._input = t, !i || !n || t.eventType & (bt | vt) && !o) this.reset();
                else if (t.eventType & mt) this.reset(), this._timer = s(function () {
                    this.state = ne, this.tryEmit()
                }, e.time, this);
                else if (t.eventType & bt) return ne;
                return 32
            },
            reset: function () {
                clearTimeout(this._timer)
            },
            emit: function (t) {
                this.state === ne && (t && t.eventType & bt ? this.manager.emit(this.options.event + "up", t) : (this._input.timeStamp = ot(), this.manager.emit(this.options.event, this._input)))
            }
        }), c(q, R, {
            defaults: {
                event: "rotate",
                threshold: 0,
                pointers: 2
            },
            getTouchAction: function () {
                return [Vt]
            },
            attrTest: function (t) {
                return this._super.attrTest.call(this, t) && (Math.abs(t.rotation) > this.options.threshold || this.state & Zt)
            }
        }), c(Y, R, {
            defaults: {
                event: "swipe",
                threshold: 10,
                velocity: .3,
                direction: Tt | Dt,
                pointers: 1
            },
            getTouchAction: function () {
                return U.prototype.getTouchAction.call(this)
            },
            attrTest: function (t) {
                var e, n = this.options.direction;
                return n & (Tt | Dt) ? e = t.overallVelocity : n & Tt ? e = t.overallVelocityX : n & Dt && (e = t.overallVelocityY), this._super.attrTest.call(this, t) && n & t.offsetDirection && t.distance > this.options.threshold && t.maxPointers == this.options.pointers && st(e) > this.options.velocity && t.eventType & bt
            },
            emit: function (t) {
                var e = N(t.offsetDirection);
                e && this.manager.emit(this.options.event + e, t), this.manager.emit(this.options.event, t)
            }
        }), c(V, O, {
            defaults: {
                event: "tap",
                pointers: 1,
                taps: 1,
                interval: 300,
                time: 250,
                threshold: 9,
                posThreshold: 10
            },
            getTouchAction: function () {
                return [Yt]
            },
            process: function (t) {
                var e = this.options,
                    n = t.pointers.length === e.pointers,
                    i = t.distance < e.threshold,
                    o = t.deltaTime < e.time;
                if (this.reset(), t.eventType & mt && 0 === this.count) return this.failTimeout();
                if (i && o && n) {
                    if (t.eventType != bt) return this.failTimeout();
                    var r = !this.pTime || t.timeStamp - this.pTime < e.interval,
                        a = !this.pCenter || F(this.pCenter, t.center) < e.posThreshold;
                    if (this.pTime = t.timeStamp, this.pCenter = t.center, a && r ? this.count += 1 : this.count = 1, this._input = t, 0 === this.count % e.taps) return this.hasRequireFailures() ? (this._timer = s(function () {
                        this.state = ne, this.tryEmit()
                    }, e.interval, this), Zt) : ne
                }
                return 32
            },
            failTimeout: function () {
                return this._timer = s(function () {
                    this.state = 32
                }, this.options.interval, this), 32
            },
            reset: function () {
                clearTimeout(this._timer)
            },
            emit: function () {
                this.state == ne && (this._input.tapCount = this.count, this.manager.emit(this.options.event, this._input))
            }
        }), X.VERSION = "2.0.8", X.defaults = {
            domEvents: !1,
            touchAction: Ht,
            enable: !0,
            inputTarget: null,
            inputClass: null,
            preset: [
                [q, {
                    enable: !1
                }],
                [W, {
                    enable: !1
                },
                    ["rotate"]
                ],
                [Y, {
                    direction: Tt
                }],
                [U, {
                    direction: Tt
                },
                    ["swipe"]
                ],
                [V],
                [V, {
                    event: "doubletap",
                    taps: 2
                },
                    ["tap"]
                ],
                [H]
            ],
            cssProps: {
                userSelect: "none",
                touchSelect: "none",
                touchCallout: "none",
                contentZooming: "none",
                userDrag: "none",
                tapHighlightColor: "rgba(0,0,0,0)"
            }
        };
        K.prototype = {
            set: function (t) {
                return Z(this.options, t), t.touchAction && this.touchAction.update(), t.inputTarget && (this.input.destroy(), this.input.target = t.inputTarget, this.input.init()), this
            },
            stop: function (t) {
                this.session.stopped = t ? 2 : 1
            },
            recognize: function (t) {
                var e = this.session;
                if (!e.stopped) {
                    this.touchAction.preventDefaults(t);
                    var n, i = this.recognizers,
                        s = e.curRecognizer;
                    (!s || s && s.state & ne) && (s = e.curRecognizer = null);
                    for (var o = 0; o < i.length;) n = i[o], 2 === e.stopped || s && n != s && !n.canRecognizeWith(s) ? n.reset() : n.recognize(t), !s && n.state & (Zt | te | ee) && (s = e.curRecognizer = n), o++
                }
            },
            get: function (t) {
                if (t instanceof O) return t;
                for (var e = this.recognizers, n = 0; n < e.length; n++)
                    if (e[n].options.event == t) return e[n];
                return null
            },
            add: function (t) {
                if (o(t, "add", this)) return this;
                var e = this.get(t.options.event);
                return e && this.remove(e), this.recognizers.push(t), t.manager = this, this.touchAction.update(), t
            },
            remove: function (t) {
                if (o(t, "remove", this)) return this;
                if (t = this.get(t)) {
                    var e = this.recognizers,
                        n = b(e, t);
                    -1 !== n && (e.splice(n, 1), this.touchAction.update())
                }
                return this
            },
            on: function (t, e) {
                if (t !== i && e !== i) {
                    var n = this.handlers;
                    return r(g(t), function (t) {
                        n[t] = n[t] || [], n[t].push(e)
                    }), this
                }
            },
            off: function (t, e) {
                if (t !== i) {
                    var n = this.handlers;
                    return r(g(t), function (t) {
                        e ? n[t] && n[t].splice(b(n[t], e), 1) : delete n[t]
                    }), this
                }
            },
            emit: function (t, e) {
                this.options.domEvents && J(t, e);
                var n = this.handlers[t] && this.handlers[t].slice();
                if (n && n.length) {
                    e.type = t, e.preventDefault = function () {
                        e.srcEvent.preventDefault()
                    };
                    for (var i = 0; i < n.length;) n[i](e), i++
                }
            },
            destroy: function () {
                this.element && Q(this, !1), this.handlers = {}, this.session = {}, this.input.destroy(), this.element = null
            }
        }, Z(X, {
            INPUT_START: mt,
            INPUT_MOVE: gt,
            INPUT_END: bt,
            INPUT_CANCEL: vt,
            STATE_POSSIBLE: Jt,
            STATE_BEGAN: Zt,
            STATE_CHANGED: te,
            STATE_ENDED: ee,
            STATE_RECOGNIZED: ne,
            STATE_CANCELLED: ie,
            STATE_FAILED: 32,
            DIRECTION_NONE: yt,
            DIRECTION_LEFT: St,
            DIRECTION_RIGHT: Ct,
            DIRECTION_UP: xt,
            DIRECTION_DOWN: At,
            DIRECTION_HORIZONTAL: Tt,
            DIRECTION_VERTICAL: Dt,
            DIRECTION_ALL: wt,
            Manager: K,
            Input: x,
            TouchAction: z,
            TouchInput: G,
            MouseInput: M,
            PointerEventInput: P,
            TouchMouseInput: $,
            SingleTouchInput: _,
            Recognizer: O,
            AttrRecognizer: R,
            Tap: V,
            Pan: U,
            Swipe: Y,
            Pinch: W,
            Rotate: q,
            Press: H,
            on: h,
            off: d,
            each: r,
            merge: at,
            extend: rt,
            assign: Z,
            inherit: c,
            bindFn: l,
            prefixed: S
        }), (void 0 !== t ? t : "undefined" != typeof self ? self : {}).Hammer = X, "function" == typeof define && define.amd ? define(function () {
            return X
        }) : "undefined" != typeof module && module.exports ? module.exports = X : t.Hammer = X
    }(window, document),
    function (t, e) {
        "object" == typeof exports && "undefined" != typeof module ? module.exports = e(t) : "function" == typeof define && define.amd ? define(e) : e(t)
    }("undefined" != typeof self ? self : "undefined" != typeof window ? window : "undefined" != typeof global ? global : this, function (global) {
        "use strict";
        global = global || {};
        var _Base64 = global.Base64,
            version = "2.5.2",
            buffer;
        if ("undefined" != typeof module && module.exports) try {
            buffer = eval("require('buffer').Buffer")
        } catch (t) {
            buffer = void 0
        }
        var b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
            b64tab = function (t) {
                for (var e = {}, n = 0, i = t.length; n < i; n++) e[t.charAt(n)] = n;
                return e
            }(b64chars),
            fromCharCode = String.fromCharCode,
            cb_utob = function (t) {
                if (t.length < 2) return (e = t.charCodeAt(0)) < 128 ? t : e < 2048 ? fromCharCode(192 | e >>> 6) + fromCharCode(128 | 63 & e) : fromCharCode(224 | e >>> 12 & 15) + fromCharCode(128 | e >>> 6 & 63) + fromCharCode(128 | 63 & e);
                var e = 65536 + 1024 * (t.charCodeAt(0) - 55296) + (t.charCodeAt(1) - 56320);
                return fromCharCode(240 | e >>> 18 & 7) + fromCharCode(128 | e >>> 12 & 63) + fromCharCode(128 | e >>> 6 & 63) + fromCharCode(128 | 63 & e)
            },
            re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g,
            utob = function (t) {
                return t.replace(re_utob, cb_utob)
            },
            cb_encode = function (t) {
                var e = [0, 2, 1][t.length % 3],
                    n = t.charCodeAt(0) << 16 | (t.length > 1 ? t.charCodeAt(1) : 0) << 8 | (t.length > 2 ? t.charCodeAt(2) : 0);
                return [b64chars.charAt(n >>> 18), b64chars.charAt(n >>> 12 & 63), e >= 2 ? "=" : b64chars.charAt(n >>> 6 & 63), e >= 1 ? "=" : b64chars.charAt(63 & n)].join("")
            },
            btoa = global.btoa ? function (t) {
                return global.btoa(t)
            } : function (t) {
                return t.replace(/[\s\S]{1,3}/g, cb_encode)
            },
            _encode = function (t) {
                return "[object Uint8Array]" === Object.prototype.toString.call(t) ? t.toString("base64") : btoa(utob(String(t)))
            },
            encode = function (t, e) {
                return e ? _encode(String(t)).replace(/[+\/]/g, function (t) {
                    return "+" == t ? "-" : "_"
                }).replace(/=/g, "") : _encode(t)
            },
            encodeURI = function (t) {
                return encode(t, !0)
            },
            re_btou = /[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3}/g,
            cb_btou = function (t) {
                switch (t.length) {
                    case 4:
                        var e = ((7 & t.charCodeAt(0)) << 18 | (63 & t.charCodeAt(1)) << 12 | (63 & t.charCodeAt(2)) << 6 | 63 & t.charCodeAt(3)) - 65536;
                        return fromCharCode(55296 + (e >>> 10)) + fromCharCode(56320 + (1023 & e));
                    case 3:
                        return fromCharCode((15 & t.charCodeAt(0)) << 12 | (63 & t.charCodeAt(1)) << 6 | 63 & t.charCodeAt(2));
                    default:
                        return fromCharCode((31 & t.charCodeAt(0)) << 6 | 63 & t.charCodeAt(1))
                }
            },
            btou = function (t) {
                return t.replace(re_btou, cb_btou)
            },
            cb_decode = function (t) {
                var e = t.length,
                    n = e % 4,
                    i = (e > 0 ? b64tab[t.charAt(0)] << 18 : 0) | (e > 1 ? b64tab[t.charAt(1)] << 12 : 0) | (e > 2 ? b64tab[t.charAt(2)] << 6 : 0) | (e > 3 ? b64tab[t.charAt(3)] : 0),
                    s = [fromCharCode(i >>> 16), fromCharCode(i >>> 8 & 255), fromCharCode(255 & i)];
                return s.length -= [0, 0, 2, 1][n], s.join("")
            },
            _atob = global.atob ? function (t) {
                return global.atob(t)
            } : function (t) {
                return t.replace(/\S{1,4}/g, cb_decode)
            },
            atob = function (t) {
                return _atob(String(t).replace(/[^A-Za-z0-9\+\/]/g, ""))
            },
            _decode = buffer ? buffer.from && Uint8Array && buffer.from !== Uint8Array.from ? function (t) {
                return (t.constructor === buffer.constructor ? t : buffer.from(t, "base64")).toString()
            } : function (t) {
                return (t.constructor === buffer.constructor ? t : new buffer(t, "base64")).toString()
            } : function (t) {
                return btou(_atob(t))
            },
            decode = function (t) {
                return _decode(String(t).replace(/[-_]/g, function (t) {
                    return "-" == t ? "+" : "/"
                }).replace(/[^A-Za-z0-9\+\/]/g, ""))
            },
            noConflict = function () {
                var t = global.Base64;
                return global.Base64 = _Base64, t
            };
        if (global.Base64 = {
            VERSION: version,
            atob: atob,
            btoa: btoa,
            fromBase64: decode,
            toBase64: encode,
            utob: utob,
            encode: encode,
            encodeURI: encodeURI,
            btou: btou,
            decode: decode,
            noConflict: noConflict,
            __buffer__: buffer
        }, "function" == typeof Object.defineProperty) {
            var noEnum = function (t) {
                return {
                    value: t,
                    enumerable: !1,
                    writable: !0,
                    configurable: !0
                }
            };
            global.Base64.extendString = function () {
                Object.defineProperty(String.prototype, "fromBase64", noEnum(function () {
                    return decode(this)
                })), Object.defineProperty(String.prototype, "toBase64", noEnum(function (t) {
                    return encode(this, t)
                })), Object.defineProperty(String.prototype, "toBase64URI", noEnum(function () {
                    return encode(this, !0)
                }))
            }
        }
        return global.Meteor && (Base64 = global.Base64), "undefined" != typeof module && module.exports ? module.exports.Base64 = global.Base64 : "function" == typeof define && define.amd && define([], function () {
            return global.Base64
        }), {
            Base64: global.Base64
        }
    });