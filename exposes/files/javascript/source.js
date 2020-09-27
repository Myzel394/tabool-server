class ScTimeTable extends ScModule {
    constructor(t) {
        super(t)
    }

    static getLocations(t) {
        let e = t.locations || [];
        return (e = e.sort(function (t, e) {
            return t.code > e.code
        })).reduce(function (t, e, s) {
            let a = "";
            return s > 0 && (a = ", "), ScCore.isset(e.code) ? t + a + e.code : t
        }, "")
    }

    static getParticipants(t, e = !1) {
        let s = t.participants || [],
            a = parseInt(t.participants_plid),
            i = t.participant_outages || [];
        return s.reduce(function (t, s, n) {
            let l = "";
            n > 0 && (l = ", ");
            let c = !1;
            for (let t in i) s.id == i[t].id && (c = !0);
            let o = "",
                r = "";
            return 21 == scGlobals.user.type && e && (o = "<span style='color:#2384d4;cursor:pointer' onclick='ScCore.select4Mail({plid:" + a + "})'>", r = " <i class='icon f7-icons' >envelope</i></span>", "rwg" == scGlobals.client.name && (r += " <span style='color:#2384d4;cursor:pointer' onclick='ScCore.message2Group(" + a + ",true)'><i class='icon f7-icons' >chat_bubble</i></span>")), c ? t + l + "(" + o + s.code + r + ")" : t + l + o + s.code + r
        }, "")
    }

    showEvent(t) {
        let e = [];
        21 == scGlobals.user.type && (e = [
            [{
                title: scStr.ttbEventUploads,
                icon: "cloud_upload",
                action: function (e) {
                    ScCore.moduleFunc({
                        module: "ScTimeTable",
                        func: "showEventUploads",
                        params: {
                            event_id: t.event.extendedProps.data.event_id
                        }
                    })
                }
            }]
        ]), ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbEventDetails,
                config: {
                    panelSize: {
                        width: ScCore.maxFractionWidth(1 / 3),
                        height: ScCore.autoPanelHeight()
                    },
                    menu: e
                },
                contents: [{
                    module: "ScTimeTable",
                    func: "showEvent",
                    params: t
                }]
            }]
        })
    }

    showEventUploads(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbEventUploads,
                config: {
                    maximize: !0
                },
                contents: [{
                    module: "ScTimeTable",
                    func: "showEventUploads",
                    params: t
                }]
            }]
        })
    }

    showTodoList(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbTodoList,
                config: {},
                contents: [{
                    module: "ScTimeTable",
                    func: "showTodoList",
                    params: t
                }]
            }]
        })
    }

    showMyEvents(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbMyEvents,
                config: {},
                contents: [{
                    module: "ScTimeTable",
                    func: "showMyEvents",
                    params: t
                }]
            }]
        })
    }

    showCalendar(t) {
        let e = [];
        t = $.extend({
            itemType: 1,
            itemId: scGlobals.user.id
        }, t), 21 == scGlobals.user.type && (e = [
            [{
                title: scStr.ttbActivateCalendars,
                icon: "videocam",
                action: function (t) {
                    t.getContentByNumber(1).activateCalendars()
                }
            }, {
                title: scStr.ttbUnauthorizedStudentOutages,
                icon: "person_badge_minus",
                action: function (t) {
                    ScCore.moduleFunc({
                        module: "ScTimeTable",
                        func: "showUnauthorizedStudentOutages"
                    })
                }
            }, {
                title: scStr.corPrint,
                icon: "printer",
                action: function (t) {
                    t.getContentByNumber(1).printCalendar({})
                }
            }]
        ]), 27 == scGlobals.user.type && (e = [
            [{
                title: scStr.ttbActivateCalendars,
                icon: "videocam",
                action: function (t) {
                    t.getContentByNumber(1).activateCalendars()
                }
            }, {
                title: scStr.corPrint,
                icon: "printer",
                action: function (t) {
                    t.getContentByNumber(1).printCalendar({})
                }
            }]
        ]), 20 == scGlobals.user.type && (e = [
            [{
                title: scStr.ttbTodoList,
                icon: "square_list",
                action: function (t) {
                    ScCore.moduleFunc({
                        module: "ScTimeTable",
                        func: "showTodoList"
                    })
                }
            }, {
                title: scStr.ttbMyEvents,
                icon: "burst",
                action: function (t) {
                    ScCore.moduleFunc({
                        module: "ScTimeTable",
                        func: "showMyEvents"
                    })
                }
            }]
        ]), ScCore.showDialogs({
            dialogs: [{
                title: "",
                config: {
                    panelSize: {
                        width: ScCore.maxFractionWidth(2 / 3, 800),
                        height: ScCore.autoPanelHeight()
                    },
                    menu: e
                },
                contents: [{
                    module: "ScTimeTable",
                    func: "showCalendar",
                    number: 1,
                    params: t
                }]
            }]
        })
    }

    selectCalendar(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbSelectCalendar,
                config: {
                    panelSize: {
                        width: 250,
                        height: ScCore.autoPanelHeight()
                    }
                },
                contents: [{
                    module: "ScTimeTable",
                    func: "selectCalendar"
                }]
            }]
        })
    }

    showChanges(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbChanges,
                config: {
                    maximize: !0,
                    header: !1,
                    boxShadow: 0
                },
                contents: [{
                    module: "ScTimeTable",
                    func: "showChanges"
                }]
            }]
        })
    }

    setScaling(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbScaling,
                config: {},
                contents: [{
                    module: "ScTimeTable",
                    func: "setScaling"
                }]
            }]
        })
    }

    showUnauthorizedStudentOutages(t) {
        ScCore.showDialogs({
            dialogs: [{
                title: scStr.ttbUnauthorizedStudentOutages,
                config: {},
                contents: [{
                    module: "ScTimeTable",
                    func: "showUnauthorizedStudentOutages"
                }]
            }]
        })
    }
}

class ScTimeTable_showEventUploads extends ScContent {
    constructor() {
        super(), this.templates = ["corTable"]
    }

    getContexts(t) {
        this.event_id = this.params.call.params.event_id, ScCore.performQuery("cmd=600&subcmd=700&event_id=" + this.event_id, function (e) {
            if (0 == e.header.state) {
                let s = e.tables.uploads.reduce(function (t, e) {
                    return t.includes(e.week) || t.push(e.week), t
                }, []);
                s = s.sort();
                let a = 3,
                    i = {};
                for (let t in s) i[parseInt(s[t])] = parseInt(t) + a;
                s.unshift(scStr.ttbTotal), s.unshift(scStr.ttbAllFiles), s.unshift(scStr.ttbName);
                let n = e.tables.persons.sort(function (t, e) {
                        return t.name == e.name ? Intl.Collator().compare(t.prename, e.prename) : Intl.Collator().compare(t.name, e.name)
                    }),
                    l = [],
                    c = {};
                for (let t in n) {
                    c[n[t].id] = parseInt(t), l.push({
                        cols: [{
                            label: n[t].name + ", " + n[t].prename
                        }, {
                            label: "<i class='icon f7-icons scPointer ' scEventId=" + this.event_id + " scPersonId=" + n[t].id + " >doc_on_doc</i>"
                        }, {
                            label: 0
                        }]
                    });
                    for (let e in i) l[t].cols.push({})
                }
                let o = e.tables.uploads;
                for (let t in o) {
                    let e = "";
                    ScCore.isset(o[t].published) && (e = "scCloudNotPublished", 1 == o[t].published && (e = "scCloudPublished"));
                    let s = "doc";
                    o[t].opened;
                    let a = "<i class='icon f7-icons scPointer " + e + "' scTimeId=" + o[t].time_id + " scParDate=" + o[t].parDate + " scPersonId=" + o[t].person_id + " >" + s + "</i>",
                        n = l[c[o[t].person_id]],
                        r = n.cols[i[o[t].week]];
                    if (ScCore.isset(r.label)) {
                        let t = r.label;
                        r.label = t + " " + a
                    } else r.label = a;
                    n.cols[2].label = parseInt(n.cols[2].label) + 1
                }
                for (let t in l) 0 == parseInt(l[t].cols[2].label) && (l[t].cols[2].label = "", l[t].cols[1].label = "");
                t([{
                    rowCount: !0,
                    header: s,
                    rows: l
                }])
            }
        }.bind(this))
    }

