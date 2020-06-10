import os
import re

import plotly.graph_objects as go
from traitlets import default
from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import LatexExporter
from nbconvert.writers import FilesWriter

targetDirectoryFull = r'C:\Oxford\Master_Thesis\Allocation_Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksFull'
targetDirectoryCore = r'C:\Oxford\Master_Thesis\Allocation_Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksCore'
graphicsFolder = r'C:\Oxford\Master_Thesis\Allocation_Thesis\SA_CCR_Allocation\LaTeX\Graphics\ '[:-1]
latexFolder = r'C:\Oxford\Master_Thesis\Allocation_Thesis\SA_CCR_Allocation\LaTeX'

class CustomLatexExporter(LatexExporter):
    @default('template_file')
    def _template_file_default(self):
        return 'custom_latex.tplx'

def exportPlotlyFigure(fig: go.Figure, name: str):
    fig.write_image(graphicsFolder + name + '.pdf')


def export(filename):

    c = Config()

    # Configure our tag removal
    c.TagRemovePreprocessor.remove_cell_tags = ("hide_cell",)
    c.TagRemovePreprocessor.remove_all_outputs_tags = ('hide_output',)
    c.TagRemovePreprocessor.remove_input_tags = ('hide_input',)

    # Configure and run out exporter
    c.LatexExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']

    targetDirectoryFull_loc = targetDirectoryFull+"\\"+filename.replace(' ', '_')[:-6]
    targetFolder = filename.replace(' ', '_')[:-6]
    writer = FilesWriter()
    writer.build_directory = targetDirectoryFull_loc
    test = writer.write(*CustomLatexExporter(config=c).from_filename(filename), notebook_name=filename[:-6])

    createdFile = targetDirectoryFull_loc+'\\' +filename[:-6] + '.tex'
    toBeCreatedFile = targetDirectoryCore+'\\' +filename[:-6] + '.tex'
    coreFileName = targetDirectoryCore+'\\' +filename[:-6] + '_Core.tex'

    tag = 'maketitle'
    lines_to_write = []
    tag_found = False

    with open(createdFile, encoding="utf8") as in_file:
        for line in in_file:
            if tag in line:
                tag_found = True
            elif tag_found:
                line = re.sub(r"{In}{incolor}{\d*}", r"{In}{incolor}{In}", line)
                line = re.sub(r"{Out}{outcolor}{\d*}", r"{Out}{outcolor}{Out}", line)
                string = r'JupyterNotebooksFull/'+targetFolder+'/'
                line = re.sub(r"(output.*jpg})", string+r"\g<1>", line)
                if r'\prompt{Out}{outcolor}{Out}{}' in line:
                    lines_to_write.append(r'            \begin{tcolorbox}[breakable, size=fbox, boxrule=.5pt, pad at break*=1mm, opacityfill=0]' +'\n')
                    line = r'\prompt{Out}{outcolor}{Out}{\boxspacing}'
                lines_to_write.append(line)
                if r'{ \hspace*{\fill} \\}' in line:
                    lines_to_write.append(r'\end{tcolorbox}'+'\n')


    lines_to_write = lines_to_write[1:-5]
    with open(toBeCreatedFile, 'w+', encoding="utf8") as out_file:
        out_file.writelines(lines_to_write)



