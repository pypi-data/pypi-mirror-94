"""
This module contains functions and classes that perform
an analysis of various predictors in a segmentation analysis.

Goal 1: Create a consistent working functional API

Goal 2: Create an OOP Design

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import random

# TODO: Fix and normalize mask value so that it is the non-zero value.



# Only use numpy / matplotlib to keep dependencies simple

#

# With a segmentation problem.
# Translate it into a binary 0 or 1 classification problem.
# Flatten the image.
# Run an MAE.


# Dice Coefficient
# Other Itersection over Union metrics.


# For each model prediction,
# Generate a picture of wrong pixels, right pixels.
# Save it to its own pixels
# Compare results across models.
# Which samples had the most wrong... Hardest samples.
# Which were the most different (most variance)


#exi
# Is it systematically biased in shape, direction, size?


# Example
# https://stackoverflow.com/questions/31273652/how-to-calculate-dice-coefficient-for-measuring-accuracy-of-image-segmentation-i


def create_segmentation_masks(random_shift: bool = True,
                              n_samples: int = 1):
    """
    Generates a segmentation mask for demonstration purposes.

    :param random_shift: Boolean value whether you want to create randomness or not.
    :param n_samples: How many true/false mask pairs you want to create.

    :return: true_mask(s), predicted_mask(s)
    """

    all_true_masks = []
    all_predicted_masks = []

    for img_id in range(n_samples):

        if random_shift:
            v_shift = random.randint(1, 20)
            h_shift = random.randint(1, 20)
        else:
            v_shift = 0
            h_shift = 0

        mask_value = 1

        # segmentation
        predicted_seg = np.zeros((100, 100), dtype='int')
        predicted_seg[30-v_shift:70-v_shift, 30-h_shift:70-h_shift] = mask_value

        # ground truth
        ground_truth = np.zeros((100,100), dtype='int')
        ground_truth[30:70, 40:80] = mask_value

        if n_samples > 1:
            all_true_masks.append(ground_truth)
            all_predicted_masks.append(predicted_seg)

    if n_samples == 1:
        return ground_truth, predicted_seg

    elif n_samples > 1:
        return all_true_masks, all_predicted_masks

#plt.imshow(wrong_mask)
#plt.show()
# turn axes off.

def create_segmentation_masks_dataset():
    pass

def get_dice_coeff(truth: np.array,
                   predicted: np.array) -> float:
    """
    Gets the dice coefficient from a true / predict pair.

    :param truth: The true mask.
    :param predicted: The predicted mask
    :return: The dice coefficient
    """

    mask_value = 1

    dice = np.sum(predicted[truth==mask_value])*2.0 / (np.sum(predicted) + np.sum(truth))

    return dice

def show_wrong_masks(truths,
                     preds):
    pass

def show_wrong_mask(truth,
                    predicted,
                    ):
    """
    Show a plot of the wrong mask for comparison with
    the true mask.

    :param truth:
    :param predicted:
    :return:
    """
    #
    # Assert the shapes are the same.

    mask_value = 1   # This should be global-like...

    # Calculate Dice Coefficient
    dice = np.sum(seg[truth==mask_value])*2.0 / (np.sum(predicted) + np.sum(truth))

    wrong_mask = truth - predicted

    fig, axs = plt.subplots(nrows = 1, ncols = 3)

    the_title = f"True, Predicted Comparison. Dice: {dice}"
    fig.suptitle(the_title)

    axs[0].imshow(truth, cmap = "gray")
    axs[0].set_title("True")

    axs[1].imshow(predicted, cmap = "gray")
    axs[1].set_title("Predicted")

    axs[2].imshow(wrong_mask, cmap = "gray")
    axs[2].set_title("Wrong_mask")

    plt.show()

def mask_lists_to_array():
    pass

def validate_lists():
    pass


def show_many_wrongs_mask(truths,
                          preds) -> None:
    """
    Shows all true/wrong mask pairs.

    TODO: Will have to create a limit / range otherwise it will be too big.

    :return: None.  Just shows image.
    """

    assert len(truths) == len(preds)  # Make sure same number of images in both
    n_images = len(truths)

    mask_value = 1   # This should be global-like...
    dice_vals = []

    fig, axs = plt.subplots(nrows = n_images,
                            ncols = 3,
                            sharex = True,
                            sharey = True)


    for row in range(n_images):

        truth = truths[row]
        predicted = preds[row]

        dice = np.sum(predicted[truth==mask_value])*2.0 / (np.sum(predicted) + np.sum(truth))
        dice_vals.append(dice)

        if row == 0:
            axs[row, 0].set_title("True")
            axs[row, 1].set_title("Predicted")
            axs[row, 2].set_title("Wrong_mask")

        wrong_mask = truth - predicted

        axs[row, 0].imshow(truth, cmap = "gray")
        axs[row, 0].axis('off')

        axs[row, 1].imshow(predicted, cmap = "gray")
        axs[row, 1].axis('off')

        axs[row, 2].imshow(wrong_mask, cmap = "gray")
        axs[row, 2].axis('off')


    avg_dice = round(np.array(dice_vals).mean(), 2)
    the_title = f"True, Predicted Comparison. Avg Dice: {avg_dice}"
    fig.suptitle(the_title)

    plt.show()

def best_models(true_masks,
                pred_masks,
                loss,
                pred_names = None):
    """
    Placeholder function - not made yet.
    Sorts models into best and worst given a loss function.

    :true_masks: List or numpy array of true masks
    :false_masks: List or numpy array of predicted masks.
    :loss: Callable loss function
    :pred_names: A list of the names of the predictors

    :return: Sorted Descending List of Best Models
    """
    pass

def find_most_diverse_preds(true_masks, pred_masks) -> pd.DataFrame:
    """
    Placeholder Function - Not made yet.

    Finds the most diverse predictions that
    get the most different parts of the
    ground truth accurately regardless
    of how accurate they are.

    To find the most accurate AND diverse
    predictors, use find_most_diverse_good_preds()

    :true_masks:
    :pred_masks:

    :return: Sorted and ranked dataframe from most diverse
    to least diverse.

    """



    pass


def find_most_diverse_good_preds():
    """
    Finds predictions that are most similar in score
    but least similar in predictions.

    :return:
    """
    # Sort first by Accuracy score (true == pred).sum()... Add this to a DF

    # Different_predictions = ((wrongs_mask_i == wrongs_mask_j) == False).sum()
    # Create an N x N df (heatmap) of ((wrongs_mask_i == wrongs_mask_j) == False).sum()... add to DF
    # 

    # Create a dataframe which sorts according to
    # [accuracy_score (descending), differences (ascending)]


    pass

def analyze_preds_bias(true_mask_list,
                       pred_mask_list,
                       show_report = True):
    """
    Tries to find systematic bias in the predicted vs actual
    values.

    :true_mask_list: List of true masks
    :pred_masks_list: List of numpy array or 3d array of predicted masks.


    :show_report: prints output of report to screen.

    :return: mean_wrongs - an image based averaging of all the deviations.
    """

    # TODO: This should be a zipped pair for less errors.

    n_images = len(true_mask_list)
    wrong_masks = []

    for row in range(n_images):
        truth = true_mask_list[row]
        predicted = pred_mask_list[row]

        wrong_mask = truth - predicted
        wrong_masks.append(wrong_mask)

    print(np.array(wrong_masks).shape)
    mean_wrongs = np.mean(wrong_masks, axis = 0)

    plt.imshow(mean_wrongs, cmap = "gray")
    plt.show()

    return mean_wrongs

def show_demo():
    """
    Shows a demo of the segmentation mask analysis
    with a synthetic dataset.

    :return: None
    """
    gt_list, seg_list = create_segmentation_masks(n_samples = 10)
    show_many_wrongs_mask(gt_list, seg_list)

    analyze_preds_bias(gt_list, seg_list)