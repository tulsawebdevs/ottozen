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
				//make a confirm button
				me.printConfirmBttn();
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
		me.printConfirmBttn = function(){
			if ( !me.confirmBttn ) {
				me.confirmBttn = $('<button />', { id: 'add_commute_confirm', text: 'Route is correct' })
					.click(me.confirmClick)
					.insertBefore( me.cont );
			} else {
				me.confirmBttn.show();
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
