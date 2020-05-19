# restructuring the data of the raw data file into a new data file and plotting the descriptives (i.e. model vs. subj comparison)
# libraries
import numpy as np
import scipy.stats 
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd 
import os
import plotly.graph_objects as go
from statistics import mean, stdev


import orca
os.getcwd()

# getting raw data from csv
bel_updating_dat = pd.read_csv('../data/25_january_main_run.csv')
bel_updating_dat = bel_updating_dat
# dicts for storing data 
subj_trial_dat_dicts = []
subj_demog_dat_dicts = []


# transformation functions for extracting alpha and beta parameters from subjects' belief and confidence
# log transformation of confidence slider 
def log_slider(slid_val):
    slid_val = 1000 - slid_val
    minp = 0
    maxp = 1000
    minv = np.log(0.00000000000000001)
    maxv = np.log(0.08333333333333333)
    scale_adjust = (maxv-minv) / (maxp-minp);
    var = np.exp(minv + scale_adjust*(slid_val-minp))
    print(var)
    return var

# getting alpha and beta from belief and log confidence values 
def transform_param(belief, confidence):
    mu = belief/100
    var =  log_slider(confidence)
    alpha = mu * (mu * (1 - mu) / var - 1)
    beta = alpha * (1 - mu) / mu
    return [alpha, beta]

# just a reminder showing how the variance of the beta distribution is computed 
def var_beta(a,b):
    return (a * b)/((a + b)**2 * (a+b+1))

# transforming values back to initial position for comparison to make sure that data are recorder properly
def transform_bel_slider_val(slid_val):
    minv = 5
    maxv = 95
    minp = 1
    maxp = 99
    scale_adjust = (maxp- minp) / (maxv - minv)
    position = (minp + scale_adjust * (slid_val - minv))
    return position

def transform_bel_slider_pos(slid_val):
    minv = 1
    maxv = 99
    minp = 5
    maxp = 95
    scale_adjust = (maxp- minp) / (maxv - minv)
    position = (minp + scale_adjust * (slid_val - minv))
    return position

def transform_con_slider_pos(slid_val):
    minv = 1
    maxv = 99
    minp = 0
    maxp = 120
    scale_adjust = (maxp- minp) / (maxv - minv)
    position = (minp + scale_adjust * (slid_val - minv))
    return position

def transform_con_slider_val(slid_val):
    minv = 0
    maxv = 120
    minp = 1
    maxp = 99
    scale_adjust = (maxp- minp) / (maxv - minv)
    position = (minp + scale_adjust * (slid_val - minv))
    return position

# recoding key demographic variables 
def get_demographics(demographics):
    demog = {}
    if demographics['gender'] == 'male':
        demog['gender'] = 0
    elif demographics['gender'] == 'female':
         demog['gender'] = 1
    demog['age'] = int(demographics['age'])
    demog['time'] = int(demographics['instructions_duration']) + int(demographics['task_duration'])
    demog['pol_orient'] = int(demographics['pol_orient'])
    return demog

# transforming each subject's data into dicts (start of id is arbitrary)
subj = 0
while subj < len(bel_updating_dat):
    subj_trial_dat_dicts.append(eval(bel_updating_dat.iloc[subj, 4]))
    subj_demog_dat_dicts.append(eval(bel_updating_dat.iloc[subj, 3]))
    subj += 1
subj_trial_dat_dicts

