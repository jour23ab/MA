current_dir <- this.path::this.dir()
setwd(current_dir)

source("data_prep.R")
df <- load_clean_data()

#Plotting returns for raw data
# Calculate the 1st and 99th percentiles
lower <- quantile(df$`[-10, 10]`, probs = 0.01, na.rm = TRUE)
upper <- quantile(df$`[-10, 10]`, probs = 0.99, na.rm = TRUE)
interval_text <- sprintf("Most observations lie between %.2f and %.2f", lower, upper)
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
  annotate("text", x = mean(c(lower, upper)), y = 0.05, label = interval_text, size = 4, hjust = 0.5) +
  xlim(-10, 10) +
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
                 bins = 50, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-1, 1]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-1, 1]`, na.rm = TRUE)), color = "red") +
  xlim(-6, 6) +  # adjust to show full conceptual range
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
ggplot(df, aes(x = CAR_10_wins, fill = factor(Cash))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Cash Payment",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Cash") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = CAR_10_wins, fill = factor(Private))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Listing Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Private") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = CAR_10_wins, fill = factor(CrossBorder))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Abnormal Returns by Cross-Border Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "CrossBorder") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = CAR_10_wins, fill = factor(Diversification))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Diversification Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Diversification") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = CAR_10_wins, fill = factor(Crisis))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Crisis Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Crisis") +
  xlim(-10, 10) +
  theme_minimal()

#Plotting CARs by the 50-50 split in MtoB
# Create MtoB category variable (e.g., tertiles)
df$MtoB_group <- cut(df$MtoB,
                     breaks = quantile(df$MtoB, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE),
                     labels = c("Low", "Medium", "High"),
                     include.lowest = TRUE)

# Plot CARs by MtoB group
ggplot(df, aes(x = `[-10, 10]`, fill = MtoB_group)) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by MtoB Group",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "MtoB Group") +
  xlim(-10, 10) +
  theme_minimal()

