import numpy as np
import pandas as pd

class NaiveBayes():
    """
    This is a Naive Bayes spam filter that learns word spam probabilities 
    from pre-labeled training data and predicts whether emails are ham or spam.
    """
    def __init__(self):
        """
        Initialize variables that will be used for training and prediction.
        """
        self.num_train_hams = 0
        self.num_train_spams = 0
        self.word_counts_spam = {}
        self.word_counts_ham = {}
        self.HAM_LABEL = 'ham'
        self.SPAM_LABEL = 'spam'
        
    def get_word_set(self, email_text: str) -> set:
        """
        Extracts a set of unique words from an email text.
        
        :param email_text: The text content of an email
        :return: A set of all unique words in the email
        """
        # Clean the text and split into words
        text = email_text.replace('\r', '').replace('\n', ' ')
        words = text.split(' ')
        return set(words)
    
    # TODO implement:
    def fit(self, train_df: pd.DataFrame) -> None:
        """
        Trains the Naive Bayes model on the provided DataFrame.
        
        :param train_df: DataFrame with 'email' and 'label' columns
        :return: None
        """
        # 1. Count number of ham and spam emails
        self.num_train_hams = train_df[train_df.label == self.HAM_LABEL].shape[0]
        self.num_train_spams = train_df[train_df.label == self.SPAM_LABEL].shape[0]

        # 2. Reinitialize word count dictionaries
        self.word_counts_ham = {}
        self.word_counts_spam = {}

        # 3. Process each email in the training set
        for _, row in train_df.iterrows():
            word_set = self.get_word_set(row["email"])
            word_counts = self.word_counts_spam if row["label"] == self.SPAM_LABEL else self.word_counts_ham
            for word in word_set:
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1

    def predict(self, email_text: str) -> str:
        """
        Predicts whether a single email is ham or spam.
        
        :param email_text: The text content of an email
        :return: The predicted label ('ham' or 'spam').
        """
        # 1. Get words in the email
        word_set = self.get_word_set(email_text)
        # 2. Calculate prior probabilities
        ham_prior_probability = self.num_train_hams / (self.num_train_hams + self.num_train_spams)
        spam_prior_probability= self.num_train_spams / (self.num_train_hams + self.num_train_spams)


        # 3. Calculate log probabilities for ham and spam (for computational reasons)
        ham_word_probabilities = {
            word: np.log(self.word_counts_ham[word] / self.num_train_hams) for word in word_set if word in self.word_counts_ham
        }
        spam_word_probabilities = {
            word: np.log(self.word_counts_spam[word] / self.num_train_spams) for word in word_set if word in self.word_counts_spam
        }
        # 4. For each word in the email, update the log probabilities
        ham_log_probabilities_sum = sum(ham_word_probabilities.values())
        spam_log_probabilities_sum = sum(spam_word_probabilities.values())
        # 4. Predict label (in case of a tie, return HAM_LABEL)
        ham_posterior_probability = ham_prior_probability * ham_log_probabilities_sum
        spam_posterior_probability = spam_prior_probability * spam_log_probabilities_sum
        if spam_posterior_probability > ham_posterior_probability:
            return self.SPAM_LABEL
        else:
            return self.HAM_LABEL
    
    def predict_df(self, df: pd.DataFrame) -> pd.Series:
        """
        Predicts ham/spam labels for all emails in a DataFrame.
        
        :param df: DataFrame with 'email' column
        :return: Series with predicted labels
        """
        predictions = []
        for _, row in df.iterrows():
            predictions.append(self.predict(row['email']))
        return pd.Series(predictions)
        
    def accuracy(self, test_df: pd.DataFrame) -> float:
        """
        Computes the accuracy of predictions on a test DataFrame.
        
        :param test_df: DataFrame with 'email' and 'label' columns
        :return: Accuracy as a float between 0 and 1
        """
        correct = 0
        total = len(test_df)
        
        for index, row in test_df.iterrows():
            prediction = self.predict(row['email'])
            if prediction == row['label']:
                correct += 1
                
        return correct / total

# train_df = pd.read_csv("train_emails.csv")
# test_df = pd.read_csv("test_emails.csv")

# naive_bayes = NaiveBayes()
# naive_bayes.fit(train_df)
# print(naive_bayes.accuracy(test_df))