# extracting parameters from subject responses and reordering conditions 
def get_parameters(subject, demographics, subj_id):

    # creating a dictionary for each condition including model and subject parameters 
    con_1_param = {}
    con_2_param = {}
    con_3_param = {}

    # determining the index of the condition for each subject (order was randomised)
    cond_1_index = subject['rand_cond_order'].index(1)
    cond_2_index = subject['rand_cond_order'].index(2)
    cond_3_index = subject['rand_cond_order'].index(3)
    rand_pos_winner = subject['random_pos_winner']

    # re-ordering conditions so that for all subject data the conditions are in the order 1,2,3 
    if cond_1_index == 0:
        c1_r1 = -12
        if cond_2_index == 1:
            c2_r1 = -8
            c3_r1 = -4
        if cond_2_index == 2:
            c2_r1 = -4
            c3_r1 = -8
    elif cond_1_index == 1:
        c1_r1 = -8
        if cond_2_index == 0:
            c2_r1 = -12
            c3_r1 = -4
        if cond_2_index == 2:
            c2_r1 = -4
            c3_r1 = -12
    elif cond_1_index == 2:
        c1_r1 = -4
        if cond_2_index == 0:
            c2_r1 = -12
            c3_r1 = -8
        if cond_2_index == 1:
            c2_r1 = -8
            c3_r1 = -12

    # appending the parameters to the dicts
    for cond in subject['rand_cond_order']:
        if cond == 1:
            
            # including subj_id
            con_1_param['subj_id'] = subj_id
            
            # including condition
            con_1_param['cond'] = 1
            
            if rand_pos_winner == 1:
               
                # extracting subject parameters (using transformation functions)
                con_1_param['subj_prior_a'] = transform_param(float(subject['responses'][c1_r1]), float(subject['responses'][c1_r1 + 1]))[0]
                con_1_param['subj_prior_b'] = transform_param(float(subject['responses'][c1_r1]), float(subject['responses'][c1_r1 + 1]))[1]
                con_1_param['subj_post_a'] = transform_param(float(subject['responses'][c1_r1 + 2]), float(subject['responses'][c1_r1 + 3]))[0]
                con_1_param['subj_post_b'] = transform_param(float(subject['responses'][c1_r1 + 2]), float(subject['responses'][c1_r1 + 3]))[1]
                
                # raw data 
                con_1_param['subj_prior_belief'] = transform_bel_slider_val(float(subject['responses'][c1_r1]))
                con_1_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c1_r1 + 1]))
                con_1_param['subj_post_belief'] = transform_bel_slider_val(float(subject['responses'][c1_r1 + 2]))
                con_1_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c1_r1 + 3]))
           

                
            elif rand_pos_winner == 0:
        
                # flipping parameters for subjects having seen locals with flipped beliefs and certainty 
                con_1_param['subj_prior_b'] = transform_param(float(subject['responses'][c1_r1]), float(subject['responses'][c1_r1 + 1]))[0]
                con_1_param['subj_prior_a'] = transform_param(float(subject['responses'][c1_r1]), float(subject['responses'][c1_r1 + 1]))[1]
                con_1_param['subj_post_b'] = transform_param(float(subject['responses'][c1_r1 + 2]), float(subject['responses'][c1_r1 + 3]))[0]
                con_1_param['subj_post_a'] = transform_param(float(subject['responses'][c1_r1 + 2]), float(subject['responses'][c1_r1 + 3]))[1]

                # flipping subj posterior belief ratings accordingly 
                con_1_param['subj_prior_belief'] = transform_bel_slider_val(float(subject['responses'][c1_r1]))
                con_1_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c1_r1 + 1]))
                con_1_param['subj_post_belief'] = 99 - transform_bel_slider_val(float(subject['responses'][c1_r1 + 2]))
                con_1_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c1_r1 + 3]))
   

            # currently only including key demographics, can add more if needed 
            con_1_param['age'] = get_demographics(demographics)['age']
            con_1_param['gender'] = get_demographics(demographics)['gender']
            con_1_param['time'] = get_demographics(demographics)['time']
            con_1_param['pol_orient'] = get_demographics(demographics)['pol_orient']
            con_1_param['position'] = rand_pos_winner 
            
        elif cond == 2:
            con_2_param['subj_id'] = subj_id
            con_2_param['cond'] = 2
            if rand_pos_winner == 1: 
              
                con_2_param['subj_prior_a'] = transform_param(float(subject['responses'][c2_r1]), float(subject['responses'][c2_r1 + 1]))[0]
                con_2_param['subj_prior_b'] = transform_param(float(subject['responses'][c2_r1]), float(subject['responses'][c2_r1 + 1]))[1]
                con_2_param['subj_post_a'] = transform_param(float(subject['responses'][c2_r1 + 2]), float(subject['responses'][c2_r1 + 3]))[0]
                con_2_param['subj_post_b'] = transform_param(float(subject['responses'][c2_r1 + 2]), float(subject['responses'][c2_r1 + 3]))[1]
                con_2_param['subj_prior_belief'] = transform_bel_slider_val(float(subject['responses'][c2_r1]))
                con_2_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c2_r1 + 1]))
                con_2_param['subj_post_belief'] = transform_bel_slider_val(float(subject['responses'][c2_r1 + 2]))
                con_2_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c2_r1 + 3])) 
            
            elif rand_pos_winner == 0:
              
                con_2_param['subj_prior_b'] = transform_param(float(subject['responses'][c2_r1]), float(subject['responses'][c2_r1 + 1]))[0]
                con_2_param['subj_prior_a'] = transform_param(float(subject['responses'][c2_r1]), float(subject['responses'][c2_r1 + 1]))[1]
                con_2_param['subj_post_b'] = transform_param(float(subject['responses'][c2_r1 + 2]), float(subject['responses'][c2_r1 + 3]))[0]
                con_2_param['subj_post_a'] = transform_param(float(subject['responses'][c2_r1 + 2]), float(subject['responses'][c2_r1 + 3]))[1]
                con_2_param['subj_prior_belief'] = 99 - transform_bel_slider_val(float(subject['responses'][c2_r1]))
                con_2_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c2_r1 + 1]))
                con_2_param['subj_post_belief'] = 99 - transform_bel_slider_val(float(subject['responses'][c2_r1 + 2]))
                con_2_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c2_r1 + 3]))  
            con_2_param['age'] = get_demographics(demographics)['age']
            con_2_param['gender'] = get_demographics(demographics)['gender']
            con_2_param['time'] = get_demographics(demographics)['time']
            con_2_param['pol_orient'] = get_demographics(demographics)['pol_orient']
            con_2_param['position'] = rand_pos_winner 
            
            
        elif cond == 3:
            con_3_param['subj_id'] = subj_id
            con_3_param['cond'] = 3
            if rand_pos_winner == 1:
                
                con_3_param['subj_prior_a'] = transform_param(float(subject['responses'][c3_r1]), float(subject['responses'][c3_r1 + 1]))[0]
                con_3_param['subj_prior_b'] = transform_param(float(subject['responses'][c3_r1]), float(subject['responses'][c3_r1 + 1]))[1]
                con_3_param['subj_post_a'] = transform_param(float(subject['responses'][c3_r1 + 2]), float(subject['responses'][c3_r1 + 3]))[0]
                con_3_param['subj_post_b'] = transform_param(float(subject['responses'][c3_r1 + 2]), float(subject['responses'][c3_r1 + 3]))[1]
                con_3_param['subj_prior_belief'] = transform_bel_slider_val(float(subject['responses'][c3_r1]))
                con_3_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c3_r1 + 1]))
                con_3_param['subj_post_belief'] = transform_bel_slider_val(float(subject['responses'][c3_r1 + 2]))
                con_3_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c3_r1 + 3]))
            elif rand_pos_winner == 0:
               
                con_3_param['subj_prior_belief'] = 99 - transform_bel_slider_val(float(subject['responses'][c3_r1]))
                con_3_param['subj_prior_con'] = transform_con_slider_val(float(subject['responses'][c3_r1 + 1]))
                con_3_param['subj_post_belief'] = 99 - transform_bel_slider_val(float(subject['responses'][c3_r1 + 2]))
                con_3_param['subj_post_con'] = transform_con_slider_val(float(subject['responses'][c3_r1 + 3]))
                con_3_param['subj_prior_b'] = transform_param(float(subject['responses'][c3_r1]), float(subject['responses'][c3_r1 + 1]))[0]
                con_3_param['subj_prior_a'] = transform_param(float(subject['responses'][c3_r1]), float(subject['responses'][c3_r1 + 1]))[1]
                con_3_param['subj_post_b'] = transform_param(float(subject['responses'][c3_r1 + 2]), float(subject['responses'][c3_r1 + 3]))[0]
                con_3_param['subj_post_a'] = transform_param(float(subject['responses'][c3_r1 + 2]), float(subject['responses'][c3_r1 + 3]))[1]
            con_3_param['age'] = get_demographics(demographics)['age']
            con_3_param['gender'] = get_demographics(demographics)['gender']
            con_3_param['time'] = get_demographics(demographics)['time']
            con_3_param['pol_orient'] = get_demographics(demographics)['pol_orient']
            con_3_param['position'] = rand_pos_winner 

            
    # concatenating parameters into one list 
    parameters = [con_1_param, con_2_param, con_3_param]

    return parameters

