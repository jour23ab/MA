###Multiple Regression
current_dir <- this.path::this.dir()
setwd(current_dir)

source("data_prep.R")
df <- load_clean_data()

#cut of the data to check changes in some coefficients
#df <- df[df$`M&A Announced Date` <= "2015-12-31", ]

#Winsorization to remove the bottom 1% and top 99% CARs - capping outliers
df$CAR_10_wins <- Winsorize(df$`[-10, 10]`, val = quantile(df$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_7_wins  <- Winsorize(df$`[-7, 7]`, val = quantile(df$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_5_wins  <- Winsorize(df$`[-5, 5]`, val = quantile(df$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_3_wins  <- Winsorize(df$`[-3, 3]`, val = quantile(df$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_1_wins  <- Winsorize(df$`[-1, 1]`, val = quantile(df$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))

#Winsorized
model1 = lm(CAR_10_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP10 +
              GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model2 = lm(CAR_7_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP7 +
              GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model3 = lm(CAR_5_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP5 +
              GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model4 = lm(CAR_3_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP3 +
              GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model5 = lm(CAR_1_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP1 +
              GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

# Trimming to remove the bottom 1% and top 1% CARs - dropping outliers
df_10 <- df[df$`[-10, 10]` >= quantile(df$`[-10, 10]`, 0.01, na.rm = TRUE) & 
              df$`[-10, 10]` <= quantile(df$`[-10, 10]`, 0.99, na.rm = TRUE), ]

df_7 <- df[df$`[-7, 7]` >= quantile(df$`[-7, 7]`, 0.01, na.rm = TRUE) & 
             df$`[-7, 7]` <= quantile(df$`[-7, 7]`, 0.99, na.rm = TRUE), ]

df_5 <- df[df$`[-5, 5]` >= quantile(df$`[-5, 5]`, 0.01, na.rm = TRUE) & 
             df$`[-5, 5]` <= quantile(df$`[-5, 5]`, 0.99, na.rm = TRUE), ]

df_3 <- df[df$`[-3, 3]` >= quantile(df$`[-3, 3]`, 0.01, na.rm = TRUE) & 
             df$`[-3, 3]` <= quantile(df$`[-3, 3]`, 0.99, na.rm = TRUE), ]

df_1 <- df[df$`[-1, 1]` >= quantile(df$`[-1, 1]`, 0.01, na.rm = TRUE) & 
             df$`[-1, 1]` <= quantile(df$`[-1, 1]`, 0.99, na.rm = TRUE), ]

# Run models on trimmed data
model1_trim <- lm(`[-10, 10]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP10 +
                    GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, data = df_10)

model2_trim <- lm(`[-7, 7]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP7 +
                    GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, data = df_7)

model3_trim <- lm(`[-5, 5]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP5 +
                    GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, data = df_5)

model4_trim <- lm(`[-3, 3]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP3 +
                    GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, data = df_3)

model5_trim <- lm(`[-1, 1]` ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP1 +
                    GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, data = df_1)


#TS_Consumer_Discretionary + TS_Consumer_Staples + TS_Financials + TS_Industrials + TS_Information_Technology +
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



#Extract robust standard errors for the trimmed version
se_list <- list(
  sqrt(diag(hccm(model1_trim, type = "hc0"))),
  sqrt(diag(hccm(model2_trim, type = "hc0"))),
  sqrt(diag(hccm(model3_trim, type = "hc0"))),
  sqrt(diag(hccm(model4_trim, type = "hc0"))),
  sqrt(diag(hccm(model5_trim, type = "hc0")))
)

#df <- df[-c(70, 130), ]

#Generate output
stargazer(model1_trim, model2_trim, model3_trim, model4_trim, model5_trim, 
          type = "text", title = "Regression Results",
          se = se_list)

library(writexl)

df_used_model1 <- model1_trim$model

# Define path
excel_path <- file.path(dirname(current_dir), "data/final", "model1_trim_used_data.xlsx")

write_xlsx(df_used_model1, path = excel_path)