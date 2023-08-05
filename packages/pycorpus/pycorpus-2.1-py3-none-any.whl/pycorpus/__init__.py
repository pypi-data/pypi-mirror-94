# coding=utf-8
""" This module provides an easy, non-intrusive way to process a big list of files
in a parallel way. Also provides the option to process these files with a
different packs of options, evaluate and generate reports.


= Instructions:

1. Import this module from your main file

    import pycorpus

2. Create the function that process the file

    def my_process(file_name, config):
        # Do some sciences stuff with the file

3. (Optional) Create a function that return an argument parser that capture all
the configs that you need.

    def my_parser():
        # Set up your argparse parser
        # Return the parser
        return my_parser_instance

4. Add to the end of your file something like this:

    if __name__ == "__main__":
        corpus_processor = pycorpus.CorpusProcessor(
            parse_cmd_arguments=my_parser, process_file=my_process)
        corpus_processor.run_corpus()

= NOTES:

 * Dot not ADD the () to 'my_parser' and 'my_process' arguments.

 * If you don't need options you can ignore step three, and the config file come as
    None. In this case, never use the --config parameter.

 * The files are processed in a concurrent way so if you might store any results
    don't use the sys.out. Logging using a 'Filehandler' may do the trick.

"""

import os
import smtplib
import subprocess
import configargparse
from logging import getLogger
from multiprocessing import Process, cpu_count

__author__ = 'Josu Bermúdez <josu.bermudez@deusto.es>'
__created__ = '06/2013'

logger = getLogger("pycorpus")


