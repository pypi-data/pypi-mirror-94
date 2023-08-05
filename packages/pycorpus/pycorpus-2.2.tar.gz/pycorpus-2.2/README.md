This module provide a easy, non intrusive way to process a big list of files in a parallel way. Also provides the
option to process theses files with a different packs of options, evaluate and generate reports.

# Requirements:

You need the PPSS script in same dir of this file.

# Instructions:

1. Import this module from your main file

    ```python
    import pyCorpus
    ```
    
2. Create the function that process the file

    ```python
    def my_process(file_name, config):
        # Some science stuff with the file
    ```

3. (Optional) Create a function that return a argument parser that capture all the configs that you need.

    ```python
    def my_parser():
        # Set up your argparse parser
        # Return the parser
        return my_parser_instance
    ```
    
4. Add at the end of the file something like this:

    ```python
    if __name__ == "__main__":
        corpus_processor = pyCorpus.CorpusProcessor(parse_cmd_arguments, process_file)
        corpus_processor.run_corpus()
   ```
   
# NOTES:

 * Dot not ADD the () to my_parser and my_process arguments.

 * If you don't need options you can ignore step 3 and the config file come as None. But never use the --config parameter.

 * The files are processed in a concurrent way so if you might store any results don't use the sys.out use a file.
