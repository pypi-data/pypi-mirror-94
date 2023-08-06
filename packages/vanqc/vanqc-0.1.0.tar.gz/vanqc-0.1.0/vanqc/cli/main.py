#!/usr/bin/env python
"""
Variant Annotator and QC Checker for Human Genome Sequencing

Usage:
    vanqc download [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--hg19]
        [--snpeff|--funcotator|--vep] [--snpeff-jar=<path>]
        [--snpeff-db=<name>] [--http] [--dest-dir=<path>]
    vanqc normalize [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--dest-dir=<path>] <fa_path>
        <vcf_path>...
    vanqc snpeff [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--hg19] [--snpeff-jar=<path>]
        [--normalize] [--dest-dir=<path>] <db_data_dir_path> <fa_path>
        <vcf_path>...
    vanqc funcotator [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--hg19] [--normalize]
        [--dest-dir=<path>] <data_src_dir_path> <fa_path> <vcf_path>...
    vanqc funcotatesegments [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--hg19] [--dest-dir=<path>]
        <data_src_dir_path> <fa_path> <seg_path>...
    vanqc vep [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--hg19] [--normalize]
        [--dest-dir=<path>] <cache_data_dir_path> <fa_path> <vcf_path>...
    vanqc stats [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--dest-dir=<path>] <fa_path>
        <vcf_path>...
    vanqc metrics [--debug|--info] [--cpus=<int>] [--workers=<int>]
        [--skip-cleaning] [--print-subprocesses] [--dest-dir=<path>] <fa_path>
        <dbsnp_vcf_path> <vcf_path>...
    vanqc -h|--help
    vanqc --version

Commands:
    download                Download and process annotation resource data
    normalize               Normalize VCF files using Bcftools
    snpeff                  Annotate variants using SnpEff
    funcotator              Annotate variants using GATK Funcotator
    funcotatesegments       Annotate segments using GATK FuncotateSegments
    vep                     Annotate variants using Ensembl VEP
    stats                   Collect VCF stats using Bcftools
    metrics                 Collect variant calling metrics using GATK (Picard)

Options:
    -h, --help              Print help and exit
    --version               Print version and exit
    --debug, --info         Execute a command with debug|info messages
    --cpus=<int>            Limit CPU cores used
    --workers=<int>         Specify the maximum number of workers [default: 1]
    --skip-cleaning         Skip incomlete file removal when a task fails
    --print-subprocesses    Print STDOUT/STDERR outputs from subprocesses
    --hg19                  Use hg19 instead of hg38 (default) as a reference
    --snpeff, --funotator, --vep
                            Select only one of SnpEff, Funcotator, and VEP
    --snpeff-jar=<path>     Specify a path to snpEff.jar
    --http                  Use HTTP instead of FTP (for VEP)
    --dest-dir=<path>       Specify a destination directory path [default: .]
    --normalize             Normalize VCF files

Args:
    <fa_path>               Path to an reference FASTA file
                            (The index and sequence dictionary are required.)
    <vcf_path>              Path to a VCF file
    <db_data_dir_path>      Path to a SnpEff database directory
                            (e.g., ./snpeff_data/GRCh38.86)
    <data_src_dir_path>     Path to a Funcotator data source directory
                            (e.g., ./funcotator_dataSources.v1.7.20200521s)
    <cache_data_dir_path>   Path to a VEP cache data directory
                            (e.g., ./vep_cache/homo_sapiens)
    <seg_path>              Path to a segment TSV files
    <dbsnp_vcf_path>        Path to a reference dbSNP file
"""

import logging
import os
from math import floor
from pathlib import Path

from docopt import docopt
from ftarc.cli.util import build_luigi_tasks, fetch_executable, print_log
from psutil import cpu_count, virtual_memory

from .. import __version__
from ..task.bcftools import CollectVcfStats, NormalizeVcf
from ..task.gatk import (AnnotateSegWithFuncotateSegments,
                         AnnotateVariantsWithFuncotator,
                         DownloadFuncotatorDataSources)
from ..task.picard import CollectVariantCallingMetrics
from ..task.snpeff import AnnotateVariantsWithSnpeff, DownloadSnpeffDataSources
from ..task.vep import AnnotateVariantsWithEnsemblVep, DownloadEnsemblVepCache


