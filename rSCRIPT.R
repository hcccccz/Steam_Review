install.packages(car)
library(dplyr)
library(car)
library(ggplot2)
library(ggdark)
setwd("Steam_review")
data = read.table("Steam_oct18.csv",header=TRUE,quote="\"",fill=TRUE,sep=",")


data$average.total.playtime <- sub("h","",data$average.total.playtime)
data$average.recent.playtime <- sub("h","",data$average.recent.playtime)

data$average.total.playtime <- as.numeric(data$average.total.playtime)
data$average.recent.playtime <- as.numeric(data$average.recent.playtime)
data$initialprice <- data$initialprice/100
no_needed <- c("languages","genre","tags","release_date","fix","score_rank","user_socre","price","discount","ccu")
data <- data[!names(data) %in% no_needed]
nrow(data)

colnames(data)
data <- na.omit(data)
data_free <- data[data$average_price != 0,]
data_free$owners <- NULL

dim(data_free)

m <- lm(formula = estimated.players ~ review_num+positive+days_from_release+languages_supports+average_cut+duration+average_price,data = data)
summary(m)
anova(m)
colnames(data)
var(data$estimated.players)
data <- data %>% relocate(estimated.active.players)
data <- data %>% relocate(estimated.players)
names(data)
data$userscore

data %>% count(cut_width(estimated.players, 2445000))

cor(data)
scatterplotMatrix(data)

ep <- data$estimated.players

cor(data$review_num,data$estimated.active.players)



ggplot(data=data,mapping = aes(x = estimated.players)) + geom_density() +dark_theme_classic()
summary(data$estimated.players)


