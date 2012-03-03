var favorites = {};

favorites.init = function(){
	jq('#favorite-button').hover(function(){
		jq(this).find('img').toggle();
	})
}

jq(document).ready(favorites.init);