def main():
    args = docopt(__doc__, version=__version__)
    if args['--debug']:
        log_level = 'DEBUG'
    elif args['--info']:
        log_level = 'INFO'
    else:
        log_level = 'WARNING'
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=log_level
    )
    logger = logging.getLogger(__name__)
    logger.debug(f'args:{os.linesep}{args}')
    print_log(f'Start the workflow of vanqc {__version__}')
    if args['--hg19']:
        ucsc_hg = 'hg19'
        ncbi_hg = 'GRCh37'
    else:
        ucsc_hg = 'hg38'
        ncbi_hg = 'GRCh38'
    n_cpu = int(args['--cpus'] or cpu_count())
    memory_mb = virtual_memory().total / 1024 / 1024 / 2
    sh_config = {
        'log_dir_path': args['--dest-dir'],
        'remove_if_failed': (not args['--skip-cleaning']),
        'quiet': (not args['--print-subprocesses']),
        'executable': fetch_executable('bash')
    }
    if args['download']:
        anns = (
            {k for k in ['snpeff', 'funcotator', 'vep'] if args[f'--{k}']}
            or {'snpeff', 'funcotator', 'vep'}
        )
        common_kwargs = {
            'dest_dir_path': args['--dest-dir'], 'sh_config': sh_config
        }
        n_worker = min(int(args['--workers']), len(anns), n_cpu)
        build_luigi_tasks(
            tasks=(
                (
                    [
                        DownloadSnpeffDataSources(
                            snpeff=_fetch_snpeff_sh(
                                jar_path=args['--snpeff-jar']
                            ),
                            genome_version=ncbi_hg, memory_mb=memory_mb,
                            **common_kwargs
                        )
                    ] if 'snpeff' in anns else list()
                ) + (
                    [
                        DownloadFuncotatorDataSources(
                            gatk=fetch_executable('gatk'),
                            n_cpu=max(floor(n_cpu / n_worker), 1),
                            memory_mb=memory_mb, **common_kwargs
                        )
                    ] if 'funcotator' in anns else list()
                ) + (
                    [
                        DownloadEnsemblVepCache(
                            genome_version=ncbi_hg,
                            vep=fetch_executable('vep'),
                            wget=fetch_executable('wget'),
                            avoid_ftp=args['--http'], **common_kwargs
                        )
                    ] if 'vep' in anns else list()
                )
            ),
            workers=n_worker, log_level=log_level
        )
    else:
        n_sample = len(
            args['<seg_path>' if args['funcotatesegments'] else '<vcf_path>']
        )
        n_worker = min(int(args['--workers']), n_cpu, n_sample)
        common_kwargs = {
            'fa_path': args['<fa_path>'], 'dest_dir_path': args['--dest-dir'],
            'n_cpu': max(floor(n_cpu / n_worker), 1),
            'memory_mb': (memory_mb / n_worker), 'sh_config': sh_config
        }
        if args['normalize']:
            kwargs = {
                'bcftools': fetch_executable('bcftools'), **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    NormalizeVcf(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['snpeff']:
            kwargs = {
                'db_data_dir_path': args['<db_data_dir_path>'],
                'normalize_vcf': args['--normalize'],
                'snpeff': _fetch_snpeff_sh(jar_path=args['--snpeff-jar']),
                **{
                    c: fetch_executable(c)
                    for c in ['bcftools', 'bgzip', 'tabix']
                },
                **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    AnnotateVariantsWithSnpeff(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['funcotator']:
            kwargs = {
                'data_src_dir_path': args['<data_src_dir_path>'],
                'normalize_vcf': args['--normalize'],
                'ref_version': ucsc_hg,
                **{c: fetch_executable(c) for c in ['gatk', 'bcftools']},
                **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    AnnotateVariantsWithFuncotator(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['funcotatesegments']:
            kwargs = {
                'data_src_dir_path': args['<data_src_dir_path>'],
                'ref_version': ucsc_hg,
                'gatk': fetch_executable('gatk'), **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    AnnotateSegWithFuncotateSegments(
                        input_seg_path=p, **kwargs
                    ) for p in args['<seg_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['vep']:
            kwargs = {
                'cache_data_dir_path': args['<cache_data_dir_path>'],
                'normalize_vcf': args['--normalize'],
                **{
                    c: fetch_executable(c) for c in ['vep', 'pigz', 'bcftools']
                },
                **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    AnnotateVariantsWithEnsemblVep(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['stats']:
            kwargs = {
                'bcftools': fetch_executable('bcftools'),
                **{
                    c: fetch_executable(c)
                    for c in ['bcftools', 'perl', 'python3', 'pdflatex']
                },
                'plot_vcfstats': fetch_executable('plot-vcfstats'),
                **{k: v for k, v in common_kwargs.items() if k != 'memory_mb'}
            }
            build_luigi_tasks(
                tasks=[
                    CollectVcfStats(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )
        elif args['metrics']:
            kwargs = {
                'dbsnp_vcf_path': args['<dbsnp_vcf_path>'],
                'picard': (
                    fetch_executable('gatk', ignore_errors=True)
                    or fetch_executable('picard')
                ),
                **common_kwargs
            }
            build_luigi_tasks(
                tasks=[
                    CollectVariantCallingMetrics(input_vcf_path=p, **kwargs)
                    for p in args['<vcf_path>']
                ],
                workers=n_worker, log_level=log_level
            )


def _fetch_snpeff_sh(jar_path=None):
    return (
        '{0} -jar {1}'.format(
            fetch_executable('java'), Path(jar_path).resource()
        ) if jar_path else fetch_executable('snpEff')
    )
