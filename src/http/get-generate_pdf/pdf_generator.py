from io import BytesIO

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

# Arc Shared Code
from shared.translations.i18n import get_translation_for_locale


# Set up the jinja2 with File Loader.
jinja2_env = Environment(
    loader=FileSystemLoader('./templates'),
    trim_blocks=True,
)


class PDFRenderer:
    def __init__(self, template='pdf_template.html', translations=None, data=None):
        # Grab the template
        self.template = jinja2_env.get_template(template)
        # Get the translations if there aren't any
        if translations is None:
            translations = get_translation_for_locale('en')
        # Set the data set, add the translations to the data set
        self.data = data | translations
        # Create a bytes io object to store the pdf we are creating
        self.target_file = BytesIO()

    def render(self):
        """
        A view to get a pdf based on a user, a cat, and language translations
        :return: a rendered PDF file
        """
        # Pass the data to the template, this includes translation context keys
        html = self.template.render(self.data)
        # Create the PDF, using the ByteIO object as the target file
        HTML(string=html).write_pdf(target=self.target_file)
        # Set the BytesIO file buffer's current position to 0, this lets the file be iterated from the start
        self.target_file.seek(0)
        return self.target_file