    attachEvents() {
        this.div.find("[scTimeId]").click(function () {
            let t = $(this).attr("scTimeId"),
                e = $(this).attr("scParDate"),
                s = $(this).attr("scPersonId");
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 320,
                    destId: t,
                    destType: 10030,
                    parDate: e,
                    filterType: 1,
                    filterItemId: s,
                    showDropZone: !1
                },
                callback: function () {
                }
            })
        }), this.div.find("[scEventId]").click(function () {
            let t = $(this).attr("ScEventId"),
                e = $(this).attr("scPersonId");
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 320,
                    eventId: t,
                    filterType: 1,
                    filterItemId: e,
                    showDropZone: !1
                },
                callback: function () {
                }
            })
        })
    }
}

class ScTimeTable_showTodoList extends ScContent {
    constructor() {
        super(), this.templates = ["ScTimeTable_showTodoList"]
    }

    getContexts(t) {
        ScCore.performQuery("cmd=600&subcmd=400", function (e) {
            0 == e.header.state && t([{
                items: e.tables.todo.map(function (t) {
                    return {
                        color: (t.materials || [])[320] > 0 ? "#008000" : "#ff0000",
                        title: sprintf(scStr.ttbHomeworkTodoUntil, t.homework_until.mySql2Local()),
                        title_r: t.subject_name,
                        body: Base64.decode(t.homework_b64),
                        time_id: t.time_id,
                        pardate: t.pardate,
                        from: sprintf(scStr.ttbHomeworkGivenAt, t.pardate.mySql2Local())
                    }
                })
            }])
        }.bind(this))
    }

    attachEvents() {
        $("[scTimeId]").click(function () {
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 320,
                    destId: $(this).attr("scTimeId"),
                    destType: 10030,
                    parDate: $(this).attr("scPardate"),
                    filterType: 1,
                    filterItemId: scGlobals.user.id,
                    showDropZone: !0
                },
                callback: function () {
                }
            })
        })
    }
}

class ScTimeTable_showMyEvents extends ScContent {
    constructor() {
        super(), this.templates = ["ScTimeTable_showMyEvents"]
    }

    getContexts(t) {
        ScCore.performQuery("cmd=600&subcmd=420", function (e) {
            0 == e.header.state && t([{
                items: e.tables.myEvents.map(function (t) {
                    (t.materials || [])[320];
                    return {
                        datetime: t.reviewed.mySql2Local(),
                        title_r: t.subject_name,
                        file_id: t.file_id,
                        body: sprintf(scStr.ttbMyEventTypeMsg[t.type], t.homework_created.mySql2LocalDate()),
                        time_id: t.time_id,
                        pardate: t.pardate
                    }
                })
            }])
        }.bind(this))
    }

    attachEvents() {
        $("[scTimeId]").click(function () {
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 320,
                    destId: $(this).attr("scTimeId"),
                    destType: 10030,
                    parDate: $(this).attr("scPardate"),
                    filterType: 1,
                    filterItemId: scGlobals.user.id,
                    showDropZone: !0
                },
                callback: function () {
                }
            })
        })
    }
}

class ScTimeTable_showUnauthorizedStudentOutages extends ScContent {
    constructor(t) {
        super(t), this.templates = ["ScCourseBook_showUnauthorizedStudentOutages"]
    }

    getContexts(t) {
        ScCore.performQuery("cmd=600&subcmd=235", function (e) {
            0 == e.header.state && e.tables.outages.length > 0 && t([{
                title: "",
                noMarginTop: !0,
                noItems: "",
                linked: !1,
                items: e.tables.outages.map(function (t) {
                    let e = "scPointer scCourseBookAbsent";
                    t.exceeded > 0 && (e = "scPointer scCourseBookAbsentExceeded");
                    let s = "";
                    return ScCore.isset(t.name) && (s = t.name, ScCore.isset(t.prename) && (s += ", " + t.prename)), {
                        id: t.id,
                        title: s,
                        after: t.subject_code,
                        header: t.pardate.mySql2LocalDate(),
                        footer: t.maingroup_s,
                        linked: !1,
                        studentOutageId: t.student_outage_id,
                        exceeded: t.exceeded,
                        titleClass: e
                    }
                })
            }])
        }.bind(this))
    }

    attachEvents() {
        $(this.div).find("[scStudentOutageId]").unbind(), $(this.div).find("[scStudentOutageId]").click(function () {
            function t() {
                0 == s ? (i.attr("scAuthorized", 1), i.find("[personname]").removeClass("scCourseBookAbsentExceeded"), i.find("[personname]").removeClass("scCourseBookAbsent"), i.find("[personname]").addClass("scCourseBookAuthorized"), s = 1) : (i.attr("scAuthorized", 0), i.find("[personname]").removeClass("scCourseBookAuthorized"), a > 0 ? i.find("[personname]").addClass("scCourseBookAbsentExceeded") : i.find("[personname]").addClass("scCourseBookAbsent"), s = 0), ScCore.performQuery("cmd=600&subcmd=237&student_outage=" + e + "&authorized=" + s, function (t) {
                    t.header.state
                })
            }

            let e = $(this).attr("scStudentOutageId"),
                s = parseInt($(this).attr("scAuthorized")),
                a = parseInt($(this).attr("scExceeded")),
                i = $(this);
            a > 0 && 0 == s ? scApp.f7.dialog.create({
                title: "",
                text: sprintf(scStr.ttbAuthorizationExceeded, 14),
                cssClass: "custom-dialog",
                closeByBackdropClick: "true",
                buttons: [{
                    text: scStr.corOK,
                    onClick: t
                }]
            }).open() : t()
        })
    }
}

class ScTimeTable_selectCalendar extends ScContent {
    constructor(t) {
        super(t), this.templates = ["ScTimeTable_selectCalendar"]
    }

    getContexts(t) {
        ScCore.performQuery("cmd=600&subcmd=600", function (e) {
            0 == e.header.state && t([{
                items: [{
                    title: "Kollegium",
                    items: e.tables.teachers.map(function (t) {
                        return {
                            itemType: 1,
                            itemId: t.id,
                            code: t.code
                        }
                    })
                }]
            }])
        }.bind(this))
    }

    attachEvents() {
        $(this.div).find("[scItemId]").unbind(), $(this.div).find("[scItemId]").click(function () {
            ScCore.moduleFunc({
                module: "ScTimeTable",
                func: "showCalendar",
                params: {
                    itemType: parseInt($(this).attr("scItemType")),
                    itemId: parseInt($(this).attr("scItemId"))
                }
            })
        })
    }
}

class ScTimeTable_showEvent extends ScContent {
    constructor(t) {
        super(t), this.templates = ["ScTimeTable_event"], this.colorPickerId = ScCore.uniqid(), this.datePickerStartId = ScCore.uniqid(), this.datePickerEndId = ScCore.uniqid(), this.timePickerStart, this.timePickerEnd, this.timePickerStartId = ScCore.uniqid(), this.timePickerEndId = ScCore.uniqid(), this.calendarPickerId = ScCore.uniqid()
    }

