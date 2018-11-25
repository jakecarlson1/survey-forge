# Survey Forge
A tool for generating data sets that contain user-determined statistical properties. The user picks the statistical method and the desired output value(s) for that method, and the Forge generates a data set to match. The current supported methods are ANOVA, Cronbach's Alpha, and regression.

## Usage
The usage for each supported method is outlined below. All methods accept a tolerance for the desired properties of the output data set. Providing a sufficiently small tolerance can make the Forge take longer to return, but a tolerance of around 0.001 should work fine.

Once the input parameters have been determined (either through the command line or programatically), the desired generator is instantiated with the desired properties, and `generate_data()` is called. This constructs a DataFrame that adheres to the desired output properties and tolerances.

Once `generate_data()` returns, `write()` is called on the generator instance, which writes the DataFrame to the file provided to the `-f` flag.

All methods output a csv with the generated data. The `-n` flag specifies the number of rows that should appear in the output csv.

### ANOVA
ANOVA is used to compare the means for different groups in our data set. The output for ANOVA is the F-statistic, so this is the input for the Forge (`-f`). Along with this, you can provide the number of groups for the output data set through `-g`. The scale for the output value can be provided through `-s`. Currently, all the groups will share the same scale.

### Cronbach's Alpha
Alpha is a measure of inter-item similarity for a survey. This is typically applied to a survey composed of Likert scale items. The input for the Forge is the desired alpha through `-a`, and the range for the Likert scale for all the items through `-s`. You can also provide the desired number of items in the survey through `-i`.

### Regression
Regression is used to find a function that maps from a vector of input features to some target feature. For this module, you can provide the scales for each input feature (`-s`), the scale for the target feature (`-t`), and the desired values of the regression coefficients (`-b`). Currently, the Forge only supports one input feature.

## Extending the Forge
Additional generators can be added to the Forge by subclassing the Generator class. The Generator exposes the `generate_data()` method that can be called to generate a data set. The subclass must define `_generate_data()` which provides the calculations necessary for building a pandas DataFrame that adheres to the specified output properties of the module. The subclass must also provide `_is_valid()` that checks that the output properties are within the tolerance specified by the user. The Generator will call `_generate_data()` until `_is_valid()` returns True.

