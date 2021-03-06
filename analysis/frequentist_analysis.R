---
  title: "exploring the dataset"
author: "Jan-Philipp Fränken"
date: "06/01/2020"
output: html_document
---
  
  ```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)

```

# libraries 
```{r}
library(ggplot2)  
library(car)
library(Hmisc)
library(pwr)
library(heplots)
library(sjstats)
library(dplyr)
library(energy)
library(MASS)
library(mvtnorm)
library(GGally)
library(ggplot2)
library(afex)
library(scatterplot3d)
library(ez)
library(broom)
library(plotly)
library(tidyr)
library(rlang)
library(ggpubr)
library(MuMIn)
```

# getting data 
```{r}
# getting data
m_dat <- read.csv('main_data_formatted.csv')

# transforming cond int into strings for ggplot
for (i in m_dat$cond ) {
  i_str <- toString(i)
  m_dat$cond[i] <- i_str
}
# adding variable describing levels of condition
cond_meaning <- rep(c('independent', 'shared private info', 'sequential updating'),length(m_dat$cond)/3)
m_dat$cond_meaning <- cond_meaning 
head(m_dat)
```
# computing additional metrics 
```{r}
# analytic kl 
kl_divergence <-  function(p, q) {
  kl_f <- function(x) p(x) * log(p(x)) - p(x) * log(q(x))
  val <- integrate(kl_f, lower = 0, upper = 1)
  val$value
}

# analytic kl on a truncated integral to avoid -inf values for 0 mean values 
kl_divergence_truncated <-  function(p, q) {
  kl_f <- function(x) p(x) * log(p(x)) - p(x) * log(q(x))
  val <- integrate(kl_f, lower = 0.01, upper = 0.99)
  val$value
}

# Jensen-Shannon divergence (if a = 0.5, this is the symmetric kl)
js_divergence <- function(p,q,a) {
  kl_1 <- kl_divergence_truncated(p,q)
  kl_2 <- kl_divergence_truncated(q,p)
  jsd <- a * kl_1 + (1 - a) * kl_2
  return(jsd)
}

# proof that functions work and kl changes smoothly as a function of varying parameters : 

# 1) kld and jsd values must be zero here since p and are identical 
p = function(x) dbeta(x,2,2)
q = function(x) dbeta(x,2,2)
kl_divergence_truncated(p, q)
js_divergence(p, q, 0.5)

# 2) showing that kld and jsd change smoothly as a function of changing one parameter 
beta_grid = seq(1, 10, length.out = 100)

kl_grid = rep(0, 100)
js_grid = rep(0,100)

for(i in 1:length(beta_grid)) {
  beta = beta_grid[i]
  p = function(x) dbeta(x, 2, beta)
  q = function(x) dbeta(x, 2, 4)
  kl_grid[i] <- kl_divergence(p, q)
  js_grid[i] <- js_divergence(p, q, 0.5)
}

# plotting kl 
plot(beta_grid, kl_grid, type = 'l')

# plotting jsd 
plot(beta_grid, js_grid, type = 'l')
```

