import asyncio
import Gym_parken
import time
import nest_asyncio
import math
async def send_action(env,action):
    #Mithilfe von dieser Funktion können Befehle an die Simulation gesendet werden und Daten von der Simulation empfangen werden.
    if action=="nothing":
        observation, reward, sensors, parkpos, rotation = await env.step("nothing", 0.17)
    if action=="accelerate":
        observation, reward, sensors, parkpos, rotation = await env.step("accelerate", 0.17)
    if action=="reverse":
        observation, reward, sensors, parkpos, rotation = await env.step("reverse", 0.17)
    if action=="brake":
        observation, reward, sensors, parkpos, rotation = await env.step("brake", 0.17)
    if action=="steer_left": 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_left", 0.17)
    if action=="steer_right": 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_right", 0.17)
    if action=="steer_center": 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_center", 0.17)
    if action=="reset1":    
        observation, reward, sensors, parkpos, rotation = await env.step("reset1", 0.17)
    if action=="reset2":    
        observation, reward, sensors, parkpos, rotation = await env.step("reset2", 0.17)
    #print(observation)  #[(xposition,yposition), Geschwindigkeit, aktuelle Lenkrichtung]
    #print(reward)       #reward
    #print(sensors)      #Sensorwerte
    #print(parkpos)      #Position des Parkplatzes
    #print(rotation)     #Winkel des Autos (Zur x achse der Karte)
    return observation, reward, sensors, parkpos, rotation

def check_sensores(sensores, desired_input):
    #Eine Reihe von Tests wird durchgeführt, um zu überprüfen, ob das Auto droht mit einer Wand zu kollidieren.
    if desired_input!="accelerate" and desired_input!="reverse" and desired_input!="brake" and desired_input!="steer_left" and desired_input!="steer_right" and desired_input!="steer_center" and desired_input!="reset1" and desired_input != "reset2" and desired_input != "nothing":
        print("invalid input: "+desired_input)
    if observation[2] > 0:                                  #Wenn Auto nach vorne fährt
        if sensors[0]<observation[2]*5 or sensors[0]<20:    #Suche Hinderniss vorne
            print("emergency front")
            return [0, "front"]

    if observation[2] > 0 and observation[3]<0:             #Wenn Auto nach vorne-links fährt
        if sensors[7]<observation[2]*5 or sensors[7]<20:    #Suche Hinderniss vorne-links
            print("emergency frontleft")
            return [0, "frontleft"]

    if observation[2] > 0 and observation[3]>0:             #Wenn Auto nach vorne-rechts fährt
        if sensors[1]<observation[2]*5 or sensors[1]<20:    #Suche Hinderniss vorne-links
            print("emergency frontright")
            return [0, "frontright"]

    if observation[2] < 0:                                  #Wenn Auto nach hinten fährt
        if sensors[4]<abs(observation[2]*5) or sensors[4]<20:    #Suche Hinderniss hinten
            print("emergency back")
            return [0, "back"]

    if observation[2] < 0 and observation[3]<0:             #Wenn Auto nach hinten-links fährt
        if sensors[5]<abs(observation[2]*5) or sensors[5]<20:    #Suche Hinderniss hinten-links
            print("emergency backleft")
            return [0, "backleft"]

    if observation[2] < 0 and observation[3]>0:             #Wenn Auto nach hinten-rechts fährt
        if sensors[3]<abs(observation[2]*5) or sensors[3]<20:    #Suche Hinderniss hinten-rechts
            print("emergency backright")
            return [0, "backright"]
    if abs(observation[2])>10:                              #Verhindert, dass das Auto schneller als 10 kmh fährt.
        if desired_input == "accelerate" or desired_input == "reverse":
            desired_input = "nothing"

    if sensores[0]<200:                                     #signalisiert, dass es in frontaler Richtung ein Hinderniss gibt. Ein sofortiges Eingreifen ist nicht notwendig.
        return [1,desired_input]
    return [2,desired_input]


def angle_to_destination(rotation, park_pos, car_pos):
    park_pos[0]
    angle_to_x = (math.atan2(park_pos[1]-car_pos[1],park_pos[0]-car_pos[0]))*180/math.pi
    return angle_to_x-rotation

def distance_to_destination(park_pos, car_pos):
    return math.sqrt((park_pos[0] - car_pos[0])**2 + (park_pos[1] - car_pos[1])**2 )

