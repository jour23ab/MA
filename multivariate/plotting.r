#Plotting returns for raw data
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
  xlim(-10, 10) +  # adjust to show full conceptual range
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
                 bins = 30, 
                 fill = "lightblue", 
                 color = "black") +
  geom_density(alpha = 0.5, fill = "lightgreen", adjust = 1.3) +
  labs(title = "Combined Histogram and Density Plot of Abnormal Returns",
       x = "CAR [-1, 1]",
       y = "Density") +
  geom_vline(aes(xintercept = mean(`[-1, 1]`, na.rm = TRUE)), color = "red") +
  xlim(-10, 10) +  # adjust to show full conceptual range
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
ggplot(df, aes(x = `[-10, 10]`, fill = factor(Cash))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Cash Payment",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Cash") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Private))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Listing Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Private") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(CrossBorder))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Abnormal Returns by Cross-Border Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "CrossBorder") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Diversification))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Diversification Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Diversification") +
  xlim(-10, 10) +
  theme_minimal()

ggplot(df, aes(x = `[-10, 10]`, fill = factor(Crisis))) +
  geom_density(alpha = 0.3, adjust = 1.5) +
  labs(title = "Density of Cumulative Abnormal Returns by Crisis Status",
       x = "CAR [-10, 10]",
       y = "Density",
       fill = "Crisis") +
  xlim(-10, 10) +
  theme_minimal()


