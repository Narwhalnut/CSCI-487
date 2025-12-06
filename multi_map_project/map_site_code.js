// Map Data
const map_data = JSON.parse(data);
const max_floors = map_data.length;
let floor_index = 0;
// Declare some helpful path constants
const path_panorama = "/p_";
const path_floor = "img/flr_";
const path_floor_map = "/map.png";
const img_end = ".png";
const img_end_jpg = ".JPG";
// Image Sources
const src_point = "img/point.JPG";
const src_point_selected = "img/point_selected.JPG";
const src_loading_panorama = "img/loading_panorama.JPG";
const src_door = "img/door.png";
// Node References
const panorama = document.getElementById("panorama");
const floor_plan_frame = document.getElementById("floor_plan_frame");
const panorama_frame = document.getElementById("panorama_frame");
const map = document.getElementById("floor_plan");
const text_data = document.getElementById("text_data");
let point_selected = null;
let rooms = [];
let door_points = [];

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
	floor_index = 1;
	LoadFloor();
}

// Holds all data associated with a room in the given map.
class Room {
	constructor(index,x,y) {
		this.point = null;
		this.index = index;
		this.x = x;
		this.y = y;
		this.doors = [];
		
		this.CreateOnMap();
	}
	
	CreateOnMap() {
		// Create a point on the map.
		this.point = document.createElement("img");
		this.point.setAttribute("src", src_point);
		this.point.setAttribute("class", "point room_point");
		this.point.style.top = (this.y * 100).toString() + '%';
		this.point.style.left = (this.x * 100).toString() + '%';
		floor_plan_frame.appendChild(this.point);
		
		let room_index = this.index;
		// Attach an event listener.
		this.point.addEventListener("click", function(){
			DisplayRoom(room_index);
		});
	}
	
	SetDoors(arr) {
		this.doors = arr;
	}
	
	HasDoors() {
		return (this.doors.length > 0);
	}
	
	Remove() {
		this.point.remove();
	}
	
	Display() {
		// Show room in the panorama
		let path = path_floor + floor_index.toString() + path_panorama + this.index.toString() + img_end_jpg;
		panorama.src = path;
		/*pannellum.viewer('panorama', {
			"type": "equirectangular",
			"panorama": path,
			"autoLoad": true,
			"compass": true,
			"northOffset": 135,
			"yaw": 225
		});*/
		
		// Show Doors
		ClearDoors()
		if (this.HasDoors()) {
			for (let i = 0; i < this.doors.length; i++) {
				// Find the angle of this room to the target room.
				let xx = rooms[this.doors[i]].x - this.x;
				let yy = rooms[this.doors[i]].y - this.y;
				let angle = GetAngleFromVector(xx,yy);
				// Create a door to the target room.
				CreateDoor(angle, rooms[this.doors[i]]);
			}
		}
		
		text_data.textContent = "Room ID: " + this.index;
	}
}

// Event called to display a room in the panorama
function DisplayRoom(room_index) {
	// Unselect previous point
	if (point_selected != null) {
		point_selected.src = src_point;
	}
	// Find the new point of this room.
	point_selected = rooms[room_index].point;
	// Mark it as selected.
	point_selected.src = src_point_selected;
	
	rooms[room_index].Display();
}

// Puts a door in the panoramic frame.
function CreateDoor(angle, room) {
	var img = document.createElement("img");
	img.setAttribute("src", src_door);
	img.setAttribute("class", "point door_point");
	img.style.top = '66%';
	img.style.left = (angle * 100).toString() + '%';
	panorama_frame.appendChild(img);
	door_points.push(img);
	
	// Attach an event listener.
	img.addEventListener("click", function(){
		DisplayRoom(room.index);
	});
}

// Create door points.
function ClearDoors() {
	// Clear door points.
	for (let i = 0; i < door_points.length; i++) {
		door_points[i].remove();
	}
}

// Load a floor from the json data.
function LoadFloor() {
	// Clear room points.
	ClearDoors()
	for (let i = 0; i < rooms.length; i++) {
		if (rooms[i] != null) {
			rooms[i].Remove();
		}
	}
	rooms.length = 0;
	
	// Place markers on floor.
	var floor = map_data[floor_index];
	var room_data = floor.rooms;
	
	for (let i = 0; i < room_data.length; i++) {
		if ("hidden" in room_data[i]) {
			rooms.push(null);
			continue;
		}
		rooms.push( new Room(i, room_data[i].pos.x, room_data[i].pos.y) );
		if ("doors" in room_data[i]) {
			rooms[i].SetDoors(room_data[i].doors);
		}
	}
	
	// Set the map
	map.src = path_floor + floor_index.toString() + path_floor_map;
}

// Moving from floor to floor.
function ChangeFloor(sign) {
	var is_changed = false;
	// Move up
	if (sign == 1 && floor_index < max_floors - 1) {
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

// Get an angle from 0 to 1
function GetAngleFromVector(x,y) {
    var angle = Math.atan2(y, x);
    angle = (angle / (2.0 * Math.PI)) + 0.45;
	if (angle < 0.1) {
		angle = angle + 1.0;
	}
	return angle;
}

Init();