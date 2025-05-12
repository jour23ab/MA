##########################################################################################################
# Packages
#install.packages("stargazer")
#install.packages("ggfortify")
#install.packages("forecast")
#install.packages("urca")
#install.packages("strucchange")
#install.packages("timetk")
#install.packages("readr")
#install.packages("dplyr")
#install.packages("tidyr")
#install.packages("readxl")
#install.packages("corrplot")
#install.packages("sandwich")
#install.packages("ggplot2")
#install.packages("dynlm")
#install.packages("this.path")
#install.packages("DescTools")
#install.packages("fuzzyjoin")
#install.packages("openxlsx")

##########################################################################################################
# Clearing console
cat("\014")
# Clear environment
rm(list = ls())
# Clear figures
graphics.off()
############################################## Load packages
library(this.path)
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
library(fuzzyjoin)
library(lubridate)

####################################### Set working directory
current_dir <- this.path::this.dir()
setwd(current_dir)

print(getwd())

##########################################################################################################
#Loading data
#data=read_xlsx("CAR_analysis_COMPARISON_with_target_type.xlsx")
#data=read_xlsx("CAR_v2.xlsx")

# Load Excel file from sibling folder 'dataprocessed'
excel_path <- file.path(dirname(current_dir), "data/final/", "FINAL_CAR_with_gpdg_pcp.xlsx")

data <- read_xlsx(excel_path)

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
df$CashAndEquivalents <- as.numeric(df$`Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)`)
df$Size <- as.numeric(df$`Total Transaction Value (€EURmm, Historical rate)`)
df$debt_lag1_tgt <- as.numeric(df$`debt_lag1_tgt`)
df$BookEquity <- rowSums(
  df[, c("CommonEquity", "PreferredEquity")], #Removed , "MinorityInterest"
  na.rm = TRUE
)

df <- df %>%
  mutate(
    MtoB = ifelse(BookEquity != 0, MarketCap / BookEquity, NA), #Not sure if i should include minority.
    DtoE = ifelse(BookEquity != 0, Debt / BookEquity, NA)
  )

###Removing observations
#Removing Target type unknown since we need target firm observations to be either public or private
# Removing unknown method of payment since we only have 1 observation.
df <- df %>%
  filter(`Target Type` != "Unknown",
         `Unknown` != 1)

#Renaming variables
df <- df %>%
  rename(
    BullBearSpread = `Bull_Bear_Spread`,
    PCP10 = `running_positive_CAR_percentage_10`,
    PCP7 = `running_positive_CAR_percentage_7`,
    PCP5 = `running_positive_CAR_percentage_5`,
    PCP3 = `running_positive_CAR_percentage_3`,
    PCP1 = `running_positive_CAR_percentage_1`,
    GDPG = `gdp_lag1_tgt`,
  )

#Testing different relative ratios
df$StoMC = df$Size / df$MarketCap
#df$StoE = df$Size / df$BookEquity
df$StoC = df$Size / df$CashAndEquivalents
#Reformatting from million to billion
df$MarketCap = df$MarketCap / 1000
df$Size = df$Size / 1000
df$CashAndEquivalents = df$CashAndEquivalents / 1000
df$TotalAssets = df$TotalAssets / 1000

#Creating more control variables
df$Margin = df$EBITDA / df$Revenue

# One-hot encode target sector
target_dummies <- model.matrix(~ `Primary Sector [Target/Issuer]` - 1, data = df)

# Extract just the sector name from the column and clean it
clean_names <- sub(".*\\]", "", colnames(target_dummies))             # remove everything before ]
clean_names <- gsub("[`'\"]", "", clean_names)                        # remove backticks, quotes
clean_names <- gsub("\\s+", "_", clean_names)                       # optional: replace spaces with underscores

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
vars <- c("Cash", "Private", "CrossBorder", "Diversification",
"MtoB", "Crisis", "PCP10", "PCP7", "PCP3", "PCP1", "GDPG",
"Margin", "DtoE", "Hybrid", "Stock", "Size", "CashAndEquivalents", "TargetAsset", "Public", "BullBearSpread")


setdiff(vars, colnames(df))
df_subset = df[, vars]
df_subset = df_subset[sapply(df_subset, is.numeric)]
cor_matrix <- cor(df_subset, use = "pairwise.complete.obs")
corrplot(cor_matrix, method = "color", type = "lower", tl.cex = 0.5, number.cex = 0.5, addCoef.col = "black")

#Subsetting the data to remove NA values in specified columns
df <- df %>%
  filter(if_all(c("[-10, 10]", "[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]", 
                  "Cash", "Private", "CrossBorder", "Diversification", "MtoB", 
                  "Crisis", "PCP10", "PCP7", "PCP5", "PCP3", "PCP1", "GDPG", 
                  "Margin", "DtoE", "Hybrid", "Stock", "Size", "CashAndEquivalents", 
                  "TargetAsset", "Public", "BullBearSpread"),
                ~ !is.na(.)))

#Printing the number of observations for binary variables
#for (var in c("Cash", "Private", "CrossBorder", "Diversification", "Crisis")) {
 # cat(var, ": ", sum(df[[var]]), "\n")
#}

#Checking correlations of independent variables with some regressors
vars <- c("[-10, 10]","[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]",
"Cash", "Private", "CrossBorder", "Diversification",
"MtoB", "Crisis", "PCP10", "PCP7", "PCP3", "PCP1", "GDPG",
"Margin", "DtoE", "Hybrid", "Stock", "Size", "CashAndEquivalents", "TargetAsset", "Public", "BullBearSpread")


setdiff(vars, colnames(df))
df_subset = df[, vars]
df_subset = df_subset[sapply(df_subset, is.numeric)]
cor_matrix <- cor(df_subset, use = "pairwise.complete.obs")
corrplot(cor_matrix, method = "color", type = "lower", tl.cex = 0.5, number.cex = 0.5, addCoef.col = "black")

load_clean_data <- function() {
  return(df)
}

library(openxlsx)

# Define path
#excel_path <- file.path(dirname(current_dir), "data/final", "data_prepped_FINAL_CAR_gpdg_pcp.xlsx")

# Write DataFrame to Excel
#df <- df[!is.na(df[["[-10, 10]"]]), ]
#write.xlsx(df, file = excel_path)



