def AudioPreGame_sequence():

    
    PreGame_time = True
    
    global TooSoon1
    global TooSoon2
    global AudioGameInProgress
    
    TooSoon1 = False
    TooSoon2 = False
    
    StripsOff(StripAudio1)
    StripsOff(StripAudio2)

    speaker.play(c_note, 0.1) # play the middle c for 0.1 seconds
    
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
    
    while PreGame_time == True and AudioGameInProgress == True:

        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False


        while time.ticks_ms() - waiting_start < wait_time and AudioGameInProgress == True:
            

            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False

            
            if not React1Button.value(): # if the value changes
                TooSoon(StripAudio1)
                TooSoon1 = True

                    
            if not React2Button.value(): # if the value changes
                TooSoon(StripAudio2)
                TooSoon2 = True

        

       speaker.play(c_note, 0.1) # play the middle c for 0.1 seconds
    
    
    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and AudioGameInProgress == True:
            
            if not AudioGoButton.value():
                time.sleep(0.4)
                AudioGameInProgress = False


            if not React1Button.value(): # if the value changes
                TooSoon(StripAudio1)
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoon(StripAudio2)
                TooSoon2 = True
        
        
        if time.ticks_ms() - waiting_start > wait_time + random_wait:
            

            speaker.play(c_note, 0.2) # play the middle c for 0.1 seconds
        
        
            
            PreGame_time = False

def AudioGame_sequence():

    ReactWaiting = True
    
    global React1Waiting
    global React2Waiting
    
    global StripAudio1AudioTime
    global StripAudio2AudioTime
    
    global AudioGameInProgress
    
    global start_time
    global finish_time
    
    React1Waiting = True
    React2Waiting = True

    
    start_time = time.ticks_ms() #Records the current time
    
    while(ReactWaiting) and AudioGameInProgress == True:
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False

        global i
        global jAudio1
        global jAudio2
        
        i=1
        for i in range(1, LED_num):
            timeout = start_time + i * next_LED_time
        
    
            if TooSoon1 == True:
                jAudio1 = LED_num
            if TooSoon2 == True:
                jAudio2 = LED_num
        
            if React1Waiting == True and TooSoon1 == False:
                jAudio1 = i
            
            if React2Waiting == True and TooSoon2 == False:           
                jAudiol2 = i

            while time.ticks_ms() < timeout:
                if not React1Button.value():
                    StripAudio1AudioTime = time.ticks_ms()
                    React1Waiting = False
                if not React2Button.value():
                    StripAudio2AudioTime = time.ticks_ms()
                    React2Waiting = False
                pass
            

        ReactWaiting = False
        
    for j in range (0,jAudio1):
        StripAudio1[j]=(0,0,255)
        StripAudio1.write()
    for j in range (0,jAudio2):
        StripAudio2[j]=(0,0,255)
        StripAudio2.write()

    if TooSoon1 == True:
        StripAudio1AudioTime = time.ticks_ms()
    
    if TooSoon2 == True:
        StripAudio2AudioTime = time.ticks_ms()

    if React1Waiting == True:
        StripAudio1AudioTime = time.ticks_ms()
    
    if React2Waiting == True:
        StripAudio2AudioTime = time.ticks_ms()
    

    finish_time = time.ticks_ms()



def AudioTime_output():

    AudioTime1 = StripAudio1AudioTime-start_time
    print ('AudioTime1')
    print (AudioTime1)
    print('{0:04d}'.format(AudioTime1))

#    lcd_1.move_to(0,0)
#    lcd_1.putstr('Audio:')
#    lcd_1.move_to(8,0)
#    lcd_1.putstr('{0:04d}'.format(AudioTime1))


    AudioTime2 = StripAudio2AudioTime-start_time
    print ('AudioTime2')
    print (AudioTime2)
    print('{0:04d}'.format(AudioTime2))

#    lcd_2.move_to(0,0)
#    lcd_2.putstr('Audio:')
#    lcd_2.move_to(8,0)
#    lcd_2.putstr('{0:04d}'.format(AudioTime2))   

 
#    while True:
#        lcd.move_to(0,0)
#        lcd.putstr('Hello world')
    
#        lcd.clear()                # Clear display    

def AudioCelebration_sequence():

    global AudioGameInProgress
    Celebrating = True
    while Celebrating == True and AudioGameInProgress == True:
        global i
        FlashCounter = 0
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if React1Waiting == False and TooSoon1 == False:

            if StripAudio1AudioTime < StripAudio2AudioTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
            elif StripAudio1AudioTime == StripAudio2AudioTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1)
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
            elif StripAudio1AudioTime>StripAudio2AudioTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
            
        else:
            if React2Waiting == False and TooSoon2 ==False:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False