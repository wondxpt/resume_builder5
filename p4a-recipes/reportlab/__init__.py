from pythonforandroid.recipe import Recipe
from os.path import join, exists
import shutil


class ReportLabRecipe(Recipe):

    version = "4.0.9"

    url = "https://files.pythonhosted.org/packages/source/r/reportlab/reportlab-{version}.tar.gz"

    depends = ["python3", "pillow"]

    site_packages_name = "reportlab"

    def build_arch(self, arch):

        build_dir = self.get_build_dir(arch.arch)

        source_dir = join(
            build_dir,
            "reportlab-{}".format(self.version),
            "reportlab"
        )

        if not exists(source_dir):
            source_dir = join(
                build_dir,
                "reportlab"
            )

        if not exists(source_dir):
            raise RuntimeError(
                "ReportLab source directory was not found: {}".format(
                    source_dir
                )
            )

        site_packages = self.ctx.get_site_packages_dir(arch.arch)

        destination = join(
            site_packages,
            "reportlab"
        )

        if exists(destination):
            shutil.rmtree(destination)

        shutil.copytree(
            source_dir,
            destination
        )


recipe = ReportLabRecipe()
