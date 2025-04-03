###Multiple Regression
source("multivariate/data_prep.R")
df <- load_clean_data()
#Excluded TS_Health_Care because this is perfectly correlated with Diversifcation
#No data for TS_Materials, TS_Real_Estate and Unknown
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


#models = list(
#  model1,
#  model2,
#  model3,
#  model4,
#  model5
#)
#bp_results <- lapply(models, bptest)
#bp_results

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