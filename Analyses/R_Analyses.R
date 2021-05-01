# Import packages 
library(reshape2)
library(car)
library(lme4)
library(afex)
library(predictmeans)
library(lattice)
library(ggplot2)
library(dplyr)
library(effects)
#Import datasets from participants separate ----
pp1 <-  read.csv("RPEP_subject_1_corr.csv", sep = ',', dec = '.')
pp3 <-  read.csv("RPEP_subject_3_corr.csv", sep = ',', dec = '.')
pp4 <-  read.csv("RPEP_subject_4 corr.csv", sep = ',', dec = '.')
pp5 <-  read.csv("RPEP_subject_5 corr.csv", sep = ',', dec = '.')
pp6 <-  read.csv("RPEP_subject_6 corr.csv", sep = ',', dec = '.')
pp7 <-  read.csv("RPEP_subject_7 corr.csv", sep = ',', dec = '.')
pp9 <-  read.csv("RPEP_subject_9 corr.csv", sep = ',', dec = '.')
pp10 <-  read.csv("RPEP_subject_10 corr.csv", sep = ',', dec = '.')
pp11 <-  read.csv("RPEP_subject_11 corr.csv", sep = ',', dec = '.')
pp12 <-  read.csv("RPEP_subject_12 corr.csv", sep = ',', dec = '.')
pp13 <-  read.csv("RPEP_subject_13 corr.csv", sep = ',', dec = '.')
pp14 <-  read.csv("RPEP_subject_14 corr.csv", sep = ',', dec = '.')
pp15 <-  read.csv("RPEP_subject_15 corr.csv", sep = ',', dec = '.')
pp16 <-  read.csv("RPEP_subject_16 corr.csv", sep = ',', dec = '.')
pp17 <-  read.csv("RPEP_subject_17 corr.csv", sep = ',', dec = '.')
pp18 <-  read.csv("RPEP_subject_18 corr.csv", sep = ',', dec = '.')
pp19 <-  read.csv("RPEP_subject_19 corr.csv", sep = ',', dec = '.')
pp20 <-  read.csv("RPEP_subject_20 corr.csv", sep = ',', dec = '.')
pp21 <-  read.csv("RPEP_subject_21 corr.csv", sep = ',', dec = '.')
pp22 <-  read.csv("RPEP_subject_22 corr.csv", sep = ',', dec = '.')
pp23 <-  read.csv("RPEP_subject_23 corr.csv", sep = ',', dec = '.')
pp24 <-  read.csv("RPEP_subject_24 corr.csv", sep = ',', dec = '.')
pp26 <-  read.csv("RPEP_subject_26 corr.csv", sep = ',', dec = '.')



#Create large dataset ----

'dataset straight from experiment, thus no rejected trials and also no-go trials'
data.full <- rbind(pp1, pp3, pp4, pp5, pp6, pp7, pp9, pp10, pp11, pp12, pp13, pp14, pp15, pp16, pp17, pp18, pp19, pp20, pp21, pp22, pp23, pp24, pp26)

'Change the pp_number to easier name'
colnames(data.full)[3] <- "Subject"

#Use only correct trials and trials needed respons + data of only global----
'correct and response trials without outliers'

data <- filter(data.full, Accuracy == 1  & Time >= 0.2 & Time <= 1.5 )
head(data)


'same as before but only global level stimuli, just for checking the amount of trials we have for analyses'
data.glob <- filter(data.full, Accuracy == 1 & CorResp == 1 & Time >= 0.2 & Time <= 1.5 & Level ==2 )





#Excluded data descriptives --------
Ndata <- dim(data)[1]
Ndata

'Number of excluded trials'
Ndata.full <- 11520 #32 * 5 blocks * 3 conditions * 24 pp's
Nexcl <- Ndata.full - Ndata
Procent.excl <- Nexcl / Ndata.full
'2935' == '0.27%'






#Age and accuracy descriptives-------
## AGE
mean(data.full$Age)
'21'
sd(data.full$Age)
'5.17'

##Accuracy
acc1 <- mean(pp1$Accuracy)
acc3 <- mean(pp3$Accuracy)
acc4 <- mean(pp4$Accuracy)
acc5 <- mean(pp5$Accuracy)
acc6 <- mean(pp6$Accuracy)
acc7 <- mean(pp7$Accuracy)
acc9 <- mean(pp9$Accuracy)
acc10 <- mean(pp10$Accuracy)
acc11 <- mean(pp11$Accuracy)
acc12 <- mean(pp12$Accuracy)
acc13 <- mean(pp13$Accuracy)
acc14 <- mean(pp14$Accuracy)
acc15 <- mean(pp15$Accuracy)
acc16 <- mean(pp16$Accuracy)
acc17 <- mean(pp17$Accuracy)
acc18 <- mean(pp18$Accuracy)
acc19 <- mean(pp19$Accuracy)
acc20 <- mean(pp20$Accuracy)
acc21 <- mean(pp21$Accuracy)
acc22 <- mean(pp22$Accuracy)
acc23 <- mean(pp23$Accuracy)
acc24 <- mean(pp24$Accuracy)
acc26 <- mean(pp26$Accuracy)


