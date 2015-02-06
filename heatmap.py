from facepy import GraphAPI
import webbrowser


# Initialize the Graph API with a valid access token.  
#Generate access token here: https://developers.facebook.com/tools/explorer/. Make sure you choose the API version 1.0
oauth_access_token = 'Enter access token here'  
graph = GraphAPI(oauth_access_token)

#Will be used to launch a web browser and view the output
filepath = 'file:///FBHeatMap.html'

#Initialise a list to store the locations of friends.
myLocations=[]

#A string to hold the JS array  arguments that will be used later to create the heatmap.
htmlCoords=""
#Fetch the locations using FQL
locations=graph.fql('SELECT uid,current_location FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())')
for friend in locations['data']:
    if friend['current_location'] is not None:
        if friend['current_location']['name'] in myLocations:
            pass
        else:
            city=friend['current_location']['name']
            myLocations.append(city)
            lat=friend['current_location']['latitude']
            lon=friend['current_location']['longitude']
            #Format of JS: new google.maps.LatLng(X,X)
            htmlCoords+='new google.maps.LatLng('+str(lat)+","+str(lon)+"),"

#To remove the last comma which gets added by iteration of the previous statement.        
jsInput = htmlCoords[:-1]

#Create the HTML file
outputFile = open('FBHeatMap.html','w')
message="""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Heatmap</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
      #panel {
        position: absolute;
        top: 5px;
        left: 50%;
        margin-left: -180px;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
    <script>

    var map, pointarray, heatmap;

    var taxiData = ["""+jsInput+"""
  
    ];

    function initialize() {
      var mapOptions = {
        zoom: 2,
        center: new google.maps.LatLng(0,0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

     map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

      var pointArray = new google.maps.MVCArray(taxiData);

      heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
      });

  heatmap.setMap(map);
    }

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>

  <body>
    <div id="panel">
      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
       <button onclick="toggleHeatmap()">Toggle Heatmap</button>
      <button onclick="changeGradient()">Change gradient</button>
      <button onclick="changeRadius()">Change radius</button>
      <button onclick="changeOpacity()">Change opacity</button>
    </div>
    <div id="map-canvas"></div>
  </body>
</html>"""
outputFile.write(message)
outputFile.close()

#Launch a browser to view the results
webbrowser.open(filepath)




  