# creating new data structure that is more convenient for analysis
def reformat_dat(trials, demographics):
    reformat_dat = []
    for subj_trial, subj_demog in zip(trials, demographics):
        reformat_dat.append(get_parameters(subj_trial, subj_demog, trials.index(subj_trial)))
    return reformat_dat

# transforming the data structure into new data frame
dat_struc = reformat_dat(subj_trial_dat_dicts, subj_demog_dat_dicts)
bel_updating_dat_formatted = pd.DataFrame(dat_struc[0])
subj_count = 1
while subj_count < len(dat_struc):
    bel_updating_dat_formatted = bel_updating_dat_formatted.append(dat_struc[subj_count], ignore_index = True)
    subj_count += 1
    bel_updating_dat_formatted['subj_a_diff'] = bel_updating_dat_formatted['subj_post_a'] - bel_updating_dat_formatted['subj_prior_a']
    bel_updating_dat_formatted['subj_b_diff'] = bel_updating_dat_formatted['subj_post_b'] - bel_updating_dat_formatted['subj_prior_b']

# writing restructured data into csv
bel_updating_dat_formatted.to_csv('main_data_formatted.csv')


# creating data for plotting the beta pdf of subjects
def create_arrays(start_val, stop_val, cardinality, alpha, beta):
    x_arr = []
    y_arr = []
    step = (stop_val - start_val) / (cardinality - 1)
    for i in range(cardinality):
        x = start_val + (step * i)
        y = scipy.stats.beta.pdf(x, alpha, beta)
        x_arr.append(x)
        y_arr.append(y)
    return x_arr, y_arr


