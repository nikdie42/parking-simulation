import asyncio
import Gym_parken
import time
import nest_asyncio

async def main():
    env = Gym_parken.Gym()
    while 1:
        key = input("Action? ")
        action = int(key)

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
        
        
        print(observation)   #[(xposition,yposition), Geschwindigkeit, aktuelle Lenkrichtung]
        print(reward)       #reward
        print(sensors)       #Sensorwerte
        print(parkpos)      #Position des Parkplatzes
        print(rotation)       #Sensorwerte

if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

