import asyncio
import Gym_parken
import time
import nest_asyncio
import math

observation = []
reward = []
sensors = []
rotation = []


def berechneAbstand(observation,parkpos):
    abstand = math.sqrt((parkpos[0]-observation[0])**2 + (parkpos[1]-observation[1])**2)
    return abstand

async def main(env, action):
    
    if action==1:
        observation, reward, sensors, parkpos, rotation = await env.step("accelerate", 0.17)
    if action==2:
        observation, reward, sensors, parkpos, rotation = await env.step("reverse", 0.17)
    if action==3:
        observation, reward, sensors, parkpos, rotation = await env.step("brake", 0.17)
    if action==4: 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_left", 0.17)
    if action==5: 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_right", 0.17)
    if action==6: 
        observation, reward, sensors, parkpos, rotation = await env.step("steer_center", 0.17)
    if action==7:    
        observation, reward, sensors, parkpos, rotation = await env.step("reset1", 0.17)
    if action==8:    
        observation, reward, sensors, parkpos, rotation = await env.step("reset2", 0.17)
    
    
    #print(observation)   #[(xposition,yposition), Geschwindigkeit, aktuelle Lenkrichtung]
    #print(reward)       #reward
    #print(sensors)       #Sensorwerte
    #print(parkpos)      #Position des Parkplatzes
    #print(rotation)       #Sensorwerte
    return observation, reward, sensors, parkpos, rotation

if __name__ == "__main__":
    env = Gym_parken.Gym()
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()

    parkplatz = "0"
    while parkplatz != "1" and parkplatz != "2":
        parkplatz = input("Drücken Sie 1, um auf dem ersten Parkplatz zu starten oder 2, um auf dem zweiten zu starten.")
    if parkplatz =="1":
        parkplatz = 7
    else:
        parkplatz = 8
    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,parkplatz))

    bereich = 1

    # Im Bereich 1 steuert der Agent das Auto bis zur Parklücke. Dabei darf die Geschwindigkeit 40 km/h nicht überschreiten.
    # Sobald der Agent an der Parklücke vorbeigefahren ist, springt er in Bereich 2.
    if bereich == 1:
        while sensors[0] > 100 and observation[0] < parkpos[0]:

            if  observation[2] < 40:
                observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,1))

            if observation[2] > 40:
                observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))

            if sensors[0] < 100:
                observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))

            if observation[0] > parkpos[0]:
                bereich = 2
    # In Bereich 2 wird das Auto angehalten. 
    if bereich == 2:       
        while observation[2] > 0:
            observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))

        if observation[2] == 0:
            if observation[1] < parkpos[1]:
                bereich = 3
            if observation[1] > parkpos[1]:
                bereich = 4
    
    if bereich == 3:
        while reward < 500:
            while sensors[0] > 30 and sensors[1] > 30 and sensors[2] > 30 and sensors[3] > 30 and sensors[4] > 30 and sensors[5] > 30 and sensors[6] > 30 and sensors[7] > 30 and reward < 500:
                while rotation > -(math.pi/11) and observation[0]>parkpos[0] and observation[1] < parkpos[1]:
                    while observation[3] < 8:
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,5))
                    if abs(observation[2]) < 9: 
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,5))
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,2))
                    else:
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,5))
                while rotation < -(math.pi/11):
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,4))
                while rotation > -(math.pi/11) and observation[0]<parkpos[0] and observation[2] != 0:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,5))
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))
                    
    
            while sensors[0] < 30 or sensors[1] < 30 or sensors[2] < 30 or sensors[3] < 30 or sensors[4] < 30 or sensors[5] < 30 or sensors[6] < 30 or sensors[7] < 30:
                if observation[2] > 0:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,1))
                else:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,2))
        if reward > 500:
            bereich = 5
    
    if bereich == 4:
        while reward < 500:
            while sensors[0] > 30 and sensors[2] > 30 and sensors[4] > 30 and sensors[6] > 30 and reward <500:
                while rotation < math.pi/3.6:
                    if abs(observation[2]) < 27: 
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,4))
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,2))
                    else:
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,4))
                    
                while rotation > math.pi/3.6 and rotation < math.pi/2.7:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,5))
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))
                    
                while rotation > math.pi/2.7 and reward < 500:
                    if abs(observation[2]) != 0:
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,6))
                        observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,3))
                    
    
            while sensors[0] < 30 or sensors[1] < 30 or sensors[2] < 30 or sensors[3] < 30 or sensors[4] < 30 or sensors[5] < 30 or sensors[6] < 30 or sensors[7] < 30 :
                if observation[2] > 0:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,1))
                else:
                    observation, reward, sensors, parkpos, rotation = loop.run_until_complete(main(env,2))
                
        if reward > 500:
            bereich = 5

    if bereich == 5:
        print(reward)




        
        
        

 

            
        
