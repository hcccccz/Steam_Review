install.packages(car)
library(dplyr)
library(car)
library(ggplot2)
setwd("~/repo/Steam_review/")

data = read.table("Steam1.csv",header=TRUE,quote="\"",fill=TRUE,sep=",")




data$average.total.playtime <- sub("h","",data$average.total.playtime)
data$average.recent.playtime <- sub("h","",data$average.recent.playtime)

data$average.total.playtime <- as.numeric(data$average.total.playtime)
data$average.recent.playtime <- as.numeric(data$average.recent.playtime)

data <- data[!names(data) %in% "score_rank"]
data <- data[!names(data) %in% "fix"]
nrow(data)
data <- na.omit(data)
nrow(data)
names(data)
no_needed <- c("appid","name","developer","publisher","owners","discount","languages","genre","tags","release_date")
data <- data[!names(data) %in% no_needed]

data <- data %>% relocate(estimated.active.players)
data <- data %>% relocate(estimated.players)
names(data)


data %>% count(cut_width(estimated.players, 2445000))

cor(data)
scatterplotMatrix(data)

ep <- data$estimated.players



max(ep)/20




sample_ <- sample(nrow(data),100)
data <- data[sample_,]

