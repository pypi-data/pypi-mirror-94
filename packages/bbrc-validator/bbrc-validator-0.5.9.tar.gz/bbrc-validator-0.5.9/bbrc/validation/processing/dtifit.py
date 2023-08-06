from ..test import ExperimentTest, Results
import logging as log
import tempfile

class HasCorrectNumberOfItems(ExperimentTest):
    '''Passes if a TOPUP_DTIFIT resource is found and this resource has the
    correct number of items (i.e. 40).'''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',
    CORRECT_NUMBER = 40

    def run(self, experiment_id):
        data = []

        files = list(self.xnat_instance.select.experiment(experiment_id).\
                     resource('TOPUP_DTIFIT').files())

        res = len(files) == self.CORRECT_NUMBER

        if not res:
            data.append('%s has %s items (different from %s)'%(experiment_id,
                                                             len(files),
                                                             self.CORRECT_NUMBER))

        return Results(res, data)

class HasCorrectItems(ExperimentTest):
    '''Passes if a TOPUP_DTIFIT resource is found and this resource has the
    correct items.'''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        from fnmatch import fnmatch

        expected_items = ['acqparams.txt',
                          'AP_b0.nii.gz',
                          'AP_PA_b0.nii.gz',
                          '*_dn.nii.gz',
                          '*_dn_ec.eddy_command_txt',
                          '*_dn_ec.eddy_movement_rms',
                          '*_dn_ec.eddy_outlier_map',
                          '*_dn_ec.eddy_outlier_n_sqr_stdev_map',
                          '*_dn_ec.eddy_outlier_n_stdev_map',
                          '*_dn_ec.eddy_outlier_report',
                          '*_dn_ec.eddy_parameters',
                          '*_dn_ec.eddy_post_eddy_shell_alignment_parameters',
                          '*_dn_ec.eddy_post_eddy_shell_PE_translation_parameters',
                          '*_dn_ec.eddy_restricted_movement_rms',
                          '*_dn_ec.eddy_rotated_bvecs',
                          '*_dn_ec.eddy_values_of_all_input_parameters',
                          '*_dn_ec_fit_FA.nii.gz',
                          '*_dn_ec_fit_L1.nii.gz',
                          '*_dn_ec_fit_L2.nii.gz',
                          '*_dn_ec_fit_L3.nii.gz',
                          '*_dn_ec_fit_MD.nii.gz',
                          '*_dn_ec_fit_MO.nii.gz',
                          '*_dn_ec_fit_RD.nii.gz',
                          '*_dn_ec_fit_S0.nii.gz',
                          '*_dn_ec_fit_V1.nii.gz',
                          '*_dn_ec_fit_V2.nii.gz',
                          '*_dn_ec_fit_V3.nii.gz',
                          '*_dn_ec.nii.gz',
                          'index.txt',
                          'PA_b0.nii.gz',
                          'topup_fieldcoef.nii.gz',
                          'topup.log',
                          'topup_movpar.txt',
                          'unwarped_b0_bet_mask.nii.gz',
                          'unwarped_b0_bet.nii.gz',
                          'unwarped_b0.nii.gz']

        res = self.xnat_instance.select.experiment(experiment_id).\
            resource('TOPUP_DTIFIT')

        file_list = set([e._urn for e in res.files()])

        missing = []
        for e in expected_items:
            if not [f for f in file_list if fnmatch(f, e)]:
                missing.append(e)

        if missing:
            return Results(False, data=missing)

        return Results(True, data=[])

    def report(self):
        report = []
        if self.results.data:
            report.append(('Missing items: %s.'%self.results.data).replace('\'','`'))
        return report

