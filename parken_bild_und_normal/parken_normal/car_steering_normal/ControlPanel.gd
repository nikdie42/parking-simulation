extends Control

export (NodePath) var player_path
var SettingSlider = preload("res://SettingSlider.tscn")
var player = null


var car_settings = ['engine_power']
var ranges = {'engine_power': [0.5, 2, 1]}
			
func _ready():
	if player_path:
		player = get_node(player_path)
		for setting in car_settings:
			var ss = SettingSlider.instance()
			ss.name = setting
			$Panel/VBoxContainer.add_child(ss)
			ss.get_node("Label").text = setting
			ss.get_node("Value").text = str(player.get(setting))	
			ss.get_node("Slider").connect("value_changed", self, "_on_Value_changed", [ss])
			
func _on_Value_changed(value, node):
	player.set(node.name, value)
	node.get_node("Value").text = str(value)

func _input(event):
	if event.is_action_pressed("ui_focus_next"):
		visible = !visible

func _process(delta):
	var speedinkmh
	if player:
		speedinkmh=player.exportspeed/32*3.6
		$Panel/VBoxContainer/Speedometer/Speed.text = "%4.1f" % speedinkmh
		$Panel/VBoxContainer/Speedometer2/Speed.text = "%4.1f" % rad2deg(player.steer_direction)
		$Panel/VBoxContainer/Speedometer3/Speed.text = "%4.1f" % player.score
		
#func show_message(text):
#	$Message.text = text
#	$Message.show()
#	$MessageTimer.start()
#
#
#func show_game_over():
#	show_message("Game Over")
#	yield($MessageTimer, "timeout")
#	yield(get_tree().create_timer(1), "timeout")
#

