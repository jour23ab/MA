###Multiple Regression
current_dir <- this.path::this.dir()
setwd(current_dir)

source("data_prep.R")
df <- load_clean_data()

#Creating the Crisis variable based on the provided intervals from the vstoxx sensitivity analysis
#100EMA and 23 threshold. Model A.
'crisis_periods = list(
  c(as.Date("2008-01-25"), as.Date("2011-04-14")),
  c(as.Date("2011-07-15"), as.Date("2012-11-23")),
  c(as.Date("2015-06-30"), as.Date("2016-09-06")),
  c(as.Date("2020-03-17"), as.Date("2021-03-15")),
  c(as.Date("2022-02-22"), as.Date("2023-01-12"))
)'
'#100EMA and 24 threshold. Model B
crisis_periods = list(
  c(as.Date("2008-02-05"), as.Date("2008-05-23")),
  c(as.Date("2008-07-11"), as.Date("2011-01-14")),
  c(as.Date("2011-08-04"), as.Date("2012-10-25")),
  c(as.Date("2015-08-31"), as.Date("2016-08-18")),
  c(as.Date("2020-03-18"), as.Date("2021-02-11")),
  c(as.Date("2022-02-28"), as.Date("2022-12-27"))
)'

'#100 EMA and 26 threshold. Model C
crisis_periods = list(
  c(as.Date("2008-03-10"), as.Date("2008-04-22")),
  c(as.Date("2008-09-26"), as.Date("2010-03-04")),
  c(as.Date("2010-05-12"), as.Date("2010-10-29")),
  c(as.Date("2011-08-11"), as.Date("2012-09-13")),
  c(as.Date("2015-08-31"), as.Date("2016-08-18")),
  c(as.Date("2016-01-28"), as.Date("2016-04-18")),
  c(as.Date("2016-06-20"), as.Date("2016-07-20")),
  c(as.Date("2020-03-19"), as.Date("2020-12-04")),
  c(as.Date("2022-03-08"), as.Date("2022-11-22"))
)'

#100 EMA and 27 threshold. Model D.
'crisis_periods = list(
  c(as.Date("2008-10-02"), as.Date("2010-01-05")),
  c(as.Date("2010-05-18"), as.Date("2010-10-13")),
  c(as.Date("2011-08-16"), as.Date("2012-08-14")),
  c(as.Date("2016-02-11"), as.Date("2016-03-22")),
  c(as.Date("2020-03-20"), as.Date("2020-11-20")),
  c(as.Date("2022-03-11"), as.Date("2022-08-11")),
  c(as.Date("2022-09-29"), as.Date("2022-11-09"))
)'

#50 EMA and 25 threshold. Model E
'crisis_periods = list(
  c(as.Date("2008-01-30"), as.Date("2008-05-02")),
  c(as.Date("2008-09-17"), as.Date("2010-03-08")),
  c(as.Date("2010-05-06"), as.Date("2010-10-20")),
  c(as.Date("2011-08-04"), as.Date("2012-09-13")),
  c(as.Date("2015-08-31"), as.Date("2015-11-02")),
  c(as.Date("2016-01-13"), as.Date("2016-04-20")),
  c(as.Date("2016-06-15"), as.Date("2016-07-26")),
  c(as.Date("2020-03-12"), as.Date("2020-12-01")),
  c(as.Date("2022-02-23"), as.Date("2022-11-22"))
)'

#75 EMA and 25 threshold. Model F.
crisis_periods = list(
  c(as.Date("2008-02-07"), as.Date("2008-05-07")),
  c(as.Date("2008-09-18"), as.Date("2010-03-15")),
  c(as.Date("2010-05-07"), as.Date("2010-12-09")),
  c(as.Date("2011-08-08"), as.Date("2012-09-19")),
  c(as.Date("2015-09-03"), as.Date("2015-11-05")),
  c(as.Date("2016-01-14"), as.Date("2016-05-10")),
  c(as.Date("2016-06-15"), as.Date("2016-07-29")),
  c(as.Date("2020-03-16"), as.Date("2020-12-09")),
  c(as.Date("2022-03-01"), as.Date("2022-11-29"))
)

#125EMA and 25 threshold. Model G.
'crisis_periods = list(
  c(as.Date("2008-03-05"), as.Date("2008-05-06")),
  c(as.Date("2008-09-22"), as.Date("2010-04-01")),
  c(as.Date("2010-05-05"), as.Date("2010-12-21")),
  c(as.Date("2011-08-10"), as.Date("2012-10-15")),
  c(as.Date("2015-09-15"), as.Date("2015-11-03")),
  c(as.Date("2016-01-15"), as.Date("2016-08-08")),
  c(as.Date("2020-03-23"), as.Date("2021-01-14")),
  c(as.Date("2022-03-08"), as.Date("2022-12-14"))
)'


#150 EMA and 25 threshold. Model H.
'crisis_periods = list(
  c(as.Date("2008-03-17"), as.Date("2008-04-28")),
  c(as.Date("2008-09-24"), as.Date("2011-01-10")),
  c(as.Date("2011-08-10"), as.Date("2012-10-30")),
  c(as.Date("2015-09-24"), as.Date("2015-10-28")),
  c(as.Date("2016-01-18"), as.Date("2016-08-09")),
  c(as.Date("2020-03-26"), as.Date("2021-02-04")),
  c(as.Date("2022-03-10"), as.Date("2022-12-20"))
)'

df$AnnouncementDate <- as.Date(df$`M&A Announced Date`)
is_in_crisis <- function(date, intervals) {
  any(sapply(intervals, function(interval) date >= interval[1] & date <= interval[2]))
}
df$Crisis <- sapply(df$AnnouncementDate, is_in_crisis, intervals = crisis_periods)
df$Crisis <- as.integer(df$Crisis)  # convert TRUE/FALSE to 1/0

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


#Extract robust standard errors
se_list <- list(
  sqrt(diag(hccm(model1, type = "hc0"))),
  sqrt(diag(hccm(model2, type = "hc0"))),
  sqrt(diag(hccm(model3, type = "hc0"))),
  sqrt(diag(hccm(model4, type = "hc0"))),
  sqrt(diag(hccm(model5, type = "hc0")))
)

#Generate output
stargazer(model1, model2, model3,model4, model5, 
          type = "text", title = "Regression Results",
          se = se_list)


binary_vars <- c("Cash", "Stock", "Private", "CrossBorder", "Diversification", "Crisis")
for(var in binary_vars) {
  cat("\n\n", var, "\n")
  print(table(df[[var]]))
}