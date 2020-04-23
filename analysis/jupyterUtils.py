from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import HTMLExporter, LatexExporter
from nbconvert.writers import FilesWriter

targetdirectory = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooks'

def export(filename):

    c = Config()

    # Configure our tag removal
    c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
    c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
    c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)

    # Configure and run out exporter
    c.LatexExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']

    writer = FilesWriter()
    writer.build_directory = targetdirectory
    writer.write(*LatexExporter(config=c).from_filename(filename), notebook_name=filename[:-6])