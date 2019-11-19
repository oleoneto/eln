import os
import click
import fileinput
import inflection
from datetime import datetime
from eln.helpers.logger import log_error
from eln.helpers.parser import sanitized_string
from eln.helpers.template import rendered_file_template

DEFAULT_IMPORT_WARNING = "Module already imported. Skipping..."

DEFAULT_OVERRIDE_WARNING = "File {} already exists. Override file?"

DEFAULT_NOUN_NUMBER_OPTION = "Change resource name from {} to {}?"

DEFAULT_PARSED_CONTENT_LOG = """Filename: {}\nFilepath: {}\n\n---- Begin content ----\n{}\n---- End content ----"""

DEFAULT_DESTROY_LOG = """Will delete...\nFilename: {}\nFilepath: {}\n\nWill also remove imports in __init__.py"""

DEFAULT_ERRORS = {
    "package": "Unable to create package. Will exit.",
    "folder": "Unable to create folder. Skipping...",
    "clean": "Unable to remove default files. Skipping...",
    "repo": "Unable to initialize repository. Skipping...",
    "touch": "Unable to create default files. Skipping...",
}

DEFAULT_APP_PACKAGES = {
    'tests', 'dummy',
}

DEFAULT_CWD = '.'

DEFAULT_PREVIOUS_WD = '..'


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIRS = {
    'package': os.path.join(BASE_DIR, 'package/templates'),
    'bottle': os.path.join(BASE_DIR, 'bottle/templates'),
    'cpp': os.path.join(BASE_DIR, 'cpp/templates'),
}

PACKAGE_TEMPLATES = [f for f in os.listdir(TEMPLATE_DIRS['package']) if f.endswith('tpl')]

BOTTLE_TEMPLATES = [f for f in os.listdir(TEMPLATE_DIRS['bottle']) if f.endswith('tpl')]

CPP_TEMPLATES = [f for f in os.listdir(TEMPLATE_DIRS['cpp']) if f.endswith('tpl')]


