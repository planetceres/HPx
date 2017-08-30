'''
Hyperparams
-----------
Usage:
    Note that key value for each hyperparam is a string value and corresponds to the key
    on physical keyboard.

Format:
< name_of_variable >: {
                    'action': < key_on_keyboard >,
                    'value': < initial_value_of_hyperparameter >,
                    'increment': < value_to_increment_by >,
                    'name': < name_of_hyperparam >,
                    }
So to set 'epochs' to number 1 on keyboard:
    'epochs': {
        'action': '1',
        'value': 90,
        'increment': 1,
        'name': 'epochs'
        },



'''
hyperparams = {
    # number of steps to take (and plot horizontally)
    'epochs': {
        'action': '1',
        'value': 90,
        'increment': 5,
        'name': 'epochs'
        },
    # learning rate
    'alpha': {
        'action': '2',
        'value': 0.10,
        'increment': 0.005,
        'name': 'learning_rate'
        },
    # std of the samples around current parameter vector
    'sigma': {
        'action': '3',
        'value': 8,
        'increment': 1,
        'name': 'standard_deviation'
        },
    # pop size of each generation of samples
    'population_size': {
        'action': '4',
        'value': 20,
        'increment': 5,
        'name': 'population_size',
        }
}