def turn_to_destination(turnstatus, angle, observation, sensors):
    #Richtet das Auto in die gewünschte Richtung aus

    #turnstatus = 0: (start) Drehe Räder
    #turnstatus = 1: Fahre vorwärts
    #turnstatus = 2: Hinderniss entdeckt. Bremse zum Stillstand, um danach rückwärts zu fahren
    #turnstatus = 3: Drehe Räder zum rückwärts fahren
    #turnstatus = 4: Fahre rückwärts
    #turnstatus = 5: Hinderniss entdeckt. Bremse zum Stillstand, um danach vorwärts zu fahren
    #turnstatus = 6: Zielausrichtung wurde annähernd erreicht. Bremse ab.
    #rurnstatus = 7: Zielausrichtung erreicht
    if abs(angle)<5:
        return turnstatus6(angle, observation) 
    if turnstatus == 0:
        return turnstatus0(angle, observation)
    if turnstatus == 1:
        return turnstatus1(angle, observation, sensors)
    if turnstatus == 2:
        return turnstatus2(angle, observation)
    if turnstatus == 3:
        return turnstatus3(angle, observation)
    if turnstatus == 4:
        return turnstatus4(angle, observation, sensors)
    if turnstatus == 5:
        return turnstatus5(angle, observation)
    if turnstatus == 6:
        return turnstatus6(angle, observation)


def turnstatus0(angle, observation):
    if angle < 0:
        if observation[3] == -22:
            print("drive")
            return [1, "nothing"]
        return [0, "steer_left"]
    else:
        if observation[3] == 22:
            print("drive")
            return [1, "nothing"]
        return [0, "steer_right"]
def turnstatus1(angle, observation,sensores):
    sensorstatus=check_sensores(sensores, "accelerate")[0]
    if sensorstatus != 0:
        return [1, "accelerate"]
    else:
        print("brake")
        return [2, "brake"]
def turnstatus2(angle, observation):
    if observation[2]!=0:
        return [2, "brake"]
    else:
        print("steer")
        return [3, "nothing"]
def turnstatus3(angle, observation):
    if angle < 0:
        if observation[3] == 22:
            return [4, "nothing"]
            print("brake")
        return [3, "steer_right"]
    else:
        if observation[3] == -22:
            return [4, "nothing"]
        return [3, "steer_left"]
def turnstatus4(angle, observation, sensores):
    sensorstatus=check_sensores(sensores, "reverse")[0]
    if sensorstatus!=0:
        return [4, "reverse"]
    else:
        return [5, "brake"]
def turnstatus5(angle, observation):
    if observation[2]!=0:
        return [5, "brake"]
    else:
        return [0, "nothing"]
def turnstatus6(angle, observation):
    if observation[2]!=0:
        return [6, "brake"]
    elif observation[3]!=0:
        return [6,"steer_center"]
    else:
        print("Angle towards Parkingspot reached. Proceeding with Phase 2")
        return [7, "nothing"]


def proccess_command(env, command, car_pos):
    #Diese Funktion überprüft ein letztes Mal den gewünschten Befehl und schickt ihn  an die Funktion send_action, damit er in der Simulation ausgeführt wird.
    if command!="accelerate" and command!="reverse" and command!="brake" and command!="steer_left" and command!="steer_right" and command!="steer_center" and command!="reset1" and command != "reset2" and command != "nothing":
        command = "brake"
        print("input warning")
    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(send_action(env,command))
    distance = distance_to_destination(parkpos, car_pos)
    return observation, reward, sensors, parkpos, rotation, distance

def init_simulation(desired_input):
    env = Gym_parken.Gym()
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    if desired_input == "1":
        desired_input = "reset1"
    if desired_input == "2":
        desired_input = "reset2"
    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(send_action(env,desired_input)) #send_action
    start_pos = [observation[0],observation[1]]
    return env, loop, observation, reward, sensors, parkpos, rotation, start_pos

def phase_1(observation, sensors, parkpos, rotation, turnstatus):
    angle = angle_to_destination(rotation, parkpos, [observation[0],observation[1]])
    turnstatus, desired_input = turn_to_destination(turnstatus, angle, observation, sensors)
    sensorstatus, desired_input = check_sensores(sensors, desired_input)
    observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    return observation, sensors, rotation, distance, turnstatus