    getContexts(t) {
        let e = this.params.call.params.event,
            s = e.extendedProps.data,
            a = this.params.call.params.calendars,
            i = !1,
            n = !1;
        if (ScCore.isset(a[s.calendar])) {
            let t = a[s.calendar].PAM;
            i = ScCore.bitTest(t, 5), n = ScCore.bitTest(t, 8)
        }
        let l = [];
        if (i) {
            l.push({
                cols: [{
                    label: scStr.ttbEventType
                }, {
                    label: "<b>" + scStr.ttbEventTypes[s.type] + "</b>"
                }]
            }), (s.calendar < 300 || s.calendar > 399) && l.push({
                cols: [{
                    label: scStr.ttbCalendar
                }, {
                    label: '<input type="text" style="cursor:pointer"  placeholder="' + a[s.calendar].name + '" readonly="readonly" id="' + this.calendarPickerId + '"/>'
                }]
            }), l.push({
                cols: [{
                    label: scStr.ttbTitle
                }, {
                    label: '<textarea class="resizable" scInputTitle  rows="3">' + s.title + "</textarea>"
                }]
            });
            let t = 1 == s.allday ? "checked" : "";
            l.push({
                cols: [{
                    label: scStr.ttbAllday
                }, {
                    label: '<label class="toggle toggle-init ">\n\t\t\t\t<input type="checkbox" ' + t + ' scInputAllday>\n\t\t\t\t<span class="toggle-icon"></span>\n\t\t\t  </label>'
                }]
            }), l.push({
                cols: [{
                    label: scStr.ttbStartTime
                }, {
                    label: ScCore.dialogsDatePickerInsert({
                        id: this.datePickerStartId,
                        placeholder: scStr.ttbStartDate
                    }) + ScCore.dialogsTimePickerInsert({
                        id: this.timePickerStartId,
                        placeholder: scStr.ttbStartTimePh
                    })
                }]
            }), l.push({
                cols: [{
                    label: scStr.ttbEndTime
                }, {
                    label: ScCore.dialogsDatePickerInsert({
                        id: this.datePickerEndId,
                        placeholder: scStr.ttbEndDate
                    }) + ScCore.dialogsTimePickerInsert({
                        id: this.timePickerEndId,
                        placeholder: scStr.ttbEndTimePh
                    })
                }]
            }), s.edit = !0
        } else l.push({
            cols: [{
                label: scStr.ttbEventType
            }, {
                label: "<b>" + scStr.ttbEventTypes[s.type] + "</b>"
            }]
        }), (s.calendar < 300 || s.calendar > 399) && l.push({
            cols: [{
                label: scStr.ttbCalendar
            }, {
                label: a[s.calendar].name
            }]
        }), s.title && l.push({
            cols: [{
                label: scStr.ttbTitle
            }, {
                label: s.title
            }]
        }), s.moved_to && l.push({
            cols: [{
                label: scStr.ttbMovedTo
            }, {
                label: "<b>" + s.moved_to.mySql2Local() + "</b>"
            }]
        }), s.moved_from && l.push({
            cols: [{
                label: scStr.ttbMovedFrom
            }, {
                label: "<b>" + s.moved_from.mySql2Local() + "</b>"
            }]
        }), 1 != s.type && s.weekday && l.push({
            cols: [{
                label: scStr.ttbWeekday
            }, {
                label: scStr.corWeekdaysLong[s.weekday]
            }]
        }), l.push({
            cols: [{
                label: scStr.ttbStartTime
            }, {
                label: s.start_time.mySql2Iso1().iso2Local()
            }]
        }), l.push({
            cols: [{
                label: scStr.ttbEndTime
            }, {
                label: s.end_time.mySql2Iso1().iso2Local()
            }]
        }), s.participants && l.push({
            cols: [{
                label: scStr.ttbParticipants
            }, {
                label: ScTimeTable.getParticipants(s, !0)
            }]
        }), s.old_subject_code && s.new_subject_code ? l.push({
            cols: [{
                label: scStr.ttbOldSubject
            }, {
                label: s.old_subject_code
            }]
        }) : s.subject_code && l.push({
            cols: [{
                label: scStr.ttbSubject
            }, {
                label: s.subject_code
            }]
        }), s.new_subject_code && l.push({
            cols: [{
                label: scStr.ttbNewSubject
            }, {
                label: s.new_subject_code
            }]
        }), s.teacher_code ? l.push({
            cols: [{
                label: scStr.ttbTeacher
            }, {
                itemType: 1,
                itemId: s.teacher,
                label: s.teacher_code
            }]
        }) : s.old_teacher_code && l.push({
            cols: [{
                label: scStr.ttbOldTeacher
            }, {
                itemType: 1,
                itemId: s.old_teacher,
                label: s.old_teacher_code
            }]
        }), s.new_teacher_code && l.push({
            cols: [{
                label: scStr.ttbNewTeacher
            }, {
                itemType: 1,
                itemId: s.new_teacher,
                label: s.new_teacher_code
            }]
        }), s.old_location_code && s.new_location_code ? l.push({
            cols: [{
                label: scStr.ttbOldLocation
            }, {
                label: s.old_location_code
            }]
        }) : s.locations && l.push({
            cols: [{
                label: scStr.ttbLocation
            }, {
                label: ScTimeTable.getLocations(s)
            }]
        }), s.new_location_code && l.push({
            cols: [{
                label: scStr.ttbNewLocation
            }, {
                label: "<b>" + s.new_location_code + "<b>"
            }]
        }), s.information && l.push({
            cols: [{
                label: scStr.ttbInformation
            }, {
                label: s.information
            }]
        });
        let c = !1,
            o = !1,
            r = !1,
            d = !1;
        300 == s.calendar && 1 == e.calendarParams.itemType && e.calendarParams.itemId == scGlobals.user.id && (s.type < 1e3 || 1010 == s.type) && (c = !0, s.type < 1e3 && (o = !0), d = !0), s.calendar > 1e4 && (c = !0), 20 != scGlobals.user.type && 21 != scGlobals.user.type && 27 != scGlobals.user.type && (c = !1, o = !1, r = !1), t([{
            edit: i,
            canDelete: n,
            material: c,
            homework: o,
            documentation: r,
            courseBook: d,
            rows: l
        }])
    }

