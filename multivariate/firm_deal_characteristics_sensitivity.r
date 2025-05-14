###Multiple Regression
current_dir <- this.path::this.dir()
setwd(current_dir)

source("data_prep.R")
df <- load_clean_data()

#------Checking the range of firm and deal characteristics-------

# Define variables of interest
vars_to_check <- c("MtoB", "Size", "Margin", "MarketCap", "DtoE")
df$MarketCap <- df$MarketCap / 1000 #Convert to trillions of Euros for easier interpretation
#1. Summary Statistics + Quantiles
summary_stats <- df %>%
  select(all_of(vars_to_check)) %>%
  summarise(across(everything(), list(
    min = ~min(., na.rm = TRUE),
    q01 = ~quantile(., 0.01, na.rm = TRUE),
    q05 = ~quantile(., 0.05, na.rm = TRUE),
    q10 = ~quantile(., 0.10, na.rm = TRUE),
    median = ~median(., na.rm = TRUE),
    mean = ~mean(., na.rm = TRUE),
    q90 = ~quantile(., 0.90, na.rm = TRUE),
    q95 = ~quantile(., 0.95, na.rm = TRUE),
    q99 = ~quantile(., 0.99, na.rm = TRUE),
    max = ~max(., na.rm = TRUE),
    sd = ~sd(., na.rm = TRUE)
  ), .names = "{.col}__{.fn}"))  # Use double underscore to avoid splitting errors

# Reshape to long format (Variable and Statistic columns)
summary_stats_long <- summary_stats %>%
  pivot_longer(cols = everything(), names_to = "VarStat", values_to = "Value") %>%
  separate(VarStat, into = c("Variable", "Statistic"), sep = "__") %>%
  pivot_wider(names_from = "Statistic", values_from = "Value")

quantile_stats <- summary_stats_long %>%
  select(Variable, q01, q05, q10, q90, q95, q99)
central_stats <- summary_stats_long %>%
  select(Variable, min, mean, median, max, sd)

print(quantile_stats)
print(central_stats)

#2. Boxplots for Visual Outlier Detection

# MtoB
ggplot(df, aes(y = MtoB)) +
  geom_boxplot(fill = "lightblue", outlier.color = "red") +
  labs(title = "Boxplot of MtoB", y = "MtoB") +
  theme_minimal()

# Size of deal
ggplot(df, aes(y = Size)) +
  geom_boxplot(fill = "lightblue", outlier.color = "red") +
  labs(title = "Boxplot of Deal Size", y = "Size (Billions)") +
  theme_minimal()

# EBITDA Margin
ggplot(df, aes(y = Margin)) +
  geom_boxplot(fill = "lightblue", outlier.color = "red") +
  labs(title = "Boxplot of EBITDA Margin", y = "EBITDA Margin (in decimals)") +
  theme_minimal()

# MarketCap
ggplot(df, aes(y = MarketCap)) +
  geom_boxplot(fill = "lightblue", outlier.color = "red") +
  labs(title = "Boxplot of Market Cap", y = "Market Cap (Billions)") +
  theme_minimal()

# DtoE
ggplot(df, aes(y = DtoE)) +
  geom_boxplot(fill = "lightblue", outlier.color = "red") +
  labs(title = "Boxplot of Debt-to-Equity", y = "Debt-to-Equity") +
  theme_minimal()


#3. Histogram or Density Plot
ggplot(df, aes(x = MtoB)) +
  geom_density(fill = "steelblue", alpha = 0.4, adjust = 1.5) +
  labs(title = "Density Plot of Acquirer Market-to-Book Ratio",
       x = "Market-to-Book",
       y = "Density") +
  theme_minimal()

ggplot(df, aes(x = Size)) +
  geom_density(fill = "steelblue", alpha = 0.4, adjust = 1.5) +
  labs(title = "Density Plot of Deal Size (Billions)",
       x = "Size",
       y = "Density") +
  theme_minimal()

ggplot(df, aes(x = Margin)) +
  geom_density(fill = "steelblue", alpha = 0.4, adjust = 1.5) +
  labs(title = "Density Plot of EBITDA Margin",
       x = "Margin",
       y = "Density") +
  theme_minimal()

ggplot(df, aes(x = MarketCap)) +
  geom_density(fill = "steelblue", alpha = 0.4, adjust = 1.5) +
  labs(title = "Density Plot of Market Cap (Billions)",
       x = "Market Cap",
       y = "Density") +
  theme_minimal()