class HasCorrectANTsVersion(ExperimentTest):
    '''This test checks the ANTs version used for processing the images.
    Passes if TOPUP_DTIFIT outputs were created using the expected (`2.3.1.0`) version.'''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):

        expected_ants_version = 'ANTs Version: 2.3.1.0.post149-gd15f7'

        data = self.xnat_instance.array.mrsessions(experiment_id=experiment_id,
                                                   columns=['label']
                                                   ).data
        exp_label, project, subject_id = [data[0][e] for e in \
            ['label', 'project', 'xnat:mrsessiondata/subject_id']]

        res = self.xnat_instance.select.project(project).subject(subject_id)\
            .experiment(experiment_id).resource('TOPUP_DTIFIT')

        if res.file('LOGS/%s.log' % exp_label).exists():
            log = res.file('LOGS/%s.log' % exp_label)
        else:
            return Results(False, data=['TOPUP_DTIFIT log file not found.'])

        log_data = self.xnat_instance.get(log.attributes()['URI']).text
        ants_version = [line for line in log_data.splitlines() if line.startswith('ANTs Version')]

        if not ants_version or not ants_version[0].startswith(expected_ants_version) :
            return Results(False, data=['%s' % ants_version[0]])

        return Results(True, data=[])

class HasCorrectFSLVersion(ExperimentTest):
    '''This test checks the FSL version used for processing the images.
    Passes if TOPUP_DTIFIT outputs were created using the expected (`6.0.1`) version.'''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):

        expected_fsl_version = 'FSL Version: 6.0.1'

        data = self.xnat_instance.array.mrsessions(experiment_id=experiment_id,
                                                   columns=['label']
                                                   ).data
        exp_label, project, subject_id = [data[0][e] for e in \
            ['label', 'project', 'xnat:mrsessiondata/subject_id']]

        res = self.xnat_instance.select.project(project).subject(subject_id)\
            .experiment(experiment_id).resource('TOPUP_DTIFIT')

        if res.file('LOGS/%s.log'%exp_label).exists():
            log = res.file('LOGS/%s.log' % exp_label)
        elif res.file('LOGS/%s_dtifit.log' % exp_label).exists():
            log = res.file('LOGS/%s_dtifit.log' % exp_label)
        else:
            return Results(False, data=['TOPUP_DTIFIT log file not found.'])

        log_data = self.xnat_instance.get(log.attributes()['URI']).text
        fsl_version = [line for line in log_data.splitlines() if line.startswith('FSL Version')]

        if not fsl_version or fsl_version[0] != expected_fsl_version :
            return Results(False, data=['%s' % fsl_version[0]])

        return Results(True, data=[])


class DTIFITSnapshotFA(ExperimentTest):
    '''This test generates a snapshot of the FA map generated by TOPUP_DTIFIT.
    Passes if the snapshot is created successfully. Fails otherwise. Does not
    tell anything on the segmentation quality. '''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):

        resource_name = 'TOPUP_DTIFIT'
        r = self.xnat_instance.select.experiment(experiment_id)\
                .resource(resource_name)
        print(r, r.exists())

        if not r.exists():
            log.error('%s resource not found for %s'%(resource_name, experiment_id))
            return Results(False, data=['%s resource not found'%resource_name])
        fa_map = list(r.files('*FA.nii.gz'))

        if len(fa_map) != 1:
            return Results(False, data=['FA map not found. %s'%fa_map])


        _, fa_fp = tempfile.mkstemp(suffix='.nii.gz')
        fa_map[0].get(dest=fa_fp)

        from nilearn import plotting
        paths = []
        for each in 'xyz':
            _, path = tempfile.mkstemp(suffix='.jpg')
            paths.append(path)
            im = plotting.plot_stat_map(fa_fp, draw_cross=False, black_bg=True,
                bg_img=None, display_mode=each, cut_coords=10)
            im.savefig(path)

        return Results(True, data=paths)

    def report(self):
        report = []

        for path in self.results.data:
            report.append('![snapshot](%s)'%path)
        return report