```{r}
# now computing missing metrics (mean, variance, differences, kl, jsd, etc) for subjects 

# getting individual parameters 
prior_a <- m_dat$subj_prior_a
prior_b <- m_dat$subj_prior_b
post_a <- m_dat$subj_post_a
post_b <- m_dat$subj_post_b
conds <- m_dat$cond

# metrics 
klds = rep(0, length(prior_a))
jsds = rep(0, length(prior_a))
post_mean = rep(0, length(prior_a))
post_var = rep(0, length(prior_a))
prior_mean = rep(0, length(prior_a))
prior_var = rep(0, length(prior_a))
mean_diff_prior = rep(0, length(prior_a))
mean_diff_post = rep(0, length(prior_a))
var_diff_prior = rep(0, length(prior_a))
var_diff_post = rep(0, length(prior_a))
klds_prior = rep(0, length(prior_a))
jsds_prior = rep(0, length(prior_a))
klds_post = rep(0, length(prior_a))
jsds_post = rep(0, length(prior_a))

# computing metrics (# numbers in the function are based on the normative parameters from the model)
for(i in 1:length(prior_a)) {
  p = function(x) dbeta(x, prior_a[i], prior_b[i])
  q = function(x) dbeta(x, post_a[i], post_b[i])
  mod_p = function(x) dbeta(x, 2, 2)
  mod_q_1 =  function(x) dbeta(x, 147,66.5)
  mod_q_2 =  function(x) dbeta(x, 124,61.75)
  mod_q_3 =  function(x) dbeta(x, 52,47)
  klds[i] <- kl_divergence_truncated(p, q)
  jsds[i] <- js_divergence(p, q, 0.5)
  post_mean[i] <- (post_a[i] / (post_a[i] + post_b[i]))
  post_var[i] <- (post_a[i] * post_b[i])/((post_a[i] + post_b[i])**2 * (post_a[i]+post_b[i]+1))
  prior_mean[i] <- (prior_a[i] / (prior_a[i] + prior_b[i]))
  prior_var[i] <- (prior_a[i] * prior_b[i])/((prior_a[i] + prior_b[i])**2 * (prior_a[i]+prior_b[i]+1))
  mean_diff_prior[i] <- prior_mean[i] - 0.5
  var_diff_prior[i] <- prior_var[i] - 0.05
  klds_prior[i] <- kl_divergence_truncated(p, mod_p )
  jsds_prior[i] <- js_divergence(p, mod_p, 0.5)
  if (conds[i] == 1) {
    mean_diff_post[i] <- post_mean[i] - 0.6885245901639344
    var_diff_post[i] <- post_var[i] - 0.0009998064284546413
    klds_post[i] <- kl_divergence_truncated(q, mod_q_1)
    jsds_post[i] <- js_divergence(q, mod_q_1, 0.5)
  }
  else if  (conds[i] == 2) {
    mean_diff_post[i] <- post_mean[i] - 0.6675639300134589
    var_diff_post[i] <- post_var[i] - 0.0011883391130304932
    klds_post[i] <- kl_divergence_truncated(q, mod_q_2)
    jsds_post[i] <- js_divergence(q, mod_q_2, 0.5)
  }
  else if (conds[i] == 3) {
    mean_diff_post[i] <- post_mean[i] - 0.5252525252525253
    var_diff_post[i] <- post_var[i] - 0.0024936230996837057
    klds_post[i] <- kl_divergence_truncated(q, mod_q_3)
    jsds_post[i] <- js_divergence(q, mod_q_3, 0.5)
  }
}

# adding metrics to data frame 
m_dat$kld <- klds
m_dat$jsd <- jsds
m_dat$post_mean <- post_mean
m_dat$post_var <- post_var
m_dat$prior_mean <- prior_mean
m_dat$prior_var <- prior_var
m_dat$log_kld <- log(klds)
m_dat$log_jsd <- log(jsds)
m_dat$mean_diff_prior <- mean_diff_prior
m_dat$mean_diff_post <- mean_diff_post
m_dat$var_diff_prior <- var_diff_prior
m_dat$var_diff_post <- var_diff_post
m_dat$kld_prior <- klds_prior
m_dat$kld_post <- klds_post
m_dat$jsd_prior <- jsds_prior
m_dat$jsd_post <- jsds_post
```

# outlier checks 
```{r}
# checking if there is a subject that did not change the slider values, hence log of minus infinity
out_log_jsd <- m_dat$subj_id[which(m_dat$log_jsd == -Inf)]

# removing subject from data frame 
m_dat <- m_dat[which(!(m_dat$subj_id%in%out_log_jsd)),]

# removing subjects with nans (just subject id 9)
m_dat <- m_dat[which(!(m_dat$subj_id == 9)),]
```

