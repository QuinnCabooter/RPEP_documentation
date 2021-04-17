""""
Go/no-go task 
Author:         Quinn Cabooter
Function:       Master's student
Affiliation:    Ghent University
Departement:    Theoretical and experimental psychology
Academic year:  2020-21
An experiment programmed for the RPEP course.
Paper: EFFECT OF VERBAL RESPONSE METHOD ON LEFT VISUAL FIELD ADVANTAGE
COMPARED TO MANUAL RESPONSE METHOD.
"""

#import modules
from psychopy import visual, event, core, gui, data
import os, pandas, time
import numpy as np 
from psychopy import voicekey as vk
vk.pyo_init()


speedy  = 0


# file management and participant info

## set the directory
my_directory = os.getcwd()

## construct the name of the folder that will hold the data
directory_to_write_to = my_directory + "/data"
    
## if the folder doesn't exist yet, make it
if not os.path.isdir(directory_to_write_to):
    os.mkdir(directory_to_write_to)

## initialize the participant information dialog box
info = {"Participant name": "", "Participant number": 0, "Age": 0, "Sex": ["Female", "Male"], "Hand preference" : ["Right", "Left", "Ambidexter"]}

## make sure the data file has a novel name
already_exists = True
while already_exists:
    
    ## present the dialog box
    myDlg = gui.DlgFromDict(dictionary = info, title = "GO/ NO-GO TASK",order = ["Participant name", "Participant number"])
    
    ## construct the name of the data file
    file_name = directory_to_write_to + "/RPEP_subject_" + str(info["Participant number"]) + ".csv"
    
    ## check whether the name of the data file has already been used
    if not os.path.isfile(file_name):
        
        ## if there isn't a data file with this name used yet, we're ready to start
        already_exists = False
        
    else:
        
        ## if the data file name has already been used, ask the participant to inser a different participant number
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("Try another participant number")
        myDlg2.show()



## guarantee anonimity
## extract name from the dialog box
info_name =     info["Participant name"]
participant =   info["Participant number"]
## remove from info section
info.pop("Participant name")



###########################################################################################################
#Randomisation
##Set parameters
n_conditions        = 3     #should be 3 for experiment
n_trials            = 280   #5 blocks of 56 trials, should be 280

## initialize required responses
respons             = ["space", "escape",'f']


##Declare factorlevels 
###Stimulus position

LVF                 = (-4,0)
RVF                 = (4,0)
pos_options         = np.array([LVF, RVF])


###Stimulus options (28 stimuli)
stim_options        =np.array(['H_E.png', 'H_F.png', 'H_N.png', 'H_Y.png', 'T_E.png', 'T_F.png', 'T_N.png',
                    'T_Y.png', 'E_H.png', 'F_H.png', 'N_H.png', 'Y_H.png', 'E_T.png', 'F_T.png', 'N_T.png',
                    'Y_T.png', 'E_F.png', 'E_N.png', 'E_Y.png', 'F_E.png', 'F_N.png', 'F_Y.png', 'N_E.png',
                    'N_F.png', 'N_Y.png', 'Y_E.png', 'Y_F.png', 'Y_N.png'])

level               = np.array([2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0])

practice_pos        = np.array([LVF, RVF,RVF,LVF,RVF,LVF, RVF,RVF,LVF,RVF])
cue_pos             = np.array([0, 1,1,0,1,0, 1,1,0,1])
practice_stim       = np.array(['H_E.png', 'Y_E.png','T_E.png','F_E.png','Y_T.png','H_E.png', 'Y_E.png','T_E.png','F_E.png','Y_T.png'])
feedback            = np.array(['The answer was YES = press space','The answer was NO = no answer',
                    'The answer was YES = press space','The answer was NO = no answer','The answer was YES = press space', 'The answer was YES = press space',
                    'The answer was NO = no answer',
                    'The answer was YES = press space','The answer was NO = no answer','The answer was YES = press space' ])
###Targets
targets             = np.array([1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0])


## define number of levels for the factors
Nstim_pos           = len(pos_options)
Nstim               = len(stim_options)
## define number of unique trials
Nunique             = Nstim_pos * Nstim 
UniqueTrials        = np.array(range(Nunique))

## make the 2x2 factorial design
Stim_pos            = np.floor(UniqueTrials / Nstim) %Nstim_pos
Stim                = np.floor(UniqueTrials / 1) % Nstim


## deduce correct response
CorResp = targets


## BLOCK structure
##################
##56 trials so 5 repetitions of each unique trial
## combine arrays of core caracteristics in trial matrix = 56 eenheden
Design              = np.column_stack([Stim_pos, Stim, UniqueTrials, targets, level, CorResp])

## deduce how many times we need to repeat these trials per block 280/56 = 5 reps
n_reps              = int(n_trials / Nunique)

