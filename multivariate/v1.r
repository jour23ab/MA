library(readxl)
library(car)
library(sandwich)
library(lmtest)
library(DescTools)

# Set working directory
current_dir <- this.path::this.dir()
setwd(current_dir)

# Load dataset
excel_path <- file.path(dirname(current_dir), "data/final", "pcp_sensitivity_dataset.xlsx")
df <- read_excel(excel_path)

# Winsorize each CAR variable manually
df$CAR_10_wins <- Winsorize(df$`[-10, 10]`, val = quantile(df$`[-10, 10]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_7_wins <- Winsorize(df$`[-7, 7]`, val = quantile(df$`[-7, 7]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_5_wins <- Winsorize(df$`[-5, 5]`, val = quantile(df$`[-5, 5]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_3_wins <- Winsorize(df$`[-3, 3]`, val = quantile(df$`[-3, 3]`, probs = c(0.01, 0.99), na.rm = TRUE))
df$CAR_1_wins <- Winsorize(df$`[-1, 1]`, val = quantile(df$`[-1, 1]`, probs = c(0.01, 0.99), na.rm = TRUE))

# Define mapping of event windows to column names
car_windows <- list(
  "10" = "CAR_10_wins",
  "7"  = "CAR_7_wins",
  "5"  = "CAR_5_wins",
  "3"  = "CAR_3_wins",
  "1"  = "CAR_1_wins"
)

# Define horizons
horizons <- c("1", "2", "3", "4", "5")

# Run models and print grouped results
for (h in horizons) {
  cat("\n==================== PCP Horizon:", h, "Year(s) ====================\n")
  
  for (ew in names(car_windows)) {
    car_var <- car_windows[[ew]]
    pcp_var <- paste0("pcp_", ew, "d_", h, "yr")
    model_label <- paste0("Model: ", ew, "d window, PCP ", h, "y")
    
    # Check if the PCP column exists
    if (!(pcp_var %in% names(df))) {
      cat("\n⚠️  Skipping", model_label, "- PCP variable missing:", pcp_var, "\n")
      next
    }
    
    # Build formula and fit model
    formula_str <- paste0(car_var, " ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + ",
                          pcp_var, " + GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread")
    model <- lm(as.formula(formula_str), data = df)
    
    # Output model with robust SEs
    cat("\n---", model_label, "---\n")
    print(coeftest(model, vcov = vcovHC(model, type = "HC0")))
  }
}
