// Map Data
const map_data = JSON.parse(data);
const max_floors = map_data.length;
let floor_index = 0;
// Declare some helpful path constants
const path_panorama = "img_placeholder/p_";
const path_floor = "img_placeholder/flr_";
const img_end = ".png";
// Image Sources
const src_point = "img_placeholder/point.png";
const src_point_selected = "img_placeholder/point_selected.png";
const src_loading_panorama = "img_placeholder/z_panorama.png";
// Node References
const panorama = document.getElementById("panorama");
const floor_plan_frame = document.getElementById("floor_plan_frame");
const map = document.getElementById("floor_plan");
let point_selected = null;
let room_points = [];

// Initialization for the app.
function Init() {
	// Hook up buttons.
	document.getElementById("button_floor_up").addEventListener("click", function(){
		ChangeFloor(1);
	});
	document.getElementById("button_floor_down").addEventListener("click", function(){
		ChangeFloor(-1);
	});
	// Load the default floor.
	LoadFloor(0);
}

// Event called to display a room in the panorama
function DisplayRoom(key, point) {
	// Unselect previous point.
	if (point_selected != null) {
		point_selected.src = src_point;
	}
	// Select new point.
	point_selected = point;
	point_selected.src = src_point_selected;
	// Show room
	panorama.src = path_panorama + key + img_end;
}

// Creates a room on the map from the given parameters.
function CreateRoom(floor, room, x, y) {
	// Create a point on the map.
	var img = document.createElement("img");
	img.setAttribute("src", src_point);
	img.setAttribute("class", "point");
	img.style.top = (x * 100).toString() + '%';
	img.style.left = (y * 100).toString() + '%';
	floor_plan_frame.appendChild(img);
	room_points.push(img);
	
	// Attach an event listener.
	img.addEventListener("click", function(){
		DisplayRoom(floor.toString() + '_' + room.toString(), img);
	});
}

// Load a floor from the json data.
function LoadFloor() {
	// Clear room points.
	for (let i = 0; i < room_points.length; i++) {
		room_points[i].remove();
	}
	
	// Place markers on floor.
	var floor = map_data[floor_index];
	var rooms = floor.rooms;
	
	for (let i = 0; i < rooms.length; i++) {
		CreateRoom(floor_index, i, rooms[i].coordinates.x, rooms[i].coordinates.y);
	}
	
	// Clear panorama
	panorama.src = src_loading_panorama;
	
	// Set the map
	map.src = path_floor + floor_index.toString() + img_end;
}

// Moving from floor to floor.
function ChangeFloor(sign) {
	var is_changed = false;
	// Move up
	if (sign == 1 && floor_index < max_floors) {
		floor_index = floor_index + 1;
		is_changed = true;
	}
	// Move down
	if (sign == -1 && floor_index > 0) {
		floor_index = floor_index - 1;
		is_changed = true;
	}
	
	if (is_changed) {
		LoadFloor();
	}
}

Init();