# analysis with parametric tests 
```{r}
# creating a compressed data frame based on mean, var, kl, jsd, and log jsd 
c_1_post_mean <- m_dat$post_mean[m_dat$cond == '1']
c_2_post_mean <- m_dat$post_mean[m_dat$cond == '2']
c_3_post_mean <- m_dat$post_mean[m_dat$cond == '3']

c_1_post_var <- m_dat$post_var[m_dat$cond == '1']
c_2_post_var <- m_dat$post_var[m_dat$cond == '2']
c_3_post_var <- m_dat$post_var[m_dat$cond == '3']

c_1_jsd <- m_dat$jsd[m_dat$cond == '1']
c_2_jsd <- m_dat$jsd[m_dat$cond == '2']
c_3_jsd <- m_dat$jsd[m_dat$cond == '3']

c_1_log_jsd <- m_dat$log_jsd[m_dat$cond == '1']
c_2_log_jsd <- m_dat$log_jsd[m_dat$cond == '2']
c_3_log_jsd <- m_dat$log_jsd[m_dat$cond == '3']

c_1_kld <- m_dat$kld[m_dat$cond == '1']
c_2_kld <- m_dat$kld[m_dat$cond == '2']
c_3_kld <- m_dat$kld[m_dat$cond == '3']

mean(m_dat$kld[m_dat$cond == '1'])
mean(m_dat$kld[m_dat$cond == '2'])
mean(m_dat$kld[m_dat$cond == '3'])

mean(m_dat$jsd[m_dat$cond == '1'])
mean(m_dat$jsd[m_dat$cond == '2'])
mean(m_dat$jsd[m_dat$cond == '3'])

jsds <- c(c_1_jsd, c_2_jsd, c_3_jsd)
klds <- c(c_1_kld, c_2_kld, c_3_kld)
log_jsds <-  c(c_1_log_jsd, c_2_log_jsd, c_3_log_jsd)
post_means <- c(c_1_post_mean, c_2_post_mean, c_3_post_mean)
post_vars <- c(c_1_post_var, c_2_post_var, c_3_post_var)
subj <- c(seq(1,length(c_1_jsd)), seq(1,length(c_2_jsd)), seq(1,length(c_3_jsd)))
cond <- rep(c(1,2,3), each = length(jsds)/3)
m_dat_restr <- data.frame(subj,cond, post_means,jsds,klds,post_vars, log_jsds)

m_dat_restr$cond_string <- factor(m_dat_restr$cond, levels = c(1,2,3), labels = c('c1', 'c2','c3'))
m_dat_restr$cond_string <- as.character(m_dat_restr$cond)

# function for getring refression coefficients 
PrepareCoeffDf = function(CoeffDf){
  CoeffDf$coefficient <- rownames(CoeffDf)
  # get rid of the intercept
  CoeffDf <- CoeffDf[which(!CoeffDf$coefficient%in%c("(Intercept)")),]
}

# models 
# model for the mean
mixed_means_minimal <- lmer(post_means ~ 1 + (1|subj), data = m_dat_restr)
mixed_means_maximal <- lmer(log(post_means) ~ cond_string + (1|subj), data = m_dat_restr)
anova(mixed_means_minimal, mixed_means_maximal)
summary(mixed_means_maximal)
leveneTest(residuals(mixed_means_maximal)~m_dat_restr$cond_string)
hist(residuals(mixed_means_maximal))
co_means <- PrepareCoeffDf(data.frame(summary(mixed_means_maximal)$coefficients))
co_means_scaled <- scale(co_means$Estimate)



# model for variance 
mixed_vars_minimal <- lmer(post_vars ~ 1 + (1|subj), data = m_dat_restr)
mixed_vars_maximal <- lmer(post_vars ~ cond_string + (1|subj), data = m_dat_restr)
anova(mixed_vars_minimal,mixed_vars_maximal)
#summary(mixed_vars)
#leveneTest(residuals(mixed_vars)~m_dat_restr$cond_string)
#ist(residuals(mixed_vars))
co_vars <- PrepareCoeffDf(data.frame(summary(mixed_vars_maximal)$coefficients))
co_vars_scaled <- scale(co_vars$Estimate)

# model for log variance 
mixed_vars_log <- lmer(post_means ~ cond_string + (1|subj), data = m_dat_restr)
summary(mixed_vars_log)
leveneTest(residuals(mixed_vars)~m_dat_restr$cond_string)
hist(residuals(mixed_vars))
co_vars <- PrepareCoeffDf(data.frame(summary(mixed_vars)$coefficients))
co_vars_scaled <- scale(co_vars$Estimate)

# model for jsd
mixed_jsds_norm_minimal <- lmer(jsds ~ 1 + (1|subj), data = m_dat_restr)
mixed_jsds_norm_maximal <- lmer(jsds ~ cond_string + (1|subj), data = m_dat_restr)
anova(mixed_jsds_norm_minimal, mixed_jsds_norm_maximal)
summary(mixed_jsds_norm_maximal)
leveneTest(residuals(mixed_jsds_norm)~m_dat_restr$cond_string)
hist(residuals(mixed_jsds_norm))
co_jsd <- PrepareCoeffDf(data.frame(summary(mixed_jsds_norm)$coefficients))
co_jsd_scaled <- scale(co_jsd$Estimate)

# model for log jsd
mixed_jsds_log_minimal <- lmer(log_jsds ~ 1 + (1|subj), data = m_dat_restr)
mixed_jsds_log_maximal <- lmer(log_jsds ~ cond_string + (1|subj), data = m_dat_restr)
anova(mixed_jsds_log_minimal, mixed_jsds_log_maximal)
summary(mixed_jsds_log_maximal)
leveneTest(residuals(mixed_jsds_log)~m_dat_restr$cond_string)
hist(residuals(mixed_jsds_log))
co_jsd_log <- PrepareCoeffDf(data.frame(summary(mixed_jsds_log)$coefficients))
co_jsd_scaled_log <- scale(co_jsd_log$Estimate)

# model for kld
mixed_klds <- lmer(log(klds) ~ cond_string + (1|subj), data = m_dat_restr)
summary(mixed_klds)
leveneTest(residuals(mixed_klds)~m_dat_restr$cond_string)
hist(residuals(mixed_klds))

# BIC of models 
anova(mixed_jsds_log_maximal, mixed_jsds_log_minimal)

# plotting residuals and bics for jsd and log jsd 
m_dat_restr %>% 
  group_by(cond_string) %>% 
  summarise(jsds = mean(jsds)) %>% 
  plot_ly(x=~cond_string, y = ~ jsds)

m_dat_restr %>% 
  group_by(cond_string) %>% 
  summarise(means = mean(post_means)) %>% 
  plot_ly(x=~cond_string, y = ~ means)

cbind(m_dat_restr$jsds,
      m_dat_restr$jsds_pred)

m_dat_restr$jsds_pred = predict(mixed_jsds_norm)
m_dat_restr %>%
  select(cond_string, jsds_pred, jsds) %>% 
  group_by(cond_string) %>% 
  mutate(jsds = scale(jsds), jsds_pred = scale(jsds_pred)) %>% 
  mutate(sq_diff = abs(jsds-jsds_pred)) %>% 
  summarise(mean_sq_diff = mean(sq_diff))%>% 
  summarise(mean = mean(mean_sq_diff))

m_dat_restr$jsds_pred_log = predict(mixed_jsds_log)
m_dat_restr %>%
  select(cond_string, jsds_pred_log, log_jsds) %>% 
  group_by(cond_string) %>% 
  mutate(log_jsds = scale(log_jsds), jsds_pred_log = scale(jsds_pred_log)) %>% 
  mutate(sq_diff = abs(log_jsds-jsds_pred_log)) %>% 
  summarise(mean_sq_diff = mean(sq_diff)) %>% 
  summarise(mean = mean(mean_sq_diff))

# r squared values 
r.squaredGLMM(mixed_jsds_norm)
r.squaredGLMM(mixed_jsds_log)
r.squaredGLMM(mixed_vars)
r.squaredGLMM(mixed_means)

# checking residual plots seperately for homoskedasticity assumption 
res_log_jsd <- residuals(mixed_jsds_log)
plot(density(res_log_jsd))
res_jsd <- residuals(mixed_jsds)
plot(density(res_jsd))
res_mean <- residuals(mixed_means)
plot(density(res_mean))
res_var <- residuals(mixed_vars)
plot(density(residuals(mixed_jsds_log)))
sqrt(mean(m_dat$jsd[m_dat$cond == 3]))


BIC(mixed_klds)
print(mean(log(m_dat$kld[m_dat$cond ==1])))
print(mean(log(m_dat$kld[m_dat$cond ==2])))
print(mean(log(m_dat$kld[m_dat$cond ==3])))

anova(mixed_jsds_log, mixed_jsds_norm, mixed_means, mixed_vars)
summary(mixed_jsds_norm_maximal)


```

