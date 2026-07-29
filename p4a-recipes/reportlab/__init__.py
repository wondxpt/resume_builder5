from pythonforandroid.recipe import PythonRecipe


class ReportLabRecipe(PythonRecipe):

    version = "4.0.9"

    url = "https://files.pythonhosted.org/packages/source/r/reportlab/reportlab-{version}.tar.gz"

    depends = ["pillow"]

    site_packages_name = "reportlab"


recipe = ReportLabRecipe()
