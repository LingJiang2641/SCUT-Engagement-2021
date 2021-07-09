1.
data<- read.csv("Data/student-mat.csv",sep=";")

2.
data <- data[,-31]
data <- data[,-31]
str(data)

3.
hist(G3)

4.
install.packages("glmnet")
library(glmnet)

x<- model.matrix(G3~.,data)[,-1]
class(x)
y<-data$G3

set.seed(1)
cvfit <- cv.glmnet(x,y,alpha=0)
plot(cvfit)
cvfit$lambda.min
cvfit$lambda.1se
coef(cvfit,s = "lambda.min")

5.
cvfit <- cv.glmnet(x,y,alpha=1)
plot(cvfit)
cvfit$lambda.min
cvfit$lambda.1se
coef(cvfit,s = "lambda.min")


6.
cvfit <- cv.glmnet(x,y,alpha=0.5)
plot(cvfit)
cvfit$lambda.min
cvfit$lambda.1se
coef(cvfit,s = "lambda.min")


7.
set.seed(1)
foldid<- sample(1:10,size = 395,replace = TRUE)
cv.error<- numeric(11)
for (i in 1:11){
	cvfit<-cv.glmnet(x,y,foldid = foldid,alpha = (i-1)/10)
	cv.error[i] <-min(cvfit$cvm)
}
cv.error
min(cv.error)
which.min(cv.error)


8.
set.seed(1)
train <-sample(395,295)
cvfit <- cv.glmnet(x[train,],y[train],alpha=0)
coef(cvfit,s = "lambda.min")


bestlam <- cvfit$lambda.min
pred_train <- predict(cvfit,newx = x[train,],s=bestlam)
mean((pred_train-y[train])^2)
pred_test <- predict(cvfit,newx = x[-train,],s=bestlam)
mean((pred_test-y[-train])^2)
coef(cvfit,s = "lambda.min")