class CorpusProcessor:
    """ The class that manages the parallel process of all files of the corpus.
    Also have useful functions like send_mail and launch.
    """

    namePrefix = "#"

    def __init__(self, generate_parser_function, process_file_function,
                 evaluation_script=None, report_script=None):
        self.parser_generator = generate_parser_function
        self.process_file_function = process_file_function
        self.evaluation_script = evaluation_script
        self.report_script = report_script
        self.arguments = None

        # configargparse.ArgumentParser.convert_item_to_command_line_arg = convert_item_to_command_line_arg
        # configargparse.already_on_command_line = lambda x, y: False

    @staticmethod
    def parse_cmd_arguments():
        """ Parse command line arguments and put options into an object.
        """
        parser = configargparse.ArgumentParser(
            description="Process a text file or a directory tree of files using multiprocess",
            config_file_parser_class=configargparse.YAMLConfigFileParser)

        parser.add_argument(
            '-p', '--parameters', is_config_file=True,
            help='Config file path ')
        parser.add_argument(
            '--jobs', dest='jobs', action='store', default=cpu_count(), type=int,
            help="Set the max number of parallel process.")
        parser.add_argument(
            '--file', dest="files", action='append', default=[],
            help="File to processed. May be used multiple times and"
                 "with directory parameter. ")
        parser.add_argument(
            '--directory', dest='directories', action="append", default=[],
            help="All the files contained by the directory(recursively) "
                 "are processed. May be used multiple times and with"
                 "the file parameter.")
        parser.add_argument(
            '--extension', dest='extensions', action='append', default=[],
            help="The extensions of the files(without dot) that must "
                 "be processed form directories. The '*' is used as accept "
                 "all. May be used multiple times ."
                 "WARNING doesn't filter files from --files.")
        parser.add_argument(
            '--config', nargs='*', dest='config', action='append', default=[],
            help="The config files that contains the parameter each experiment."
                 "Use {0} to set the experiment name at the end of the line \n"
                 "    --config my_file.yam my_file2.yam '{0}base case' "
                 "Repeat the parameter for multiple (series of)experiments.\n"
                 "   --config my_file.yam my_file2.yam '{0}base case' "
                 "--config my_file.yam my_file3.yam '{0}New approach'"
            .format(CorpusProcessor.namePrefix))
        parser.add_argument(
            '--common', nargs='*', dest='common', action='store', default=[],
            help="A common config for all experiments")
        parser.add_argument(
            '--series_name', dest='series_name', action='store', default="series")
        parser.add_argument(
            '--experiment_name', dest='series_name', action='store', default="experiment")
        parser.add_argument(
            '--only_evaluate', dest='only_evaluate', action='store_true',
            help="Only do the evaluation.")
        parser.add_argument(
            '--evaluate', dest='evaluate', action='store_true',
            help="Activates the evaluation.")
        parser.add_argument(
            '--report', dest='report', action='store_true',
            help="Activates report system.")
        parser.add_argument(
            '--verbose', dest='verbose', action='store_true',
            help="More output.")
        return parser

    @staticmethod
    def launch_with_output(command, cwd=None):
        """Launch a process send the input and return the error an out streams.
        :param cwd: The working directory (optional).
        :param command: The command to launch
        """
        p = subprocess.Popen(
            command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
        out, err = p.communicate()
        return err, out

    @staticmethod
    def rebuild_tread_parameters(thread_config, common, process_parser):
        config_files = [arg_file for arg_file in common + thread_config if not arg_file.startswith("#")]

        for f in config_files:
            if not os.path.exists(f):
                logger.warning("File don't exist: %s", f)

        wrapper_parser = configargparse.ArgumentParser(parents=[process_parser],
                                                       default_config_files=config_files, add_help=False,
                                                       config_file_parser_class=configargparse.YAMLConfigFileParser)
        # Only process the config files
        process_arguments = wrapper_parser.parse_args(args="")
        experiment_name = [token.replace(CorpusProcessor.namePrefix, "", 1)
                           for token in thread_config if token.startswith(CorpusProcessor.namePrefix)]
        if experiment_name:
            process_arguments.experiment_name = experiment_name[0]
        return process_arguments

    @staticmethod
    def _create_file_list(options):
        """ With the argument create a unique file list that contains all files
        that must be processed.

        :param options: Namespace with options(from argsparse). Usable options:

            +files: Files processed(if a directory is provided these are added
                anyway)
            +directories: All the files contained by the directory(recursively)
                are processed.
            +extension:The extensions of the files(without point) that must be
                processed form directories. The '*' and '*.*' are accepted as
                all extensions. WARNING doesn't filter files from --files.
        """
        # Generate unique file list
        no_filter_extensions = "*" in options.extensions
        # Add the selected files
        file_list = options.files or []
        # Add the files included in the directories
        for directory in options.directories:
            for root, dirs, files in os.walk(os.path.expanduser(directory)):
                # In case of no recursive adding
                for fullname in files:
                    name, ext = os.path.splitext(fullname)
                    # Remove staring point
                    if len(ext) and ext[0] == ".":
                        ext = ext[1:]
                    # Filter , if necessary, the included files
                    if no_filter_extensions or (ext in options.extensions):
                        file_list.append(
                            os.path.abspath(os.path.join(root, fullname)))
        return file_list

    def evaluate(self, processor_parameters, experiment_parameters):
        """ Call the user defined evaluation function
        :param processor_parameters: The parameters of the corpus processor
        :param experiment_parameters: The parameters of the experiment
        """
        self.evaluation_script(processor_parameters, experiment_parameters)

    def report(self, experiment_pack, common_arguments, experiment_parameters):
        """ Call the user defined report function with the general parameters
        and the common parameters

        :param experiment_pack: The parameters of the corpus processor.
        :param common_arguments: The common parameters of the experiment.
        :param experiment_parameters: The parameters of the experiment
        """
        self.report_script(experiment_pack, common_arguments, experiment_parameters)

    @staticmethod
    def send_mail(mail_server, from_email, to_emails, body, subject):
        """ Send a mail using SMTP mail server.

        :param mail_server: The server that delivers the mail
        :param subject: A subject added to the email
        :param from_email: A email direction
        :param to_emails: A LIST of email directions
        :param body: The text of the mail.
        """
        subject = 'Subject: {0}\n'.format(subject)
        server = smtplib.SMTP(mail_server)

        return server.sendmail(from_email, to_emails, subject + body)

    @staticmethod
    def launch_parallel(function, parameters_lists, common_parameters, jobs=cpu_count(), verbose=False):
        """Call a process that executes process function over selected files
        with the config argument

        :param function: The function to execute.
        :param jobs: The maximum number of concurrent jobs.
        :param parameters_lists: The list of lists of parameters for each launch.
        :param common_parameters: The list of common parameters for all launch .
        :param verbose: Additional info in the output.
        """

        running = []
        logger.info("Executing %s jobs in : %s", jobs, os.path.abspath(os.curdir))
        logger.info("loading workers")
        if jobs == 1:
            for parameters in parameters_lists:
                p = Process(target=function, name=str(parameters), args=(parameters, common_parameters))
                logger.debug("Process %s start", p.name)
                p.start()
                p.join()
                if p.exitcode != 0:
                    logger.info("Process %s finished with errors", p.name)
                elif verbose:
                    logger.info("Process %s finished", p.name)
            return

        while parameters_lists or running:
            while (len(running) < jobs) and parameters_lists:
                parameters = parameters_lists.pop()
                p = Process(target=function, name=str(parameters), args=(parameters, common_parameters))
                p.start()
                running.append(p)
                logger.debug("Process %s start", p.name)
            for p in running:
                if not p.is_alive():
                    running.remove(p)
                    if p.exitcode != 0:
                        logger.info("Process %s finished with errors", p.name)
                    elif verbose:
                        logger.info("Process %s finished", p.name)

        logger.info("Corpus Processed")

    def run_corpus(self, config_files=False):
        """ Run the process all over the corpus also evaluate and report if
        are selected.
        :param config_files: The name of the config file

        """

        parser = self.parse_cmd_arguments()
        if config_files:
            parser._default_config_files = config_files
            arguments = parser.parse_args()
        else:
            arguments = parser.parse_args()
        self.arguments = arguments
        process_parser = self.parser_generator()
        logger.info("Process")
        files = (self._create_file_list(options=arguments))
        logger.info("Files: %s", len(files))
        logger.info("Common config: %s", arguments.common)
        process_arguments_list = []
        for config in arguments.config:
            process_arguments = self.rebuild_tread_parameters(
                config, arguments.common, process_parser)
            process_arguments.series_name = arguments.series_name
            process_arguments_list.append(process_arguments)
            logger.info("config: %s", config)
            if not arguments.only_evaluate:
                self.launch_parallel(
                    function=self.process_file_function,
                    parameters_lists=list(list(files),), common_parameters=process_arguments,
                    jobs=arguments.jobs, verbose=arguments.verbose)
            if arguments.evaluate or arguments.only_evaluate:
                logger.info("Evaluation")
                self.evaluate(arguments, process_arguments)
        if arguments.report:
            logger.info("Report generation")
            common_arguments = self.rebuild_tread_parameters(
                thread_config=[], common=arguments.common, process_parser=process_parser)
            self.report(arguments, common_arguments, process_arguments_list)