ggplot(df, aes(x = DtoE)) +
  geom_density(fill = "steelblue", alpha = 0.4, adjust = 1.5) +
  labs(title = "Density Plot of Debt-to-Equity",
       x = "Debt-to-Equity",
       y = "Density") +
  theme_minimal()

#### Checking negative values in Margin
# Identify observations
df$negative <- df$Margin < -1

summary <- df %>%
  group_by(Crisis) %>%
  summarise(
    total_obs = n(),
    negative_obs = sum(negative, na.rm = TRUE)
  ) %>%
  mutate(negative_pct = 100 * negative_obs / total_obs)

# Replace Crisis indicator with labels for readability
summary$Crisis <- ifelse(summary$Crisis == 1, "Crisis", "Non-crisis")

# Print summary
print(summary)


# Removing all outliers to begin with.
clean_outliers_trimmed <- function(data) {
  n_original <- nrow(data)
  
  #1. Trim EBITDA Margin < -100%
  data_step1 <- data %>% filter(Margin >= -1)
  n_step1 <- nrow(data_step1)
  
  #2. Remove negative MtoB
  data_step2 <- data_step1 %>% filter(MtoB >= 0)
  n_step2 <- nrow(data_step2)
  
  #3. Trim MtoB outside [1%, 99%]
  mtoB_q01 <- quantile(data_step2$MtoB, 0.01, na.rm = TRUE)
  mtoB_q99 <- quantile(data_step2$MtoB, 0.99, na.rm = TRUE)
  data_step3 <- data_step2 %>% filter(MtoB >= mtoB_q01, MtoB <= mtoB_q99)
  n_step3 <- nrow(data_step3)
  
  #4. Trim Size outside [1%, 99%]
  rs_q01 <- quantile(data_step3$Size, 0.01, na.rm = TRUE)
  rs_q99 <- quantile(data_step3$Size, 0.99, na.rm = TRUE)
  data_step4 <- data_step3 %>% filter(Size >= rs_q01, Size <= rs_q99)
  n_step4 <- nrow(data_step4)
  
  #5. Trim MarketCap outside [1%, 99%]
  mc_q01 <- quantile(data_step4$MarketCap, 0.01, na.rm = TRUE)
  mc_q99 <- quantile(data_step4$MarketCap, 0.99, na.rm = TRUE)
  data_step5 <- data_step4 %>% filter(MarketCap >= mc_q01, MarketCap <= mc_q99)
  n_ste p5 <- nrow(data_step5)
  
  #6. Remove negative DtoE and trim at [99%]
  data_step6 <- data_step5 %>% filter(DtoE >= 0)
  dte_q99 <- quantile(data_step6$DtoE, 0.99, na.rm = TRUE)
  data_final <- data_step6 %>% filter(DtoE <= dte_q99)
  n_final <- nrow(data_final)
  
  cat("Observation count summary:\n")
  cat("Original data:           ", n_original, "\n")
  cat("After trimming Margin:   ", n_step1, " (Removed:", n_original - n_step1, ")\n")
  cat("After removing MtoB < 0: ", n_step2, " (Removed:", n_step1 - n_step2, ")\n")
  cat("After trimming MtoB:     ", n_step3, " (Removed:", n_step2 - n_step3, ")\n")
  cat("After trimming Size:     ", n_step4, " (Removed:", n_step3 - n_step4, ")\n")
  cat("After trimming MCap:     ", n_step5, " (Removed:", n_step4 - n_step5, ")\n")
  cat("After trimming DtoE:     ", n_final, " (Removed:", n_step5 - n_final, ")\n")
  cat("Total observations removed: ", n_original - n_final, "\n")
  
  return(data_final)
}
df_trimmed <- clean_outliers_trimmed(df)
#summary of df_trimmed

df<- df_trimmed

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

binary_vars <- c("Cash", "Stock", "Private", "CrossBorder", "Diversification", "Crisis", "TargetAsset")
for(var in binary_vars) {
  cat("\n\n", var, "\n")
  print(table(df[[var]]))
}

#Export the trimmed dataframe with trimmed characteristics to Excel
#Commmenting out so we don't overwrite the original data each time this script is run
#excel_path <- file.path(dirname(current_dir), "data/final", "df_trimmed_characteristics.xlsx")
#write.xlsx(df, file = excel_path)
