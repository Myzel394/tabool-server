let t = [],
    s = ScCore.serializeForm(this.div),
    e = (scGlobals.client.name,
            Base64.encode("deae89179ff419b4ab488b7a2211c96f" + Base64.encode(this.div.find("[name=fPassword]").val()) + "406d8f390f07c425c4bc3088a7488131")
    );
this.div.find("[name=fPassword]").val(e), t.length < 1 ?
    ScCore.performQuery(this.div.find("form").serialize(), function (t) {
        4 == t.header.state ? (
            this.closeDialog(), setTimeout(function () {
                ScCore.exSaveLogin(s.fInstitution, s.fUsername, s.fPassword, t.header.authString);
                ScCore.afterLogin(t.header.log, t.header.authString);
                scGlobals.layout.loginRunning = !1
            }, 500)) : this.div.find("[name=fPassword]").val("")
    }