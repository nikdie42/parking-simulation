import asyncio
import Gym_parken_fkt
import time
import nest_asyncio
import show_image as si


async def main():
    width = 100
    height = 60

    env = Gym_parken_fkt.Gym()
    while 1:
        key = input("Action? ")
        action = int(key)

        if action==1:
            reward = await env.step("accelerate", 0.17)
        if action==2:
            reward = await env.step("reverse", 0.17)
        if action==3:
            reward = await env.step("brake", 0.17)
        if action==4: 
            reward = await env.step("steer_left", 0.17)
        if action==5: 
            reward = await env.step("steer_right", 0.17)
        if action==6: 
            reward = await env.step("steer_center", 0.17)
        if action==7:    
            reward = await env.step("reset1", 0.17)
        if action==8:    
            reward = await env.step("reset2", 0.17)
        
        
       # print(reward)
        print("#")       #reward
        image_mode = 'RGB'
        try:
            # Test show Image
            si.show_image(image_mode, width, height, reward)
                       
        except Exception as e:
            print("failed showing image: " + str(e))

if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

