(function($){
	
	$(document).ready(function(){
		
		console.log('herro ready');
		
		loginForm();
		
	});
	
	function loginForm(){
		if ( $('#login-cont').length ) {
			
			var form = $('#login-cont').find('form'),
				uname = form.find('[name="dummy_name"]'),
				pass = form.find('[name="password"]');
			
			form.submit(function(e){
				
				e.preventDefault();
				
				$.post( form.attr('action'), form.serialize(), function(data, status){
					
					console.log('login post', data, status);
					
					if ( status === 'success' ) {
						//do stuff
					} else {
						//error, do other stuff
					}
				});
				
			});
			
		}
	}
	
	
})(jQuery)