    attachEvents() {
        let t = this.params.call.params.event,
            e = t.extendedProps.data;
        this.div.find("[scItemType=1]").click(function () {
        }), ScCore.dialogsColorPickerAttach(this.colorPickerId, e.backgroundColor).on("close", function (e, s) {
            t.setProp("backgroundColor", e.value.hex), t.setProp("borderColor", e.value.hex)
        });
        let s = ScCore.dialogsDatePickerAttach({
            id: this.datePickerStartId,
            value: [t._instance.range.start.toISOString().substr(0, 10)]
        });
        s.on("close", function (t) {
        }), this.timePickerStart = ScCore.dialogsTimePickerAttach({
            id: this.timePickerStartId,
            value: [t._instance.range.start.toISOString().substr(11, 2), t._instance.range.start.toISOString().substr(14, 2)]
        });
        let a = new Date(t._instance.range.end);
        1 == e.allday && a.setDate(a.getDate() - 1);
        let i = ScCore.dialogsDatePickerAttach({
            id: this.datePickerEndId,
            value: [a.toISOString().substr(0, 10)]
        });
        this.timePickerEnd = ScCore.dialogsTimePickerAttach({
            id: this.timePickerEndId,
            value: [a.toISOString().substr(11, 2), a.toISOString().substr(14, 2)]
        });
        let n = this.params.call.params.calendars,
            l = [],
            c = [];
        for (let t in n) ScCore.bitTest(n[t].PAM, 5) && (l.push(n[t].id), c.push(n[t].name));
        let o = scApp.f7.picker.create({
            inputEl: "#" + this.calendarPickerId,
            formatValue: function (t, e) {
                return e
            },
            value: [e.calendar],
            cols: [{
                textAlign: "center",
                values: l,
                displayValues: c,
                onChange: function (t, e, s) {
                }
            }]
        });
        ScCore.isset(n[e.calendar]) && $("#" + this.calendarPickerId).val(n[e.calendar].name);
        let r = this;
        this.div.find("[scInputAllday]").change(function () {
            let t = $(this).prop("checked");
            e.allday = t ? 1 : 0, r.updateTimes()
        }), this.updateTimes(), this.div.find("[scButtonSave]").click(function () {
            let t = r.div.find("[scInputAllday]").prop("checked"),
                a = r.timePickerStart.value[0].pad(2, "0") + r.timePickerStart.value[1].pad(2, "0"),
                n = r.timePickerEnd.value[0].pad(2, "0") + r.timePickerEnd.value[1].pad(2, "0"),
                l = r.getDate(i.value);
            t && (a = "0000", n = "0000", l.setDate(l.getDate() + 1));
            let c = "cmd=600&subcmd=300";
            c += "&calendar=" + o.value[0], c += "&timeId=" + (e.time_id || 0), c += "&eventId=" + (e.event_id || 0), c += "&startDate=" + r.getDate(s.value).yyyymmdd(), c += "&endDate=" + l.yyyymmdd(), c += "&startTime=" + a, c += "&endTime=" + n, c += "&allday=" + (t ? 1 : 0), c += "&title=" + r.div.find("[scInputTitle]").val(), ScCore.performQuery(c, function (t) {
                0 == t.header.state && (ScCore.isset(e.deleteId) && r.params.call.params.calendar.getEventById(e.deleteId).remove(), scApp.dialogs.updateData("ScTimeTable_showCalendar"))
            }.bind(this)), r.closeDialog()
        }), this.div.find("[scButtonDelete]").click(function () {
            scApp.f7.dialog.confirm(scStr.ttbDeleteEventConfirm, scStr.ttbDeleteEvent, function () {
                let t = e.time_id || 0;
                if (t > 0) {
                    let s = "cmd=600&subcmd=310";
                    s += "&calendar=" + o.value[0], s += "&timeId=" + t, s += "&eventId=" + (e.event_id || 0), ScCore.performQuery(s, function (t) {
                        0 == t.header.state && scApp.dialogs.updateData("ScTimeTable_showCalendar")
                    }.bind(this))
                } else r.params.call.params.calendar.getEventById(e.deleteId).remove();
                r.closeDialog()
            })
        }), this.div.find("[scButtonMaterial]").click(function () {
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 310,
                    destId: e.time_id,
                    destType: 10030,
                    parDate: e.start_time
                },
                callback: function () {
                }
            })
        }), this.div.find("[scButtonHomework]").click(function () {
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 320,
                    destId: e.time_id,
                    destType: 10030,
                    parDate: e.start_time
                },
                callback: function () {
                }
            })
        }), this.div.find("[scButtonDocumentation]").click(function () {
            ScCore.moduleFunc({
                module: "ScCloud",
                func: "showDir",
                params: {
                    id: 330,
                    destId: e.time_id,
                    destType: 10030
                },
                callback: function () {
                }
            })
        }), this.div.find("[scButtonCourseBook]").click(function () {
            ScCore.moduleFunc({
                module: "ScCourseBook",
                func: "edit",
                params: {
                    time_id: e.time_id,
                    pardate: e.start_time
                },
                callback: function () {
                }
            })
        })
    }

    getDate(t) {
        return t = new Date(t), new Date(Date.UTC(t.getFullYear(), t.getMonth(), t.getDate()))
    }

    updateTimes() {
        if (1 == this.params.call.params.event.extendedProps.data.allday) $("#" + this.timePickerStartId).hide(), $("#" + this.timePickerEndId).hide();
        else {
            let t = this.timePickerStart.value,
                e = (this.timePickerEnd.value, this.params.call.params.calendar.getOption("minTime").split(":"));
            this.params.call.params.calendar.getOption("maxTime").split(":");
            parseInt(t[0]) < parseInt(e[0]) && (this.timePickerStart.setValue([e[0].pad(2, "0"), e[1].pad(2, "0")]), this.timePickerEnd.setValue([(parseInt(e[0]) + 1).pad(2, "0"), e[1].pad(2, "0")])), $("#" + this.timePickerStartId).show(), $("#" + this.timePickerEndId).show()
        }
    }
}

class ScTimeTable_showCalendar extends ScContent {
    constructor(t) {
        super(t), this.dependencies = [{
            name: "fullcalendar",
            extern: !0
        }], this.calendar, this.calendars = {}, this.lastData, this.firstCreateCalendar = 0, this.slotDuration = 20, this.activeCalendars = []
    }

    getContexts(t) {
        setTimeout(function () {
            t([])
        }, 200)
    }

    prepare() {
        let t = this;
        this.setContent('<div class=" block-footer scTimeTableHeader" scLastScheduleUpdate></div><div scType="calendar" style="padding:4px;" class="swipeout"></div>');
        let e = this.div.find("[scType=calendar]")[0],
            s = {
                plugins: ["interaction", "dayGrid", "timeGrid", "list"],
                header: {
                    left: "prev,next today",
                    center: "title",
                    right: "timeGridWeek,timeGridDay"
                },
                nowIndicator: !0,
                height: "phone" == scGlobals.device.type ? this.getHeight() + 64 : this.getHeight() + 30,
                locale: "de",
                buttonIcons: !0,
                weekNumbers: !0,
                navLinks: !0,
                editable: !1,
                eventLimit: !0,
                defaultView: "phone" == scGlobals.device.type ? "timeGridDay" : "timeGridWeek",
                hiddenDays: [0, 6],
                slotDuration: "00:" + this.slotDuration + ":00",
                slotLabelFormat: {
                    hour: "numeric",
                    minute: "2-digit",
                    omitZeroMinute: !1,
                    meridiem: "short"
                },
                scrollTime: "08:00:00",
                dateClick: function () {
                },
                eventClick: function (t) {
                    let e = t.event;
                    e.calendarParams = this.params.call.params, ScCore.moduleFunc({
                        module: "ScTimeTable",
                        func: "showEvent",
                        params: {
                            event: e,
                            calendars: this.calendars,
                            calendar: this.calendar,
                            parent: this.params.dialogId
                        }
                    })
                }.bind(this),
                eventOrder: function (t, e) {
                    return t.data.type > e.data.type ? 1 : t == e ? 0 : -1
                },
                dayRender: function (t) {
                },
                datesRender: function (e) {
                    t.updateCalendar(e)
                },
                eventRender: function (t) {
                },
                displayEventEnd: !0,
                selectable: !0,
                unselectAuto: !0,
                select: function (t) {
                    if (this.firstCreateCalendar > 0) {
                        ScDebug.out(t);
                        let e = ScCore.uniqid();
                        this.calendar.addEvent({
                            id: e,
                            title: scStr.ttbNewEvent,
                            start: t.start,
                            end: t.end,
                            allDay: t.allDay,
                            data: {
                                type: 1,
                                calendar: this.firstCreateCalendar,
                                title: scStr.ttbNewEvent,
                                allday: t.allDay,
                                deleteId: e
                            }
                        })
                    }
                }.bind(this)
            };
        "_testgym" == scGlobals.client.name && (s.defaultDate = "2020-04-27", ScCore.alert("Das Startdatum in der Testumgebung ist standardmäßig auf den 27.04.2020 gesetzt.\nNormalerweise wird hier der aktuelle Tag bzw. die aktuelle Woche angezeigt."));
        let a = new FullCalendar.Calendar(e, s);
        a.setOption("minTime", "08:00:00"), a.setOption("maxTime", "21:00:00"), a.render(), this.adjustCalendar(), this.calendar = a;
        let i = new Hammer(this.div[0]);
        i.on("swipeleft", function (e) {
            t.calendar.next()
        }), i.on("swiperight", function (e) {
            t.calendar.prev()
        })
    }

    attachEvents() {
    }

    adjustCalendar() {
        this.div.find(".fc-today-button").hide(), this.params.dialog.phone ? this.div.find("h2").css("font-size", "11px") : this.div.find("h2").css("font-size", "20px"), this.div.find("h2").css("margin-left", "8px"), this.div.find("button").css("background-color", "#" + scGlobals.layout.colors.main), this.div.find("button").css("border", "0px"), this.div.find("button").css("margin-right", "4px")
    }

    updateData() {
        this.updateCalendar()
    }

    updateCalendar(t) {
        if (ScCore.isset(t)) {
            let e = t.view.calendar.state.dateProfile.activeRange;
            this.startDate = e.start, this.endDate = e.end
        }
        let e = this.startDate.toMySql(),
            s = this.endDate.toMySql();
        ScCore.performQuery("cmd=600&subcmd=100&itemType=" + this.params.call.params.itemType + "&itemId=" + this.params.call.params.itemId + "&startDate=" + e + "&endDate=" + s, function (t) {
            if (0 == t.header.state) {
                if (0 == this.activeCalendars.length)
                    for (let e in t.tables.calendars.data) {
                        10050 != t.tables.calendars.data[e].id && this.activeCalendars.push(parseInt(t.tables.calendars.data[e].id))
                    }
                let e = t.item.code || scStr.ttbCalendar;
                scGlobals.user.maingroup_s.length > 0 && (e += ", (" + scGlobals.user.maingroup_s + ")"), this.setTitle(e), this.div.find("[scLastScheduleUpdate]").text(scStr.ttbLastScheduleUpdate + " " + t.item.lastScheduleUpdate.mySql2Local()), this.updateEvents(t)
            }
        }.bind(this)), ScDebug.out("Update Calendar: " + this.startDate + " -> " + this.endDate)
    }

