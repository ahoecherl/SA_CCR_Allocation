from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import LatexExporter
from nbconvert.writers import FilesWriter

targetDirectoryFull = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksFull'
targetDirectoryCore = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksCore'

def export(filename):

    c = Config()

    # Configure our tag removal
    c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
    c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
    c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)

    # Configure and run out exporter
    c.LatexExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']

    writer = FilesWriter()
    writer.build_directory = targetDirectoryFull
    test = writer.write(*LatexExporter(config=c).from_filename(filename), notebook_name=filename[:-6])

    createdFile = targetDirectoryFull+'\\' +filename[:-6] + '.tex'
    toBeCreatedFile = targetDirectoryCore+'\\' +filename[:-6] + '.tex'

    tag = 'maketitle'
    lines_to_write = []
    tag_found = False

    with open(createdFile, encoding="utf8") as in_file:
        for line in in_file:
            if tag in line:
                tag_found = True
            elif tag_found:
                lines_to_write.append(line)

    lines_to_write = lines_to_write[1:-5]
    with open(toBeCreatedFile, 'w+', encoding="utf8") as out_file:
        out_file.writelines(lines_to_write)



