# Naive Bayes Spam Filter in R

NaiveBayes <- R6::R6Class(
  classname = "NaiveBayes",
  public = list(
    # Class constants
    HAM_LABEL = "ham",
    SPAM_LABEL = "spam",
    
    # Instance variables
    num_train_hams = 0,
    num_train_spams = 0,
    word_counts_spam = list(),
    word_counts_ham = list(),
    
    # Initialize the model
    initialize = function() {
      self$num_train_hams <- 0
      self$num_train_spams <- 0
      self$word_counts_spam <- list()
      self$word_counts_ham <- list()
    },
    
    # Extract unique words from email text
    get_word_set = function(email_text) {
      # Clean text and split into words
      text <- gsub("\r", "", email_text)
      text <- gsub("\n", " ", text)
      words <- unlist(strsplit(text, " "))
      return(unique(words))
    },
    
    # TODO implement:
    #' Trains the Naive Bayes model on the provided DataFrame.
    #'
    #' @param train_df A data frame with 'email' and 'label' columns.
    #' @return None
    fit = function(train_df) {
      # 1. Count number of ham and spam emails
      # 2. Reinitialize word count dictionaries
      # 3. Process each email in the training set
      stop("Fit method not implemented") # Delete this line when you implement the method
    },
    
    # TODO implement:
    #' Predicts whether a single email is ham or spam.
    #'
    #' @param email_text The text content of an email.
    #' @return The predicted label ('ham' or 'spam').
    predict = function(email_text) {
      # 1. Get words in the email
      # 2. Calculate prior probabilities
      # 3. Calculate log probabilities for ham and spam (for computational reasons)
      # 4. For each word in the email, update the log probabilities
      # 4. Predict label (in case of a tie, return HAM_LABEL)
      stop("Fit method not implemented") # Delete this line when you implement the method
    },
    
    # Predict ham/spam labels for all emails in a data frame
    predict_df = function(df) {
      predictions <- character(nrow(df))
      for (i in 1:nrow(df)) {
        predictions[i] <- self$predict(df$email[i])
      }
      return(predictions)
    },
    
    # Compute accuracy of predictions on a test data frame
    accuracy = function(test_df) {
      predictions <- self$predict_df(test_df)
      correct <- sum(predictions == test_df$label)
      return(correct / nrow(test_df))
    }
  )
)