    getCalendars(t) {
        this.calendars = {};
        let e = t.tables.calendars.data;
        for (let t in e) this.calendars[e[t].id] = e[t]
    }

    checkCanCreate(t) {
        this.firstCreateCalendar = 0;
        for (let t in this.calendars)
            if (ScCore.bitTest(this.calendars[t].PAM, 7)) {
                this.firstCreateCalendar = this.calendars[t].id;
                break
            }
    }

    updateEvents(t) {
        this.getCalendars(t), this.checkCanCreate(t);
        let e = this.calendar.getEventSources();
        for (let t in e) e[t].remove();
        let s = [],
            a = [],
            i = 0;
        for (let e in t.tables.schedule) {
            let s = t.tables.schedule[e];
            if (100 == s.type || 200 == s.type) {
                let t = new KolorWheel("#" + scGlobals.layout.colors.main);
                t.h += 30 * i, t.l += -15 * (1 + i % 2), t.s += -20, a[s.event_id] = t, i++
            }
        }
        // Farben
        let n = ["#25d4a3", "#26ac78", "#a7bc2b", "#e08641", "#00aaa4", "#72ACD1", "#006464", "#373866", "#7F2042"];
        i = 0;
        for (let t in a) a[t] = new KolorWheel(n[i % n.length]), i++;
        for (let e in t.tables.schedule) {
            let i = t.tables.schedule[e],
                n = ScTimeTable.getParticipants(i),
                l = "",
                c = "";
            if (ScCore.isset(i.title) && i.title.length > 0 && (l = i.title + "\n"), 100 == i.type || 200 == i.type) {
                i.className = "";
                let t = i.subject_code || "";
                if (t.length > 0) {
                    let e = i.coursenumber || 0;
                    e > 0 && (t += e), t += ", ", ScCore.isset(i.lessontype) && ("D71A" == i.lessontype.substr(0, 4) && (t = t.toUpperCase()), "7782" == i.lessontype.substr(0, 4) && (t = t.toLowerCase()))
                }
                n.length > 0 && (l += n + ", "), l += t, ScCore.isset(i.teacher) && (l += i.teacher_code + ", "), l += ScTimeTable.getLocations(i);
                let e = a[i.event_id].getHex();
                if (ScCore.issetMinLength(i.moved_to) && (e = "", i.className = "scFcMovedTo", l += "\n" + i.moved_to.mySql2Local()), i.backgroundColor = e, ScCore.issetMinLength(i.participant_outages)) {
                    let t = i.participants.length || 0;
                    i.participant_outages.length == t ? i.className = "scFcParticipantOutage" : i.className = "scFcParticipantOutage1"
                }
                let o = new KolorWheel(i.backgroundColor).isDark() ? "#ffffff" : "#000000",
                    r = i.backgroundColor;
                i.className = "scFcBorderMaterial";
                let d = ScCore.isset(i.homework_until) && 20 == scGlobals.user.type;
                if (ScCore.isset(i.materials) || (i.materials = {
                    310: 0,
                    320: 0
                }), ScCore.isset(i.materials))
                    if (21 == scGlobals.user.type) {
                        if (i.materials[310] > 0 && (r = "#0000ff"), i.materials[320] > 0) {
                            let t = Math.round(i.materials[320] / i.participants_count * 100);
                            t > 0 && t < 10 && (t = 10), t = 10 * Math.round(t / 10), i.className = "scFcBorderMaterial scFcBorderMaterial" + t
                        }
                    } else c = i.materials[310] > 0 ? "1" : "0", c += d ? i.materials[320] > 0 ? "2" : "1" : "0", i.className = "scFcBorderMaterial scFcBorderMaterialS" + c;
                ", " == l.slice(-2) && (l = l.substr(0, l.length - 2)), s.push({
                    id: "ti_" + i.time_id,
                    title: l,
                    data: i,
                    start: i.start_time.mySql2Iso1(),
                    end: i.end_time.mySql2Iso1(),
                    textColor: o,
                    backgroundColor: i.backgroundColor,
                    borderColor: r,
                    className: i.className
                })
            }
            // Setzt, welche Art von Stunde das ist (Vertretung, Freistunde, etc...)
            if (i.type > 1e3 && 40 != i.gapreason) {
                i.className = "", l += n + " ";
                let t = "",
                    e = i.old_subject_code || i.subject_code || "";
                if (
                    i.new_subject_code
                        ? t += "+" + i.new_subject_code + (e.length > 0 ? " (" + e + ")" : "")
                        : ScCore.issetMinLength(e) && (t += e),
                    t.length > 0 && (l += t + "\n"), ScCore.issetMinLength(i.new_location_code)
                ) {
                    let t = i.old_location_code || "";
                    t.length > 0 && (t = "(" + t + ")"), l += "+" + i.new_location_code + " " + t + "\n"
                } else ScCore.issetMinLength(i.old_location_code) && (l += i.old_location_code), l += "\n";
                ScCore.issetMinLength(i.new_teacher_code) ?
                    (
                        l += "+" + i.new_teacher_code + " ",
                        ScCore.issetMinLength(i.old_teacher_code
                        ) && (l += "(" + i.old_teacher_code + ")\n"))
                    :
                    ScCore.issetMinLength(i.old_teacher_code) && (l += i.old_teacher_code + "\n"), i.className = "scFcImportant";
                1030 == i.type && (i.className = "scFcUnImportant");
                1050 == i.type && (i.className = "scFcCancelled");
                1060 == i.type && (i.className = "scFcSelf");
                ScCore.issetMinLength(i.moved_from) && (l += i.moved_from.mySql2Local(), i.className = "scFcMovedFrom");
                ScCore.issetMinLength(i.moved_to) && (l += i.moved_to.mySql2Local(), i.className = "scFcMovedTo");
                s.push({
                    id: "ch_" + i.change_id,
                    title: l,
                    data: i,
                    start: i.start_time.mySql2Iso1(),
                    end: i.end_time.mySql2Iso1(),
                    textColor: "#ffffff",
                    className: i.className
                })
            }
            if (90 == i.type && s.push({
                id: "ot_" + i.outage_id,
                data: i,
                start: i.start_time.mySql2Iso1(),
                end: i.end_time.mySql2Iso1(),
                className: "scFcOwnAbsence",
                rendering: "background"
            }), 1 == i.type && this.activeCalendars.includes(parseInt(i.calendar))) {
                let t = this.calendars[i.calendar].color || "#000000",
                    e = 1 == i.allday;
                s.push({
                    id: "ti_" + i.time_id,
                    title: l,
                    data: i,
                    allDay: e,
                    start: i.start_time.mySql2Iso1(),
                    end: i.end_time.mySql2Iso1(),
                    textColor: t,
                    backgroundColor: "#f0f0f0",
                    borderColor: t
                })
            }
        }
        this.calendar.addEventSource(s), this.div.find("[scType=calendar]").find(".fc-time-grid-event").each(function () {
            let t = parseInt($(this).css("left"));
            t > 0 && $(this).css("left", t / 2)
        })
    }

    activateCalendars() {
        this.activeCalendars.push(10050), this.updateData()
    }

    changeSlotDuration(t) {
        this.slotDuration += t, this.slotDuration > 60 && (this.slotDuration = 60), this.slotDuration < 10 && (this.slotDuration = 10), this.calendar.setOption("slotDuration", "00:" + this.slotDuration + ":00"), this.adjustCalendar()
    }

    printCalendar(t) {
        ScCore.performQuery("cmd=600&subcmd=110", function (t) {
            0 == t.header.state && this.exportCalender2PDF({
                data: t
            })
        }.bind(this))
    }

