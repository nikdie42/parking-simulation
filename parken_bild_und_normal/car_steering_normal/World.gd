extends Node2D

var client
var server
var client_id
var car_data
export var deltaN = 0.001
var action_pressed = InputEventAction.new()
var action = InputEventAction.new()
var testa = false
#func _ready():
#	set_camera_limits()

func set_camera_limits():
	var map_limits = $TileMap.get_used_rect()
	var map_cellsize = $TileMap.cell_size
	$CarTest/Camera2D.limit_left = map_limits.position.x * map_cellsize.x
	$CarTest/Camera2D.limit_top = map_limits.position.y * map_cellsize.y
	$CarTest/Camera2D.limit_right = map_limits.end.x * map_cellsize.x
	$CarTest/Camera2D.limit_bottom = map_limits.end.y * map_cellsize.y

# The port we will listen to.
const PORT = 9080
# Our WebSocketServer instance.
var _server = WebSocketServer.new()

func _ready():
	# Connect base signals to get notified of new client connections,
	# disconnections, and disconnect requests.
	_server.connect("client_connected", self, "_connected")
	_server.connect("client_disconnected", self, "_disconnected")
	_server.connect("client_close_request", self, "_close_request")
	# This signal is emitted when not using the Multiplayer API every time a
	# full packet is received.
	# Alternatively, you could check get_peer(PEER_ID).get_available_packets()
	# in a loop for each connected peer.
	_server.connect("data_received", self, "_on_data")
	# Start listening on the given port.
	var err = _server.listen(PORT)
	if err != OK:
		print("Unable to start server")
		set_process(false)



func _connected(id, proto):
	print("test")
	# This is called when a new peer connects, "id" will be the assigned peer id,
	# "proto" will be the selected WebSocket sub-protocol (which is optional)
	#print("Client %d connected with protocol: %s" % [id, proto])
	client_id = id
	print("Client %d connected with protocol: %s" % [id, proto])


func _close_request(id, code, reason):
	# This is called when a client notifies that it wishes to close the connection,
	# providing a reason string and close code.
	print("Client %d disconnecting with code: %d, reason: %s" % [id, code, reason])


func _disconnected(id, was_clean = false):
	client_id = null
	# This is called when a client disconnects, "id" will be the one of the
	# disconnecting client, "was_clean" will tell you if the disconnection
	# was correctly notified by the remote peer before closing the socket.
	print("Client %d disconnected, clean: %s" % [id, str(was_clean)])


func _on_data(id):
	# Print the received packet, you MUST always use get_peer(id).get_packet to receive data,
	# and not get_packet directly when not using the MultiplayerAPI.
	for i in InputMap.get_actions():
		action_pressed = InputEventAction.new()
		action_pressed.action = i
		action_pressed.pressed = false
		Input.parse_input_event(action_pressed)
		
	var pkt = _server.get_peer(id).get_packet()
	print("Got data from client %d: %s ... echoing" % [id, pkt.get_string_from_utf8()])
	var commands = (JSON.parse(pkt.get_string_from_utf8())).get_result()
	print(commands)
	if(commands):
		for i in commands[0]:
			action = InputEventAction.new()
			action.action = i
			action.pressed = true
			Input.parse_input_event(action)
			print(action)
			testa = true
			$Car._network_process(0.01)
			car_data = get_car_data_as_utf8_JSON()
			if(client_id):
				_server.get_peer(client_id).put_packet(car_data)
#	car_data = get_car_data_as_utf8_JSON()
#	_server.get_peer(id).put_packet(car_data)
	


func _process(delta):
	# Call this in _process or _physics_process.
	#print(delta)
	#print([$Car.velocity.length()/32*3.6/deltaN,rad2deg($Car.steer_direction),$Car.score,$Car.distance_sensors])
	# Data transfer, and signals emission will only happen when calling this function.
	#time(delta)
	_server.poll()
	update()

func get_car_data_as_utf8_JSON():
	print($Car.rotation)
	var data = [$Car.car_position[0],$Car.car_position[1],$Car.velocity.length()/32*3.6,rad2deg($Car.steer_direction),$Car.score,$Car.distance_sensors2,$Car.parkpos,$Car.rotation]
	return (JSON.print(data)).to_utf8()