class CreatorHelper:

    def __init__(self, path, dry=False, force=False):
        self.__path = path
        self.__dry = dry
        self.__force = force

    def __parse_templates(
            self,
            project,
            template_files_dict,
            template_names,
            template_dir,
            folders,
            inner=False,
            **kwargs
    ):
        project = sanitized_string(project)

        try:
            os.makedirs(project)
            if inner:
                os.makedirs(f'{project}/{project}')
        except FileExistsError:
            log_error("Directory already exists")

        for folder in folders:
            try:
                os.makedirs(folder)
            except FileExistsError:
                pass

        os.chdir(project)

        for file, template in template_files_dict.items():
            i = template_names.index(template)
            template = template_names[i]

            content = rendered_file_template(
                path=template_dir,
                template=template,
                context=kwargs.get('context')
            )

            self.__create_file(
                path=os.getcwd(),
                filename=file,
                content=content,
            )

    def create_package(self, project):
        """
        Create a project and any associated modules
        """

        project = sanitized_string(project)

        folders = [
            f'{project}/docs',
            f'{project}/dummy',
            f'{project}/tests',
        ]

        templates = {
            'app.py': 'app.tpl',
            'setup.py': 'setup.tpl',
            'setup.cfg': 'setup_cfg.tpl',
            'Pipfile': 'pipfile.tpl',
            'README.md': 'readme.tpl',
            'MANIFEST.in': 'manifest.tpl',
            'LICENSE.txt': 'license.tpl',
            '.gitignore': 'gitignore.tpl',
        }

        self.__parse_templates(
            project=project,
            template_files_dict=templates,
            template_names=PACKAGE_TEMPLATES,
            template_dir=TEMPLATE_DIRS['package'],
            folders=folders,
            inner=True,
            context={'project': project}
        )

    def create_bottle_app(self, project):
        """
        Create a bottle app project and any associated modules
        """
        project = sanitized_string(project)

        folders = [
            f'{project}/views',
            f'{project}/static',
            f'{project}/media',
            f'{project}/tests',
            f'{project}/templates'
         ]

        templates = {
            'app.py': 'app.tpl',
            'Pipfile': 'pipfile.tpl',
            'db.py': 'dbconfig.tpl',
            '.gitignore': 'gitignore.tpl'
        }

        self.__parse_templates(
            project=project,
            template_files_dict=templates,
            template_names=BOTTLE_TEMPLATES,
            template_dir=TEMPLATE_DIRS['bottle'],
            folders=folders,
            inner=True,
            context={'project': project}
        )

    def create_cpp_project(self, project, classes):
        """
        Create a bottle app package and any associated modules
        """
        project = sanitized_string(project)

        templates = {
            'main.cpp': 'main.tpl',
            'main_test.cpp': 'main_test.tpl',
            '.gitignore': 'gitignore.tpl'
        }

        self.__parse_templates(
            project=project,
            template_files_dict=templates,
            template_names=CPP_TEMPLATES,
            template_dir=TEMPLATE_DIRS['cpp'],
            folders=[],
            context={'project': project, 'date': datetime.now()}
        )

        for c in classes:
            self.__create_class(project, c)

    def __create_class(self, project_name, classname):
        classname = inflection.camelize(sanitized_string(classname))

        templates = {
            f'{classname}.h': 'header.tpl',
            f'{classname}.cpp': 'class.tpl',
        }

        for file, template in templates.items():
            i = CPP_TEMPLATES.index(template)
            template = CPP_TEMPLATES[i]

            content = rendered_file_template(
                path=TEMPLATE_DIRS['cpp'],
                template=template,
                context={
                    'project': project_name,
                    'date': datetime.now(),
                    'classname': classname
                }
            )

            self.__create_file(
                path=os.getcwd(),
                filename=file,
                content=content
            )

    def __parse_and_create(self, **kwargs):
        content = self.__parsed_template(**kwargs)

        if self.__dry:
            self.__log_dry(
                path=kwargs['path'],
                filename=kwargs['filename'],
                content=content,
            )
        else:
            return self.__create_file(
                path=kwargs['path'],
                filename=kwargs['filename'],
                content=content,
            )
        return False

    def __create_file(self, content, filename, path=None):
        directory = os.getcwd()

        path = path if path else self.__path

        try:
            os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chdir(path)

        try:
            with open(filename, 'x') as file:
                file.write(content)
                file.write('\n')
            file.close()
            os.chdir(directory)
            return True
        except FileExistsError:
            if self.__force or click.confirm(DEFAULT_OVERRIDE_WARNING.format(filename)):
                with open(filename, 'w') as file:
                    file.write(content)
                    file.write('\n')
                file.close()
                os.chdir(directory)
                return True
            pass

    def __destroy(self, filename, path=None):
        path = path if path else self.__path

        if self.__dry:
            click.echo(DEFAULT_DESTROY_LOG.format(filename, path))
            return False
        else:
            try:
                os.chdir(path)
                os.remove(filename)
            except FileNotFoundError:
                log_error("File does not exist.")
                return False
        return True

    def __add_import(self, template, **kwargs):
        filename = '__init__.py'
        content = template.render(**kwargs)

        if self.__dry:
            self.__log_dry(
                path=self.__path,
                filename=filename,
                content=content,
            )
            return content
        try:
            os.chdir(self.__path)

            # Prevent duplicate imports
            for line in fileinput.input(filename):
                if content in line:
                    log_error(DEFAULT_IMPORT_WARNING)
                    fileinput.close()
                    return
            fileinput.close()

            with open(filename, 'a') as file:
                file.write(content)
                file.write('\n')
            file.close()
        except FileNotFoundError:
            with open(filename, 'w') as file:
                file.write(content)
                file.write('\n')

        return content

    def __log_dry(self, content, filename, path=None):
        """
            Responsible for logging commands to the console.
            Used when --dry flag is specified.
        """

        path = path if path else self.__path

        click.echo(DEFAULT_PARSED_CONTENT_LOG.format(
            filename,
            path,
            content
        ))

    @classmethod
    def __parsed_template(cls, template, **kwargs):
        return template.render(**kwargs)
