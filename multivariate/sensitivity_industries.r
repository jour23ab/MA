##########################################################################################################
# Clearing console
cat("\014")
# Clear environment
rm(list = ls())
# Clear figures
graphics.off()
############################################## Load packages
library(readxl)       # To read the Excel file
library(dplyr)        # For data manipulation (if needed)
library(DescTools)    # For Winsorize function
library(car)          # For hccm() to get robust standard errors
library(sandwich)     # Alternative robust SE estimators (some overlap with car)
library(stargazer)    # To format regression output

####################################### Set working directory
current_dir <- this.path::this.dir()
setwd(current_dir)

print(getwd())

# Load Excel file from sibling folder 'dataprocessed'
excel_path <- file.path(dirname(current_dir), "data/final/", "graph_data.xlsx")
data <- read_xlsx(excel_path)

# Create binary variable for sub-industry
data$Is_PharmaBio <- ifelse(data$`Industry Classifications [Buyers/Investors]` == 
                              "Pharmaceuticals, Biotechnology and Life Sciences (Primary)", 1, 0)

# Rename single variable. This was never winsorized but just name changed for convenience earlier.
data <- data %>%
  rename("[-10, 10]" = CAR_10_wins)

# Winsorize CARs

data$CAR_10_wins <- Winsorize(data$`[-10, 10]`, val = quantile(data$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
data$CAR_7_wins  <- Winsorize(data$`[-7, 7]`, val = quantile(data$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
data$CAR_5_wins  <- Winsorize(data$`[-5, 5]`, val = quantile(data$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
data$CAR_3_wins  <- Winsorize(data$`[-3, 3]`, val = quantile(data$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
data$CAR_1_wins  <- Winsorize(data$`[-1, 1]`, val = quantile(data$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))

# Run models including new control variable
model1 <- lm(CAR_10_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP10 +
               GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread + Is_PharmaBio, data)

model2 <- lm(CAR_7_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP7 +
               GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread + Is_PharmaBio, data)

model3 <- lm(CAR_5_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP5 +
               GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread + Is_PharmaBio, data)

model4 <- lm(CAR_3_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP3 +
               GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread + Is_PharmaBio, data)

model5 <- lm(CAR_1_wins ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP1 +
               GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread + Is_PharmaBio, data)


# Extract robust standard errors (HC0)
se_list <- list(
  sqrt(diag(hccm(model1, type = "hc0"))),
  sqrt(diag(hccm(model2, type = "hc0"))),
  sqrt(diag(hccm(model3, type = "hc0"))),
  sqrt(diag(hccm(model4, type = "hc0"))),
  sqrt(diag(hccm(model5, type = "hc0")))
)

# Output regression table
stargazer(model1, model2, model3, model4, model5, 
          type = "text", title = "Regression Results with Sub-Industry Control",
          se = se_list)

# Create a list of models
models <- list(model1, model2, model3, model4, model5)
model_names <- c("[-10,10]", "[-7,7]", "[-5,5]", "[-3,3]", "[-1,1]")

# Initialize data frame to store results
pharma_results <- data.frame(
  Event_Window = model_names,
  Coefficient = NA,
  Robust_SE = NA,
  T_statistic = NA,
  P_value = NA
)

# Loop through each model and extract values for Is_PharmaBio
for (i in seq_along(models)) {
  mod <- models[[i]]
  se <- sqrt(diag(hccm(mod, type = "hc0")))
  
  coef_val <- coef(mod)["Is_PharmaBio"]
  se_val <- se["Is_PharmaBio"]
  t_stat <- coef_val / se_val
  p_val <- 2 * (1 - pt(abs(t_stat), df = mod$df.residual))
  
  pharma_results$Coefficient[i] <- coef_val
  pharma_results$Robust_SE[i] <- se_val
  pharma_results$T_statistic[i] <- t_stat
  pharma_results$P_value[i] <- p_val
}

# Print the table
print(pharma_results)