acc_list <- c(acc1, acc3, acc4, acc5, acc6, acc7, acc9, acc10, acc11,acc12, acc13, acc14, acc15, acc16, acc17, acc18, acc19, acc20, acc21, acc22, acc23, acc24, acc26)

mean(acc_list)
'0.843323'
sd(acc_list)
'0.09673855'
"Accuracy is collected using data that has not rejected outliers "



# Actual analyses (previous code can be ignored for the following part; Environment can be cleared)------
data <-  read.csv("Reduced_data2.csv", sep = ',', dec = '.')


data$Gender <- factor(data$Gender)
data$Handedness <- factor(data$Handedness)
data$Position <- factor(data$Position)
data$Target <- factor(data$Target)
data$Level <- factor(data$Level)
data$Type <- factor(data$Type)
data$CorResp <- factor(data$CorResp)
data$Block <- factor(data$Block)
data$Response <- factor(data$Response)
data$Accuracy <- factor(data$Accuracy)


'Change the pp_number to easier name'
colnames(data)[1] <- "Subject"
head(data)

df <- subset(data, select = -c(UniqueTrials, Response, CorResp, stimulus))
head(df)

df1 <- filter(df, Level == 'Glob')
df1$TypeMV[(df1$Type == 'RH')] <- "Man"
df1$TypeMV[(df1$Type == 'LH')] <- "Man"
df1$TypeMV[(df1$Type == 'Verbal')] <- "Verb"
df1$TypeMV <- as.factor(df1$TypeMV)

head(df1)
##Visualisation of data
bwplot(Time~ Level, data= df)
bwplot(Time~ Position, data = df)
bwplot(Time~ Type, data = df)
bwplot(Time~ Level:Position, data = df)
bwplot(Time~ Position:Type, data= df)
bwplot(Time~ Level:Position:Type, data=df)



## LMER approach ------
###Analyses with level as predictor
'set contrasts'
options(contrasts = c("contr.sum", "contr.poly"))


'fit linear model'
lm <- lmer(Time ~ Level*Position*Type + (1 | Subject), data = df)

summary(lmer(Time ~ Level*Position*Type + (1 | Subject), data = df), corr = FALSE)

Anova(lmer(Time ~ Level*Position*Type + (1 | Subject), data = df), type = "III")
Anova(lmer(Time ~ Level*Position*Type + (1 | Subject), data = df), type = "III", test.statistic = "F") #Takes a long time

aov_car(Time ~ Level*Position*Type + Error(Subject/(Level*Position*Type)), data = df) #used for results section


### Analyses wit only global level 

lm1 <- lmer(Time ~ Position*Type + (1 | Subject), data = df1)

summary(lm1, corr = FALSE)
Anova(lmer(Time ~ Position*Type + (1 | Subject), data = df1), type = "III")
Anova(lmer(Time ~ Position*TypeMV + (1 | Subject), data = df1), type = "III", test.statistic = "F") #Takes a long time again

aov_car(Time ~ Position*Type + Error(Subject|(Position*Type)), data = df1)

'Verbal vs manual, so only two levels'
aov_car(Time ~ Position*TypeMV + Error(Subject|(Position*TypeMV)), data = df1) #used for results section

#plotting the main effect of Type
plot(effect('Type', lm1), main = "")


dcast(.~TypeMV, data = df1, value.var = 'Time', mean)
dcast(.~Position, data = df1, value.var = 'Time', mean)

##Visualisation of data
bwplot(Time~ Position, data = df1)
bwplot(Time~ Type, data = df1)
bwplot(Time~ Position:Type, data= df1)


## Trying for multivariate approach (wide data)--------
'set contrasts'
options(contrasts = c("contr.sum", "contr.poly"))


'create a molten dataset'
data.melt <- melt(df1, measure.vars ="Time")
head(data.melt)


data.wide <- dcast(Subject  ~ Level + Position  + Type , data = data.melt, value.var = "value", fun.aggregate = mean ) 
head(data.wide) 

#Anova for effects of response hand
colMeans(data.wide)
'mean LH'
mean(c(0.3445538, 0.3394336))

'mean RH'
mean(c(0.3911734,0.3922453))


'main effect of VHF'
M1 <- cbind(c(1,1,0,-1,-1,0))
fit <- lm(cbind(Glob_LVF_LH,Glob_LVF_RH,Glob_LVF_Verbal,Glob_RVF_LH,Glob_RVF_RH,Glob_RVF_Verbal)%*% M1 ~ 1, data=data.wide)
Anova(fit, type = "III")

'main effect of hand'
M2 <- cbind(c(1/2,-1/2,0,1/2,-1/2,0))
fit2 <- lm(cbind(Glob_LVF_LH,Glob_LVF_RH,Glob_LVF_Verbal,Glob_RVF_LH,Glob_RVF_RH,Glob_RVF_Verbal)%*% M2 ~ 1, data=data.wide)
Anova(fit2, type = "III")

'interaction effect'
M3 <- cbind(c(1,-1,0,-1,1,0))
fit3 <- lm(cbind(Glob_LVF_LH,Glob_LVF_RH,Glob_LVF_Verbal,Glob_RVF_LH,Glob_RVF_RH,Glob_RVF_Verbal)%*% M3 ~ 1, data=data.wide)
Anova(fit3, type = "III")