    exportCalender2PDF(t) {
        let e = {
            filename: scStr.ttbCalendar,
            pages: []
        };
        this.firstPDFPage(e);
        let s = 0,
            a = 60,
            i = -1;
        for (let n in t.data.tables.events) {
            let l = t.data.tables.events[n];
            (a += 5) > 275 && (e.pages.push({
                orientation: "p",
                elements: []
            }), a = 30, s++);
            let c = e.pages[s].elements,
                o = parseInt(l.start_time.substr(5, 2)) - 1;
            parseInt(l.start_time.substr(0, 4));
            o != i && (a > 260 ? (e.pages.push({
                orientation: "p",
                elements: []
            }), a = 30, s++, c = e.pages[s].elements) : 30 != a && (a += 5), c.push({
                type: "text",
                position: [24, a],
                text: scStr.corMonthNames[o],
                fontSize: 12,
                fontStyle: "bold"
            }), c.push({
                type: "line",
                rect: [22.5, a + 1.5, 190, a + 1.5]
            }), i = o, a += 5);
            let r = l.start_time.mySql2Date(),
                d = l.end_time.mySql2Date(),
                m = ScCore.dateDiffInDays(r, d),
                u = l.start_time.substr(8, 2) + "." + l.start_time.substr(5, 2),
                h = l.start_time.substr(11, 5);
            if ("00:00" == h ? h = "" : h += " - " + l.end_time.substr(11, 5), 1 == l.allday) {
                if (m > 1) {
                    let t = d.addDays(0).toMySql();
                    u += " - " + t.substr(8, 2) + "." + t.substr(5, 2)
                }
                h = ""
            }
            c.push({
                type: "text",
                position: [24, a],
                text: u,
                fontSize: 8
            }), c.push({
                type: "text",
                position: [49, a],
                text: h,
                fontSize: 8
            }), c.push({
                type: "text",
                position: [74, a],
                text: l.title,
                fontSize: 8
            }), c.push({
                type: "line",
                rect: [22.5, a + 1.5, 190, a + 1.5]
            })
        }
        ScCore.moduleFunc({
            module: "ScPrint",
            func: "print",
            params: e
        })
    }

    firstPDFPage(t) {
        let e = {
            orientation: "p",
            elements: [{
                type: "text",
                position: [24, 18],
                text: scGlobals.client.fullname,
                fontSize: 20
            }, {
                type: "text",
                position: [24, 24],
                text: scStr.ttbCalendar + " für das Schuljahr 2020/21",
                fontSize: 12
            }, {
                type: "text",
                position: [24, 29],
                text: "Die aktuellsten Termine finden Sie unter:",
                fontSize: 10
            }, {
                type: "text",
                position: [24, 33],
                text: "scooso.org/rwg",
                fontSize: 10
            }, {
                type: "text",
                position: [24, 40],
                text: "Stand: " + (new Date).ddmmyyyy(),
                fontSize: 12,
                fontStyle: "bold"
            }, {
                type: "image",
                data: "",
                rect: [136, 4, 56, 44],
                imageType: "PNG"
            }]
        };
        t.pages.push(e)
    }
}

class ScTimeTable_showChanges extends ScContent {
    constructor(t) {
        super(t), this.templates = ["ScTimeTable_changes"], this.currentPage = 0, this.pageNum = 0
    }

    getContexts(t) {
        ScCore.performQuery("cmd=16100&subcmd=1000&days=1&type=daVinci", function (e) {
            0 == e.header.state && t([this.getContextChanges(e)])
        }.bind(this))
    }

    prepare() {
        this.firstPage()
    }

    attachEvents() {
    }

    firstPage() {
        this.div.find("[scPageNum]").hide(), this.div.find("[scPageNum=0]").show(), this.currentPage = 0, this.div.find("[scType=curPage]").html(this.currentPage + 1), setTimeout(function () {
            this.nextPage()
        }.bind(this), 1e4)
    }

    nextPage() {
        this.currentPage++, this.currentPage %= this.pageNum, this.div.find("[scType=curPage]").html(this.currentPage + 1), this.div.find("[scPageNum]").hide(), this.div.find("[scPageNum=" + this.currentPage + "]").show(), setTimeout(function () {
            this.nextPage()
        }.bind(this), 1e4)
    }

    getContextChanges(t) {
        let e = [],
            s = 80,
            a = 47,
            i = 33,
            n = 0,
            l = this.div.parents().height(),
            c = s,
            o = [],
            r = [];
        for (let d in t.tables.envolvedTeachers) {
            let m = a + t.tables.envolvedTeachers[d].length * i;
            c + m > l && (r.push({
                items: o
            }), o = [], c = s, 2 == ++n && (e.push({
                cols: r
            }), r = [], n = 0));
            let u = [];
            for (let e in t.tables.envolvedTeachers[d]) {
                let s = t.tables.envolvedTeachers[d][e],
                    a = t.tables.changes[s],
                    i = a.time > 0,
                    n = [],
                    l = "",
                    c = "";
                t.item.date != a.startdate && (c = "scTimeTableOtherDay ");
                let o = t.tables.versions.length - a.version;
                if (o < t.tables.versions.length && (c += " scTimeTableVersionV" + o), n.push({
                    label: ScCore.getShortDateFromString(a.startdate),
                    class: "scTimeTableShortDate"
                }), n.push({
                    label: scStr.corWeekdaysShort[a.weekday],
                    class: "scTimeTableWeekday"
                }), n.push({
                    label: a.position,
                    class: "scTimeTablePosition"
                }), a.lack_class) {
                    for (let t in a.classes) a.lack_class == a.classes[t] && (a.classes[t] = "(" + a.classes[t] + ")");
                    l = scStr.ttbMsgClassLacks
                }
                let r = (a.classes || []).join() + (a.newclasses || []).join();
                n.push({
                    label: r,
                    class: "scNum"
                });
                let m = a.oldsubject;
                a.newsubject && (m = i ? "+" + a.newsubject + " (" + m + ")" : a.newsubject), n.push({
                    label: m
                });
                let h = a.oldroom;
                a.newrooms.length > 0 && (h = "", i && (h += "+"), h += (a.newrooms || []).join(), i && (h += " (" + a.oldroom + ")"), l = scStr.ttbMsgRoomChange), n.push({
                    label: h,
                    class: "scNum"
                });
                let p = a.oldteacher;
                a.lack_teacher && (l = scStr.ttbMsgCanceled), a.newteachers.length > 0 && (p = "", i && (p += "+"), p += a.newteachers.join(), i && a.oldteacher && (p += " (" + a.oldteacher + ")"), l = ""), n.push({
                    label: p
                }), a.newsubject = a.newsubject || "", (a.newsubject.length > 0 || a.newsubjects.length > 0) && (l = ""), a.newclasses.length > 0 && (l = ""), a.mirrorInfo.length > 0 && (l = a.mirrorInfo), a.information.length > 0 && (l.length > 0 ? l += "<br>" + a.information : l = a.information), n.push({
                    label: l
                }), u.push({
                    class: c,
                    cols: n
                })
            }
            o.push({
                name: d,
                rows: u
            }), c += m
        }
        return r.push({
            items: o
        }), e.push({
            cols: r
        }), this.pageNum = e.length, {
            colClass: "tablet-50",
            header: "Vertretungsplan für den " + ScCore.getDateFromString(t.item.date),
            lastUpdate: "Stand: " + ScCore.getTimeFromString(t.item.lastUpdate),
            version: t.tables.versions.length,
            totalPages: e.length,
            pages: e
        }
    }
}

class ScTimeTable_setScaling extends ScContent {
    constructor(t) {
        super(t), this.templates = ["ScTimeTable_scaling"]
    }

    getContexts(t) {
        t([])
    }

    attachEvents() {
    }
}

