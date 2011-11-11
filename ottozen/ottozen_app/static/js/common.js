(function($){
	
	var maincont,
		oMap = null;
	
	$(document).ready(function(){
				
		maincont = $('#main-container');
		
		loginForm();

		if ( $('#gmapCont').length ) {
			oMap = new ottoMap();
		}

		console.log('herro ready', maincont, oMap);

	});
	
	function loginForm(){
		if ( $('#login-cont').length ) {
			
			var form = $('#login-cont').find('form'),
				uname = form.find('[name="dummy_name"]'),
				pass = form.find('[name="password"]'),
				errorCont = form.find('.login_error');
			
			form.submit(function(e){
				
				e.preventDefault();
				
				//hide the arror alert if it is showing.
				errorCont.hide();
				
				var jqxhr = $.post( form.attr('action'), form.serialize(), function(data, status){
					
					console.log('login post', data, status);
					
					//do stuff
					window.location.href = window.location.href + 'myroutes';
				}).error(function(data){
					
					console.log('login error');
					
					errorCont.html(data.responseText).show();
					
				});
				
			});
			
		}
	}
	
	
	function ottoMap(config){
		//default configurable variables
		var me = this,
			defaults = {
				zoom: 11,
				centerLat: 36.151737,
				centerLng: -95.990295,
				mapsApiUrl: 'http://maps.googleapis.com/maps/api/js?sensor=false',
				contId: 'gmapCont',
				mapTypeId: 'ROADMAP'
			};
		for (var key in config) {
			defaults[key] = config[key] || defaults[key];
		}
		for (var key in defaults) {
			me[key] = defaults[key];
		}
		//constants
		me.infowindow = new google.maps.InfoWindow();
		me.directionsService = new google.maps.DirectionsService();
		//me.directionsDisplay = new google.maps.DirectionsRenderer({ suppressMarkers: true });
		me.directionsDisplay = new google.maps.DirectionsRenderer();
		//keep that map out of it for now.
		me.directionsDisplay.setMap( null );
		me.center;
		me.cont;
		me.map;
		me.form;
		me.startAddy = '';
		me.endAddy = '';
		me.currentRoute = null;
		me.confirmBttn;
		me.waypoints = [];
		me.dblclickListener;

		me.init = function(){
			//console.log('herro init', me, 'google', google);
			//configure form and handlers
			me.configureForm();

			//find the container
			me.cont = document.getElementById( me.contId );
			//console.log('container', me.cont, $(me.cont) );
			//set the google center
			me.center = new google.maps.LatLng( me.centerLat, me.centerLng );
			//get the map
			me.map = new google.maps.Map( me.cont, {
				center: me.center,
				zoom: me.zoom,
				mapTypeId: google.maps.MapTypeId[ me.mapTypeId ]
			});
            me.loadTrifIncidents();
			//add a dblclick listener to deal with way points
			google.maps.event.addListener( me.map, 'dblclick', me.mapDoubleClick, false );
			};
			me.mapDoubleClick = function(e){
			//console.log('mapDblClick', e);
			//make sure route is rendered
			if ( me.currentRoute ) {

				//me.waypoints.push( new google.maps.LatLng( e.latLng.Ma, e.latLng.Na ) );
				me.waypoints.push( { location: e.latLng, stopover: false } );

				me.getRoute();

				//console.log( 'current route & waypoint:', me.currentRoute, me.waypoints );
			}
		};
        // From http://anentropic.wordpress.com/2009/06/25/javascript-iso8601-parser-and-pretty-dates/
        me.parseISO8601 = function(str) {
            // we assume str is a UTC date ending in 'Z'

            var parts = str.split('T'),
            dateParts = parts[0].split('-'),
            timeParts = parts[1].split('Z'),
            timeSubParts = timeParts[0].split(':'),
            timeSecParts = timeSubParts[2].split('.'),
            timeHours = Number(timeSubParts[0]),
            _date = new Date;

            _date.setUTCFullYear(Number(dateParts[0]));
            _date.setUTCMonth(Number(dateParts[1])-1);
            _date.setUTCDate(Number(dateParts[2]));
            _date.setUTCHours(Number(timeHours));
            _date.setUTCMinutes(Number(timeSubParts[1]));
            _date.setUTCSeconds(Number(timeSecParts[0]));
            if (timeSecParts[1]) _date.setUTCMilliseconds(Number(timeSecParts[1]));

            // by using setUTC methods the date has already been converted to local time(?)
            return _date;
        }
        me.drawTrifPins = function(data){
            alerts = data.alerts;
            var open_infowindow;
            for(a in alerts){
                var position = new google.maps.LatLng(alerts[a].geo.latitude, alerts[a].geo.longitude);
                var icon;
                if(alerts[a].type === 'closure'){
                    icon = 'https://maps.google.com/mapfiles/ms/icons/red.png';
                }else if(alerts[a].type === 'incident'){
                    icon = 'https://maps.google.com/mapfiles/ms/icons/yellow.png';
                }
                var marker = new google.maps.Marker({
                    position: position,
                    map: me.map,
                    title: alerts[a].title,
                    icon: icon
                });

                d = me.parseISO8601(alerts[a].start);
                start = d.toLocaleDateString() + " " +d.toLocaleTimeString();

                info_content = '<dl>' +
                    '<dt>Title</dt><dd>' + alerts[a].title + '</dd>' +
                    '<dt>Description</dt><dd>' + alerts[a].description + '</dd>' +
                    '<dt>Type</dt><dd>' + alerts[a].type + '</dd>' +
                    '<dt>Category</dt><dd>' + alerts[a].category + '</dd>' +
                    '<dt>Started</dt><dd>' + start + '</dd>' +
                    '<dt>TRIF Details</dt><dd><a href="' + alerts[a].detail_link + '" target="trif_link">Trif</a></dd>';
                if(alerts[a].hasOwnProperty('source_link')){
                    info_content += '<dt>Source Details</dt><dd><a href="' + alerts[a].source_link + '" target="src_link">Source</a></dd>';
                }
                info_content += '</dl>';

                marker.info_window = new google.maps.InfoWindow({
                    content: info_content 
                });

                google.maps.event.addListener(marker, 'click', function(){
                    if(open_infowindow){open_infowindow.close();}
                    this.info_window.open(me.map, this);
                    open_infowindow = this.info_window;
                });
            }
        };
        me.loadTrifIncidents = function(){
            $.getJSON('http://trif.tulsawebdevs.org/alerts/incidents.jsonp?callback=?', me.drawTrifPins);
        };
		me.getRoute = function(){
			//console.log( 'me.getRoute', me.startAddy, me.endAddy, me.waypoints );
			me.directionsService.route({
				//origin: ttp.geo.userLocation,
				origin: me.startAddy,
				destination: me.endAddy,
				travelMode: google.maps.TravelMode.DRIVING,
				optimizeWaypoints: true,
				waypoints: me.waypoints
			}, me.directionsServiceCallback);
		};
		me.directionsServiceCallback = function(response, status){
			if (status == google.maps.DirectionsStatus.OK) {
				me.currentRoute = response.routes;
				//disable double click zoom when route is showing
				me.map.setOptions({ disableDoubleClickZoom: true });
				//console.log('directions gotten', response, me.currentRoute);
				//show the signup button
                $('button#signup').show();
				//display the directions on the map
				me.directionsDisplay.setMap( me.map );
				me.directionsDisplay.setDirections(response);
			} else {
				//the directions couldn't be found for some reason, most likely cause there is no route, but could be server error
				//too many waypoints?
				if ( status == 'MAX_WAYPOINTS_EXCEEDED' ) {
					me.waypoints.pop();
					alert('Sorry, but you have provided as many waypoints as we can handle');
				} else {
					alert('Something went wrong fetching the directions: ' + status);
				}
				//me.currentRoute = null;
				//me.map.setOptions({ disableDoubleClickZoom: false });
			}
		};
		me.confirmClick = function(){
			//everything is alright, so submit the form
			//console.log('confirmation clicked', me.form.serialize(), me.waypoints );
			if ( me.waypoints.length )
				me.form.find('[name="waypoints"]').val( JSON.stringify( me.waypoints ) );
               $.post(window.location.href, $('#add_commute_form').serialize())
		};
		me.configureForm = function(){
			//get that
			me.form = $('#add_commute_form');
            me.form.find('button#signup').hide();

			if ( $('#user-routes').length && $('#user-routes').find('.route').length ) {
				var routes = $('#user-routes').find('.route');
				
				var time = routes.last().attr('time');
				me.startAddy = routes.last().children().first().attr('addy');
				me.endAddy = routes.last().children().last().attr('addy');
				
				me.form.find('[name="start_address"]').val( me.startAddy );
				me.form.find('[name="end_address"]').val( me.endAddy );
				me.form.find('[name="time"]').val( time );
				console.log('ROUTES!', routes);
				
				me.getRoute();
			}
			
			//handle that
			me.form.submit(me.formSubmit);
		};
		me.formSubmit = function(e){
			e.preventDefault();
			//clear the waypoints
			me.waypoints = [];
			//hide the confirm button if it was showing
			if ( me.confirmBttn )
				me.confirmBttn.hide();
			//console.log( 'form submit', me.form.serialize() );
			//get the start and end inputs to send to google.
			me.startAddy = me.form.find('[name="start_address"]').val(),
			me.endAddy= me.form.find('[name="end_address"]').val();
			if( me.startAddy && me.endAddy )
				me.getRoute();
			//console.log( 'form submit', me.startAddy, me.endAddy );
		};
		me.init();
		return me;
	}
	
})(jQuery)
