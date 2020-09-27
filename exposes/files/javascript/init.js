// +++++++++++++++++++++++++++++++++
// DOM7
// +++++++++++++++++++++++++++++++++
let $$ = Dom7;
// +++++++++++++++++++++++++++++++++
// ROUTES
// +++++++++++++++++++++++++++++++++

let scRoutes = [{
    path: '/',
    content: '<div id="view-home" class="view view-main tab tab-active">' + document.getElementById("view-home").innerHTML + '</div>'
},
    // Default rout for queries
    {
        path: '/query/:scId/:scContentId/:title',
        async: function (routeTo, routeFrom, resolve, reject) {
            ScDebug.out(routeTo.params)
            resolve({
                template: $("#scBasicPageTemplate").html()
            }, {
                context: {
                    scId: routeTo.params.scId,
                    scContentId: routeTo.params.scContentId,
                    title: routeTo.params.title
                },
            })
        }
    }
];


// +++++++++++++++++++++++++++++++++
// The App
// +++++++++++++++++++++++++++++++++

// Framework7 App main instance
// default theme for desktop is ios
if (scGlobals.device.type == "desktop") scGlobals.layout.theme_f7 = 'ios'
let scApp = {
    f7: new Framework7({
        root: '#app', // App root element
        id: 'com.scoosoft.scooso', // App bundle ID
        name: 'Scooso', // App name
        theme: scGlobals.layout.theme_f7,
        routes: scRoutes, // App routes
        lng: "de",
        iosTranslucentBars: false,
        touch: {
            // Enable fast clicks
            fastClicks: true
        },
        picker: {
            toolbarCloseText: scStr["corDone"]
        },
        input: {
            //scrollIntoViewOnFocus: true,
            scrollIntoViewCentered: true
        },
        actions: {
            forceToPopover: true
        }
    }),
    dialogs: new ScDialogs(),
    modules: new ScModules(),
    templates: {},
    actions: {},
    flags: {
        // only phone - mode
        transitionRunning: false,
        mountingRunning: false
    }
}
// Init/Create views
let homeView = scApp.f7.views.create('#view-home', {
    url: '/',
    stackPages: true, // muy importante for scooso!!!
    allowDuplicateUrls: true // muy importante for scooso!!!
});
/*
	let settingsView = scApp.f7.views.create('#view-settings', {
	  url: '/settings/'
	});
*/


// +++++++++++++++++++++++++++++
// Layout
// +++++++++++++++++++++++++++++
// enlarge icons
if (scApp.f7.theme == "ios") {
    $$(".icon").css("font-size", "30px");
    $$(".icon").css("line-height", "1.5");
} else {
    $$(".icon").css("line-height", "1.5");
}

// define function with function
// http://jsben.ch/D2xTG


// +++++++++++++++++++++++++++++
// Events
// +++++++++++++++++++++++++++++
$(document).on('touchstart', function (event) { //used ???
    let xPos = event.originalEvent.touches[0].pageX;
});


// --------------
// jsPanel
// --------------
// remove jspanel Dialog
$(document).on('jspanelclosed', function (event) {
    scApp.dialogs.remove(event.detail)
});

// --------------
// framework7
// --------------
//Event will be triggered right before page is going to be transitioned out of view

// is no realized with ScCore.clearHTML by pressing back button

$(document).on('page:beforeout', function (event) {
    let dlgId = event.detail.$el.attr("id")
    /*
    console.log(scApp.flags.mountingRunning)
    console.log(scApp.dialogs.dialogOrder)
    console.log(event.detail.$el.attr("id"))
    */
    // delete all content before swipe out to improve rendering
    if (!scApp.flags.mountingRunning)
        $(event.target).find(".page-content").html("")
});

$(document).on('page:mounted', function (event) {
    scApp.flags.mountingRunning = true
});

// remove f7-page Dialog
// Event will be triggered after page transitioned out of view
$(document).on('page:beforeremove', function (event) {
    scApp.dialogs.remove(event.detail.$el.attr("id"))
    ScDebug.out("afterout:", event)
    ScCore.afterOut(event)
});

