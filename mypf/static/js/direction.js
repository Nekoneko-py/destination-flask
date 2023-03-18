function initMap() {
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: { lat: 35.686524724837966, lng: 139.7630477265107 },
  });
  directionsRenderer.setMap(map);
  addEventListener("load", () => {
      calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
  }

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  const waypts = [];
  

  for (let i = 0; i < destinations.length; i++) {
    {
      waypts.push({
        location: destinations[i],
        stopover: true,
      });
    }
  }
  
  directionsService
    .route({
      origin: start,
      destination: end,
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode[mode]})
    .then((response) => {
      directionsRenderer.setDirections(response);

      const route = response.routes[0];
      const summaryPanel = document.getElementById("directions-panel");

      summaryPanel.innerHTML = "";
      const distance_list = []
      const duration_list = []

      // For each route, display summary information.
      for (let i = 0; i < route.legs.length; i++) {
        const routeSegment = i + 1;
        const distance = route.legs[i].distance.text
        const duration = route.legs[i].duration.text

        summaryPanel.innerHTML +=
          "<b>移動区間: " + routeSegment + "</b><br>";
        summaryPanel.innerHTML += route.legs[i].start_address + " to ";
        summaryPanel.innerHTML += route.legs[i].end_address + "<br>";
        summaryPanel.innerHTML += "<b>区間移動距離:</b>" + distance + "<br>";
        summaryPanel.innerHTML += "<b>所要時間:</b>" + duration + "<br><br>";
        distance_list.push(Number(route.legs[i].distance.value))
        duration_list.push(Number(route.legs[i].duration.value))
        
      };
      const distance_sum_meter = distance_list.reduce(function(sum,element){
        return sum + element;
      },0);
      const distance_sum_kilometer = distance_sum_meter / 1000;
      const duration_sum_sec = duration_list.reduce(function(sum,element){
        return sum + element;
      },0);
      const duration_sum_hour = Math.floor(duration_sum_sec / 3600);
      const duration_sum_min = Math.floor(duration_sum_sec % 3600 / 60);
      summaryPanel.innerHTML += "<b>総移動距離:</b>" + distance_sum_kilometer.toFixed(1) + '<b>km : </b>' ;
      summaryPanel.innerHTML += "<b>総移動時間:</b>" + duration_sum_hour + '<b>時間</b>' + duration_sum_min + '<b>分</b>'; 
    })
    .catch((e) => window.alert("次の理由により、ルート リクエストに失敗しました: " + status));
  }
  


window.initMap = initMap;
