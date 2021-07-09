install.packages("viridis")
library(viridis)

library(AppliedPredictiveModeling)
data(concrete)
dim(concrete)
install.packages("gbm")
library(gbm)
plot(fit)

1.
set.seed(1)
train_index<-sample(1030,730)
train<-concrete[train_index,]
test<-concrete[-train_index,]
set.seed(123)
fit<-gbm(CompressiveStrength~.,data=train,distribution="gaussian",n.trees=5000,cv.folds=5,interaction.depth=4,shrinkage=0.01,bag.fraction=0.5,n.minobsinnode=5)

fit

2.
summary(fit)

3.
plot(fit,i.var = "Age",main="Partial Importance Plot", ylab = "CompressiveStrength")
plot(fit,i.var = "Cement",main="Partial Importance Plot", ylab = "CompressiveStrength")
plot(fit,i.var = c("Age","Cement"),main="Partial Importance Plot", ylab = "CompressiveStrength")

4.
gbm.perf(fit,method="cv")
abline(h=0,lty=2)
legend("top",legend=c("Training Error","CV Error"),lty=1,
col = c("black","green"))

5.
min(fit$train.error)
which.min(fit$train.error)

min(fit$cv.error)
which.min(fit$cv.error)

6.
pred<- predict(fit, test,n.trees = 5000)
test_y<-test[,"CompressiveStrength"]
mean((pred-test_y)^2)