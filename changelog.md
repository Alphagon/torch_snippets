# Changelog

#### 0.504

🧹 `phasify` loads by default
🧹 `show_big_dataframe` can show more rows
🎉 add a new submodule `trainer.hooks`
🧹 `show` delegated kwargs to `plt.imshow` for a better readme
🎉 `batchify` can batchify multiple containers at once
🎉 `cat_with_padding` new function in `torch_loader`
🧹 `L` is json compatible
🐞 `BB` will not decide if something is relative/absolute
🎉 `__contains__` for config
🎉 `to` works on `AttrDict`
👶🏼 `track2` is a better version of `track` uses corouties
👶🏼 `debug_mode` temporarily activates `DEBUG` mode on
👶🏼 `if in_debug_mode():` lets you know if `DEBUG` mode is on
🧹 `reset_logger` can accept lowercase levels also
🧹 `dumpdill` will return a Path after dumping

#### 0.503

bugfix in `loader.show`
add `today` function to dates
add `are_equal_dates` to dates
add dpi option to pdf

#### 0.502

bugfix in attrdict.map

#### 0.500

All notebooks are formatted with black
`parse` can parse python expressions
Add DeepLearningConfig class that can be used to load model hyperparameters
Add GenericConfig class that can be used to load generic (such as training, evaluation) hyperparameters
Add date utilities
`patch_to`, `Timer`, `timeit`, `io` are loaded by default
`lovely_tensors` is optional
Add phasify function to loader

#### 0.499.29

attrdict can deserialize "L"

#### 0.499.28

- `show` can render a dataframe with a title
- `show` can accept a csv file as input (no need to load it and send)
- `backup_this_notebook` will back up as `backups/file/file__0000.html` instead of `backups/file/0000.html` for easier sharability
- module loads `decorators` by default (`io`, `timeit`, `check_kwargs_not_none`)
- `ishow` is less opinionated
- `shutdown_this_notebook` is a new function

## Todo

override_previous_backup should not trigger when there's no backup to begin with
instead of showing markdown objects using display, directly show HTML objects so that the text is preserved on reopen h2 in Backup instead of h1