class DTIFITSnapshotRGB(ExperimentTest):
    '''This test generates a RGB map of the tensor generated by TOPUP_DTIFIT.
    Passes if the snapshot is created successfully. Fails otherwise. Does not
    tell anything on the segmentation quality. '''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        import tempfile

        resource_name = 'TOPUP_DTIFIT'
        r = self.xnat_instance.select.experiment(experiment_id)\
                .resource(resource_name)

        if not r.exists():
            log.error('%s resource not found for %s'%(resource_name, experiment_id))
            return Results(False, data=['%s resource not found'%resource_name])
        v1_map = list(r.files('*V1.nii.gz'))

        if len(v1_map) != 1:
            return Results(False, data=['V1 map not found. %s'%v1_map])

        _, v1_fp = tempfile.mkstemp(suffix='.nii.gz')
        v1_map[0].get(dest=v1_fp)

        import nibabel as nib
        import numpy as np
        from matplotlib import pyplot as plt
        data = nib.load(v1_fp).dataobj
        plt.rcParams['figure.facecolor'] = 'black'

        paths = []

        _, path = tempfile.mkstemp(suffix='.jpg')
        paths.append(path)

        fig = plt.figure(dpi=300)

        slices = range(10, data.shape[2] - 10, int(data.shape[2] / 12.0))

        border_w = 25
        border_h = 5
        for i, slice_index in enumerate(slices):
            fig.add_subplot(1, len(slices), i+1)
            test = np.flip(np.swapaxes(np.abs(data[:,:,slice_index,:]), 0, 1), 0)
            w, h, _ = test.shape
            plt.imshow(test[border_h:h - border_h, border_w: w - border_w,:], interpolation='none')
            plt.axis('off')

        fig.savefig(path, facecolor=fig.get_facecolor(),
               bbox_inches='tight',
               transparent=True,
               pad_inches=0)


        _, path = tempfile.mkstemp(suffix='.jpg')
        paths.append(path)
        fig = plt.figure(dpi=300)

        slices = range(10, data.shape[1] - 10, int(data.shape[1] / 12.0))

        border_w = 25
        border_h = 0
        for i, slice_index in enumerate(slices):
            fig.add_subplot(1, len(slices), i+1)
            test = np.flip(np.swapaxes(np.abs(data[:,slice_index,:,:]), 0, 1), 0)
            h, w, _ = test.shape
            plt.imshow(test[border_h:h - border_h, border_w: w - border_w,:], interpolation='none') # black_bg=True)
            plt.axis('off')

        fig.savefig(path, facecolor=fig.get_facecolor(),
               bbox_inches='tight',
               transparent=True,
               pad_inches=0)

        return Results(True, data=paths)

    def report(self):
        report = []

        for path in self.results.data:
            report.append('![snapshot](%s)'%path)
        return report




class DTIFITSnapshotTOPUP(ExperimentTest):
    '''This generates a snapshot depicting the distortions corrected by TOPUP.
    Pre-`TOPUP` image (green colormap) is loaded as an overlay to the post-`TOPUP`
    corrected image (red colormap). Passes if the snapshot is created successfully.
    Fails otherwise. Does not tell anything on the segmentation quality. '''

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272', # has no ANTS resource

    def run(self, experiment_id):
        import os

        if os.getenv('SKIP_SNAPSHOTS_TESTS') == 'True':
            return Results(experiment_id == self.passing[0],
                 data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])

        resource_name = 'TOPUP_DTIFIT'
        r = self.xnat_instance.select.experiment(experiment_id).resource(resource_name)
        if not r.exists():
            log.error('%s resource not found for %s'%(resource_name, experiment_id))
            return Results(False, data=['%s resource not found'%resource_name])

        f = list(r.files('PA_b0.nii.gz'))[0]
        fd2, pre_fp = tempfile.mkstemp(suffix='.nii.gz')
        f.get(pre_fp)

        f = list(r.files('unwarped_b0.nii.gz'))[0]
        fd1, post_fp = tempfile.mkstemp(suffix='.nii.gz')
        f.get(post_fp)

        from . import topup_snapshot
        snaps = topup_snapshot(pre_fp, post_fp)

        return Results(True, data=snaps)

    def report(self):
        report = []

        for path in self.results.data:
            report.append('![snapshot](%s)'%path)
        return report
