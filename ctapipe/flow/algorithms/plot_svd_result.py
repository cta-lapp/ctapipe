from ctapipe.core import Component
from traitlets import Unicode
import hipecta.data as cd
import hipecta.plots as ctaplt
from os.path import isdir, join, isfile
from os import makedirs, listdir, symlink


"""
When connecting thanks to ssh you need to add -Y or -X option, otherwise this script with fail due to matplotlib
"""



class PlotSVDResult(Component):

    """`StringWriter` class represents a Stage or a Consumer for pipeline.
        It writes received objects to file
    """
    input_dir = Unicode('/tmp', help='input directory containing pcalib files' ).tag(
        config=True, allow_none=True)
    output_dir = Unicode('/tmp', help='output directory ').tag(
        config=True, allow_none=True)
    psimu_dir = Unicode('/tmp', help='input directory containing psimu files').tag(
        config=True, allow_none=True)

    def init(self):
        if self.output_dir:
            if not isdir(self.output_dir):
                makedirs(self.output_dir)
            return True

    def run(self, obj):
        pass

    def finish(self):
        # create symbolic link for psimu files
        files_list = [f for f in listdir(self.psimu_dir) if
                      isfile(join(self.psimu_dir, f)) and
                      f.split('.')[-1] == 'psimu']

        try:
            for src in files_list:
                self.log.info('src {}, self.input_dir {}'.
                            format(self.psimu_dir + '/' + src, self.input_dir + '/' + src))
                symlink(self.psimu_dir + '/' + src, self.input_dir + '/' + src )
        
        except FileExistsError:
            pass


        self.log.info("--- PlotSVDResult start plotting from directory {} ---".format(self.input_dir))
        a = cd.AnaData()
        a.load_bin_from_dir(self.input_dir)

        p = ctaplt.plot_from_anadata(a)
        p.set_site('north')

        p.set_outdir(self.output_dir)

        # p.plot_all()
        p.energy_resolution(MultiplicityMin=[2])

        p.effective_area_per_energy()
        p.impact_resolution_per_energy()
        p.angular_res_per_energy()

        a.save_to_parchive(Outfile=self.output_dir + '/save.p')

        self.log.info("--- PlotSVDResult finish---")

