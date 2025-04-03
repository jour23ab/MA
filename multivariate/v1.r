###Multiple Regression
source("multivariate/data_prep.R")
data <- load_clean_data()
#Excluded TS_Health_Care because this is perfectly correlated with Diversifcation
#No data for TS_Materials, TS_Real_Estate and Unknown
model1 = lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model2 = lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model3 = lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model4 = lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model5 = lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)

#Winsorization to remove the bottom 1% and top 99% CARs - capping outliers
df$CAR_10_wins <- Winsorize(df$`[-10, 10]`, val = quantile(df$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_7_wins  <- Winsorize(df$`[-7, 7]`, val = quantile(df$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_5_wins  <- Winsorize(df$`[-5, 5]`, val = quantile(df$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_3_wins  <- Winsorize(df$`[-3, 3]`, val = quantile(df$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_1_wins  <- Winsorize(df$`[-1, 1]`, val = quantile(df$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))

#Winsorized
model1 = lm(CAR_10_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model2 = lm(CAR_7_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model3 = lm(CAR_5_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model4 = lm(CAR_3_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)
model5 = lm(CAR_1_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + Margin + DtoE + Hybrid + Size + Cash_and_Equivalents + TargetAsset + TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology, df)


"""models = list(
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


