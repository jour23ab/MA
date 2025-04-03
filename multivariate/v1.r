##########################################################################################################
# Clearing console
cat("\014")
# Clear environment
rm(list = ls())
# Clear figures
graphics.off()
##########################################################################################################
# What is the current working directory?
getwd()
# Set working directory
setwd('C:/Users/johan/Documents/Documents/Universitet/5. år MSc/Thesis')
# Confirm working directory
getwd()
##########################################################################################################
# Packages
# install.packages("stargazer")
# install.packages("ggfortify")
# install.packages("forecast")
# install.packages("urca")
# install.packages("strucchange")
# install.packages("timetk")
# install.packages("readr")
# install.packages("dplyr")
# install.packages("tidyr")
# install.packages("readxl")
# install.packages("corrplot")
# install.packages("sandwich")
#install.packages
#install.packages("ggplot2")


library(stargazer)
library(ggfortify)
library(forecast)
library(urca)
library(strucchange)
library(timetk)
library(readr)
library(dynlm)
library(lmtest)
library(car)
library(dplyr)
library(tidyr)
library(readxl)
library(corrplot)
library(sandwich)
library(DescTools)
library(ggplot2)
##########################################################################################################
#Loading data
#data=read_xlsx("CAR_analysis_COMPARISON_with_target_type.xlsx")
#data=read_xlsx("CAR_v2.xlsx")
data=read_xlsx("CAR_v5.xlsx")


#Creating variables
df <- data %>%
  mutate(
    #Diversification = ifelse(`Industry Classifications [Buyers/Investors]` != `Industry Classifications [Target/Issuer]`, 1, 0),
    Diversification = ifelse(`Primary Sector [Buyers/Investors]` != `Primary Sector [Target/Issuer]`, 1, 0),
    CrossBorder = ifelse(`Geographic Locations [Buyers/Investors]` != `Geographic Locations [Target/Issuer]`, 1, 0),
    Public = ifelse(`Target Type` == "Public", 1, 0),
    Private = ifelse(`Target Type` == "Private", 1, 0),
    # Public = ifelse(`Company Type [Target/Issuer]` %in% c("Public Company", "Public Investment Firm"), 1, 0),
    # Private = ifelse(`Company Type [Target/Issuer]` == "Private Company", 1, 0),
    # Asset = ifelse(`Company Type [Target/Issuer]` == "Assets/Products", 1, 0),
    Cash = ifelse(`Consideration Offered` == "Cash", 1, 0),
    Stock = ifelse(`Consideration Offered` == "Common Equity", 1, 0),
    Hybrid = ifelse(`Consideration Offered` == "Combinations" | grepl("Cash;", `Consideration Offered`, fixed = TRUE), 1, 0),
    Unknown = ifelse(`Consideration Offered` == "Unknown" | 
                       (grepl("Unknown", `Consideration Offered`, fixed = TRUE) & 
                          !grepl("Cash|Common Equity", `Consideration Offered`)), 1, 0),
    TargetEquity = ifelse(grepl("Common Equity", `Target Security Types`, fixed = TRUE), 1, 0),
    TargetAsset = ifelse(`Target Security Types` == "Asset", 1, 0),
  )

#Converting to numerical values
df$Revenue <- as.numeric(df$`Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)`)
df$EBITDA <- as.numeric(df$`Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)`)
df$`Earnings` <- as.numeric(df$`Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)`)
df$Debt <- as.numeric(df$`Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)`)
df$TotalAssets <- as.numeric(df$`Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)`)
df$CommonEquity <- as.numeric(df$`Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)`)
df$PreferredEquity <- as.numeric(df$`Acquirer LTM Financials - Total Preferred (at Announcement) (€EURmm, Historical rate)`)
df$MinorityInterest <- as.numeric(df$`Acquirer LTM Financials - Minority Interest (at Announcement) (€EURmm, Historical rate)`)
df$MarketCap <- as.numeric(df$`Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)`)
df$`Cash and Equivalents` <- as.numeric(df$`Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)`)
df$Size <- as.numeric(df$`Total Transaction Value (€EURmm, Historical rate)`)
df$BookEquity <- rowSums(
  df[, c("CommonEquity", "PreferredEquity")], #Removed , "MinorityInterest"
  na.rm = TRUE
)

df <- df %>%
  mutate(
    MtoB = ifelse(BookEquity != 0, MarketCap / BookEquity, NA), #Not sure if i should include minority.
    DtoE = ifelse(BookEquity != 0, Debt / BookEquity, NA)
  )

