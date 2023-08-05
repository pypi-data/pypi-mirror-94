# SModelWrap
## You probably should not use this
I had to quickly create something and upload it to pypy so that I could get something working properly with an
 AWS Sagemaker pipeline that I don't own.
 
## What is it
Provides the class ```ModelPerClass``` which implements a custom predict method that will allow predictions on a single model 
per unique value in a row of a pandas DataFrame.
