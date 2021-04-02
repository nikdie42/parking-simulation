extends KinematicBody2D

#signal end
#signal win
var exited = 0
var parked = 0
var parkpos = [445, 674]

export var distance_sensors= []
export var distance_sensors2= []
export var car_position= []
var NUMBER_OF_SENSORS=8

var unfall = "Unfall!"
var delta2 = 0.017
var current_speed=0
onready var start_time = OS.get_ticks_msec()
var lauf = OS.get_ticks_msec()+1000
var lenken = delta2*59
var turn = 0
var max_winkel = 220
var wheel_base = 70
var steering_angle = 0.1
var engine_power = 1
var braking = -360
var max_speed_reverse = 250

var acceleration = Vector2.ZERO
var velocity = Vector2.ZERO
var steer_direction

var score = 300
var collisionTimer = 1
var scoreTimer = 1
var startposition=[]
var startvelocity=[]
var startrotation
var startscore
var startturn = 0

var exportspeed=0
var d=0

var colstep = 0
var is_score_edit = 0

var direction_degree
var offset_current=0
var offset=0
var direction = 0

func _physics_process(delta):

	acceleration = Vector2.ZERO
	get_input(delta)
	calculate_steering(delta2)
	is_parked()
	calc_distance_Sensor()
	
func _network_process(delta):
	acceleration = Vector2.ZERO
	get_input(delta)
	calculate_steering(delta2)
	calc_distance_Sensor()
	calc_direction_with_offset()
	is_parked()
	score -= 0.01

func _ready():
	set_physics_process(false)
	_physics_process(0.01)
	randomize()
	for i in range(NUMBER_OF_SENSORS):
		distance_sensors.append(0)
	startposition.append([-1100,-800,300,550])
	startposition.append([-1100,-800,1150,1500])
	rotation = rand_range(0,6.8)
	position= Vector2(rand_range(startposition[0][0],startposition[0][1]),rand_range(startposition[0][2],startposition[0][3]))
	
	startvelocity=velocity
	startrotation=rotation
	startscore = score


	
func calc_distance_Sensor():
	#var rot = 2PI/len(dist_sensors)
	#var t = Transform2D(Vector2(velocity.normalized().x,0),Vector2(0,velocity.normalized().y),Vector2(0,0))
	var t = self.global_transform
	for j in range(len(distance_sensors)):
		var rot = 2*PI/len(distance_sensors)*j#t.get_rotation()

		var i = 0
		while (!test_move(self.global_transform,i*t.rotated(rot).basis_xform(Vector2(1,0)).normalized(),false)&&i<500): #t.rotated(rot).basis_xform(Vector2(1,1))
			i = i+10

		distance_sensors[j] = i*t.rotated(rot).basis_xform(Vector2(1,0)).normalized()
		distance_sensors2[j] = distance_sensors[j].length()

	
	
func get_input(delta):
	calc_steering(delta)
	calc_acceleration(delta)
	velocity += acceleration * delta
	
	var col = move_and_collide(velocity*delta)
	if col:
		velocity = velocity.normalized()
		colstep += 1
		if (colstep % 4 == 0 || colstep == 1):
			score -= 50
	if !col:
		colstep = 0
		
	if Input.is_action_pressed("brake"):
		if velocity.length()<10:
			velocity=transform.x*0
		
func calculate_steering(delta2):
	var rear_wheel = position - transform.x * wheel_base/2.0
	var front_wheel = position + transform.x * wheel_base/2.0
	car_position=position.round()
	rear_wheel += velocity * delta2
	front_wheel += velocity.rotated(steer_direction) * delta2
	var new_heading = (front_wheel - rear_wheel).normalized()
	d = new_heading.dot(velocity.normalized())
	if d > 0:
		velocity = new_heading * velocity.length()
		direction = 1
	if d < 0:
		velocity = -new_heading * min(velocity.length(), max_speed_reverse)
		direction = -1
	if d<0:
		exportspeed=velocity.length()*-1
	else:
		exportspeed=velocity.length()
	rotation = new_heading.angle()
	
func calc_direction_with_offset():
	direction_degree=rad2deg(rotation)
	if offset_current<offset:
		offset_current=offset_current+0.01
	elif offset_current>offset:
		offset_current=offset_current-0.01
	if round(offset_current)==offset:
		offset = randi()%30-15
		offset = 0
	direction_degree=direction_degree+offset_current

	
func calc_acceleration(delta):
	if Input.is_action_pressed("accelerate"):
		print("accelerate")
		current_speed = sqrt(pow(velocity[0],2)+pow(velocity[1],2))/32
		acceleration= transform.x * (0.0001*pow(current_speed,3)-0.0093*pow(current_speed,2)+0.0802*current_speed+7.0157)
		acceleration=acceleration*32*engine_power
	if Input.is_action_pressed("reverse"):
		acceleration = transform.x * (braking * engine_power)
	if lauf<OS.get_ticks_msec():
		lauf += 1000
		print("Elapsed time: ", OS.get_ticks_msec() - start_time)
		print(rotation)
	if Input.is_action_pressed("brake"):
		if d > 0:
			acceleration = transform.x * (braking * engine_power)
		if d < 0:
			acceleration = transform.x * (-braking * engine_power)
	if Input.is_action_pressed("reset1") or Input.is_action_pressed("reset2"):
		print("resetting")
		if Input.is_action_pressed("reset1"):
			position= Vector2(rand_range(startposition[0][0],startposition[0][1]),rand_range(startposition[0][2],startposition[0][3]))
			parkpos = [445, 674]
		else:
			position= Vector2(rand_range(startposition[1][0],startposition[1][1]),rand_range(startposition[1][2],startposition[1][3]))
			parkpos = [90,950]
		for i in InputMap.get_actions():
			var a = InputEventAction.new()
			a.action = i
			a.pressed = false
			Input.parse_input_event(a)
		velocity=startvelocity
		rotation=rand_range(0,2*6.283)
		print(startrotation)
		score = startscore
		turn = startturn
		steer_direction=0
		exportspeed=0
		exited = 0
		parked = 0
		is_score_edit = 0


func calc_steering(delta):
	if Input.is_action_pressed("steer_right"):
		turn += 2*lenken
	elif Input.is_action_pressed("steer_left"):
		turn -= 2*lenken
	elif Input.is_action_pressed("steer_center"):
		if turn > 0:
			turn -= 2*lenken
		if turn < 0:
			turn += 2*lenken
		if abs(turn)<2:
			turn=0
			

	if turn < -max_winkel:
		turn = -max_winkel
	if turn > max_winkel:
		turn = max_winkel
	steer_direction = turn * steering_angle
	steer_direction = deg2rad(steer_direction)
	

	

func _on_Area2D_body_exited(body):
	exited = 1

func _on_Area2D_body_entered(body):
	exited = 0

func is_parked():
	var speed = sqrt(pow(velocity[0],2)+pow(velocity[1],2))/32
	if exited == 1 && speed == 0 && colstep == 0:
		parked = 1
	if is_score_edit == 0 && parked:
		is_score_edit = 1
		score += 500