#Testing different relative ratios
df$StoMC = df$Size / df$MarketCap
df$StoE = df$Size / df$BookEquity
df$StoC = df$Size / df$`Cash and Equivalents`

#Reformatting from million to billion
df$Size = df$Size / 1000
df$`Cash and Equivalents` = df$`Cash and Equivalents` / 1000
df$TotalAssets = df$TotalAssets / 1000

#Creating more control variables
df$Margin = df$EBITDA / df$Revenue

# One-hot encode buyer sector
#buyer_dummies <- model.matrix(~ `Primary Sector [Buyers/Investors]` - 1, data = df)
#colnames(buyer_dummies) <- paste0("BS_", gsub("[^[:alnum:]_]", "", colnames(buyer_dummies)))  # clean col names
#df <- cbind(df, buyer_dummies)

# One-hot encode buyer sector
target_dummies <- model.matrix(~ `Primary Sector [Target/Issuer]` - 1, data = df)

# Extract just the sector name from the column and clean it
clean_names <- sub(".*\\]", "", colnames(target_dummies))             # remove everything before ]
clean_names <- gsub("[`'\"]", "", clean_names)                        # remove backticks, quotes
clean_names <- gsub("\\s+", "_", clean_names)                         # optional: replace spaces with underscores

# Add prefix
colnames(target_dummies) <- paste0("TS_", clean_names)

# Combine
df <- cbind(df, target_dummies)



#Creating the Crisis variable
crisis_periods = list(
  c(as.Date("2008-02-19"), as.Date("2008-05-07")),
  c(as.Date("2008-09-19"), as.Date("2010-03-22")),
  c(as.Date("2010-05-07"), as.Date("2010-12-15")),
  c(as.Date("2011-08-09"), as.Date("2012-10-01")),
  c(as.Date("2015-09-08"), as.Date("2015-11-05")),
  c(as.Date("2016-01-14"), as.Date("2016-08-04")),
  c(as.Date("2020-03-18"), as.Date("2021-01-05")),
  c(as.Date("2022-03-04"), as.Date("2022-12-06"))
)
df$AnnouncementDate <- as.Date(df$`M&A Announced Date`)
is_in_crisis <- function(date, intervals) {
  any(sapply(intervals, function(interval) date >= interval[1] & date <= interval[2]))
}
df$Crisis <- sapply(df$AnnouncementDate, is_in_crisis, intervals = crisis_periods)
df$Crisis <- as.integer(df$Crisis)  # convert TRUE/FALSE to 1/0

#Correlation matrix to make sure that the variables look correct
vars <- c("Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis", "Margin", "DtoE", "Hybrid", "Stock", "Size", "Cash and Equivalents", "TotalAssets", "TargetAsset", "TargetEquity", "Public", "Unknown", "StoMC", "StoE", "StoC", "TS_Consumer_Discretionary", "TS_Consumer_Staples", "TS_Financials", "TS_Health_Care", "TS_Industrials", "TS_Information_Technology", "TS_Materials", "TS_Real_Estate")
setdiff(vars, colnames(df))
df_subset = df[, vars]
df_subset = df_subset[sapply(df_subset, is.numeric)]
cor_matrix <- cor(df_subset, use = "pairwise.complete.obs")
corrplot(cor_matrix, method = "color", type = "lower", tl.cex = 0.5, number.cex = 0.5, addCoef.col = "black")

#Checking correlations of independent variables with some regressors
vars <- c("[-10, 10]","[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]","Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis", "Margin", "DtoE", "Hybrid", "Stock", "Size", "Cash and Equivalents", "TotalAssets", "TargetAsset", "TargetEquity", "Public", "Unknown", "StoMC", "StoE", "StoC", "TS_Consumer_Discretionary", "TS_Consumer_Staples", "TS_Financials", "TS_Health_Care", "TS_Industrials", "TS_Information_Technology", "TS_Materials", "TS_Real_Estate")
setdiff(vars, colnames(df))
df_subset = df[, vars]
df_subset = df_subset[sapply(df_subset, is.numeric)]
cor_matrix <- cor(df_subset, use = "pairwise.complete.obs")
corrplot(cor_matrix, method = "color", type = "lower", tl.cex = 0.5, number.cex = 0.5, addCoef.col = "black")

