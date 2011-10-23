(function($){
	
	var maincont;
	
	$(document).ready(function(){
				
		maincont = $('#main-container');
		
		loginForm();

		console.log('herro ready', maincont);

		
	});
	
	function loginForm(){
		if ( $('#login-cont').length ) {
			
			var form = $('#login-cont').find('form'),
				uname = form.find('[name="dummy_name"]'),
				pass = form.find('[name="password"]'),
				errorCont = form.find('.login-error');
			
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
					
					errorCont.html( data ).show();
					
				});
				
			});
			
		}
	}
	
	
})(jQuery)
