#!/usr/bin/env python
'''
Collects all JSON from validation steps and compiles some global scores over an
XNAT instance.
'''
def validation_scores(args):
    import traceback
    import logging as log
    import os.path as op
    import json
    import dateparser
    # BEGINNING Path hack.
    #sys.path.insert(0, op.abspath('..'))
    # END Path hack.
    from bbrc.validation.utils import collect_reports
    from pyxnat import Interface

    import bbrc
    f = op.join(op.dirname(bbrc.__file__), 'data', 'versions.json')
    with open(f, 'r') as fp:
        versions = json.load(fp)

    config_file = op.abspath(args.config.name)
    version = args.version

    from bbrc import __version__
    log.info('BBRC-validator version: %s' % __version__)

    if args.verbose :
        log.getLogger().setLevel(log.INFO)
    else :
         log.getLogger().setLevel(log.WARNING)

    try :
        xnat_instance = Interface(config=config_file)
        j = collect_reports(xnat_instance, validator_name=args.validator, project=args.project)
        res = []
        fields = []

        for k, v in j.items():
            if 'version' not in v.keys():
                log.warning('Version not found in report %s'%k)
                continue
            if v['version'] != version: continue
            fields = list(v.keys())
            break

        try:
            for e in ['version', 'generated', 'experiment_id']:
                fields.remove(e)
        except ValueError:
            msg = 'No valid report found (version %s).' % version
            log.error(e)
            raise Exception(msg)

        for k, v in j.items():
            if 'version' not in v.keys():
                log.warning('Version not found in report %s'%k)
                continue
            if v['version'] != version:
                if v['version'] not in versions.keys() :
                    log.warning('Version %s (%s) not registered as a valid/existing version' % (v['version'],
                                                                                                v['generated']))
                    continue
                if dateparser.parse(v['generated']) < dateparser.parse(versions[version]['date']) :
                    continue

            log.info(v[fields[0]])
            row = [v['experiment_id']]
            row.extend([v[f]['has_passed'] for f in fields])
            res.append(row)

        import pandas as pd
        fields.insert(0,'experiment_id')
        df = pd.DataFrame(res, columns=fields).set_index('experiment_id')
        df.to_excel(args.output.name)

        if xnat_instance._user and not xnat_instance._anonymous :
            xnat_instance.disconnect()

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        raise e

def create_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Compile validation scores')
    parser.add_argument('--config', help='XNAT configuration file',
                        type=argparse.FileType('r'), required=True)
    parser.add_argument('--version', '-v', help='Filter specific version',
                        required=True)
    parser.add_argument('--validator', required=False, default='ArchivingValidator',
                        help='Validator name (default:ArchivingValidator)')
    parser.add_argument('--output', '-o', required=True,type=argparse.FileType('w'),
                        help='CSV output file')
    parser.add_argument('--project', '-p', required=False, default=None,
                        help='Specific XNAT project to collect validation results from (optional)')
    parser.add_argument('--verbose', '-V', action='store_true', required=False, default=False,
                        help='Display verbosal information (optional)')
    return parser

if __name__=="__main__" :
    parser = create_parser()
    args = parser.parse_args()
    validation_scores(args)
