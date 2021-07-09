1.
data<- read.csv("Data/Meter_D.csv")
str(data)
data[,44] = as.factor(data[,44])
str(data)

2.
set.seed(1)
train <-sample(180,100)

x<- data[,-44]
y<- data[44]
train_x = data[train,][,-44]
train_y = data[,44][train]

test_x = data[-train,][,-44]
test_y = data[,44][-train]

library(e1071)
fit <- svm(V44~.,data = data[train,],kernel = "linear",cost = 0.5,scale=TRUE)

pred<- predict(fit,data[-train,])
(table <- table(Predicted=pred,Actual=test_y))
(accuracy<- sum(diag(table))/sum(table))

3.
fit <- svm(V44~.,data = data[train,],kernel = "polynomial",degree = 2,cost = 0.5,gamma = 0.5,scale=TRUE)
pred<- predict(fit,data[-train,])
(table <- table(Predicted=pred,Actual=test_y))
(accuracy<- sum(diag(table))/sum(table))

4.
fit <- svm(V44~.,data = data[train,],kernel = "radial",cost = 1,gamma = 1,scale=TRUE)
pred<- predict(fit,data[-train,])
(table <- table(Predicted=pred,Actual=test_y))
(accuracy<- sum(diag(table))/sum(table))

5.
set.seed(123)
tune.out<- tune(svm,V44~.,data = data ,kernel="linear",
ranges=list(cost=c(0.001,0.01,0.1,1,5,10,100)))
tune.out

fit <- svm(V44~.,data = data[train,],kernel = "linear",cost = 5,scale=TRUE)
fit
pred<- predict(fit,data[-train,])
(table <- table(Predicted=pred,Actual=test_y))
(accuracy<- sum(diag(table))/sum(table))

6.
accuracy<- numeric(14)
ranges<-list(0.001,0.01,0.1,1,5,10,20,30,40,50,60,70,80,100)
for (i in 1:14){
	fit <- svm(V44~.,data = data[train,],kernel = "linear",cost = ranges[i],scale=TRUE)
	pred<- predict(fit,data[-train,])
	table <- table(Predicted=pred,Actual=test_y)
	accuracy[i]<- sum(diag(table))/sum(table)
}
accuracy
max(accuracy)
which.max(accuracy)

plot(ranges,accuracy)