# plotting the pdfs for each condition (both model and subject)

# average parameters for plotting

# averages across prior order position left 
# # priors
# a_subj_c_1_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_a']
# b_subj_c_1_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_b']
# a_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_a']
# b_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_b']
# a_subj_c_3_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_a']
# b_subj_c_3_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_prior_b']

# # posteriors|
# a_subj_c_1_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_a']
# b_subj_c_1_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_b']
# a_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_a']
# b_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_b']
# a_subj_c_3_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_a']
# b_subj_c_3_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['clust_post'] == 2) , 'subj_post_b']


# # priors
# a_subj_c_1_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_a']
# b_subj_c_1_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_b']
# a_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_a']
# b_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_b']
# a_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_a']
# b_subj_c_2_prior = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['position'] == 0) , 'subj_prior_b']

# # posteriors
# a_subj_c_1_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_a']
# b_subj_c_1_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 1) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_b']
# a_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_a']
# b_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 2) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_b']
# a_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_a']
# b_subj_c_2_post = bel_updating_dat_formatted.loc[(bel_updating_dat_formatted['cond'] == 3) & (bel_updating_dat_formatted['position'] == 0) , 'subj_post_b']

# # # priors
a_subj_c_1_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 1, 'subj_prior_a']
b_subj_c_1_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 1, 'subj_prior_b']
a_subj_c_2_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 2, 'subj_prior_a']
b_subj_c_2_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 2, 'subj_prior_b']
a_subj_c_3_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 3, 'subj_prior_a']
b_subj_c_3_prior = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 3, 'subj_prior_b']

