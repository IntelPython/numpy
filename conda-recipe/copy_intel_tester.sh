# As suggested by Michael Sarahan:
# Since the output is considered to have a different recipe from the parent (a different final rendered recipe), 
# conda-build stores the original recipe in that parent folder.  That's the true original recipe, rather than 
# the frozen rendered recipe (which is specific to just the one output).
cp $RECIPE_DIR/intel_tester_config.py $SRC_DIR
