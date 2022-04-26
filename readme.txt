Cole Feely and Zachary Zhao
CS 383
Homework 2

Thoughts on eval function-

our eval function was:

   def evaluation(self, state):

        columns_array = state.get_cols()

        middle = state.num_rows // 2
        positives = columns_array[middle].count(1) # count the number of '1's' in the middle column
        negatives = columns_array[middle].count(-1) # count the number of '-1's' in the middle column


        return (positives - negatives)

We decided to go down the simple but effective route because we wanted to have an efficient working version ASAP.
Our evaluation function takes the score based off of the number peices near the middle column.
The function grabs all the columns and stores them into an array. From there we grab the middle row with a simple
floor division. From there we just count the number of peices near the middle and return the difference.