$(document).on('routeChanged', function (event) {
    console.log("routeChanged")
});

//$$(document).on('page:init', '.page[data-name="about"]', function (e) {
$$(document).on('page:afterin', function (event) {
    ScDebug.out("afterin")

    let dlgId = event.detail.$el.attr("id")
    if (ScCore.isset(scApp.dialogs.dialogs[dlgId])) {
        scApp.dialogs.dialogs[dlgId].addContents()
    }

    // working through queue, if more than one dialog is added
    scApp.dialogs.addDialogs()
    ScCore.icons2Unicode()
    scApp.flags.mountingRunning = false
})


// ++++++++++++++++++++++++++++
// basic content templates
// ++++++++++++++++++++++++++++

$.extend(scApp.templates, {
        "corList": // linked:true for linked list
            Template7.compile(`
		{{#if count}}<div class="block">##corEntries##: {{count}}</div>{{//if}}	
			<div class="list {{#if linked}}links-list{{else}}simple-list{{/if}}">
			  <form>
				  <ul>
					{{#each items}}
						<li>
							{{#if @root.linked}}<a href="#" scItemId="{{itemId}}" scItemType="{{type}}">{{/if}}
								{{text}} 
							{{#if @root.linked}}</a>{{/if}}
						</li>
					{{/each}}
				  </ul>
			  </form>
			</div>	
		`)
    }, {
        "corComplexList": // linked:true for linked list, TODO: checkboxes not working, when linked
            Template7.compile(`
		{{#if searchbar}}
			<div class="scSticky">
				<form class="searchbar " id="{{scId}}_searchbar">
					<div class="searchbar-inner">
						<div class="searchbar-input-wrap">
							<input type="search" placeholder="">
							<i class="searchbar-icon"></i>
							<span class="input-clear-button"></span>
						</div>
						<!-- <span class="searchbar-disable-button if-not--aurora">Abbrechen</span> -->
					</div>
				</form>
			</div>
		{{/if}}
		<div class="block {{#if noMarginTop}} scBlockNoMarginTop {{/if}} ">
		

		
		
		
		{{#if title}}
		<b>{{title}}</b>
		{{/if}}
		<!-- not working properly -->
		<!-- {{#if text}}<br>{{text}}{{//if}}	-->
			
			<!-- -------------------------	-->
			<!-- display number of entries 	-->
			<!-- -------------------------	-->

			{{#if count}}
				{{#js_if "this.count==1"}}
					<br>{{itemName1}}
				{{else}}
					{{#js_if "this.count==0"}}
						<br>{{noItems}}
					{{else}}
						<br>{{count}} {{itemName}}
					{{/js_if}}
				{{/js_if}}
				
			{{//if}}
		</div>

		
		
		<!-- -------------- -->
		<!-- List of items 	-->
		<!-- --------------	-->
		
		<div class="list" scIndexedList>
		  <form>
              {{#if listGroup}}
			    <div class="list-group" >	
			  {{/if}}
			  
			  <ul>
				<!-- Select all -->
				{{#if selectAll}}
					{{#js_if "this.count>0"}}

						<li>
							<div class="item-inner">
								<label class="item-checkbox item-content">
									<input type="checkbox" scTemplateCheckboxSelectAll>
									<i class="icon icon-checkbox"></i>
								</label>
								<div class="item-title">
								{{selectAll}}
								</div>
											<div class="item-after">
												{{after}}
											</div>
							</div>
						</li>
					{{/js_if}}
				{{/if}}
				{{#each items}}
					{{#if listGroup}}
						{{#js_if "@index>0"}}
							</ul>
							</div>
							<div class="list-group">
							<ul>
						{{/js_if}}
						<li class="list-group-title">{{listGroup}}</li>
					
					{{else}}
						<li scItemId="{{id}}" scItemType="{{type}}" scPars="{{pars}}">
							{{#if linked}}
								<a class="item-link item-content">
							{{/if}}
							
							
									<div class="item-inner">
									
										<label class="item-checkbox item-content">
											{{#if inputName}}
												<input name="{{inputName}}" type="checkbox" {{checked}}>
												<i class="icon icon-checkbox"></i>
											{{/if}}
											{{#if image}}
												<img class="lazy scImageInList scInvisible" data-src="{{image}}" >
											{{/if}}
											
										</label>
										
										<div class="item-title">
											{{#if header}}
												<div class="item-header">{{header}}</div>
											{{/if}}
											{{#if titleClass }}<span class="{{titleClass}}">{{/if}}
											{{title}}
											{{#if titleClass }}</span>{{/if}}
											{{#if footer}}
												<div class="item-footer">{{footer}}</div>									
											{{/if}}
											
										</div>
										<div class="item-after">
											{{after}}
										</div>
									</div>
							{{#if linked}}
								</a>
							{{/if}}
						</li>
					{{/if}}
				{{/each}}
			  </ul>
              {{#if listGroup}}
			    </div>	
			  {{/if}}
			  
		  </form>
		</div>	
		
		`)
    },

    {
        "corInputList": Template7.compile(`
			<div class="list">
			  <form>
				  <ul>
					{{#each items}}
						<li>
						  <div class="item-content item-input">
							<div class="item-inner">
							  <!-- <div class="item-title item-label"></div> -->
							  <div class="item-input-wrap">
								<input type="{{type}}" name="{{name}}" placeholder="{{placeholder}}" class="no-fastclick" value="{{value}}"/>
							  </div>
							</div>
						  </div>
						</li>
					{{/each}}
				  </ul>
			  </form>
			</div>	
			<div class="block">
				{{#each buttons}}
					<p>
						<button class="button {{addClass}}" scid="{{scid}}">{{text}}</button>
					</p>
				{{/each}}
			</div>
		`)
    }, {
        "corFileList": Template7.compile(`
			<div class="list no-hairlines">
			  <ul>
				{{#each items}}
					<li>
					  <div class="item-content">
						<div class="item-inner">
						  <div class="item-title">{{filename}}</div> 
						  <div class="item-after"><i class="icon f7-icons" >trash</i></div>
						</div>
					  </div>
					</li>
				{{/each}}
			  </ul>
			</div>	
		`)
    }, {
        "corInstructionList": Template7.compile(`
			<div class="block">
			<p>
				  <ul>
						{{#each lines}}
							<li>
								{{text}}
							</li>
						{{/each}}
				  </ul>
			</p>
			</div>
			
		`)
    }, {
        "corInstruction": Template7.compile(`
			<div class="block">
				<p>{{text}}</p>
			</div>
			
		`)
    }, {
        "corMainMenu": Template7.compile(`	<div>
								{{> "menu"}}
								<div class="block">Scooso 2019 by <a scTypeExternalLink href=\'https://www.scoosoft.com\' class="link external" target="_blank">ScooSoft</a></div>
							</div>
		`)
    }, {
        "corSearchBar": Template7.compile(`
			<form class="searchbar">
			  <div class="searchbar-inner">
				<div class="searchbar-input-wrap">
				  <input type="search" name="{{name}}" placeholder="{{placeholder}}">
				  <i class="searchbar-icon"></i>
				  <span class="input-clear-button"></span>
				</div>
				<span class="searchbar-disable-button">Cancel</span>
			  </div>
			</form>	
			
		`)
    }, {
        "corTable": Template7.compile(`
			<div  class="data-table">
			<table id={{id}} class="display" style="width:100%">
				<thead>
					<tr>
						{{#if @root.rowCount}}
							<td class=scNr>#</td>
						{{/if}}
						{{#header}}
							<th>{{this}}</th>
						{{/header}}
					</tr>
				</thead>
				<tbody>
				{{#rows}}
					<tr>
						{{#if @root.rowCount}}
							<td class=scNr>{{@index+1}}</td>
						{{/if}}
						{{#cols}}
							<td class="label-cell {{class}}-cell {{scClass}}" scItemId='{{formid}}' scTokenId='{{formtoken}}'>{{label}}</td>
						{{/cols}}
					</tr>
				{{/rows}}
				</tbody>
			</table>
			</div>
		`)
    }
)

