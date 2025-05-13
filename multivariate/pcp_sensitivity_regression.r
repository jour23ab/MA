library(readxl)
library(car)
library(sandwich)
library(lmtest)
library(stargazer)
library(DescTools)

# Set working directory
current_dir <- this.path::this.dir()
setwd(current_dir)

# Load dataset
excel_path <- file.path(dirname(current_dir), "data/final", "pcp_sensitivity_dataset.xlsx")
df <- read_excel(excel_path)

# Winsorization to remove the bottom 1% and top 99% CARs - capping outliers
df$CAR_10_wins <- Winsorize(df$`[-10, 10]`, val = quantile(df$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_7_wins  <- Winsorize(df$`[-7, 7]`, val = quantile(df$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_5_wins  <- Winsorize(df$`[-5, 5]`, val = quantile(df$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_3_wins  <- Winsorize(df$`[-3, 3]`, val = quantile(df$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_1_wins  <- Winsorize(df$`[-1, 1]`, val = quantile(df$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))


# Use winsorized column names
car_windows <- list("10" = "CAR_10_wins",
                    "7"  = "CAR_7_wins",
                    "5"  = "CAR_5_wins",
                    "3"  = "CAR_3_wins",
                    "1"  = "CAR_1_wins")

# Define time horizons
horizons <- c("1", "2", "3", "4", "5")

# Model and SE storage
model_list <- list()
robust_results <- list()

# Loop: group by horizon
for (h in horizons) {
  for (ew in names(car_windows)) {
    car_var <- car_windows[[ew]]
    pcp_var <- paste0("pcp_", ew, "d_", h, "yr")
    model_name <- paste0("model_", ew, "d_", h, "y")
    
    formula_str <- paste0(car_var, " ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + ",
                          pcp_var, " + GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread")
    
    model <- lm(as.formula(formula_str), data = df)
    model_list[[model_name]] <- model
    robust_results[[model_name]] <- sqrt(diag(vcovHC(model, type = "HC0")))
    
    model_key <- paste0("model_", ew, "d_", h, "y")
    
    if (!is.null(model_list[[model_key]]) && !is.null(robust_results[[model_key]])) {
      models[[length(models) + 1]] <- model_list[[model_key]]
      se_list[[length(se_list) + 1]] <- robust_results[[model_key]]
    } else {
      cat("⚠️  Skipping missing model:", model_key, "\n")
    }
    
  }
}


# Generate one Stargazer table per horizon with event windows side by side
for (h in horizons) {
  models <- list()
  se_list <- list()
  
  for (w in car_windows) {
    name <- paste0("model_", w, "d_", h, "y")
    models[[length(models) + 1]] <- model_list[[name]]
    se_list[[length(se_list) + 1]] <- robust_results[[name]]
  }
  
  cat("\n\n==================== Stargazer Output for PCP Horizon:", h, "year(s) ====================\n")
  stargazer(models,
            type = "text",
            title = paste("Regression Results with", h, "Year PCP Horizon"),
            column.labels = paste0(car_windows, "d CAR"),
            se = se_list,
            omit.stat = c("f", "ser"),
            digits = 3)
}
