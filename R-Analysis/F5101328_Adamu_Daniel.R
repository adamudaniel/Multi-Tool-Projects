#1. INSTALLING AND LOADING NECESSARY PACKAGES
install.packages("tidyverse")
install.packages("e1071")
install.packages("caTools")
install.packages("caret")
install.packages("reshape2")

library(reshape2)
library(tidyverse)
library(e1071)
library(caTools)
library(caret)

#2. LOADING THE DATA INTO R
churn_data = read.csv("Churn_Modelling.csv", na = c("", "NA"))

#3. DATA CLEANING
# Exploring the data
cat("\n--- Data Structure (Summary) ---\n")
head(churn_data)
dim(churn_data)
str(churn_data)
summary(churn_data)
sapply(churn_data, class)

# Checking for missing or blanks in the data
cat("\n--- Count of missing values ---\n")
sum(is.na(churn_data)) #outputs total count of missing rows
colSums(is.na(churn_data)) #check to see which columns contain missing row

# Inputting missing values
mode_of_Geograpgy = churn_data %>%
  count(Geography) %>%        # Group by Geography and count observations
  slice_max(n, n = 1) %>%
  pull(Geography)             # Extracts the maximum count (n) in column
print(paste("The mode of Geograpgy is:", mode_of_Geograpgy))

churn_data$Geography[is.na(churn_data$Geography)] = 'France' #Input the mode 'France' in missing row

churn_data$Age = ifelse(is.na(churn_data$Age),
                        ave(churn_data$Age, FUN = function(x) mean(x, na.rm = TRUE)),
                        churn_data$Age) #Input value for missing in Age column

churn_data$HasCrCard[is.na(churn_data$HasCrCard)] = "Yes" #Input the mode in HasCrCard column

churn_data$IsActiveMember[is.na(churn_data$IsActiveMember)] = 'Yes' #Input the mode in IsActiveMember column

# Removing duplicates in the data
churn_data = distinct(churn_data)
cat("2 duplicate rows removed from dataset.\n")

#removing irrelevant columns
churn_data$RowNumber = NULL
churn_data$CustomerId = NULL
churn_data$Surname = NULL 
        #remove 'RowNumber','customerID' and 'Surname' columns from data

#Checking the final cleaned data
colSums(is.na(churn_data)) #no blanks or missing found
summary(churn_data)

# Ensuring proper formatting of numeric variables as numbers
churn_data$CreditScore = as.numeric(churn_data$CreditScore)
churn_data$Tenure = as.numeric(churn_data$Tenure)
churn_data$NumOfProducts = as.numeric(churn_data$NumOfProducts)

#4. VISUALIZING THE DATA (EXPLORATORY DATA ANALYSIS)
#(Target Distribution plot,Categorical Variable,Numerical Variable)

# Set color for churn outcomes
churn_colors <- c("No" = "#2A9D8F", "Yes" = "#E76F51")

#plot of Target variable (Exited)
ggplot(data = churn_data, aes(x = Exited, fill = Exited)) +
  geom_bar() +
  # Adding percentage to bars
  geom_text(
    stat = 'count',
    aes(label = scales::percent(..count../sum(..count..)), y = ..count../sum(..count..) * 0.95),
    vjust = 1, size = 5) + scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Churn Rate (Target Variable Distribution)",
       x = "Exited Status",
       y = "Count",
       fill = "Exit Status") +
  theme_minimal(base_size = 14) +
  theme(legend.position = "none", plot.title = element_text(hjust = 0.5, face = "bold"))