# plotting coefficients 
```{r}

co_mixed_means_maximal <- data.frame(summary(mixed_means_maximal)$coefficients)
co_mixed_vars_maximal <- data.frame(summary(mixed_vars_maximal)$coefficients)
co_mixed_jsd_maximal <- data.frame(summary(mixed_jsds_norm_maximal)$coefficients)
co_mixed_logjsd_maximal <- data.frame(summary(mixed_jsds_log_maximal)$coefficients)

# function for getring refression coefficients 
PrepareCoeffDf = function(CoeffDf){
  CoeffDf$coefficient <- rownames(CoeffDf)
  # get rid of the intercept
  CoeffDf <- CoeffDf[which(!CoeffDf$coefficient%in%c("(Intercept)")),]
}

co_mixed_means_maximal <- PrepareCoeffDf(co_mixed_means_maximal)
co_mixed_vars_maximal <- PrepareCoeffDf(co_mixed_vars_maximal)
co_mixed_jsd_maximal <- PrepareCoeffDf(co_mixed_jsd_maximal)
co_mixed_logjsd_maximal <- PrepareCoeffDf(co_mixed_logjsd_maximal)


stdCoeffsM <- co_mixed_means_maximal$Estimate
Predictors <- c("sequential", "shared")
coeffErrM <- co_mixed_means_maximal$Std..Error
coeffDatM <- data.frame(stdCoeffsM, Predictors, coeffErrM)

stdCoeffsV <- co_mixed_vars_maximal$Estimate
Predictors <- c("sequential", "shared")
coeffErrV <- co_mixed_vars_maximal$Std..Error
coeffDatV <- data.frame(stdCoeffsV, Predictors, coeffErrV)

stdCoeffsJ <- co_mixed_jsd_maximal$Estimate
Predictors <- c("sequential", "shared")
coeffErrJ <- co_mixed_jsd_maximal$Std..Error
coeffDatJ <- data.frame(stdCoeffsJ, Predictors, coeffErrJ)

stdCoeffsLJ <- co_mixed_logjsd_maximal$Estimate
Predictors <- c("sequential", "shared")
coeffErrLJ <- co_mixed_logjsd_maximal$Std..Error
coeffDatLJ <- data.frame(stdCoeffsLJ, Predictors, coeffErrLJ)

My_Theme = theme(
  axis.title.x = element_text(size = 14, color = 'black'),
  axis.text.x = element_text(size = 14, color = 'black'),
  axis.title.y = element_text(size = 14, face= 'bold'),
  axis.text.y = element_text(size = 16, color = 'black'),
  plot.title = element_text(size = 14, face= 'bold', color = 'black'))

m_plot<- coeffDatM%>%
  ggplot(aes(x = Predictors, y = stdCoeffsM, color = Predictors)) + 
  geom_point(size = 3, aes(shape = Predictors)) + theme(legend.position = "none") +
  geom_errorbar(aes(ymin=stdCoeffsM-coeffErrM, ymax=stdCoeffsM+coeffErrM), width=.2) + 
  geom_hline(yintercept=0, linetype = 'dashed', colour = 'grey', size = 0.5) + 
  theme_classic() +  
  My_Theme + 
  labs(title = "Posterior Mean", x="", y="") +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_vline(xintercept=5.5, size = 0.5) +
  geom_vline(xintercept=6.5, size = 0.5) + 
  theme(axis.text.x=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.title=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank()) + annotate("text", x = 1, y = -.0475, label = "*", size = 7)
m_plot

v_plot<- coeffDatV%>%
  ggplot(aes(x = Predictors, y = stdCoeffsV, color = Predictors)) + 
  geom_point(size = 3, aes(shape = Predictors)) + theme(legend.position = "none") +
  geom_errorbar(aes(ymin=stdCoeffsV-coeffErrV, ymax=stdCoeffsV+coeffErrV), width=.2) + 
  geom_hline(yintercept=0, linetype = 'dashed', colour = 'grey', size = 0.5) + 
  theme_classic() +  
  My_Theme + 
  labs(title = "Posterior Variance", x="", y="") +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_vline(xintercept=5.5, size = 0.5) +
  geom_vline(xintercept=6.5, size = 0.5) + 
  theme(axis.text.x=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.title=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank()) 
v_plot

j_plot<- coeffDatJ%>%
  ggplot(aes(x = Predictors, y = stdCoeffsJ, color = Predictors)) + 
  geom_point(size = 3, aes(shape = Predictors)) + theme(legend.position = "none") +
  geom_errorbar(aes(ymin=stdCoeffsJ-coeffErrJ, ymax=stdCoeffsJ+coeffErrJ), width=.2) + 
  geom_hline(yintercept=0, linetype = 'dashed', colour = 'grey', size = 0.5) + 
  theme_classic() +  
  My_Theme + 
  labs(title = "JSD", x="", y="") +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_vline(xintercept=5.5, size = 0.5) +
  geom_vline(xintercept=6.5, size = 0.5) + 
  theme(axis.text.x=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.title=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank()) + annotate("text", x = 1, y = -2.325, label = "*", size = 7) 
j_plot

lj_plot<- coeffDatLJ%>%
  ggplot(aes(x = Predictors, y = stdCoeffsLJ, color = Predictors)) + 
  geom_point(size = 3, aes(shape = Predictors)) + theme(legend.position = "none") +
  geom_errorbar(aes(ymin=stdCoeffsLJ-coeffErrLJ, ymax=stdCoeffsLJ+coeffErrLJ), width=.2) + 
  geom_hline(yintercept=0, linetype = 'dashed', colour = 'grey', size = 0.5) + 
  theme_classic() +  
  My_Theme + 
  labs(title = "logJSD", x="", y="") +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_vline(xintercept=5.5, size = 0.5) +
  geom_vline(xintercept=6.5, size = 0.5) + 
  theme(axis.text.x=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.title=element_text(angle=0,margin = margin(0.5, unit = "cm"),vjust =1)) + 
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank()) + annotate("text", x = 1, y = -.905, label = "**", size = 7) +    annotate("text", x = 2, y = -.905, label = "**", size = 7) 
lj_plot
# repeat the above for n plots of interest 

meansPlot  # -0.045
varPlot
jsdPlot # - 2.82
log_jsdPlot


# then create figure combining single plots 
fullFigure <- ggarrange(m_plot, v_plot, j_plot, lj_plot + rremove("x.text"), 
                        labels = c("a)", "b)", "c)","d)"),
                        ncol = 2, nrow = 2)

annotate_figure(fullFigure,
                bottom = text_grob("* = p < 0.05     ** = p < 0.01", color = "black",
                                   hjust = 0.5, x = 0.5, size = 16),
                left = text_grob("Fixed effects coefficients", color = "black", rot = 90, size = 16))

pdf("ggplot.pdf")
print(fullFigure)


```


