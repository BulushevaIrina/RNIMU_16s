!!!!!!!! https://forum.qiime2.org/t/comparison-of-dada2-with-deblur/3503 !!!!!!!

#conda activate qiime2-2020.2

#1# make manifest file

#2# import manifest file with the following command
qiime tools import \
     --type 'SampleData[PairedEndSequencesWithQuality]' \
     --input-path manifest.txt \
     --output-path UMtutorial-demux-paired-end.qza \
     --input-format PairedEndFastqManifestPhred33


#3# high-level summary of your sequence quality using the qiime demux summarize command

qiime demux summarize  \
     --i-data UMtutorial-demux-paired-end.qza  \
     --o-visualization UMtutorial-demux-paired-end.qzv  \
     --p-n 100000
#produce a QIIME visualization of your data quality and tabular summary of the sequences in your dataset, which you can view by dragging and dropping it at the q2view website: https://view.qiime2.org/


#4# DADA2 module in QIIME to denoise your sequences into amplicon sequence variants (ASVs) or operational taxonomic units (OTUs)


qiime cutadapt trim-paired \
     --i-demultiplexed-sequences UMtutorial-demux-paired-end.qza \
     --p-cores 8 \
     --p-front-f GTGYCAGCMGCCGCGGTAA \
     --p-front-r GGACTACNVGGGTWTCTAAT \
     --verbose \
     --o-trimmed-sequences trimmed_sequences.qza

or (clearer for pipe is above variant)

qiime cutadapt trim-paired \
     --i-demultiplexed-sequences UMtutorial-demux-paired-end.qza \
     --p-cores 8 \
     --p-front-f GTGYCAGCMGCCGCGGTAA \
     --p-front-r GGACTACNVGGGTWTCTAAT \
     --verbose \
     --output-dir trimmed


qiime vsearch join-pairs \
     --i-demultiplexed-seqs trimmed_sequences.qza \
     --p-minovlen 10 \
     --p-maxdiffs 10 \
     --p-threads 8 \
     --verbose \
     --o-joined-sequences demux-joined.qza

I didnot use:
qiime quality-filter q-score-joined
–i-demux trimmed/deblur/ndemux-joined.qza
–o-filtered-sequences trimmed/deblur/demux-joined-filtered.qza
–o-filter-stats trimmed/deblur/demux-joined-filter-stats.qza

demux-joined-filter-stats.qza is input in -i-demultiplexed-seqs


qiime deblur denoise-16S \
     --i-demultiplexed-seqs demux-joined.qza \
     --p-trim-length 150 \
     --p-jobs-to-start 8 \
     --p-sample-stats \
     --o-representative-sequences UMrep-seqs-deblur.qza \
     --o-table UMtable-deblur.qza \
     --o-stats deblur-stats.qza 

#qiime tools validate demux.qza



qiime feature-table tabulate-seqs \
     --i-data UMrep-seqs-deblur.qza \
     --o-visualization UMrep-seqsO.qzv

#feature frequency
qiime feature-table summarize \
   --i-table UMtable-deblur.qza \
   --o-visualization UM-exp.qzv

qiime tools export \
  --input-path UM-exp.qzv \
  --output-path feature_frequency

qiime tools export \
  --input-path UMrep-seqsO.qzv \
  --output-path feature_sequences