def phase_2(observation, sensors, parkpos, rotation):
    angle = angle_to_destination(rotation, parkpos, [observation[0],observation[1]])
    sensorstatus, desired_input = check_sensores(sensors, "accelerate")
    if sensorstatus == 1:
        if sensors[7]>sensors[1]:
            desired_input ="steer_left"
        elif sensors[7]<sensors[1]:
            desired_input ="steer_right"
        else:
            desired_input ="accelerate"
    elif observation[3] !=0:
        desired_input = "steer_center"
    if observation[2]<10:
        desired_input ="accelerate"
    observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    return observation, sensors, rotation, distance, angle

def phase_3_szenario_1(observation):
    desired_input = "nothing"
    observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    while sensors[2]<100:   #Fahre bis das Auto neben der Parklücke steht
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    while sensors[2]>75:    #Fahre bis die Spitze des Autos das ende der Parklücke erreicht hat. Weiche währenddessen hindernissen aus
        sensorstatus, desired_input = check_sensores(sensors, "accelerate")
        if sensorstatus == 1:
            desired_input ="steer_left"
        else:
            desired_input = "steer_center"
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "nothing"
    for i in range(70):             #Fahre 70 Iterationen an der Parklücke vorbei
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "brake"         #Bremse auf 0
    while observation[2]!=0:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "steer_right"   #Schlage das Lenkrad so weit wie möglich ein
    while observation[3]!=22:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "reverse"       #Fahre rückwerts in die Parklücke
    for i in range(25):
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "steer_left"    #Lenke zurück, um wieder in eine Paralele Position zur Straße zu kommen
    while observation[3]!=-22:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "brake"         #Bremse ab, Fertig
    while observation[2]!=0:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action

def phase_3_szenario_2(observation):
    desired_input = "nothing"
    observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    while sensors[6]<100:   #Fahre bis das Auto neben der Parklücke steht
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    while sensors[6]>75:    #Fahre bis die Spitze des Autos das ende der Parklücke erreicht hat. Weiche währenddessen hindernissen aus
        sensorstatus, desired_input = check_sensores(sensors, "accelerate")
        if sensorstatus == 1:
            desired_input ="steer_right"
        else:
            desired_input = "steer_center"
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "nothing"
    for i in range(40):             #Fahre 40 Iterationen an der Parklücke vorbei
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "brake"
    while observation[2]!=0:        #Bremse auf 0
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "steer_left"    #Schlage das Lenkrad so weit wie möglich ein
    while observation[3]!=-22:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "reverse"       #Fahre rückwerts in die Parklücke
    for i in range(68):
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action
    desired_input = "brake"         #Bremse ab, Fertig
    while observation[2]!=0:
        observation, reward, sensors, parkpos, rotation, distance = proccess_command(env, desired_input, [observation[0],observation[1]]) #send_action

if __name__ == "__main__":
    parkingspot=0
    while parkingspot!="1" and parkingspot!="2":
        parkingspot = input("Press 1 for the parkingspot 1 and 2 for the spot 2: ")
    env, loop, observation, reward, sensors, parkpos, rotation, start_pos = init_simulation(parkingspot)
    in_progress = 1
    while in_progress:
        turnstatus = 3
        print("phase 1: Turn towards destination")
        while turnstatus != 7:  #Phase 1: Zum Parkplatz hin ausrichten.            
            observation, sensors, rotation, distance, turnstatus = phase_1(observation, sensors, parkpos, rotation, turnstatus)
        print("phase 2: drive towards destination")
        angle = 0
        while angle<25 and distance>175:    #Phase 2: Zum Parkplatz fahren. 
            observation, sensors, rotation, distance, angle = phase_2(observation, sensors, parkpos, rotation)
        if distance<175:        #Phase 3: Zum Parkplatz fahren. 
            print("phase 3: park the car")
            if sensors[2]<120:
                szenario=1
            elif sensors[6]<120:
                szenario=2
            else:
                print("attempt failed")
                in_progress = 0
            if szenario == 1:
                phase_3_szenario_1(observation)     #Szenario 1 für den ersten Parkplatz
            if szenario == 2:
                phase_3_szenario_2(observation)     #Szenario 2 für den ersten Parkplatz
            in_progress = 0
    print("done")






