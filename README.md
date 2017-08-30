## Interactive Dynamic Hyperparameters

This is a demo of a python module that allows for dynamic and interactive \
hyperparameter tuning during model training.

![alt text](https://github.com/planeteceres/HPx/assets/HPx001.gif "HPx demo")
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

The module is still under development and has not been tested extensively.


### How to run Demo

Clone the repository, and install dependencies.

At the command prompt, run:

`sudo python HPx_demo.py`

**Note: To use with OSx, the script must be run as root (administrator). \
Otherwise, it throws an OSError.**

The demo will open a new window that shows plot of a simulated data set as it \
trains using an evolution strategies algorithm. More algorithm examples will be\
 added soon.

The console will display the training step along with the current parameter \
settings and key mapping.

```
Training Step: 1  |1| epochs: 90  |2| alpha: 0.03  |3| sigma: 8  |4| population_size: 100				
Training Step: 2  |1| epochs: 90  |2| alpha: 0.03  |3| sigma: 8  |4| population_size: 100				
Training Step: 3  |1| epochs: 90  |2| alpha: 0.03  |3| sigma: 8  |4| population_size: 100				
Training Step: 4  |1| epochs: 90  |2| alpha: 0.03  |3| sigma: 8  |4| population_size: 100
```

### Keymapping and setting hyperparameter values

Hyperparameters can each be mapped to a key following the example in the \
`settings.py` file.

Format:

```
< name_of_variable >: {
                    'action': < key_on_keyboard >,
                    'value': < initial_value_of_hyperparameter >,
                    'increment': < value_to_increment_by >,
                    'name': < name_of_hyperparam >,
                    }
```                    

**Example:**
To set 'epochs' to number 1 on keyboard:

```
'epochs': {
    'action': '1',
    'value': 90,
    'increment': 1,
    'name': 'epochs'
    }
```

### Interacting with hyperparameters

To interact with a hyperparameter during training, press and hold the mapped \
key and increment by the designated increment value by tapping '-' or '=' \
[for - or +] the corresponding number of times.

**Example:**

To increment the value of `epochs` from the example above from `90` to `95`:

1. Press and hold `1`
2. While holding `1` tap `=` five times

At the epoch following a hyperparameter modification, you should see a console \
message similar to the following:

```
[epochs: 90] + 5(x5)
```

Similarly, to decrement the value of `epochs` from the example above from `90` \
to `87`:

1. Press and hold `1`
2. While holding `1` tap `-` three times

At the epoch following a hyperparameter modification, you should see a console \
message similar to the following:

```
[epochs: 90] + 3(x5)
```

Where:

```
[<hyperparameter>: <previous_value>] + <total_change>(x<increments>)
```

The value of `increment` is user determined, and could just as well be a unit \
of `10`, where one tap of `=` would result in a new value of `epochs=100`.


### License

MIT License. Please maintain attribution.
