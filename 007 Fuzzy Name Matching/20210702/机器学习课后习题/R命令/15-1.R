library(AppliedPredictiveModeling)
data(abalone)
data<-abalone
1.
dummyType <- model.matrix(~Type, data)
dummyType[0]
data <- model.matrix(~data$Type+LongestShell+Diameter+Height+
WholeWeight+ShuckedWeight+VisceraWeight+ShellWeight+Rings,data)
data<-as.data.frame(data)

2.
maxs <- apply(data,2,max)
mins <- apply(data,2,min)
data_s <-as.data.frame(scale(data,center=mins,scale=maxs-mins))

3.
install.packages("neuralnet")
library(neuralnet)
y.test<- data[-train,"Rings"]

set.seed(1)
train <-sample(4177,1000)
set.seed(123)
fit<- neuralnet(Rings~data$TypeI+data$TypeM+LongestShell+Diameter+Height+
WholeWeight+ShuckedWeight+VisceraWeight+ShellWeight,data=data_s[train,],hidden = 3,
  act.fct="logistic",linear.output=TRUE)
plot(fit)

4.
pred<- predict(fit,data_s[-train,])
pred<- pred*(max(data$Rings)-min(data$Rings))+min(data$Rings)
mean((pred-y.test)^2)

5.
fit.ols<-lm(Rings~.,data=data[train,])
pred.ols<- predict(fit.ols,data[-train,])
mean((pred.ols-y.test)^2)

6.
MSE <- numeric(10)
for (i in 1:10){
set.seed(123)
fit<- neuralnet(Rings~data$TypeI+data$TypeM+LongestShell+Diameter+Height+
WholeWeight+ShuckedWeight+VisceraWeight+ShellWeight,data=data_s[train,],
hidden = i,act.fct="logistic",linear.output=TRUE)
pred<- predict(fit,data_s[-train,])
pred<- pred*(max(data$Rings)-min(data$Rings))+min(data$Rings)
MSE[i]<-mean((pred-y.test)^2)
}
min(MSE)
which.min(MSE)
plot(1:10,MSE,type="b",xlab="Number of Hidden Neurons",
main = "Abalone Data")
abline(v = which.min(MSE),lty=2)