# posteriors
a_subj_c_1_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 1, 'subj_post_a']
b_subj_c_1_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 1, 'subj_post_b']
a_subj_c_2_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 2, 'subj_post_a']
b_subj_c_2_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 2, 'subj_post_b']
a_subj_c_3_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 3, 'subj_post_a']
b_subj_c_3_post = bel_updating_dat_formatted.loc[bel_updating_dat_formatted['cond'] == 3, 'subj_post_b']


# summarising parameters in dicts 
aver_param = {'prior': [[mean(a_subj_c_1_prior), mean(b_subj_c_1_prior)], 
                        [mean(a_subj_c_2_prior), mean(b_subj_c_2_prior)], 
                        [mean(a_subj_c_3_prior), mean(b_subj_c_3_prior)]],
             'post': [[mean(a_subj_c_1_post), mean(b_subj_c_1_post)], 
                      [mean(a_subj_c_2_post), mean(b_subj_c_2_post)], 
                      [mean(a_subj_c_3_post), mean(b_subj_c_3_post)]]}

aver_param_final_no_outlier = {'prior': [[18.73621,19.85711], 
                        [19.49668,18.53587], 
                        [19.36877,18.91516]],
             'post': [[33.72615,15.17615], 
                      [29.65699,13.8521], 
                      [31.90255, 16.05496]]}

print(aver_param)


def plot_beta_pdfs(parameters):
    
    # mean model parameters always same 
    norm_prior = [[2,2], [2,2], [2,2]]
    norm_post = [[147,66.5], [52,47], [124,61.75]]
    
    

    # subject parameters 
    subj_prior = [parameters['prior'][0], parameters['prior'][2], parameters['prior'][1]]
    subj_post = [parameters['post'][0], parameters['post'][2], parameters['post'][1]]
    
    # data used for plotting
    dat_norm_prior = []
    dat_norm_post = []
    dat_subj_prior = []
    dat_subj_post = []

    # creating data based on parameters 
    for param in norm_prior:
        a = param[0]
        b = param[1]
        x, y = create_arrays(0.005, .995, 500, a, b)
        dat_norm_prior.append([x,y])
    for param in norm_post:
        a = param[0]
        b = param[1]
        x, y = create_arrays(0.005, .995, 500, a, b)
        dat_norm_post.append([x,y])
    for param in subj_prior:
        a = param[0]
        b = param[1]
        x, y = create_arrays(0.005, .995, 500, a, b)
        dat_subj_prior.append([x,y])
    for param in subj_post:
        a = param[0]
        b = param[1]
        x, y = create_arrays(0.005, .995, 500, a, b)
        dat_subj_post.append([x,y])
    
    # creating plot 
    fig = make_subplots(rows=3, cols=4, subplot_titles=("Model Prior", "Model Posterior", "Subject Prior", "Subject Posterior"))
    
    
    # adding y axis labesl (one for each condition)
    fig.update_yaxes(title_text="independent", row=1, col=1)
    fig.update_yaxes(title_text="sequential", row=2, col=1)
    fig.update_yaxes(title_text="shared", row=3, col=1)
    
    
#     # adding x-axis labels model
    fig.update_xaxes(title_text="B(2, 2)<br>&mu;=0.5, &#x3C3;<sup>2</sup>=0.05", row=1, col=1)
    fig.update_xaxes(title_text="B(2, 2)<br>&mu;=0.5, &#x3C3;<sup>2</sup>=0.05", row=2, col=1)
    fig.update_xaxes(title_text="B(2, 2)<br>&mu;=0.5, &#x3C3;<sup>2</sup>=0.05", row=3, col=1)
    fig.update_xaxes(title_text="B(147,66.5)<br>&mu;=0.6885, &#x3C3;<sup>2</sup>=0.0009", row=1, col=2)
    fig.update_xaxes(title_text="B(52,47)<br>&mu;=0.5252, &#x3C3;<sup>2</sup>=0.0025", row=2, col=2)
    fig.update_xaxes(title_text="B(124,61.75)<br>&mu;=0.6675, &#x3C3;<sup>2</sup>=0.0012", row=3, col=2)
    
    

    
