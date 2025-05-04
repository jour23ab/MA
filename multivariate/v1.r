###Multiple Regression
current_dir <- this.path::this.dir()
setwd(current_dir)

source("data_prep.R")
df <- load_clean_data()

#cut of the data to check changes in some coefficients
#df <- df[df$`M&A Announced Date` <= "2015-12-31", ]

df$car_10_default <- df$`[-10, 10]`
df$car_7_default <- df$`[-7, 7]`
df$car_5_default <- df$`[-5, 5]`
df$car_3_default <- df$`[-3, 3]`
df$car_1_default <- df$`[-1, 1]`

#default model for getting the residual plots to test for meeting the assumptions of regression analysis.
model1_default = lm(car_10_default ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP10 +
                GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model2_default = lm(car_7_default ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP7 +
                GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model3_default = lm(car_5_default ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP5 +
                GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model4_default = lm(car_3_default ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP3 +
                GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

model5_default = lm(car_1_default ~ Cash + Private + CrossBorder + Diversification + MtoB + Crisis + PCP1 +
                GDPG + Margin + DtoE + Hybrid + Size + CashAndEquivalents + TargetAsset + BullBearSpread, df)

print(summary(model1_default))


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



# === Save residual diagnostic plots for both winsorized and trimmed models ===

# Create output directories
winsor_plot_dir <- file.path(dirname(current_dir), "multivariate", "residual_plots_winsorized")
trimmed_plot_dir <- file.path(dirname(current_dir), "multivariate", "residual_plots_trimmed")
default_plot_dir <- file.path(dirname(current_dir), "multivariate", "residual_plots_default")

dir.create(winsor_plot_dir, showWarnings = FALSE)
dir.create(trimmed_plot_dir, showWarnings = FALSE)
dir.create(default_plot_dir, showWarnings = FALSE)

# Named lists of models
winsor_models <- list(
  model1 = model1,
  model2 = model2,
  model3 = model3,
  model4 = model4,
  model5 = model5
)

trimmed_models <- list(
  model1_trim = model1_trim,
  model2_trim = model2_trim,
  model3_trim = model3_trim,
  model4_trim = model4_trim,
  model5_trim = model5_trim
)

default_models <- list(
  model1_default = model1_default,
  model2_default = model2_default,
  model3_default = model3_default,
  model4_default = model4_default,
  model5_default = model5_default
)

# Function to generate plots
save_diagnostic_plots <- function(models, output_dir) {
  for (model_name in names(models)) {
    model <- models[[model_name]]
    plot_path <- file.path(output_dir, paste0(model_name, "_residuals.png"))

    png(filename = plot_path, width = 800, height = 800)
    par(mfrow = c(2, 2))
    plot(model)
    par(mfrow = c(1, 1))
    dev.off()
  }
}

# Generate plots for each model set
save_diagnostic_plots(winsor_models, winsor_plot_dir)
save_diagnostic_plots(trimmed_models, trimmed_plot_dir)
save_diagnostic_plots(default_models, default_plot_dir)









library(writexl)

df_used_model1 <- model1_trim$model

# Define path
excel_path <- file.path(dirname(current_dir), "data/final", "model1_trim_used_data.xlsx")

write_xlsx(df_used_model1, path = excel_path)

