#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# PROGRAMMER: Kevin North
# DATE CREATED: 9/15/2018
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # collecting start time
    start_time = time()
    
    # line arguments
    in_arg = get_input_args()
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_arg.dir)

    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)
    

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("\n** Total Elapsed Runtime:", tot_time)



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser(
        description="Retrieves and parses the command line arguments created and defined using the argparse module. This function returns these arguments as an ArgumentParser object."
    )
    parser.add_argument('--dir', metavar='str', type=str, help="Path to the pet image files(default- 'pet_images/')", default="pet_images/")
    parser.add_argument('--arch', choices=['vgg','alexnet','resnet'], type=str, metavar='str', help="CNN model architecture to use for image classification(default- pick any of the following vgg, alexnet, resnet)",default='vgg')
    parser.add_argument('--dogfile', type=str, metavar='str', help="Text file that contains all labels associated to dogs(default'dognames.txt'",default='dognames.txt')
    args = parser.parse_args()
#     print("arg 1: {0}\narg 2: {1}\narg 3: {2}".format(args.dir, args.arch, args.dogfile))
    return args

def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    import re
    regexp = re.compile(r'(.jpg)|\d+')
    petlabels_dic = {}
    for f in listdir(image_dir):
        petlabels_dic[f] = " ".join(str(i) for i in f.split('_') if not regexp.search(i))
#     print(petlabels_dic)
    return petlabels_dic


def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    results_dic = {}
    for k,v in petlabel_dic.items():
        classifier_label = classifier("{0}/{1}".format(images_dir,k), model)
        results_dic[k] = [v,classifier_label,match(classifier_label,v)]
#     print(results_dic)
    return results_dic

                          
def match(classifier_names,label):
    return 1 if label.lower() in classifier_names.lower().split(',') else 0
                          
                          
def adjust_results4_isadog(results_dic, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    try:
        with open(dogsfile) as f:
            dogs = [dog.strip().lower() for dog in f.readlines()]
        for k,v in results_dic.items():
            v.append(1 if v[0].lower() in dogs else 0)
            v.append(1 if v[1].lower() in dogs else 0)
    except IOError as e:
        print(str(e))
#     print(results_dic)


def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    results_stats = {}
    results_stats['n_images'] = len(results_dic)
    results_stats['n_dogs_img'] = sum(v[3] for k,v in results_dic.items())
    results_stats['n_notdogs_img'] = sum(1 if v[3] == 0 else 0 for k,v in results_dic.items())
    results_stats['pct_correct_dogs'] = round(len([v for k,v in results_dic.items() if v[3] == v[4] and v[4] == 1]) / float(results_stats['n_dogs_img'])) * 100
    results_stats['pct_correct_notdogs'] = round(len([v for k,v in results_dic.items() if v[3] == v[4] and v[4] == 0]) / float(results_stats['n_notdogs_img'])) * 100
    results_stats['pct_correct_breed'] = round(sum(v[2] for k,v in results_dic.items() if v[3] == v[4] and v[4] == 1) / float(results_stats['n_images'])) * 100
    return results_stats
    
def num_notdogs(result):
    return 1 if result[3] == 0 else 0

def print_results(results_dic, results_stats, model, print_incorrect_dogs, print_incorrect_breed):
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
# Code for checking results_stats_dic -
    # Checks calculations of counts & percentages BY using results_dic
    # to re-calculate the values and then compare to the values
    # in results_stats_dic
    
    # Initialize counters to zero and number of images total
    n_images = len(results_dic)
    n_pet_dog = 0
    n_class_cdog = 0
    n_class_cnotd = 0
    n_match_breed = 0
    
    # Interates through results_dic dictionary to recompute the statistics
    # outside of the calculates_results_stats() function
    for key in results_dic:

        # match (if dog then breed match)
        if results_dic[key][2] == 1:

            # isa dog (pet label) & breed match
            if results_dic[key][3] == 1:
                n_pet_dog += 1

                # isa dog (classifier label) & breed match
                if results_dic[key][4] == 1:
                    n_class_cdog += 1
                    n_match_breed += 1

            # NOT dog (pet_label)
            else:

                # NOT dog (classifier label)
                if results_dic[key][4] == 0:
                    n_class_cnotd += 1

        # NOT - match (not a breed match if a dog)
        else:
 
            # NOT - match
            # isa dog (pet label) 
            if results_dic[key][3] == 1:
                n_pet_dog += 1

                # isa dog (classifier label)
                if results_dic[key][4] == 1:
                    n_class_cdog += 1

            # NOT dog (pet_label)
            else:

                # NOT dog (classifier label)
                if results_dic[key][4] == 0:
                    n_class_cnotd += 1

                    
    # calculates statistics based upon counters from above
    n_pet_notd = n_images - n_pet_dog
    pct_corr_dog = ( n_class_cdog / n_pet_dog )*100
    pct_corr_notdog = ( n_class_cnotd / n_pet_notd )*100
    pct_corr_breed = ( n_match_breed / n_pet_dog )*100
    
    # prints calculated statistics
    print("\n ** Statistics from calculates_results_stats() function:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (results_stats['n_images'], results_stats['n_dogs_img'],
             results_stats['n_notdogs_img'], results_stats['pct_correct_dogs'],
             results_stats['pct_correct_notdogs'],
             results_stats['pct_correct_breed']))
    print("\n ** Check Statistics - calculated from this function as a check:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f  Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (n_images, n_pet_dog, n_pet_notd, pct_corr_dog, pct_corr_notdog,
             pct_corr_breed))
    
    if print_incorrect_dogs:
        for dog in [v[0] for k,v in results_dic.items() if v[4] == 1 and v[3] == 0]:
            print(dog)
    if print_incorrect_breed:
        for dog in [v[0] for k,v in results_dic.items() if v[3] == v[4] and v[4] == 1 and v[2] == 0]:
            print(dog)
        

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