#Removing observations due to some error.
# df <- df %>%
#   filter(Asset != 1)
df <- df %>%
  filter(`Target Type` != "Unknown")

###Multiple Regression
#Excluded TS_Health_Care because this is perfectly correlated with Diversifcation
#No data for TS_Materials, TS_Real_Estate and Unknown
model1 = lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model2 = lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model3 = lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model4 = lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model5 = lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)

#Winsorization to remove the bottom 1% and top 99% CARs - capping outliers
df$CAR_10_wins <- Winsorize(df$`[-10, 10]`, val = quantile(df$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_7_wins  <- Winsorize(df$`[-7, 7]`, val = quantile(df$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_5_wins  <- Winsorize(df$`[-5, 5]`, val = quantile(df$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_3_wins  <- Winsorize(df$`[-3, 3]`, val = quantile(df$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_1_wins  <- Winsorize(df$`[-1, 1]`, val = quantile(df$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))

#Winsorized
model1 = lm(CAR_10_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model2 = lm(CAR_7_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model3 = lm(CAR_5_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model4 = lm(CAR_3_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model5 = lm(CAR_1_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + `Cash and Equivalents` + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)


"models = list(
  model1,
  model2,
  model3,
  model4,
  model5
)
bp_results <- lapply(models, bptest)
bp_results"""

#Testing with relative deal size
# model1 = lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoE + `Cash and Equivalents` + TargetAsset, df)
# model2 = lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoE + `Cash and Equivalents` + TargetAsset, df)
# model3 = lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoE + `Cash and Equivalents` + TargetAsset, df)
# model4 = lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoE + `Cash and Equivalents` + TargetAsset, df)
# model5 = lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoE + `Cash and Equivalents` + TargetAsset, df)
# 
# model1 = lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoC + `Cash and Equivalents` + TargetAsset, df)
# model2 = lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoC + `Cash and Equivalents` + TargetAsset, df)
# model3 = lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoC + `Cash and Equivalents` + TargetAsset, df)
# model4 = lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoC + `Cash and Equivalents` + TargetAsset, df)
# model5 = lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoC + `Cash and Equivalents` + TargetAsset, df)
# 
# model1 = lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoA + TotalAssets + TargetEquity, df)
# model2 = lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoA + TotalAssets + TargetEquity, df)
# model3 = lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoA + TotalAssets + TargetEquity, df)
# model4 = lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoA + TotalAssets + TargetEquity, df)
# model5 = lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + StoA + TotalAssets + TargetEquity, df)

#Extract robust standard errors
se_list <- list(
  sqrt(diag(hccm(model1, type = "hc0"))),
  sqrt(diag(hccm(model2, type = "hc0"))),
  sqrt(diag(hccm(model3, type = "hc0"))),
  sqrt(diag(hccm(model4, type = "hc0"))),
  sqrt(diag(hccm(model5, type = "hc0")))
)

#df <- df[-c(70, 130), ]

#Generate output
stargazer(model1, model2, model3,model4, model5, 
          type = "text", title = "Regression Results",
          se = se_list)

#Plotting returns for raw data
ggplot(df, aes(x = `[-10, 10]`)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-10, 10]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-10, 10]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = `[-7, 7]`)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-7, 7]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-7, 7]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = `[-5, 5]`)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-5, 5]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-5, 5]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = `[-3, 3]`)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-3, 3]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-3, 3]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = `[-1, 1]`)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-1, 1]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-1, 1]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

#Plotting for Winsarized data
ggplot(df, aes(x = CAR_10_wins)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-10, 10]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(CAR_10_wins, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = CAR_7_wins)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-7, 7]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(CAR_7_wins, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = CAR_5_wins)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-5, 5]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(CAR_5_wins, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = CAR_3_wins)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-3, 3]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(CAR_3_wins, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

ggplot(df, aes(x = CAR_1_wins)) +
  geom_histogram(aes(y = ..density..), 
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-1, 1]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(CAR_1_wins, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
  theme_minimal()

#Plotting comparisons based on the binary coefficients
ggplot(df, aes(x = `[-10, 10]`, fill = factor(Cash))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Cash Payment",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Cash") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Private))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Listing Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Private") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(CrossBorder))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Abnormal Returns by Cross-Border Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "CrossBorder") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Diversification))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Diversification Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Diversification") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Crisis))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Crisis Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Crisis") +
  xlim(-10, 10) +
  theme_minimal()