$.extend(scApp.templates, {
    ScTimeTable_changes: Template7.compile("\n\t\t\t<h2 class=scTimeTableH2 align=center>{{header}}</h2>\n\t\t\t<h4 class=scTimeTableH4 align=center>{{lastUpdate}}, Version: {{version}}, Seite: <span scType=curPage>1</span>/{{totalPages}}</h4>\n\t\t\t\t\t{{#each pages}}\n\t\t\t\t\t\t<div class=\"row no-gap\" scPageNum={{@index}}>\n\t\t\t\t\t\t{{#each cols}}\n\t\t\t\t\t\t\t<div class=\"{{@root.colClass}}\">\n\t\t\t\t\t\t\t\t<table  class=scTimeTableTable>\n\t\t\t\t\t\t\t\t\t<tbody>\n\t\t\t\t\t\t\t\t\t\t\t{{#each items}}\n\t\t\t\t\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=scTimeTableItemName scItemId='' >{{name}}</td>\n\t\t\t\t\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t\t\t\t\t\t{{#each rows}}\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr class='{{class}}' >\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{{#cols}}\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class='scTimeTableDataItem {{class}}' scItemId='{{id}}' >{{label}}</td>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{{/cols}}\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t\t\t\t\t\t{{/each}}\n\t\t\t\t\t\t\t\t\t\t\t{{/each}}\n\t\t\t\t\t\t\t\t\t</tbody>\n\t\t\t\t\t\t\t\t</table>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t{{/each}}\n\t\t\t\t\t\t</div>\n\t\t\t\t\t{{/each}}\n\t\t\t\n\t"),
    ScTimeTable_horizontal_timeline: Template7.compile('\n\t\t<div class="timeline timeline-horizontal col-50 tablet-20">\n\t\t  \x3c!-- Timeline Item (Day) --\x3e\n\t\t  <div class="timeline-item" >\n\t\t\t<div class="timeline-item-date">21 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">\n\n\t\t\t  <div class="timeline-item-inner" style="border:solid 5px #ff0000;height:120px;">\n\t\t\t\t<div class="timeline-item-time">1. Stunde</div>\n\t\t\t\t<div class="timeline-item-title">Musik</div>\n\t\t\t\t<div class="timeline-item-subtitle">9a</div>\n\t\t\t\t<div class="timeline-item-text" style="color:#ff0000;">Vertretung</div>\n\t\t\t  </div>\n\n\t\t\t  <div class="timeline-item-inner" style="border:solid 1px #0000ff;height:120px;">\n\t\t\t\t<div class="timeline-item-time">2. Stunde</div>\n\t\t\t\t<div class="timeline-item-title">Mathematik</div>\n\t\t\t\t<div class="timeline-item-subtitle">8c</div>\n\t\t\t\t<div class="timeline-item-text"></div>\n\t\t\t  </div>\n\n\t\t\t  <div class="timeline-item-inner" style="border:solid 1px #ffff00;;height:120px;">\n\t\t\t\t<div class="timeline-item-time">3. Stunde</div>\n\t\t\t\t<div class="timeline-item-title">Mathematik</div>\n\t\t\t\t<div class="timeline-item-subtitle">10d</div>\n\t\t\t\t<div class="timeline-item-text"></div>\n\t\t\t  </div>\n\n\t\t\t</div>\n\t\t  </div>\n\t\t  <div class="timeline-item">\n\t\t\t<div class="timeline-item-date">22 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">Plain text goes here</div>\n\t\t  </div>\n\t\t  \x3c!-- Timeline Item With Card --\x3e\n\t\t  <div class="timeline-item">\n\t\t\t<div class="timeline-item-date">23 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">\n\t\t\t  <div class="card">\n\t\t\t  </div>\n\t\t\t</div>\n\t\t  </div>\n\t\t  \x3c!-- Timeline Item With List Block --\x3e\n\t\t  <div class="timeline-item">\n\t\t\t<div class="timeline-item-date">24 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">\n\t\t\t  <div class="list inset">\n\t\t\t\t<ul>\n\t\t\t\t</ul>\n\t\t\t  </div>\n\t\t\t</div>\n\t\t  </div>\n\t\t  <div class="timeline-item">\n\t\t\t<div class="timeline-item-date">25 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">\n\t\t\t  <div class="timeline-item-time">11:11</div>\n\t\t\t  <div class="timeline-item-text">Task 1</div>\n\t\t\t  <div class="timeline-item-time">12:33</div>\n\t\t\t  <div class="timeline-item-text">Task 2</div>\n\t\t\t</div>\n\t\t  </div>\n\t\t  <div class="timeline-item">\n\t\t\t<div class="timeline-item-date">26 <small>DEC</small></div>\n\t\t\t<div class="timeline-item-content">\n\t\t\t  <div class="timeline-item-inner">\n\t\t\t\t<div class="timeline-item-time">11:11</div>\n\t\t\t\t<div class="timeline-item-text">Task 1</div>\n\t\t\t  </div>\n\t\t\t  <div class="timeline-item-inner">\n\t\t\t\t<div class="timeline-item-time">12:33</div>\n\t\t\t\t<div class="timeline-item-text">Task 2</div>\n\t\t\t  </div>\n\t\t\t</div>\n\t\t  </div>\n\t\t</div>\t\t\t\n\t'),
    ScTimeTable_scaling: Template7.compile('\n\t\t<div class="block block-strong display-flex justify-content-center">\n\t\t  <div class="range-slider range-slider-init margin-right"\n\t\t\tdata-vertical="true"\n\t\t\tdata-min="0"\n\t\t\tdata-max="100"\n\t\t\tdata-label="true"\n\t\t\tdata-step="1"\n\t\t\tdata-value="25"\n\t\t\tstyle="height: 160px"\n\t\t  ></div>\n\t\t</div>\t\t\t\n\t'),
    ScTimeTable_selectCalendar: Template7.compile('\n\x3c!-- <div class="block-title">Opposite Side</div> --\x3e\n<div class="list accordion-list accordion-opposite">\n\t<ul>\n\t\t{{#each items}}\n\t\t\t<li class="accordion-item">\n\t\t\t  <a class="item-content item-link" href="#">\n\t\t\t\t<div class="item-inner">\n\t\t\t\t  <div class="item-title">{{title}}</div>\n\t\t\t\t</div>\n\t\t\t  </a>\n\t\t\t  <div class="accordion-item-content">\n\t\t\t\t<div class="block">\n\t\t\t\t\t<div class="list simple-list scPointer">\n\t\t\t\t\t\t<ul>\n\t\t\t\t\t\t{{#each items}}\n\t\t\t\t\t\t\t<li scItemId = "{{itemId}}" scItemType = "{{itemType}}">\n\t\t\t\t\t\t\t\t{{code}} \n\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t{{/each}}\n\t\t\t\t\t\t</ul>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t  </div>\n\t\t\t</li>\n\t\t{{/each}}\n\t</ul>\n</div>\n  '),
    ScTimeTable_calendar: Template7.compile("\n\t\t<div scType=calendar style='margin:8px'></div>\t\t\t\n\t"),
    ScTimeTable_event: Template7.compile('\n\t\t\t<div  class="data-table" >\n\t\t\t<table id={{id}} class="display" style="width:100%;">\n\t\t\t\t<tbody>\n\t\t\t\t\n\t\t\t\t{{#if type}}\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td class="label-cell" >{{js "scStr[\'ttbEventType\']"}}</td>\n\t\t\t\t\t\t<td class="label-cell {{class}}-cell" scItemId=\'{{formid}}\' scTokenId=\'{{formtoken}}\'><b>{{js "scStr[\'ttbEventTypes\'][this.type]"}}</b></td>\n\t\t\t\t\t</tr>\n\t\t\t\t{{/if}}\n\t\t\t\t\n\t\t\t\t{{#if title}}\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td class="label-cell" >{{js "scStr[\'ttbTitle\']"}}</td>\n\t\t\t\t\t\t<td class="label-cell {{class}}-cell">\n\t\t\t\t\t\t{{#if @root.edit}}\t\t\t\n\t\t\t\t\t\t\t<textarea class="resizable">{{title}}</textarea>\n\t\t\t\t\t\t{{else}}\n\t\t\t\t\t\t\t{{title}}\n\t\t\t\t\t\t{{/if}}\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t{{/if}}\n\n\t\t\t\t{{#if allday}}\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td class="label-cell" >{{js "scStr[\'ttbAllday\']"}}</td>\n\t\t\t\t\t\t<td class="label-cell {{class}}-cell">\n\t\t\t\t\t\t\t<label class="toggle toggle-init {{js "this.edit==\'1\'?\'\':\'disabled\'"}}">\n\t\t\t\t\t\t\t\t\t<input type="checkbox" {{js "this.allday==\'1\'?\'checked\':\'\'"}}  >\n\t\t\t\t\t\t\t\t\t<span class="toggle-icon"></span>\n\t\t\t\t\t\t\t</label>\t\t\t\t\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t{{/if}}\n\t\t\t\t\n\t\t\t\t\n\n\t\t\t\t{{#rows}}\n\t\t\t\t\t<tr   >\n\t\t\t\t\t\t{{#cols}}\n\t\t\t\t\t\t\t<td class="label-cell {{class}}-cell" scItemType=\'{{itemType}}\' scItemId=\'{{itemId}}\' >{{label}}</td>\n\t\t\t\t\t\t{{/cols}}\n\t\t\t\t\t</tr>\n\t\t\t\t{{/rows}}\n\n\t\t\t\t</tbody>\n\t\t\t</table>\n\t\t\t</div>\n\t\t\t<div class="block">\n\t\t\t\t{{#if material}}\n\t\t\t\t\t<button class="col button button-large button-fill" scButtonMaterial>{{js "scStr[\'corMaterial\']"}}</button><br>\n\t\t\t\t{{/if}}\n\t\t\t\t{{#if homework}}\n\t\t\t\t\t<button class="col button button-large button-fill" scButtonHomework>{{js "scStr[\'corHomework\']"}}</button><br>\n\t\t\t\t{{/if}}\n\t\t\t\t{{#if documentation}}\n\t\t\t\t\t<button class="col button button-large button-fill" scButtonDocumentation>{{js "scStr[\'corDocumentation\']"}}</button>\n\t\t\t\t{{/if}}\n\t\t\t\t{{#if courseBook}}\n\t\t\t\t\t<button class="col button button-large button-fill" scButtonCourseBook>{{js "scStr[\'corCourseBook\']"}}</button>\n\t\t\t\t{{/if}}\n\t\t\t\t\n\t\t\t\t\n\t\t\t</div>\n\t\t\t<div class="block">\n\t\t\t  <div class="row">\n\t\t\t\t{{#if edit}}\n\t\t\t\t\t<button class="col button button-large button-fill" scButtonSave>{{js "scStr[\'corSave\']"}}</button>\n\t\t\t\t{{/if}}\n\t\t\t\t{{#if canDelete}}\n\t\t\t\t\t<button class="col button button-large button-fill color-red" scButtonDelete>{{js "scStr[\'corDelete\']"}}</button>\n\t\t\t\t{{/if}}\n\t\t\t  </div>\n\t\t\t</div>\n\t\t'),
    ScTimeTable_showTodoList: Template7.compile('\n\t\t\x3c!-- -------------- --\x3e\n\t\t\x3c!-- List of items \t--\x3e\n\t\t\x3c!-- --------------\t--\x3e\n\t\t<div class="list" scIndexedList>\n\t\t\t\t{{#js_if "this.items.length>0"}}\n\n\t\t\t\t\t{{#each items}}\n\t\t\t\t\t\t<div class="card">\n\t\t\t\t\t\t  <div class="card-header scTimeTableTodoListHeader"><span style=\'color:{{color}}\'>{{title}}</span><br><span class=\'scTimeTableTodoSubject\'>{{title_r}}</span></div>\n\t\t\t\t\t\t  <div class="card-content card-content-padding">{{body}}</div>\n\t\t\t\t\t\t  {{#if footer}}\n\t\t\t\t\t\t\t<div class="card-footer">{{footer}}</div> \n\t\t\t\t\t\t  {{/if}}\n\t\t\t\t\t\t\t<div class="card-footer" >\n\t\t\t\t\t\t\t\t<table width=100%>\n\t\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t\t<td>{{from}}</td>\n\t\t\t\t\t\t\t\t\t\t<td class="scNr">\n\t\t\t\t\t\t\t\t\t\t\t<a href=\'#\'>\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\'icon f7-icons\' scTimeId={{time_id}} scPardate={{pardate}}>folder</i>\n\t\t\t\t\t\t\t\t\t\t\t\t\x3c!-- <i class=\'icon f7-icons\' scTimeId={{time_id}} scPardate={{pardate}}>burst</i> --\x3e\n\t\t\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t</table>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\t\t\t\t\n\t\t\t\t\t{{/each}}\n\t\t\t\t{{else}}\n\t\t\t\t\t<div class="block">\n\t\t\t\t\t\t##ttbNoEntries##\n\t\t\t\t\t</div>\n\t\t\t\t{{/js_if}}\n\t\t</div>\t\n\t'),
    ScTimeTable_showMyEvents: Template7.compile('\n\t\t\x3c!-- -------------- --\x3e\n\t\t\x3c!-- List of items \t--\x3e\n\t\t\x3c!-- --------------\t--\x3e\n\t\t<div class="list" scIndexedList>\n\t\t\t\t{{#js_if "this.items.length>0"}}\n\n\t\t\t\t\t{{#each items}}\n\t\t\t\t\t\t<div class="card">\n\t\t\t\t\t\t  <div class="card-header scTimeTableMyEventListHeader"><span style=\'color:{{color}}\'>{{datetime}}</span><br><span class=\'scTimeTableTodoSubject\'>{{title_r}}</span></div>\n\t\t\t\t\t\t  <div class="card-content card-content-padding">{{body}}</div>\n\t\t\t\t\t\t  {{#if footer}}\n\t\t\t\t\t\t\t<div class="card-footer">{{footer}}</div> \n\t\t\t\t\t\t  {{/if}}\n\t\t\t\t\t\t\t<div class="card-footer" >\n\t\t\t\t\t\t\t\t<table width=100%>\n\t\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t\t<td>{{from}}</td>\n\t\t\t\t\t\t\t\t\t\t<td class="scNr">\n\t\t\t\t\t\t\t\t\t\t\t<a href=\'#\'>\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\'icon f7-icons\' scTimeId={{time_id}} scPardate={{pardate}}>folder</i>\n\t\t\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t</table>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\t\t\t\t\n\t\t\t\t\t{{/each}}\n\t\t\t\t{{else}}\n\t\t\t\t\t<div class="block">\n\t\t\t\t\t\t##ttbNoEntries##\n\t\t\t\t\t</div>\n\t\t\t\t{{/js_if}}\n\t\t</div>\t\n\t'),
    ScCourseBook_showUnauthorizedStudentOutages: Template7.compile('\n\t\t\x3c!-- -------------- --\x3e\n\t\t\x3c!-- List of items \t--\x3e\n\t\t\x3c!-- --------------\t--\x3e\n\t\t<div class="list" scIndexedList>\n\t\t  <form>\n\t\t\t  <ul>\n\t\t\t\t{{#each items}}\n\t\t\t\t\t<li scPid="{{id}}" scStudentOutageId="{{studentOutageId}}" scAuthorized="0" scExceeded={{exceeded}}>\n\t\t\t\t\t\t\t<div class="item-inner">\n\t\t\t\t\t\t\t\t<label class="item-checkbox item-content">\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t</label>\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t<div class="item-title">\n\t\t\t\t\t\t\t\t\t{{#if header}}\n\t\t\t\t\t\t\t\t\t\t<div class="item-header">{{header}}</div>\n\t\t\t\t\t\t\t\t\t{{/if}}\n\t\t\t\t\t\t\t\t\t<span personname class=\'{{titleClass}}\'>\n\t\t\t\t\t\t\t\t\t{{title}}\n\t\t\t\t\t\t\t\t\t</span>\n\t\t\t\t\t\t\t\t\t<div class="item-footer">{{footer}}</div>\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t<div class=\'item-after\'>\n\t\t\t\t\t\t\t\t\t{{after}}\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t</li>\n\t\t\t\t{{/each}}\n\t\t\t  </ul>\n\t\t  </form>\n\t\t</div>\t\n\t')
});