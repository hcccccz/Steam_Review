install.packages(car)
library(dplyr)
library(car)
setwd("Steam_review/Data")

data = read.table("data.csv",header=TRUE,quote="\"",fill=TRUE,sep=",")




data$average.total.playtime <- sub("h","",data$average.total.playtime)
data$average.recent.playtime <- sub("h","",data$average.recent.playtime)

data$average.total.playtime <- as.numeric(data$average.total.playtime)
data$average.recent.playtime <- as.numeric(data$average.recent.playtime)

new_data <- data[!names(data) %in% "score_rank"]

nrow(new_data)
new_data <- na.omit(new_data)
nrow(new_data)
names(new_data)
no_needed <- c("appid","name","developer","publisher","owners","discount","languages","genre","tags","release_date")
new_data <- new_data[!names(new_data) %in% no_needed]

new_data <- new_data %>% relocate(estimated.active.players) 
new_data <- new_data %>% relocate(estimated.players) 
names(new_data)




cor(new_data)
scatterplotMatrix(new_data)





plot(new_data)