## repeat the unique trials to form a block = 280 eenheden 
blockTrials         = np.tile(Design, (n_reps, 1))
nColumnsBlock       = blockTrials.shape[1]

## TRIAL structure
##################
## we have 56 trials in each block. There are 15 blocks. 
## number of trials in the experiment
total_trials        = n_conditions * n_trials

## make an empty trial matrix. We add an extra column for block number.
trials              = np.ones((total_trials, 16)) * np.nan


#Elke conditie van 280 trials word apart gerandomiseerd en dan toegevoegd aan data.
## fill in the random trial order per block
for blocki in range(n_conditions):
     
    ## trial number for this block
    currentTrials = np.array(range(n_trials)) + blocki*n_trials
    
    stopcriterium = 0
    while stopcriterium != 1:
        
        ##shuffle de 280 trials
        np.random.shuffle(blockTrials)
        ##calculate the difference
        comparison = np.diff(blockTrials[:,1])
        ## shuffle again if the same stimulus appears
        if sum(comparison == 0) == 0: 
            stopcriterium = 1        
    
    ## store the trials for this block in the experiment array
    trials[currentTrials, 4:10] = blockTrials
    
    ## fill in the block number (starting from 1 instead of 0)
    trials[currentTrials, 10] = blocki+1
    
    ## insert the trial number within the block
    trials[currentTrials, 11] = np.array(range(n_trials))+1
    

##store the information about the participant
trials[:,0] = info["Age"]
trials[:,2] = info["Participant number"]

if info["Sex"] == "Male":
    trials[:,3] = 0
elif info["Sex"] == "Female":
    trials[:,3] = 1
else:
    trials[:,3] = 2
if info["Hand preference"] == "Right":
    trials[:,1] = 0
elif info["Hand preference"] == "Left":
    trials[:,1] = 1
else:
    trials[:,1] = 2
# validation of my randomization

## creating pandas dataframe from numpy array
trialsDF                      = pandas.DataFrame.from_records(trials)

## add the column names
trialsDF.columns              = ["Age", "Handedness", "Participant_number", "Gender" ,"Position",
                                        "stimulus", "UniqueTrials","Target","Level", "CorResp", "Block",
                                        "Trialnumber", "Time", "Response", "Accuracy", "Type"]

## cross table validation
print(pandas.crosstab([trialsDF.Position, trialsDF.stimulus], trialsDF.Target))
## export (just to be able to check the randomization)
trialsDF.to_csv(path_or_buf   = "DataFrame_RPEP.csv", index = False)



###########################################################################################################
###########################################################################################################
# initializing

## initialize the window
win_width       = 900#1900
win_height      = 600#1000
win_unit        = "deg"
win             = visual.Window(size = [win_width,win_height], units = win_unit, color = "white", monitor = 'testMonitor')


## initialize clock
my_clock        = core.Clock()

## graphical elements
txt_color       = "black"
img             = visual.ImageStim(win, size = (5,7))
mask            = visual.ImageStim(win, size = (5,7),image = "Images/#.png")
cue             = visual.TextStim(win,text=(""),color=txt_color)
fix             = visual.TextStim(win,text=("+"),color=txt_color)
fix2            = visual.TextStim(win,text=('MAKE SURE TO KEEP LOOKING AT THE POSITION OF THE '+'.'),color=txt_color)
example         = visual.ImageStim(win, size = (5,7),image = "Images/H_E.png")

welcome         = visual.TextStim(win,text=(    "Hello {},\n"+
                                                "Welcome to this experiment!\n"+
                                                "Thank you very much for participating. \n\n"+
                                                "Press 'SPACE' to continue.").format(info_name), color = txt_color)
                                    
instruct_gen    = visual.TextStim(win, text=(  "INSTRUCTIONS - READ CAREFULLY!\n\n"+ 
                                                "In this experiment you will be doing a GO-/NOGO-task.\n" +
                                                "You will see a number of letters. These letters are made up of a number of smaller letters. The figure will be on either the left or right-hand side of your screen.\n" +
                                                "After the figure appears, you will get a screen with 'Answer' on it. Here you will be given 2 seconds to give your answer.\n" +
                                                "The aim of the task is to press 'SPACE' or to say 'YES' out loud when you have seen the letters 'H' or 'T' (the large letter or small letter does not matter).\n"+
                                                "If you have not seen an 'H' or 'T', do NOT answer (do not press/say anything). \n"+
                                                "What kind of answer is needed ('SPACE'/'YES') is said beforehand. \n\n"+
                                                "Before each figure there will be a '+' in the centre of the screen"+ 
                                                "It is extremely important to keep looking at where the '+' is throughout the experiment! \n\n"+
                                                "Make sure that you understand the experiment correctly (ask for additional explanations if necessary). When you are ready, press 'SPACE' and an example image will appear.\n\n"
                                                "GOOD LUCK"
                                                ), color = txt_color, wrapWidth= 30)

