function viewPDB(uri, element){
// let uri = 'http://www.cathdb.info/version/current/api/rest/id/2c7wA00.pdb';
jQuery.ajax( {type: "GET",url:uri} )
  .done(function(data) {
  	// let element = divid;
  	let config = { backgroundColor: 'white' };
  	let viewer = $3Dmol.createViewer( element, config );
          let m = viewer.addModel( data, "pdb" );
           viewer.setViewStyle({style:"outline"});
          viewer.setStyle( {}, {cartoon: {"color":"spectrum",style:"edged"}} );
          viewer.zoomTo();
          viewer.render();
          console.dir(data);
  })
  .fail(function(hdr, status, err) {
  	msg = "3DView:Failed to load PDB " + uri + ": " + err;
  	console.error( msg );
  	element.text(msg);
  	viewer.setBackgroundColor('grey');
  	// console.log(getpdb.getAllResponseHeaders());
  	console.dir(hdr);// alert(request.getResponseHeader('some_he'));
  });
};


$(document).ready(function(){	
    $(".btn-primary").click(function(){
    	// var id =c

    	$($(this).attr("target")).collapse("toggle");
	    // viewPDB( $(".btn-primary").attr("pdb-url") );
		});

    $('.collapse').on('shown.bs.collapse', function () {
		// console.error('function here');
		var uri = $(this).attr("pdb-url");
		var divid = $(this).find("#container");

		viewPDB( uri , divid);
	});    
});

