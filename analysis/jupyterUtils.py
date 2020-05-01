import os
import re

import plotly.graph_objects as go
from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import LatexExporter
from nbconvert.writers import FilesWriter

targetDirectoryFull = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksFull'
targetDirectoryCore = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\JupyterNotebooksFull'
graphicsFolder = r'C:\Oxford\Master Thesis\Allocation Thesis\SA_CCR_Allocation\LaTeX\Graphics\ '[:-1]

def exportPlotlyFigure(fig: go.Figure, name: str):
    fig.write_image(graphicsFolder + name + '.svg')
    cwd = os.getcwd()
    os.chdir(graphicsFolder)
    cmd_sting = r'inkscape -D -z --file=' + name +r'.svg --export-pdf='+name+'.pdf --export-latex'
    os.system(cmd_sting)
    os.chdir(cwd)

def export(filename):

    c = Config()

    # Configure our tag removal
    c.TagRemovePreprocessor.remove_cell_tags = ("hide_cell",)
    c.TagRemovePreprocessor.remove_all_outputs_tags = ('hide_output',)
    c.TagRemovePreprocessor.remove_input_tags = ('hide_input',)

    # Configure and run out exporter
    c.LatexExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']

    writer = FilesWriter()
    writer.build_directory = targetDirectoryFull
    test = writer.write(*LatexExporter(config=c).from_filename(filename), notebook_name=filename[:-6])

    createdFile = targetDirectoryFull+'\\' +filename[:-6] + '.tex'
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
                line = re.sub(r"(output.*jpg})", r"JupyterNotebooksFull/\g<1>", line)
                lines_to_write.append(line)

    lines_to_write = lines_to_write[1:-5]
    with open(coreFileName, 'w+', encoding="utf8") as out_file:
        out_file.writelines(lines_to_write)