#instruct_manL    = visual.TextStim(win,text=("Next, you have to press 'SPACE' with your left hand during the 'answer' screen when the stimulus contained either 'H' or 'T'.\n\nGood luck!"), color=txt_color, wrapWidth= 30)
#instruct_manR    = visual.TextStim(win,text=("Next, you have to press 'SPACE' with your right hand during the 'answer' screen when the stimulus contained either 'H' or 'T'.\n\nGood luck!"), color=txt_color, wrapWidth= 30)

instruct_manL   = visual.TextStim(win,text=("Now you have to press 'SPACE' with your LEFT HAND during the 'Answer' screen if the figure contained an 'H' or 'T'."), color=txt_color, wrapWidth= 30)
instruct_manR   = visual.TextStim(win,text=("Now you have to press 'SPACE' with your RIGHT HAND during the 'Answer' screen if the figure contained an 'H' or 'T'."), color=txt_color, wrapWidth= 30)


#instruct_verb    = visual.TextStim(win,text=("Next, you have to say 'YES' during the 'answer' screen when the stimulus contained either 'H' or 'T'.\n\n" + 
#                                                "IMPORTANT: During these trials you should be as silent as possible, except for your answer!\n\nGood luck!"),color=txt_color, wrapWidth= 30)

instruct_verb   = visual.TextStim(win,text=("Next, you have to say 'YES' during the 'answer' screen when the stimulus contained either 'H' or 'T'.\n\n" + 
                                                "IMPORTANT: During these trials you should be as silent as possible, except for your answer!\n\nGood luck!"),color=txt_color, wrapWidth= 30)

instruct_answer = visual.TextStim(win,text=(   "ANSWER"),color=txt_color)

practice        = visual.TextStim(win,text=("OK! Let's practice for a while. Now there will be 10 trials to show what the experiment will look like."),color=txt_color, wrapWidth= 30)

practice_fb     = visual.TextStim(win,text=(""),color=txt_color)


goodbye         = visual.TextStim(win,text=(    "This is the end of the experiment.\n\n"+
                                                "Sign the experimenter that you are finished.\n\n"+
                                                "Thank you for your participation!"), color=txt_color, wrapWidth= 30)






#########################################################################################################################################
# execute experiment

## welcome and instructions
welcome.draw()
win.flip()
event.waitKeys(keyList = "space")


instruct_gen.draw()
win.flip()
event.waitKeys(keyList = "space")

example.draw()
win.flip()
event.waitKeys(keyList = "space")

practice.draw()
win.flip()
event.waitKeys(keyList = "space")

#now the practice trials
for prac in range (10):
    
    fix.draw()
    win.flip()
    core.wait(1)
    
    
    img.image   = "Images/" + practice_stim[prac]
    img.pos     = practice_pos[prac]
    if cue_pos[prac] == 0:
        cue.text = '<'
    else:
        cue.text = '>'
    
    img.draw()
    cue.draw()
    win.flip()
    core.wait(0.18)
    
    mask.pos    = img.pos
    mask.draw()
    win.flip()
    core.wait(1)
    
    instruct_answer.draw()
    win.flip()
    keys = event.waitKeys(keyList = respons, maxWait = 2)
     
    
    practice_fb.text = feedback[prac]
    practice_fb.draw()
    win.flip()
    core.wait(1.5)
    
    
