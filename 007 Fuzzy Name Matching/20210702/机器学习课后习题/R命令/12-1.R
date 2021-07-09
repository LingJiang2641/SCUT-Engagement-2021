1.
library(AppliedPredictiveModeling)
data(concrete)
dim(concrete)
set.seed(1)
train<-sample(1030,730)
install.packages("randomForest")
library(randomForest)
set.seed(123)
bag.fit<-randomForest(CompressiveStrength~.,data=concrete,subset=train,mtry=8,importance=TRUE)
bag.fit
plot(bag.fit,main="Bagging OOB Errors")

2.
importance(bag.fit)
varImpPlot(bag.fit,main="Variable Improtance Plot")

3.
partialPlot(bag.fit,concrete[train,],x.var=Age)
partialPlot(bag.fit,concrete[train,],x.var=Cement)

4.
bag.pred<-predict(bag.fit,newdata=concrete[-train,])
y.test<-concrete[-train,"CompressiveStrength"]
plot(bag.pred,y.test,main="bagging prediction")
abline(0,1)
mean((bag.pred-y.test)^2)

5.
concrete_train<-concrete[train,]
set.seed(12345)
foldid<-sample(1:8,size=103,replace=TRUE)
head(foldid)
MSE<-matrix(rep(0,80),ncol=10)
for(i in 1:8){
  for(j in 1:10){
   train_cv<-concrete_train[foldid!=1,]
   holdout<-concrete_train[foldid==1,]
   fit<-randomForest(CompressiveStrength~.,data=train_cv,mtry=i)
   pred<-predict(fit,newdata=holdout)
   y.test<-holdout[,"CompressiveStrength"]
   MSE[i,j]<-mean((pred-y.test)^2)
  }
 }
cv.error<-apply(MSE,1,mean)
min(cv.error)
which.min(cv.error)
plot(1:10,cv.error,type="b",xlab="mtry",main="cross-v-Errpr")
abline(v=which.min(cv.error),lty=2)

6.
MSE<-numeric(8)
set.seed(123)
for(i in 1:8){
  fit<-randomForest(CompressiveStrength~.,data=concrete,subset=train,mtry=i)
  pred<-predict(fit,newdata=concrete[-train,])
  y.test<-concrete[-train,"CompressiveStrength"]
  MSE[i]<-mean((pred-y.test)^2)
 }
min(MSE)
which.min(MSE)
plot(1:8,MSE,type="b",xlab="Test Error")
abline(v=which.min(MSE),lty=2)