```{r}


plot(density(residuals(mixed_jsds_norm_maximal)))


# comparing if subjects quantitatively align with model predictions using t tests 
t.test(m_dat$jsd_prior,mu=0, alternative = 'greater')
sd(m_dat$jsd_prior)
t.test(m_dat$mean_diff_prior,mu=0, alternative = 'two.sided')
sd(m_dat$mean_diff_prior)
t.test(m_dat$var_diff_prior,mu=0, alternative = 'two.sided')
sd(m_dat$var_diff_prior)
shapiro.test(m_dat$mean_diff_post)

t.test(m_dat$jsd_post,mu=0, alternative = 'greater')
sd(m_dat$jsd_post)
t.test(m_dat$mean_diff_post,mu=0, alternative = 'two.sided')
sd(m_dat$mean_diff_post)
t.test(m_dat$var_diff_post,mu=0, alternative = 'two.sided')
sd(m_dat$var_diff_post)
hist(m_dat$mean_diff_post)

wilcox.test(m_dat$jsd_prior,mu=0, alternative = 'greater')
wilcox.test(m_dat$var_diff_post,mu=0, alternative = 'two.sided')
wilcox.test(m_dat$mean_diff_post,mu=0, alternative = 'two.sided')
hist(log(m_dat$jsd_post))
```