Template7.registerPartial(
    'menu',
    `
	<div class="list no-hairlines">
		<ul>
			{{#each menu}}
				<li class="accordion-item no-fastclick">
				{{#if menu}}
					<a href="#" class="item-content item-link">
						<div class="item-inner">
						  <div class="item-title">{{text}}</div>
						</div>
					</a>
					<div class="accordion-item-content">
						<div class="block">
							{{> "menu"}}
						</div>
					</div>
				{{else}}
					<div class="block item-content">
						<div class="scMenuItem" scModule="{{module}}" scFunc="{{func}}" scParams="{{params}}">{{text}}</div>
					</div>
				{{/if}}
				</li>
			{{/each}}
		</ul>
	</div>
	`
);

// +++++++++++++++++++++++++++++
// Start (annoying javafx)
// Start (annoying javafx)
// +++++++++++++++++++++++++++++
$(document).ready(function () {


    ScDebug.out("Starting Scooso");
    ScCore.icons2Unicode()
    $.ajaxSetup({
        url: scGlobals.connection.path2PHP,
        global: false,
        dataType: "json",
        type: scGlobals.connection.ajaxType,
        timeout: scGlobals.connection.timeout,
    });


    function start() {

        // transition back workaround
        document.documentElement.style.setProperty("--f7-page-transition-duration", "150ms");
        if (ScCore.exGetAppSettings().waitForApp) {
            setTimeout(function () {
                start()
            }, 200);
        } else {
            // will be done by timer
            //ScCore.exSendDeviceToken()
            // Here is, where app starts functionality

            //ScCore.exCallNumber("01715278848")
            //ScCore.exOpenUrl("http://www.scoosoft.com")
            //ScCore.exOpenMail("bk@bernd-kneib.de")
            //ScCore.exShowCoords("50.3332864","7.6971167",1000,"Wolfi")
            //setTimeout(function(){ScCore.exUpdateApp(true)},4000);

            // Default Entry for login
            /*
            $("#scMainMenuContent").html(ScCore.template("corMainMenu",{
            	menu:[
            		{
            			"textT": 	"mitLogin",
            			"module":	"ScPrivate",
            			"func":		"login"
            		}
            	]
            }))
            */
            if (ScCore.isset(ScCore.exGetAppSettings().appName)) {
                $("#scWebAppName").html(ScCore.exGetAppSettings().appName)
            } else {
                $("#scWebAppName").html(scGlobals.client.fullname)
            }

            $("#scMainMenuContent").html(`<div>
					<div class="list no-hairlines">
						<ul>
							
								<li class="accordion-item no-fastclick">
								
									<div class="block item-content">
										<div class="scMenuItem" scmodule="ScPrivate" scfunc="login" scparams="">Login</div>
									</div>
								
								</li>
						</ul>
					</div>
	
					<div class="block">Scooso 2020 by <a sctypeexternallink="" href="https://www.scoosoft.com" class="link external" target="_blank">ScooSoft</a></div>
				</div>`)
            ScCore.addMenuEvents()

            if (scGlobals.start.action > 0) {
                // TODO: read action from DB
                /*
                ScCore.moduleFunc({
                	module: "ScForms",
                	func: 	"showForm",
                	params:	{
                				id:			1
                	}
                })
                */
            } else {
                ScCore.exScoosoIsRunning()

                ScCore.exAutoLogin({
                    // autologin failed, this happens also in "without app" mode
                    fail: function () {
                        ScCore.loadMenu()
                        ScCore.loadNameFile()
                        ScCore.openDefaultDialogs()
                    },
                    success: function () {
                    }
                })
            }
        }


    }

    start()

});