#Plot of Credit Score against churn
ggplot(churn_data, aes(x = Exited, y = CreditScore, fill = Exited)) +
  geom_boxplot() +
  scale_fill_manual(values = churn_colors) +
  labs(title = "Distribution of Credit Score by Churn Status",
       x = "Exited Status", 
       y = "Credit Score",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Geography against churn
ggplot(data = churn_data,aes(x = Geography, fill = Exited)) +
  geom_bar(color = "white", position = "dodge") + scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Churn Rate by Geography",
       x = "Geography",
       y = "Customers",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Gender against churn
ggplot(data = churn_data,aes(x = Gender, fill = Exited)) +
  geom_bar(color = "white", position = "dodge") + scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Churn Rate by Gender",
       x = "Gender",
       y = "Customers",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Customer Age against churn
ggplot(churn_data, aes(x = Age, fill = Exited)) + 
  geom_density(alpha = 0.6) + scale_fill_manual(values = churn_colors) +
  labs(title = "Distribution of Customer Age",
       x="Customer Age", 
       y="Density",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Customer Tenure against churn
ggplot(churn_data, aes(x = Exited, y = Tenure, fill = Exited)) +
  geom_boxplot() +
  scale_fill_manual(values = churn_colors) +
  labs(title = "Distribution of Customer Tenure by Churn Status",
       x = "Exited Status", 
       y = "Customer Tenure (years)",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Customer Balance against churn
ggplot(churn_data, aes(x = Balance, fill = Exited)) + 
  geom_density(alpha = 0.6) + scale_fill_manual(values = churn_colors) +
  labs(title = "Distribution of Customer Balance",
       x="Customer Balance", 
       y="Density",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Customer by number of products against churn
ggplot(churn_data, aes(x = NumOfProducts, fill = Exited)) +
  geom_bar(position = "dodge", color = "white") +
  scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Count by Number of Products and Churn Status",
       x = "Number of Products", 
       y = "Number of Customers",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Credit Card Status against churn
ggplot(data = churn_data,aes(x = HasCrCard, fill = Exited)) +
  geom_bar(color = "white", position = "dodge") + scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Churn Rate by Credit Card Status",
       x = "Credit Card Status",
       y = "Customers",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Member Active Status against churn
ggplot(data = churn_data,aes(x = IsActiveMember, fill = Exited)) +
  geom_bar(color = "white", position = "dodge") + scale_fill_manual(values = churn_colors) +
  labs(title = "Customer Churn Rate by Member Active Status",
       x = "Member Active Status",
       y = "Customers",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#Plot of Customer Salary against churn
ggplot(churn_data, aes(x = Exited, y = EstimatedSalary, fill = Exited)) +
  geom_boxplot() +
  scale_fill_manual(values = churn_colors) +
  labs(title = "Distribution of Customer Salary by Churn Status",
       x = "Exited Status", 
       y = "Estimated Salary",
       fill = "Exited") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom")

#5. ENCODING DATA
# Encoding categorical columns
churn_data$Geography = factor(churn_data$Geography,
                              levels = c('France', 'Spain', 'Germany'),
                              labels = c(1,2,3))
churn_data$Gender = factor(churn_data$Gender,
                           levels = c('Female', 'Male'),
                           labels = c(0,1))
churn_data$HasCrCard = factor(churn_data$HasCrCard,
                              levels = c("Yes"," No"),
                              labels = c(1,0))
churn_data$IsActiveMember = factor(churn_data$IsActiveMember,
                                   levels = c('Yes', 'No'),
                                   labels = c(1,0))

#5. SPLITTING DATA INTO TRAINING AND TEST SET 
#setting seed phrase for reproducibility
set.seed(080)

#splitting data into training and test set
split = sample.split(churn_data$Exited, SplitRatio = 0.7)

training_set = subset(churn_data, split == TRUE)
test_set = subset(churn_data, split == FALSE)

#Checking the class balance of target variable in new sets
print(paste('The Training set balance:'))
prop.table(table(training_set$Exited))

print(paste('The Test set balance:'))
prop.table(table(test_set$Exited))


#6. FEATURE SCALING OF DATA
# Identify Columns that need scaling
normalize_cols = c("CreditScore", "Age", "Tenure", "Balance", "EstimatedSalary")

# Calculating the means and standard deviations of the training set's columns
mean_sd = preProcess(training_set[,normalize_cols], 
                           method = c("center", "scale")) #'center' is to subtract the mean from each value in the column, "scale" is to divide the result by the standard deviation of the column

# Apply Standardization to datasets
training_set[,normalize_cols] = predict(mean_sd, 
                                        training_set[,normalize_cols]
                                        )
test_set[,normalize_cols] = predict(mean_sd, 
                                    test_set[,normalize_cols]
                                    )
            #Test set is also scaled, but using the means and standard deviations calculated from the training set.

#checking scaled training set
summary(training_set)


#7. TRAINING THE MODEL (SVM)
# Converting the target variables to factors
training_set$Exited <- as.factor(training_set$Exited)
test_set$Exited <- as.factor(test_set$Exited)

# Using radial kernel linear
# Using grid search to tune hyperparameter rather than using default values
Exit_training = tune(svm,
                     Exited ~ .,
                     data = training_set,
                     type = 'C-classification', 
                     kernel = 'radial', #Using the 'radial' (RBF) kernel
                     ranges = list(cost = c(0.1, 1, 10), #Testing different C values
                                   gamma = c(0.01, 0.1, 1)), #Testing different Gamma values
                     probability = TRUE)

best_model = Exit_training$best.model

summary(best_model) #outputting the best model details
print(Exit_training$best.parameters)

#Using the trained SVM to predict Exited status of test set
Exit_pred = predict(best_model, newdata = test_set[-11])
        #test_set given excluding the 10th column (Exited Status)


#8. MODEL EVALUATION
#creating a confusion matrix to compare predicted to actual results 
compare = confusionMatrix(data = Exit_pred, reference = test_set$Exited)

print(compare)

#Plotting the confusion matrix
table_compare = as.data.frame(compare$table) #Confusion matrix table

melted_table = melt(table_compare) #melting the table into a ggplot format

#Plotting the confusion matrix table
ggplot(data = melted_table, aes(x = Prediction, y = Reference, fill = value)) +
  geom_tile() +
  geom_text(aes(label = value), color = 'black', size = 6) +
  scale_fill_gradient(low = 'white', high = '#009194') +
  labs(x = 'Predicted Class', y = 'Actual Class', title = 'Confusion Matrix') +
  theme_minimal() +
  theme(legend.position = 'none')

#9. Plotting ROC Curve and calculating AUC
predictions = predict(best_model, newdata = test_set[-11], probability = TRUE)

# Getting the probabilities matrix attribute (for 'yes' class)
prob_matrix = attr(predictions, 'probabilities')[ , 'Yes']

install.packages("pROC")
library(pROC)
ROC_object = roc(response = test_set$Exited, predictor = prob_matrix)

#Calculating and printing AUC value
AUC_value = auc(ROC_object)
print(paste("The AUC Score is:", round(AUC_value, 4)))

#plotting the ROC curve with the AUC
plot(ROC_object, 
     main = 'ROC Curve (SVM - Radial Kernel)', 
     print.auc = TRUE, 
     col = '#0072B2'
     )