#     # adding x-axis labels subj
    fig.update_xaxes(title_text="B(18.73, 19.86)<br>&mu;=0.4969, &#x3C3;<sup>2</sup>=0.0213", row=1, col=3)
    fig.update_xaxes(title_text="B(19.37, 18.92)<br>&mu;=0.4924, &#x3C3;<sup>2</sup>=0.0220", row=2, col=3)
    fig.update_xaxes(title_text="B(19.50, 18.54)<br>&mu;=0.5147, &#x3C3;<sup>2</sup>=0.0227", row=3, col=3)
    fig.update_xaxes(title_text="B(33.73, 15.18)<br>&mu;=0.6738, &#x3C3;<sup>2</sup>=0.0087", row=1, col=4)
    fig.update_xaxes(title_text="B(31.90, 16.05)<br>&mu;=0.6463, &#x3C3;<sup>2</sup>=0.0101", row=2, col=4)
    fig.update_xaxes(title_text="B(29.66, 13.85)<br>&mu;=0.6616, &#x3C3;<sup>2</sup>=0.0103", row=3, col=4)
    
    # adding data to the figure 
    i = 0
    while i < 3:
        fig.add_trace(go.Scatter(
        x=dat_norm_prior[i][0][25:250], y=dat_norm_prior[i][1][25:250],
        name = False,
        fill ='tozeroy',
        mode = 'lines',
        line = {'color':'grey'},
        ),row=i+1,col=1)

        fig.add_trace(go.Scatter(
            x=dat_norm_prior[i][0][250:475], y=dat_norm_prior[i][1][250:475],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'silver'}
        ),row=i+1,col=1)
        
        fig.add_trace(go.Scatter(
            x=dat_norm_post[i][0][25:250], y=dat_norm_post[i][1][25:250],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'grey'}
        ),row=i+1,col=2)

        fig.add_trace(go.Scatter(
            x=dat_norm_post[i][0][250:475], y=dat_norm_post[i][1][250:475],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'silver'}
        ),row=i+1,col=2)

        fig.add_trace(go.Scatter(
            x=dat_subj_prior[i][0][25:250], y=dat_subj_prior[i][1][25:250],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'lavenderblush'}
        ),row=i+1,col=3)

        fig.add_trace(go.Scatter(
            x=dat_subj_prior[i][0][250:475], y=dat_subj_prior[i][1][250:475],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'thistle'}
        ),row=i+1,col=3)

        fig.add_trace(go.Scatter(
            x=dat_subj_post[i][0][25:250], y=dat_subj_post[i][1][25:250],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'lavenderblush'}
        ),row=i+1,col=4)

        fig.add_trace(go.Scatter(
            x=dat_subj_post[i][0][250:475], y=dat_subj_post[i][1][250:475],
            type = 'scatter',
            fill ='tozeroy',
            mode = 'lines',
            line = {'color':'thistle'}
        ),row=i+1,col=4)
        i +=1
        
    # layour of each subplot
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                      template = 'none',
                       font=dict(
        family="Helvetica",
        size=10,
        color="black"
    ),
                         yaxis = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                      template = 'none',
                         yaxis2 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis2 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                      template = 'none',
                         yaxis3 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis3 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                      template = 'none',
                         yaxis4 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis4 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis5 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis5 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis6 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis6 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis7 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis7 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis8 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis8 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis9 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis9 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis10 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis10 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis11 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis11 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})
    
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=2)
    fig.update_layout(hovermode = False,
                         yaxis12 = {
        'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False},
                     xaxis12 = {
          'fixedrange': True,
          'showgrid': False,
          'zeroline': False, 
          'showticklabels': False})

    fig.update_layout(showlegend=False)
    
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=11)
    fig.write_image("images/fig1.svg")
#     fig.show()


plot_beta_pdfs(aver_param_final_no_outlier)