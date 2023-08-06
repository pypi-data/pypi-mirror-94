from ..test import ExperimentTest, Results
from . import spm


class HasCorrectNumberOfItems(spm.HasCorrectNumberOfItems):
    __doc__ = spm.HasCorrectNumberOfItems.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')
    __doc__ = __doc__.replace('16', '19')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',
    resource_name = 'SPM12_SEGMENT_T1T2'
    correct_number = 19


class HasCorrectItems(spm.HasCorrectItems):
    __doc__ = spm.HasCorrectItems.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',
    resource_name = 'SPM12_SEGMENT_T1T2'
    expected_items = ['rc1*.nii.gz',
                      'rc2*.nii.gz',
                      'c1*.nii.gz',
                      'c2*.nii.gz',
                      'c3*.nii.gz',
                      'c4*.nii.gz',
                      'c5*.nii.gz',
                      'filled_c2*.nii.gz',
                      'y_*.nii.gz',
                      'iy_*.nii.gz',
                      '*_seg8.mat',
                      'pyscript_setorigin_t1.m',
                      'pyscript_setorigin_t2.m',
                      'pyscript_multichannelnewsegment.m']


class HasCorrectSPMVersion(spm.HasCorrectSPMVersion):
    __doc__ = spm.HasCorrectSPMVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00272',
    resource_name = 'SPM12_SEGMENT_T1T2'


class HasCorrectMatlabVersion(spm.HasCorrectMatlabVersion):
    __doc__ = spm.HasCorrectMatlabVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00272',
    resource_name = 'SPM12_SEGMENT_T1T2'


class HasCorrectOSVersion(spm.HasCorrectOSVersion):
    __doc__ = spm.HasCorrectOSVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',
    resource_name = 'SPM12_SEGMENT_T1T2'


class SPM12SegmentSnapshot(spm.SPM12SegmentSnapshot):
    __doc__ = spm.SPM12SegmentSnapshot.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',
    resource_name = 'SPM12_SEGMENT_T1T2'


class HasNormalSPM12Volumes(spm.HasNormalSPM12Volumes):
    __doc__ = spm.HasNormalSPM12Volumes.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E02872',
    failing = 'BBRCDEV_E00375',
    resource_name = 'SPM12_SEGMENT_T1T2'


class SPM12SegmentExecutionTime(spm.SPM12SegmentExecutionTime):
    __doc__ = spm.SPM12SegmentExecutionTime.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'SPM12_SEGMENT_T1T2')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00272',
    resource_name = 'SPM12_SEGMENT_T1T2'


class SPM12SegmentMultichannelHoles(ExperimentTest):
    """SPM segmentation in multi-channel mode might misclassify as c5 tissue
    some c2 regions such as the `pallidum` and the `dentate nucleus` (known
    issue), appearing those as _holes_ in the c1+c2 maps. This test estimates
    the size of such _holes_ when present, passing if the size < 20000 and
    failing otherwise. In addition, it generates a modified version of the
    original c2 map with those misclassified c5 areas labeled as c2.
    A snapshot composition is included to inspect this modified map visually
    (original c2 segmentation in green and detected _holes_ in red)."""



    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',
    resource_name = 'SPM12_SEGMENT_T1T2'

    def run(self, experiment_id):
        import os
        import os.path as op
        import tempfile
        import nibabel as nib
        import numpy as np
        from nilearn import image

        e = self.xnat_instance.select.experiment(experiment_id)
        if not e.resource(self.resource_name).exists():
            msg = 'Resource {} not found.'.format(self.resource_name)
            return Results(False, data=[msg])
        r = e.resource(self.resource_name)

        filepaths = []
        for each in ['c2', 'filled_c2']:
            f, fp = tempfile.mkstemp(suffix='.nii.gz')
            os.close(f)
            try:
                c = list(r.files('{}*.nii.gz'.format(each)))[0]
            except IndexError:
                return Results(False, data=['Some SPM maps are missing, check '
                                            '`HasCorrectItems` test results.'])

            c.get(fp)
            filepaths.append(fp)

        c2 = np.asarray(nib.load(filepaths[0]).dataobj)
        filled = np.asarray(nib.load(filepaths[1]).dataobj)

        holes = filled - c2
        size = len(holes[holes > 0.0])

        diff_img = op.join(op.dirname(filepaths[0]),
                           '{}_diff_c2.nii.gz'.format(experiment_id))
        image.new_img_like(filepaths[0], filled - c2).to_filename(diff_img)

        from . import holes_snapshot
        snapshots = holes_snapshot(filepaths[0], diff_img)
        os.remove(diff_img)

        res = size < 20000  # Fixme : with some threshold value
        return Results(res, data={'size': '{}'.format(size),
                                  'snapshots': snapshots})

    def report(self):
        report = []
        if isinstance(self.results.data, dict):
            report.append('Size: {}'.format(self.results.data['size']))
            for path in self.results.data['snapshots']:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data
        return report