## trial loop
trialcounter = 0
while trialcounter < trials.shape[0]:
    
    if participant%2 == 0:
        if trials[trialcounter, 10] ==1:
            trialsDF.Type[trialcounter]  = 0 #0 for verbal
        elif trials[trialcounter, 10] ==2:
            trialsDF.Type[trialcounter] = 1 #1 for manual right
        elif trials[trialcounter, 10] ==3:
            trialsDF.Type[trialcounter] = 2 # 2 for manual left
    else: 
        if trials[trialcounter, 10] ==1:
            trialsDF.Type[trialcounter] = 1
        elif trials[trialcounter, 10] ==2:
            trialsDF.Type[trialcounter] = 2
        elif trials[trialcounter, 10] ==3:
            trialsDF.Type[trialcounter] = 0
    
    ## present the instructions at the start of the block
    if participant%2 == 0: #even participants
        if trials[trialcounter,11] == 1:
            if trials[trialcounter,10] == 1:
                instruct_verb.draw()
            elif trials[trialcounter,10] == 2:
                instruct_manR.draw()
            else:
                instruct_manL.draw()
            win.flip()
            event.waitKeys(keyList = "space")
    else:
        if trials[trialcounter,11] == 1:
            if trials[trialcounter,10] == 1:
                instruct_manR.draw()
            elif trials[trialcounter,10] == 2:
                instruct_manL.draw()
            else:
                instruct_verb.draw()
            win.flip()
            event.waitKeys(keyList = "space")

    #show fixating message
    if trialcounter%11 == 0: 
        fix2.draw()
        win.flip()
        core.wait(1.5)
        
        
    ##display fixation cross
    fix.draw()
    win.flip()
    core.wait(1)



    ## display the image on the screen
    #img.image = "/Volumes/UGENT/2. Research project/Images/" + stim_options[int(trials[trialcounter,5]) ]
    img.image = "Images/" + stim_options[int(trials[trialcounter,5]) ]
    
    img.pos     = pos_options[int(trials[trialcounter, 4])]
    if int(trials[trialcounter, 4]) == 0:
        cue.text = '<'
    else:
        cue.text = '>'
    
    img.draw()
    cue.draw()
    win.flip()
    core.wait(0.18 )

    ##mask
    mask.pos    =  pos_options[int(trials[trialcounter, 4])]
    mask.draw()
    fix.draw()
    win.flip()
    core.wait(1)

    ## wait for the response
    if participant%2 == 0: #even participants
        if trials[trialcounter,10] == 1:
            event.clearEvents(eventType = 'keyboard')
            keys = event.getKeys(keyList =respons)
            vpvk = vk.OnsetVoiceKey(sec = 2, file_out = "data/PPN_{}/trial_{}.wav".format(participant, trialcounter))
            vpvk.start()
            instruct_answer.draw()
            win.flip()
                
            time.sleep(2)
            vpvk.stop()
            RT = vpvk.event_onset
            
            if RT > 0:
                keys = ['space']
            else:
                keys = ['f']
                
            if keys == 'escape':
                break
                
                
        elif trials[trialcounter,10] == 2:
            event.clearEvents(eventType = "keyboard")
            instruct_answer.draw()
            win.flip()
            my_clock.reset()
            
            keys = event.waitKeys(keyList = respons, maxWait = 2)
            RT = my_clock.getTime()
            if keys == None:
                keys = "f" # for 'false'
                RT = 99.9
                
            if keys == 'escape':
                break
        else:
            event.clearEvents(eventType = "keyboard")
            instruct_answer.draw()
            win.flip()
            my_clock.reset()
            
            keys = event.waitKeys(keyList = respons, maxWait = 2)
            RT = my_clock.getTime()
            if keys == None:
                keys = "f" # for 'false'
                RT = 99.9
                
            if keys == 'escape':
                break
    else:
        if trials[trialcounter,10] == 1:
            event.clearEvents(eventType = "keyboard")
            instruct_answer.draw()
            win.flip()
            my_clock.reset()
            
            keys = event.waitKeys(keyList = respons, maxWait = 2)
            RT = my_clock.getTime()
            if keys == None:
                keys = "f" # for 'false'
                RT = 99.9
                
            if keys == 'escape':
                break
                
        elif trials[trialcounter,10] == 2:
            event.clearEvents(eventType = "keyboard")
            instruct_answer.draw()
            win.flip()
            my_clock.reset()
            
            keys = event.waitKeys(keyList = respons, maxWait = 2)
            RT = my_clock.getTime()
            if keys == None:
                keys = "f" # for 'false'
                RT = 99.9
                
            if keys == 'escape':
                break
                
        else:
            event.clearEvents(eventType = "keyboard")
            keys = event.getKeys(keyList = respons)
            vpvk = vk.OnsetVoiceKey(sec = 2, file_out = 'data/PPN_{}/Trial_{}.wav'.format(participant,trialcounter))
            vpvk.start()
            instruct_answer.draw()
            win.flip()
                
            time.sleep(2)
            vpvk.stop()
            RT = vpvk.event_onset
            
            if RT > 0: 
                keys = ['space']
            else:
                keys = ['f']
                
            if keys == 'escape':
                break
        win.flip()
    print(RT)
    print(keys[0])
    ## calculate the derived response properties
    CorResp = targets[int(trials[trialcounter,8])]

    ## store the response information
    if keys[0] == "space":
        trialsDF.Response[trialcounter]  = 1
    else:
        trialsDF.Response[trialcounter]  = 0
        
    accuracy = ( trialsDF.Response[trialcounter] == trialsDF.CorResp[trialcounter]) *1
    
    trialsDF.Accuracy[trialcounter]     = accuracy
    trialsDF.Time[trialcounter]      = RT
    trialcounter = trialcounter + 1
    print(accuracy)
    trialsDF.to_csv(path_or_buf   =  file_name, index = False)

goodbye.draw()
win.flip()
core.wait(5)

win.close()
