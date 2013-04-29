function show_map(id, position){
  $('#' + id).gmap3({
    map:{
      options: {
        center: position,
        zoom: 15,
      }
    },
    marker: {
      latLng: position,
      options: {
        icon: new google.maps.MarkerImage("http://maps.gstatic.com/mapfiles/icon_green.png")
      },
    }
  });
}